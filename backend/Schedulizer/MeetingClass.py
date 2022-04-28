"""
Meeting class is used to define each instance a course has a meeting. If that specific meeting repeats, the repeat
delta is in an integer representing the day time delta, typically 7 or 14 representing weekly and biweekly meetings.
"""
from pydantic import BaseModel
from datetime import date, time


class Meeting(BaseModel):
    """Meeting class defines an instance of when a course meeting occurs. Has a repeated timedelta option in days.

    time_start: meeting start time.
    time_end: meeting end time.
    weekday_int: weekday int value (Sunday = 0, Monday = 1, ... , Saturday = 6, No day/async = -1).
    date_start: meeting start date window.
    date_end: meeting end date window.
    repeat_timedelta_days: represents a datetime.timedelta in days -> meeting repeat intervals, if a meeting does not
        repeat value = 0.
    location: location info (Usually format of: "Campus | Building | Room").
    """

    time_start: time
    time_end: time
    weekday_int: int
    date_start: date
    date_end: date
    repeat_timedelta_days: int = 0
    location: str | None

    def get_raw_str(self):
        return (f"time_start={self.time_start}\n"
                f"time_end={self.time_end}\n"
                f"weekday_int={self.weekday_int}\n"
                f"date_start={self.date_start}\n"
                f"date_end={self.date_end}\n"
                f"repeat_timedelta_days={self.repeat_timedelta_days}\n"
                f"location={self.location}")

    def __str__(self):
        return self.get_raw_str()
