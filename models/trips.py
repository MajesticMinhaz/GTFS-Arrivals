from core import db
from datetime import datetime


class Trips(db.Model):
    """
    This class represents a trip in the transit system. It contains information
    such as the route, service, and destination.

    Attributes:
        trip_id (str): The ID of the trip.
        route_id (str): The ID of the route associated with the trip.
        service_id (int): The ID of the service associated with the trip.
        destination (str): The destination of the trip.
        created_at (datetime): The date and time the record was created.
        updated_at (datetime): The date and time the record was last updated.
    """

    __tablename__ = 'trips'

    trip_id = db.Column(db.String(60), nullable=False, primary_key=True)
    route_id = db.Column(db.String(20), nullable=False)
    service_id = db.Column(db.Integer, nullable=False)
    trip_headsign = db.Column(db.String(200), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow
    )

    def __init__(self, trip_id: str, route_id: str, service_id: int, trip_headsign: str):
        """
        Initializes a new instance of the Trip class.

        Args:
            trip_id (str): The ID of the trip.
            route_id (str): The ID of the route associated with the trip.
            service_id (int): The ID of the service associated with the trip.
            trip_headsign (str): The destination of the trip.
        """
        self.trip_id = trip_id
        self.route_id = route_id
        self.service_id = service_id
        self.trip_headsign = trip_headsign

    def __repr__(self):
        """
        Returns a string representation of the Trip object.

        Returns:
            str: A string representation of the Trip object.
        """
        return f"Trip(id={self.trip_id}, route_id={self.route_id}, service_id={self.service_id}, destination={self.destination})"
