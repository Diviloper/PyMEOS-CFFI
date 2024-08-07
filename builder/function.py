from __future__ import annotations

from ast import Param
from dataclasses import dataclass

from joblib.testing import param

from .build_pymeos_functions_helpers import *
from .objects import conversion_map, Conversion


@dataclass
class Function:
    name: str
    parameters: List[Parameter]

    inner_return_type: str
    output_parameters: List[Parameter]
    result_parameter: Optional[Parameter]

    @staticmethod
    def from_components(name: str, return_type: str, params: str) -> Function:
        parameters = [
            Parameter.from_string(name, param_source)
            for param_source in params.split(", ")
            if param_source != "void"
        ]
        result_parameter = next((p for p in parameters if p.result), None)
        out_parameters = [p for p in parameters if p.output]

        return Function(
            name=name,
            parameters=parameters,
            inner_return_type=return_type,
            output_parameters=out_parameters,
            result_parameter=result_parameter,
        )

    def get_function_text(self) -> str:
        param_list = ", ".join(p.declaration() for p in self.parameters if p.input)
        param_conversions = "\n    ".join(p.conversion() for p in self.parameters)

        return_type = self.get_return_type()
        inner_call = self.get_inner_call()
        result = self.get_result()

        return (
            f"def {self.name}({param_list}) -> {return_type}:\n"
            f"    {param_conversions}\n"
            f"    {inner_call}\n"
            f"    _check_error()\n"
            f"    {result}"
        )

    def get_return_type(self) -> str:
        if self.result_parameter:
            main_result = self.result_parameter.type.python_type
        else:
            conversion = conversion_map.get(self.inner_return_type, None)
            if conversion:
                main_result = conversion.p_type
            else:
                main_result = f"'{self.inner_return_type}'"

        if len(self.output_parameters) == 0:
            return main_result
        else:
            out_param_types = ", ".join(
                p.type.python_type for p in self.output_parameters
            )
            return f"Tuple[{main_result}, {out_param_types}]"

    def get_inner_call(self) -> str:
        params = ", ".join(f"{p.name}_converted" for p in self.parameters)
        call = f"_lib.{self.name}({params})"
        if self.inner_return_type != "void" and not any(
            p.result for p in self.parameters
        ):
            call = f"inner_call_result = {call}"
        return call

    def get_result(self) -> str:
        if self.inner_return_type == "void" and self.result_parameter is None:
            return ""

        if self.result_parameter is None:
            main_result = "inner_call_result"
        else:
            main_result = f"{self.result_parameter.name}[0]"
        if len(self.output_parameters) > 0:
            out_params_converted = ", ".join(
                p.out_conversion() for p in self.output_parameters
            )
            main_result += f", {out_params_converted}"

        return f"return {main_result}"


@dataclass
class Parameter:
    name: str
    type: Type

    input: bool
    nullable: bool

    result: bool
    output: bool

    @staticmethod
    def from_string(function_name: str, source: str) -> Parameter:
        param_type, param_name = Parameter.split_type_name(source)

        if param_name in reserved_words:
            final_name = reserved_words[param_name]
        else:
            final_name = param_name

        is_nullable = is_nullable_parameter(function_name, param_name)
        is_result = is_result_parameter(function_name, param_name)
        is_output = is_output_parameter(function_name, param_name, param_type)
        is_input = not (is_result or is_output)

        parameter_type = Type.from_string(function_name, param_name, param_type)

        return Parameter(
            name=final_name,
            type=parameter_type,
            input=is_input,
            result=is_result,
            output=is_output,
            nullable=is_nullable,
        )

    @staticmethod
    def split_type_name(source: str) -> Tuple[str, str]:
        split = source.split(" ")

        param_type = " ".join(split[:-1])
        param_name = split[-1].lstrip("*")
        pointer_level = len(split[-1]) - len(param_name)
        if pointer_level > 0:
            param_type += " " + "*" * pointer_level

        return param_type, param_name

    def declaration(self) -> str:
        return f"{self.name}: {self.type.python_type}"

    def conversion(self) -> str:
        if self.input:
            conversion = f"{self.name}_converted = {self.type.conversion(self.name)}"
            if self.nullable:
                conversion += f" if {self.name} is not None else _ffi.NULL"
            return conversion
        else:
            return f"{self.name}_converted = {self.type.new()}"

    def out_conversion(self) -> str:
        return self.type.out_conversion(self.name)


@dataclass
class Type:
    c_type: str
    python_type: str

    is_pointer: bool
    is_array: bool

    is_interoperable: bool
    _conversion: Optional[Conversion]

    @staticmethod
    def from_string(function_name: str, parameter_name: str, source: str) -> Type:
        is_array = is_array_parameter(function_name, parameter_name, source)
        is_pointer = source.endswith("*") and not is_array

        c_type = source
        if is_array and c_type.endswith("**"):
            c_type = c_type[:-1]

        conversion = conversion_map.get(c_type, None)
        python_type = conversion.p_type if conversion is not None else f"'{source}'"

        is_interoperable = (
            conversion is None
            or python_type == source
            or python_type in ["int", "float"]
        )

        return Type(
            c_type=c_type,
            python_type=python_type,
            is_pointer=is_pointer,
            is_array=is_array,
            is_interoperable=is_interoperable,
            _conversion=conversion,
        )

    def full_c_type(self) -> str:
        full_type = self.c_type

        if self.is_pointer:
            full_type += " *"
        if self.is_array:
            full_type += "[]"

        return full_type

    def new(self) -> str:
        return f"_ffi.new('{self.full_c_type()}')"

    def conversion(self, param_name: str):
        if self.is_array:
            if self.is_interoperable:
                return f"_ffi.new('{self.c_type} []', {param_name})"
            else:
                elem_conversion = self._conversion.p_to_c("x")
                return f"[{elem_conversion} for x in {param_name}]"
        else:
            if self.is_interoperable:
                return param_name
            else:
                return self._conversion.p_to_c(param_name)

    def out_conversion(self, param_name: str, size_parameter_name: Optional[str] = None) -> str:
        if self.is_interoperable:
            return f"{param_name}_converted[0] if {param_name}_converted[0] != _ffi.NULL else None"
        if self.is_array:
            if self._conversion.c_to_p:
                conv = self._conversion.c_to_p(f"{param_name}[i]")
            else:
                conv = f"{param_name}[i]"
            return f"[{conv} for i in range({size_parameter_name}[0])]"
        else:
            if self._conversion.c_to_p:
                return self._conversion.c_to_p(param_name)
            else:
                return param_name

