"""NewEvent class is used to define external events for ics calendar generation.

Examples of external events: University wide events, exam seasons, reading week, etc.
"""

from datetime import datetime


class NewEvent:
    def __init__(self, name: str, description: str, start_datetime: datetime, end_datetime: datetime):
        """Basic event used to generate simple external events.

        This class is used to simplify .ics file generation of non-course meeting events.

        Args:
            name: Name of the event.
            description: Description for the event.
            start_datetime: Start datetime of the event. (Usually want to use time.min).
            end_datetime: End datetime of the event. (Usually want to use time.max).

        Example:
            NewEvent(
                name="Reading Week",
                description="No class",
                start_datetime=datetime.combine(date(2022, 2, 21), time.min),
                end_datetime=datetime.combine(date(2022, 2, 25), time.max)
        """
        self.name = name
        self.description = description
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def __str__(self):
        """For prototyping purposes only.

        Returns:
            Default str similar to regular __str__ methods.
        """
        return (f"name={self.name}\n"
                f"description={self.description}\n"
                f"start_datetime={self.start_datetime}\n"
                f"end_datetime={self.end_datetime}")
