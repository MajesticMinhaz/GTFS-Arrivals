from core import db
from datetime import timedelta
from datetime import datetime


class StopTimes(db.Model):
    """
    A model class representing stop times for trips.
    """
    __tablename__ = 'stop_times'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.String(60), nullable=False)
    arrival_time = db.Column(db.Interval, nullable=False)
    departure_time = db.Column(db.Interval, nullable=False)
    stop_id = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow
    )

    def __init__(self, trip_id: str, arrival_time: timedelta, departure_time: timedelta, stop_id: str):
        """
        Constructor method to initialize an instance of StopTimes.

        Args:
            trip_id (str): The ID of the trip.
            arrival_time (timedelta): The arrival time at the stop.
            departure_time (timedelta): The departure time from the stop.
            stop_id (str): The ID of the stop.
        """
        self.trip_id = trip_id
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.stop_id = stop_id

    def __repr__(self):
        """
        Returns a string representation of the StopTimes instance.

        Returns:
            str: A string representation of the StopTimes instance.
        """
        return f"StopTime(stop_id={self.stop_id}, trip_id={self.trip_id}, arrival_time={self.arrival_time}, departure_time={self.departure_time})"
