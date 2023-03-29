from core import db
from datetime import datetime


class Routes(db.Model):
    """
    A class used to represent a route in a transportation system.

    Attributes:
    -----------
    route_id : str
        The unique identifier for the route.
    route_short_name : str
        A short name or number that identifies the route.
    route_type : int
        The type of transportation used on the route, e.g. bus or train.
    created_at : datetime.datetime
        The timestamp indicating when the route was created.
    updated_at : datetime.datetime
        The timestamp indicating when the route was last updated.
    """

    __tablename__ = 'routes'

    route_id = db.Column(db.String(20), nullable=False, primary_key=True)
    route_short_name = db.Column(db.String(255), nullable=False)
    route_type = db.Column(db.Integer, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow
    )

    def __init__(self, route_id: str, route_short_name: str, route_type: str):
        """
        Parameters:
        ----------
        route_id : str
            The unique identifier for the route.
        route_short_name : str
            A short name or number that identifies the route.
        route_type : int
            The type of transportation used on the route, e.g. bus or train.
        """
        self.route_id = route_id
        self.route_short_name = route_short_name
        self.route_type = route_type

    def __repr__(self):
        """
        Returns a string representation of the Route object.

        Returns:
        -------
        str
            A string representation of the Route object.
        """
        return f"Route(id={self.route_id}, name={self.route_short_name}, type={self.route_type})"
