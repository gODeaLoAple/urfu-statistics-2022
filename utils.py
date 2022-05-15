def try_parse_int(x: str) -> [bool, int]:
    if x is None:
        return False, 0
    try:
        return True, int(x)
    except:
        return False, 0