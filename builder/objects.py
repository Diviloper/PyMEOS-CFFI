from dataclasses import dataclass
from collections.abc import Callable


@dataclass
class Conversion:
    c_type: str
    p_type: str
    p_to_c: Callable[[str], str] | None
    c_to_p: Callable[[str], str] | None


def expand_conversions(
    c_type: str,
    p_type: str,
    p_to_c: Optional[Callable[[str], str]],
    c_to_p: Optional[Callable[[str], str]],
) -> Dict[str, Conversion]:
    return {
        c_type: Conversion(c_type, p_type, p_to_c, c_to_p),
        f"{c_type} *": Conversion(f"{c_type} *", p_type, p_to_c, c_to_p),
        f"const {c_type}": Conversion(f"const {c_type}", p_type, p_to_c, c_to_p),
        f"const {c_type} *": Conversion(f"const {c_type} *", p_type, p_to_c, c_to_p),
    }


def int_conversions() -> Dict[str, Conversion]:
    int_types = [
        "int8",
        "int16",
        "int32",
        "int64",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "uint8_t",
    ]
    return {
        int_t: Conversion(
            int_t, "int", lambda p_obj: f"_ffi.cast('{int_t}', {p_obj})", None
        )
        for int_t in int_types
    }


conversion_map: dict[str, Conversion] = {
    "void": Conversion("void", "None", None, None),
    "bool": Conversion("bool", "bool", None, None),
    "int": Conversion("int", "int", None, None),
    **int_conversions(),
    "double": Conversion("double", "float", None, None),
    "char *": Conversion(
        "char *",
        "str",
        lambda p_obj: f"{p_obj}.encode('utf-8')",
        lambda c_obj: f"_ffi.string({c_obj}).decode('utf-8')",
    ),
    "const char *": Conversion(
        "const char *",
        "str",
        lambda p_obj: f"{p_obj}.encode('utf-8')",
        lambda c_obj: f"_ffi.string({c_obj}).decode('utf-8')",
    ),
    **expand_conversions(
        "text",
        "str",
        lambda p_obj: f"cstring2text({p_obj})",
        lambda c_obj: f"text2cstring({c_obj})",
    ),
    "Timestamp": Conversion(
        "Timestamp",
        "int",
        lambda p_obj: f"_ffi.cast('Timestamp', {p_obj})",
        None,
    ),
    **expand_conversions(
        "TimestampTz",
        "datetime",
        lambda p_obj: f"datetime_to_timestamptz({p_obj})",
        lambda c_obj: f"timestamptz_to_datetime({c_obj})",
    ),
    **expand_conversions(
        "DateADT",
        "date",
        lambda p_obj: f"date_to_date_adt({p_obj})",
        lambda c_obj: f"date_adt_to_date({c_obj})",
    ),
    **expand_conversions(
        "Interval",
        "timedelta",
        lambda p_obj: f"timedelta_to_interval({p_obj})",
        lambda c_obj: f"interval_to_timedelta({c_obj})",
    ),
    "TimeOffset": Conversion("TimeOffset", "int", lambda p_obj: f"_ffi.cast('TimeOffset', {p_obj})", None),
    "interpType": Conversion("interpType", "InterpolationType", None, None),
}
