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

        self._time_start = time_start
        self._time_end = time_end
        self._weekday_int = weekday_int
        self._date_start = date_start
        self._date_end = date_end
        self._repeat_timedelta_days = repeat_timedelta_days
        self._location = location

    @property
    def time_start(self):
        return self._time_start

    @property
    def time_end(self):
        return self._time_end

    @property
    def weekday_int(self):
        return self._weekday_int

    @property
    def date_start(self):
        return self._date_start

    @property
    def date_end(self):
        return self._date_end

    @property
    def repeat_timedelta_days(self):
        return self._repeat_timedelta_days

    @property
    def location(self):
        return self._location

    def get_raw_str(self):
        return (f"time_start={self._time_start}\n"
                f"time_end={self._time_end}\n"
                f"weekday_int={self._weekday_int}\n"
                f"date_start={self._date_start}\n"
                f"date_end={self._date_end}\n"
                f"repeat_timedelta_days={self._repeat_timedelta_days}\n"
                f"location={self._location}")

    def __str__(self):
        return self.get_raw_str()
