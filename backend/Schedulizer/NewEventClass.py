"""NewEvent class is used to define external events for ics calendar generation.

Examples of external events: University wide events, club events, exam seasons,
reading week, etc.
"""

import json
from datetime import datetime
from types import SimpleNamespace


class NewEvent:
    def __init__(self, name: str, description: str, start_datetime: datetime,
                 end_datetime: datetime):
        """Basic event used to generate simple external events.

        This class is used to simplify .ics file generation of non-Course
        structure meeting events.

        Args:
            name: Name of the event.
            description: Description for the event.
            start_datetime: Start datetime of the event. (Usually want to use
                time.min for all day events).
            end_datetime: End datetime of the event. (Usually want to use
                time.max for all day events).

        Example:
            NewEvent(
                name="Reading Week",
                description="No class",
                start_datetime=datetime.combine(date(2022, 2, 21), time.min),
                end_datetime=datetime.combine(date(2022, 2, 25), time.max)
            )
        """
        self.name = name
        self.description = description
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime

    def to_json(self):
        """Converts a NewEvent object to json str.

        Returns:
            json string of the NewEvent object.
        """

        def default(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, int):
                return obj
            else:
                return obj.__dict__

        return json.dumps(self, default=default)

    @staticmethod
    def from_json(json_str: str):  # -> NewEvent:
        """Converts a json str to Course object.

        Args:
            json_str: json string of the Course object to decode from.

        Returns:
            Course from the decoded object.
        """
        simple = json.loads(json_str, object_hook=lambda d: SimpleNamespace(**d))

        return NewEvent(name=simple.name,
                        description=simple.description,
                        start_datetime=simple.start_datetime,
                        end_datetime=simple.end_datetime)

    def __str__(self):
        """For prototyping purposes only.

        Returns:
            Default str similar to regular __str__ methods.
        """
        return (f"name={self.name}\n"
                f"description={self.description}\n"
                f"start_datetime={self.start_datetime}\n"
                f"end_datetime={self.end_datetime}")
