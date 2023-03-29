from datetime import datetime
from pytz import utc


def parse_date(date_string: str, date_format: str = '%Y%m%d') -> datetime.date or None:
    """
    Parse a date string based on the given format string and return a datetime.date() object.
    If the date string and format do not match, return None.

    :param date_string: A string representing a date in the given format.
    :param date_format: A string representing the expected date format using datetime formatting codes.
    :return: A datetime.date() object representing the parsed date or None if the date string and format do not match.
    """
    try:
        date_obj = datetime.strptime(date_string, date_format)
        date_obj = utc.localize(date_obj)
        return date_obj
    except ValueError:
        return None
