from typing import List, Set, Tuple, Dict

from .build_pymeos_functions_modifiers import *
from .build_pymeos_functions_overrides import *

reserved_words = {
    "str": "string",
    "is": "iset",
    "from": "from_",
}

hidden_functions: List[str] = [
    "_check_error",
]

# List of MEOS functions that should not be defined in functions.py
skipped_functions: List[str] = [
    "py_error_handler",
    "meos_initialize_timezone",
    "meos_initialize_error_handler",
    "meos_finalize_timezone",
]

function_overrides: Dict[str, str] = {
    "meos_initialize": meos_initialize_override(),
    "cstring2text": cstring2text_override(),
    "text2cstring": text2cstring_override(),
    "temporal_from_wkb": from_wkb_override("temporal_from_wkb", "Temporal"),
    "set_from_wkb": from_wkb_override("set_from_wkb", "Set"),
    "span_from_wkb": from_wkb_override("span_from_wkb", "Span"),
    "spanset_from_wkb": from_wkb_override("spanset_from_wkb", "SpanSet"),
    "tbox_from_wkb": from_wkb_override("tbox_from_wkb", "TBOX"),
    "stbox_from_wkb": from_wkb_override("stbox_from_wkb", "STBOX"),
}

function_modifiers: Dict[str, Callable[[str], str]] = {
    "meos_finalize": remove_error_check_modifier,
    "spanset_make": spanset_make_modifier,
    "temporal_as_wkb": as_wkb_modifier,
    "set_as_wkb": as_wkb_modifier,
    "span_as_wkb": as_wkb_modifier,
    "spanset_as_wkb": as_wkb_modifier,
    "tbox_as_wkb": as_wkb_modifier,
    "stbox_as_wkb": as_wkb_modifier,
    "tstzset_make": tstzset_make_modifier,
    "dateset_make": dateset_make_modifier,
    "intset_make": array_parameter_modifier("values", "count"),
    "bigintset_make": array_parameter_modifier("values", "count"),
    "floatset_make": array_parameter_modifier("values", "count"),
    "textset_make": textset_make_modifier,
    "geoset_make": array_length_remover_modifier("values", "count"),
    "tsequenceset_make_gaps": array_length_remover_modifier("instants", "count"),
}

# List of result function parameters in tuples of (function, parameter)
result_parameters: Set[Tuple[str, str]] = {
    ("tbool_value_at_timestamptz", "value"),
    ("ttext_value_at_timestamptz", "value"),
    ("tint_value_at_timestamptz", "value"),
    ("tfloat_value_at_timestamptz", "value"),
    ("tpoint_value_at_timestamptz", "value"),
}

# List of output function parameters in tuples of (function, parameter).
# All parameters named result are assumed to be output parameters, and it is
# not necessary to list them here.
output_parameters: Set[Tuple[str, str]] = {
    ("temporal_time_split", "time_buckets"),
    ("temporal_time_split", "count"),
    ("tint_value_split", "value_buckets"),
    ("tint_value_split", "count"),
    ("tfloat_value_split", "value_buckets"),
    ("tfloat_value_split", "count"),
    ("tint_value_time_split", "value_buckets"),
    ("tint_value_time_split", "time_buckets"),
    ("tint_value_time_split", "count"),
    ("tfloat_value_time_split", "value_buckets"),
    ("tfloat_value_time_split", "time_buckets"),
    ("tfloat_value_time_split", "count"),
    ("tpoint_space_split", "space_buckets"),
    ("tpoint_space_split", "count"),
    ("tpoint_space_time_split", "space_buckets"),
    ("tpoint_space_time_split", "time_buckets"),
    ("tpoint_space_time_split", "count"),
    ("tbox_as_hexwkb", "size"),
    ("stbox_as_hexwkb", "size"),
    ("tintbox_tile_list", "count"),
    ("tfloatbox_tile_list", "count"),
    ("stbox_tile_list", "cellcount"),
}

