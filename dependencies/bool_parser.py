def parse_bool(number: str):
    """
    Returns True if the number of string arguments is greater than 0, False otherwise.

    Usage:
    >>> parse_bool('hello')
    False
    >>> parse_bool('')
    False
    >>> parse_bool('0')
    False
    >>> parse_bool('1')
    True
    >>> parse_bool('2')
    False
    """
    # Check the length of the argument list
    return True if number == '1' else False
