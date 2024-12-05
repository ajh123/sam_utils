import math

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

def is_prime(num: int) -> bool:
    nums = list(range(2, int(math.sqrt(num))))
    # Iterate all numbers before self
    for cn in nums:
        # Check if remainder of self / current number is 0
        # This means that self cannot be divided by the current number
        if (num % cn) == 0:
           return False 
    return True

if __name__ == "__main__":
    print(is_prime(1))
    print(is_prime(6))
    print(is_prime(7))
    print(is_prime(10))
    print(is_prime(11))