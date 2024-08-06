import re
from collections.abc import Callable


def array_length_remover_modifier(list_name: str, length_param_name: str = "count") -> Callable[[str], str]:
    return lambda function: function.replace(f", {length_param_name}: int", "").replace(
        f", {length_param_name}", f", len({list_name})"
    )


def array_parameter_modifier(list_name: str, length_param_name: str | None = None) -> Callable[[str], str]:
    def custom_array_modifier(function: str) -> str:
        type_regex = list_name + r": Annotated\[(?:(?:_ffi\.CData)|(?:list)), '([\w \*]+)'\]"
        match = next(re.finditer(type_regex, function))
        whole_type = match.group(1)
        base_type = " ".join(whole_type.split(" ")[:-1])
        function = function.replace(match.group(0), f"{list_name}: 'list[{base_type}]'").replace(
            f"_ffi.cast('{whole_type}', {list_name})",
            f"_ffi.new('{base_type} []', {list_name})",
        )
        if length_param_name:
            function = function.replace(f", {length_param_name}: int", "").replace(
                f", {length_param_name}", f", len({list_name})"
            )
        return function

    return custom_array_modifier


def textset_make_modifier(function: str) -> str:
    function = array_parameter_modifier("values", "count")(function)
    return function.replace("_ffi.cast('const text *', x)", "cstring2text(x)").replace(
        "'list[const text]'", "list[str]"
    )


def remove_error_check_modifier(function: str) -> str:
    return function.replace("    _check_error()\n", "")


def as_wkb_modifier(function: str) -> str:
    return function.replace("-> \"Tuple['uint8_t *', 'size_t *']\":", "-> bytes:").replace(
        "return result if result != _ffi.NULL else None, size_out[0]",
        "result_converted = bytes(result[i] for i in range(size_out[0])) if result != _ffi.NULL else None\n"
        "    return result_converted",
    )


def tstzset_make_modifier(function: str) -> str:
    return (
        function.replace("values: int", "values: list[int]")
        .replace(", count: int", "")
        .replace(
            "values_converted = datetime_to_timestamptz(values)",
            "values_converted = [_ffi.cast('const TimestampTz', x) for x in values]",
        )
        .replace("count", "len(values)")
    )


def dateset_make_modifier(function: str) -> str:
    return (
        function.replace("values: date", "values: List[date]")
        .replace(", count: int", "")
        .replace(
            "values_converted = date_to_date_adt(values)",
            "values_converted = [_ffi.cast('const DateADT', x) for x in values]",
        )
        .replace("count", "len(values)")
    )


def spanset_make_modifier(function: str) -> str:
    return (
        function.replace(
            "spans: Annotated[_ffi.CData, 'Span *'], count: int", "spans: list[Annotated[_ffi.CData, 'Span *']]"
        )
        .replace("_ffi.cast('Span *', spans)", "_ffi.new('Span []', spans)")
        .replace(", count", ", len(spans)")
    )


def mi_span_span_modifier(function: str) -> str:
    return function.replace(
        '-> Annotated[_ffi.CData, "Span *"]', '-> tuple[Annotated[_ffi.CData, "Span *"], int]'
    ).replace("return out_result", "return out_result, result")
