from datetime import timedelta


def parse_time(time_string: str) -> timedelta or None:
    """
    Parse a time string in HH:MM:SS format and return a timedelta object representing the time interval.
    If the hour is greater than 23, add a day to the interval and subtract 24 hours from the hour value.

    :param time_string: A string representing a time in HH:MM:SS format.
    :return: A timedelta object representing the time interval.
    """
    try:
        hours, minutes, seconds = map(int, time_string.split(':'))
        days = hours // 24
        hours %= 24
        interval = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        return interval
    except ValueError:
        return None
