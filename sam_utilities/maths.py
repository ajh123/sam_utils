def is_even(num: int | float):
    """
    Checks if a number is even.

    Parameters:
        num (int | float): The number to compare against.

    Returns:
        out (bool): `True`, if the number is even, `False` if the number is odd.
    """
    if num % 2 == 0:
        return True
    return False

def is_numeric(thing):
    """
    Checks if a thing is a number (integers or floats).

    Parameters:
        thing (Any): The object you want to compare against.

    Returns:
        out (bool): `True` if the object is an integer or a float, `False` if the object is not.
    """
    if isinstance(thing, (int, float)):
        return True
    return False

def is_positive(num: int | float):
    """
    Checks if a number (integers or floats) is positive.
    
    Parameters:
        num (int | float): The number you want to check.
    
    Returns:
        out (bool): `True` if the number is positive, `False` if not.
    """
    if is_numeric(num):
        if num > 0:
            return True
    return False