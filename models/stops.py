from core import db
from datetime import datetime


class Stops(db.Model):
    """Class representing a stop in a transportation system."""

    __tablename__ = 'stops'

    stop_id = db.Column(db.String(20), nullable=False, primary_key=True)
    """The ID of the stop. Primary key of the table."""

    stop_name = db.Column(db.String(255), nullable=False)
    """The name of the stop."""

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow
    )

    def __init__(self, stop_id: str, stop_name: str):
        """Constructor for a new Stop object.

        Args:
            stop_id: The ID of the stop.
            stop_name: The name of the stop.
        """
        self.stop_id = stop_id
        self.stop_name = stop_name

    def __repr__(self):
        """Returns a string representation of the Stop object."""
        return f"Stop(id={self.stop_id}, name={self.stop_name})"
