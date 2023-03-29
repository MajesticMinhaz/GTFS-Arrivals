import datetime


def seconds_until(upcoming_datetime: datetime.datetime) -> int:
    """
    Calculates the number of seconds between the current time in UTC and a given upcoming datetime.

    Args:
        upcoming_datetime: A datetime object representing the upcoming datetime.

    Returns:
        An integer representing the number of seconds between the current time and the given upcoming datetime.
    """
    now = datetime.datetime.utcnow()
    diff_seconds = (upcoming_datetime - now).total_seconds()
    return int(diff_seconds)


def seconds_until_midnight() -> float:
    """
    Calculates the number of seconds until midnight UTC.

    Returns:
        A floating-point number representing the number of seconds until midnight UTC.
    """
    # Get the current date and time in UTC
    now = datetime.datetime.utcnow()

    # Calculate the number of seconds until the next day
    tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    seconds_until_tomorrow = seconds_until(upcoming_datetime=tomorrow)

    return seconds_until_tomorrow
