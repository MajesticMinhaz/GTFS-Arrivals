from flask_sqlalchemy.query import Query
from flask_sqlalchemy.session import Session
from datetime import datetime
from models import Stops, StopTimes, Trips, Routes, Calendar


def create_query(
        session: Session,
        stop_id: str,
        query_datetime_with_timezone: datetime,
        limit: int,
        skip: int
) -> Query:
    weekday_columns = {
        0: Calendar.monday,
        1: Calendar.tuesday,
        2: Calendar.wednesday,
        3: Calendar.thursday,
        4: Calendar.friday,
        5: Calendar.saturday,
        6: Calendar.sunday
    }
    weekday_column = weekday_columns[query_datetime_with_timezone.weekday()]

    arrival_datetime = StopTimes.arrival_time + query_datetime_with_timezone.replace(hour=0, minute=0, second=0)

    departure_datetime = StopTimes.departure_time + query_datetime_with_timezone.replace(hour=0, minute=0, second=0)

    query = session.query(
        Stops.stop_name.label('stop_name'),
        Trips.trip_headsign.label('destination'),
        Routes.route_short_name.label('route_name'),
        arrival_datetime.label('arrival'),
        departure_datetime.label('departure')
    ).join(
        StopTimes,
        Stops.stop_id == StopTimes.stop_id
    ).join(
        Trips,
        StopTimes.trip_id == Trips.trip_id
    ).join(
        Routes,
        Trips.route_id == Routes.route_id
    ).join(
        Calendar,
        Trips.service_id == Calendar.service_id
    ).filter(
        Stops.stop_id == stop_id,
        weekday_column,
        Calendar.start_date <= query_datetime_with_timezone,
        Calendar.end_date >= query_datetime_with_timezone,
        arrival_datetime >= query_datetime_with_timezone
    ).order_by(
        'arrival'
    ).limit(limit).offset(skip)

    try:
        return query
    except Exception as e:
        print(e)
