
def positive_int(value: int, name: str):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} value must be a positive integer")
    return value
