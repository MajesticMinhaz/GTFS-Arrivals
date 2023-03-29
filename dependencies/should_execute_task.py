from redis import Redis
from datetime import date, datetime, timedelta
from .calculate_time import seconds_until_midnight
from .calculate_time import seconds_until


def set_redis_key_with_expiry(redis: Redis, key_name: str,  value: str = None, expiry_datetime: datetime = None) -> bool:
    """
    Sets a Redis key with a given name and expiry datetime.

    Args:
        redis: An instance of Redis.
        key_name: A string representing the name of the key.
        expiry_datetime: A datetime object representing the expiry datetime for the key.
        value: The value of key

    Returns:
        A boolean representing whether the key was successfully set.
    """
    key_exists = redis.setnx(key_name, value)
    if key_exists and expiry_datetime:
        seconds_until_expiry = seconds_until(expiry_datetime)
        redis.expire(key_name, int(seconds_until_expiry))
    return key_exists


def should_execute_process_zip_task(redis: Redis) -> bool:
    """
    Check if a 'process_zipfile_{today}' key exists in Redis. If the key doesn't exist,
    set it with a TTL equal to the number of seconds until midnight (UTC) and return True.
    If the key already exists, return False.

    Args:
        redis: A Redis instance to use for checking and setting the key.

    Returns:
        A boolean value representing whether the key was successfully set.
    """
    # Get the current date in ISO format
    today = date.today().isoformat()

    # Construct the key name with today's date
    key_name = f'process_zipfile_{today}'

    # Calculate the number of seconds until midnight (UTC)
    seconds_until_midnight_val = seconds_until_midnight()

    # Set the key with a TTL equal to seconds until midnight
    return set_redis_key_with_expiry(
        redis=redis,
        key_name=key_name,
        value="1",
        expiry_datetime=datetime.utcnow() + timedelta(seconds=seconds_until_midnight_val)
    )


def should_execute_query(redis: Redis, unique_identifier: str) -> bool:
    """
    Sets a task with a given task name, unique identifier, and expiry datetime in Redis.

    Args:
        redis: An instance of Redis.
        unique_identifier: A unique identifier for the task.

    Returns:
        A boolean representing whether the task was successfully set.
    """
    is_exists = redis.exists(unique_identifier)
    return not bool(is_exists)
