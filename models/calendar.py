from core import db
from datetime import datetime


class Calendar(db.Model):
    """
    Model representing a service's calendar schedule.
    """

    __tablename__ = 'calendar'

    # Columns of the table
    service_id = db.Column(db.Integer, primary_key=True, nullable=False)
    monday = db.Column(db.Boolean, nullable=False)
    tuesday = db.Column(db.Boolean, nullable=False)
    wednesday = db.Column(db.Boolean, nullable=False)
    thursday = db.Column(db.Boolean, nullable=False)
    friday = db.Column(db.Boolean, nullable=False)
    saturday = db.Column(db.Boolean, nullable=False)
    sunday = db.Column(db.Boolean, nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), nullable=False)
    end_date = db.Column(db.DateTime(timezone=True), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow
    )

    def __init__(self, service_id: int, monday: bool, tuesday: bool, wednesday: bool, thursday: bool, friday: bool, saturday: bool, sunday: bool, start_date: datetime.date, end_date: datetime.date):
        """
        Constructor for the Calendar model.

        Args:
            service_id (int): The ID of the service this calendar is for.
            monday (bool): Whether the service operates on Mondays.
            tuesday (bool): Whether the service operates on Tuesdays.
            wednesday (bool): Whether the service operates on Wednesdays.
            thursday (bool): Whether the service operates on Thursdays.
            friday (bool): Whether the service operates on Fridays.
            saturday (bool): Whether the service operates on Saturdays.
            sunday (bool): Whether the service operates on Sundays.
            start_date (datetime.date): The first date that this calendar applies to.
            end_date (datetime.date): The last date that this calendar applies to.
        """
        self.service_id = service_id
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object.
        """
        return f"Calendar(service_id={self.service_id}, monday={self.monday}, tuesday={self.tuesday}, wednesday={self.wednesday}, thursday={self.thursday}, friday={self.friday}, saturday={self.saturday}, sunday={self.sunday}, start_date={self.start_date}, end_date={self.end_date})"
