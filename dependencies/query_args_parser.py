from typing import Dict, Any
from datetime import datetime
from dependencies import parse_date, parse_time
from pytz import FixedOffset


def parse_args(args: Dict[str, Any]) -> tuple[int, int, datetime | Any, Any | None, Any | None]:
    """
    Parses the 'skip', 'limit', timezone, date and time query parameters from the given args dictionary.

    Args:
        args (Dict[str, Any]): A dictionary of request query parameters.

    Returns:
        tuple[int, int, datetime | Any, Any | None, Any | None]: A tuple containing the parsed 'skip' and 'limit' values,
        the parsed datetime value (if available), and flags indicating whether the 'date' and/or 'time' parameters
        were provided.

    Raises:
        ValueError: If any of the query parameter values cannot be parsed.

    """
    skip = int(args.get('skip', 0))  # Get the 'skip' parameter, or use 0 if it's not provided.
    limit = int(args.get('limit', 10))  # Get the 'limit' parameter, or use 100 if it's not provided.

    utc_offset = float(args.get('tz', 0))  # Get the 'tz' parameter or use +0.0 if it's not provided.

    # Parse the 'date' parameter or use the current UTC date if it's not provided.
    date = parse_date(args.get('date', datetime.utcnow().date().isoformat()), date_format='%Y-%m-%d')

    # Parse the 'time' parameter or use the current UTC time rounded to the nearest second if it's not provided.
    time = parse_time(args.get('time', datetime.utcnow().time().replace(microsecond=0).isoformat()))

    # Create a FixedOffset object for the local timezone based on the 'tz' parameter.
    local_tz = FixedOffset(int(utc_offset * 60))

    # If both 'date' and 'time' were provided, combine them into a single datetime object in the local timezone.
    if date and time:
        parsed_datetime = (date + time).astimezone(local_tz)
    # Otherwise, use the current datetime in the local timezone.
    else:
        parsed_datetime = datetime.now().replace(microsecond=0).astimezone(local_tz)

    # Determine if the 'date' and 'time' parameters were provided.
    has_time = 'time' in args
    has_date = 'date' in args

    return skip, limit, parsed_datetime, has_date, has_time