# List of nullable function parameters in tuples of (function, parameter)
nullable_parameters: Set[Tuple[str, str]] = {
    ("meos_initialize", "tz_str"),
    ("meos_set_intervalstyle", "extra"),
    ("temporal_append_tinstant", "maxt"),
    ("temporal_as_mfjson", "srs"),
    ("geo_as_geojson", "srs"),
    ("tstzspan_shift_scale", "shift"),
    ("tstzspan_shift_scale", "duration"),
    ("tstzset_shift_scale", "shift"),
    ("tstzset_shift_scale", "duration"),
    ("tstzspanset_shift_scale", "shift"),
    ("tstzspanset_shift_scale", "duration"),
    ("temporal_shift_scale_time", "shift"),
    ("temporal_shift_scale_time", "duration"),
    ("tbox_make", "p"),
    ("tbox_make", "s"),
    ("stbox_make", "p"),
    ("stbox_shift_scale_time", "shift"),
    ("stbox_shift_scale_time", "duration"),
    ("temporal_tcount_transfn", "state"),
    ("temporal_extent_transfn", "p"),
    ("tnumber_extent_transfn", "box"),
    ("tpoint_extent_transfn", "box"),
    ("tbool_tand_transfn", "state"),
    ("tbool_tor_transfn", "state"),
    ("tbox_shift_scale_time", "shift"),
    ("tbox_shift_scale_time", "duration"),
    ("tint_tmin_transfn", "state"),
    ("tfloat_tmin_transfn", "state"),
    ("tint_tmax_transfn", "state"),
    ("tfloat_tmax_transfn", "state"),
    ("tint_tsum_transfn", "state"),
    ("tfloat_tsum_transfn", "state"),
    ("tnumber_tavg_transfn", "state"),
    ("ttext_tmin_transfn", "state"),
    ("ttext_tmax_transfn", "state"),
    ("temporal_tcount_transfn", "interval"),
    ("timestamptz_tcount_transfn", "interval"),
    ("tstzset_tcount_transfn", "interval"),
    ("tstzspan_tcount_transfn", "interval"),
    ("tstzspanset_tcount_transfn", "interval"),
    ("timestamptz_extent_transfn", "p"),
    ("timestamptz_tcount_transfn", "state"),
    ("tstzset_tcount_transfn", "state"),
    ("tstzspan_tcount_transfn", "state"),
    ("tstzspanset_tcount_transfn", "state"),
    ("stbox_tile_list", "duration"),
    ("tintbox_tile_list", "xorigin"),
    ("tintbox_tile_list", "torigin"),
    ("tfloatbox_tile_list", "xorigin"),
    ("tfloatbox_tile_list", "torigin"),
    ("tpoint_at_geom_time", "zspan"),
    ("tpoint_at_geom_time", "period"),
    ("tpoint_minus_geom_time", "zspan"),
    ("tpoint_minus_geom_time", "period"),
    ("stbox_make", "s"),
    ("tsequenceset_make_gaps", "maxt"),
}

# List of parameters that are arrays
array_parameters: Set[Tuple[str, str]] = set()


# Checks if parameter in function is nullable
def is_nullable_parameter(function: str, parameter: str) -> bool:
    return (function, parameter) in nullable_parameters


# Checks if parameter in function is actually a result parameter
def is_result_parameter(function: str, parameter: str) -> bool:
    if parameter == "result":
        return True
    return (function, parameter) in result_parameters


# Checks if parameter in function is actually an output parameter
def is_output_parameter(function: str, parameter: str, parameter_type: str) -> bool:
    if parameter.endswith("_out"):
        return True
    if parameter == "count" and parameter_type.endswith("*"):
        return True
    return (function, parameter) in output_parameters


# Checks if parameter in function is actually an array
def is_array_parameter(function: str, parameter: str, parameter_type: str) -> bool:
    if parameter_type.endswith("**"):
        return True
    if parameter_type.endswith("[]"):
        return True
    return (function, parameter) in array_parameters


def check_modifiers(functions: List[str]) -> None:
    for func in function_overrides.keys():
        if func not in functions:
            print(f"Override defined for non-existent function {func}")

    for func in function_modifiers.keys():
        if func not in functions:
            print(f"Modifier defined for non-existent function {func}")

    for func, param in result_parameters:
        if func not in functions:
            print(
                f"Result parameter defined for non-existent function {func} ({param})"
            )

    for func, param in output_parameters:
        if func not in functions:
            print(
                f"Output parameter defined for non-existent function {func} ({param})"
            )

    for func, param in nullable_parameters:
        if func not in functions:
            print(
                f"Nullable Parameter defined for non-existent function {func} ({param})"
            )
