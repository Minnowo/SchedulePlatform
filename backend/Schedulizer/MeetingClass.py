"""
Meeting class is used to define each instance a course has a meeting. If that specific meeting repeats, the repeat
delta is in an integer representing the day time delta, typically 7 or 14 representing weekly and biweekly meetings.
"""


class Meeting:
    def __init__(self, time_start, time_end, weekday_int, date_start, date_end, repeat_timedelta_days, location):
        """
        :param datetime.time time_start: meeting start time.
        :param datetime.time time_end: meeting end time.
        :param int weekday_int: weekday int value (Sunday = 0, Monday = 1, ... , Saturday = 6, No day/async = -1).
        :param datetime.date date_start: meeting start date window.
        :param datetime.date date_end: meeting end date window.
        :param int repeat_timedelta_days: represents a datetime.timedelta in days -> meeting repeat intervals,
            if a meeting does not repeat value = 0.
        :param str location: location info (Usually format of: "Campus | Building | Room").
        """

        self.time_start = time_start
        self.time_end = time_end
        self.weekday_int = weekday_int
        self.date_start = date_start
        self.date_end = date_end
        self.repeat_timedelta_days = repeat_timedelta_days
        self.location = location

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
