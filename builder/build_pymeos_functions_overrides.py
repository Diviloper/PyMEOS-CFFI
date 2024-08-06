def meos_initialize_override() -> str:
    return """def meos_initialize(tz_str: "Optional[str]") -> None:
    if "PROJ_DATA" not in os.environ and "PROJ_LIB" not in os.environ:
        proj_dir = os.path.join(os.path.dirname(__file__), "proj_data")
        if os.path.exists(proj_dir):
            # Assume we are in a wheel and the PROJ data is in the package
            os.environ["PROJ_DATA"] = proj_dir
            os.environ["PROJ_LIB"] = proj_dir
    
    tz_str_converted = tz_str.encode('utf-8') if tz_str is not None else _ffi.NULL
    _lib.meos_initialize(tz_str_converted, _lib.py_error_handler)"""


def cstring2text_override() -> str:
    return """def cstring2text(cstring: str) -> 'text *':
    cstring_converted = cstring.encode('utf-8')
    result = _lib.cstring2text(cstring_converted)
    return result"""


def text2cstring_override() -> str:
    return """def text2cstring(textptr: 'text *') -> str:
    result = _lib.text2cstring(textptr)
    result = _ffi.string(result).decode('utf-8')
    return result"""


def from_wkb_override(function: str, return_type: str) -> str:
    return f"""def {function}(wkb: bytes) -> '{return_type} *':
    wkb_converted = _ffi.new('uint8_t []', wkb)
    result = _lib.{function}(wkb_converted, len(wkb))
    return result if result != _ffi.NULL else None"""
