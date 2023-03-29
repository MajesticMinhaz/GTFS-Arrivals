import json
import pytz
from dependencies import convert_timezone
from typing import Dict
from flask import Blueprint, jsonify, request
from dependencies import parse_args
from dependencies import should_execute_query
from datetime import datetime
from dependencies import response_model_creator
from core import db
from models import create_query
from dependencies import set_redis_key_with_expiry
from core import my_redis


stops_blueprint = Blueprint('stops', __name__)


def dataset_handle(dataset: list, keys: list, target_tz: pytz.FixedOffset):
    """
    Process a given dataset and keys and return dataset of dict.

    Args:
        dataset (list): Stop ID to filter the query results.
        keys (list): Maximum number of records to retrieve.
        target_tz (pytz.FixedOffset): Target Timezone

    Returns:
        rows (List[Dict[str, Any]]): List of dictionaries containing the query results, where each dictionary represents a row
        in the results set with the column names as keys and the corresponding cell values as values.
        first_arrival_datetime (Any | None): The datetime of the first arrival, or None if no arrivals were found.
    """

    # Execute the SQL statement with the provided parameters

    # Map the query results to a list of dictionaries, where each dictionary represents a row in the results set with
    # the column names as keys and the corresponding cell values as values
    rows = [dict(zip(keys, row)) for row in dataset]
    first_arrival = None

    for index, row in enumerate(rows):
        if 'arrival' in row and index == 0:
            first_arrival = row['arrival'].replace(tzinfo=None)

            print(row['arrival'])
            print(type(row['arrival']))

        if 'arrival' in row:
            row['arrival'] = convert_timezone(
                utc_timezone=datetime.fromisoformat(row['arrival'].isoformat()),
                offset=target_tz
            ).isoformat()

            row['departure'] = convert_timezone(
                utc_timezone=datetime.fromisoformat(row['departure'].isoformat()),
                offset=target_tz
            ).isoformat()

    return rows, first_arrival


def get_stops(stop_id: str, skip: int, limit: int, _datetime: datetime, redis_key: str) -> Dict:
    """
    Gets Stops data for a given bus stop.

    :param stop_id: The ID of the bus stop to get arrival data for.
    :param skip: The number of results to skip (for pagination).
    :param limit: The maximum number of results to return (for pagination).
    :param _datetime: The datetime of stops
    :param redis_key: The unique key of redis
    :return: A dictionary containing arrival data for the specified bus stop.
    """

    result = create_query(
        session=db.session,
        stop_id=stop_id,
        query_datetime_with_timezone=_datetime.astimezone(pytz.utc),
        limit=limit,
        skip=skip
    )

    dataset, expiry_datetime = dataset_handle(
        dataset=result.all(),
        keys=["stop_name", "destination", "route_name", "arrival", "departure"],
        target_tz=_datetime.tzinfo
    )

    # # Use the dataset to create a response JSON object.
    json_data = response_model_creator(dataset=dataset)

    if expiry_datetime:
        # Cache the response JSON object in Redis with an expiry time.
        set_redis_key_with_expiry(my_redis, redis_key, json.dumps(json_data), expiry_datetime)
        return json_data

    # If no arrivals were found, return a message indicating so.
    else:
        return {
            'stop_id': stop_id,
            'skip': skip,
            'limit': limit,
            'msg': 'no arrival found'
        }


@stops_blueprint.route(rule='/<string:stop_id>', methods=['GET'])
def get_arrival_by_stop_id(stop_id: str):
    """
    Flask route function to retrieve all arrivals for a particular stop.

    Query parameters 'skip' and 'limit' are supported for pagination.

    Args:
        stop_id: The ID of the stop to retrieve arrivals for.

    Returns:
        A JSON response containing the list of arrivals.
    """
    # Parse skip and limit arguments from query parameters
    skip, limit, parsed_datetime, has_date, has_time = parse_args(request.args)

    unique_identifier = f'stops_{stop_id}{skip}{limit}{has_date}{has_time}{parsed_datetime.strftime("%z")}'

    if should_execute_query(redis=my_redis, unique_identifier=unique_identifier):
        try:
            json_data = get_stops(
                stop_id=stop_id,
                skip=skip,
                limit=limit,
                _datetime=parsed_datetime,
                redis_key=unique_identifier
            )

        except Exception as e:
            # If the task doesn't complete within the timeout period, return an error message
            json_data = {"msg": f"something went wrong!!, {e}"}

    else:
        # If the data is cached in Redis, retrieve it
        json_data = json.loads(my_redis.get(unique_identifier))

    return jsonify(json_data)
