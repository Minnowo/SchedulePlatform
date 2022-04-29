"""
Meeting class is used to define each instance a course has a meeting. If that specific meeting repeats, the repeat
delta is in an integer representing the day time delta, typically 7 or 14 representing weekly and biweekly meetings.
"""
from pydantic import BaseModel
from datetime import date, time, timedelta


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

    def get_actual_date_start(self) -> date:
        """Get the actual date of the first matching weekday_int.

        Returns:
            First datetime.date of the actual date which the meeting starts.

        Say a Meeting object has a self.weekday_int of 0 (representing a meeting on Monday), but has a
        self.date_start value that has a weekday (int) value that is not 0.
            Under certain circumstances a Meeting object can have a self.date_start that does not fall on the
            self.weekday_int. This commonly occurs with Courses running repeating meetings weekly/biweekly, due to
            the way schools might set their date start and end. They often set start and end dates of weekly
            courses with the start and end of the semester).
        This function works to return the correct first date of the in which the Meeting should be on.
        """
        # Note I created/utilized this nested function since this is a really useful function that might one day be
        # needed outside this class structure.

        def get_minimum_date_of_target_weekday(target_weekday_int: int, base_date: date) -> date:
            """Get the first instance of a date that matches the target weekday in that falls on or after the base date.

            Args:
                target_weekday_int: Target weekday we want on the date.
                    Follows datetime.datetime.weekday() index convention. (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
                base_date: Initial date to start on.

            Returns:
                New date with the correct target weekday.

            Examples:
                >>> get_minimum_date_of_target_weekday(target_weekday_int=0,base_date=date(2022, 4, 1))
                datetime.date(2022, 4, 4)
                >>> get_minimum_date_of_target_weekday(target_weekday_int=4,base_date=date(2022, 4, 1))
                datetime.date(2022, 4, 1)
                >>> get_minimum_date_of_target_weekday(target_weekday_int=5,base_date=date(2022, 4, 1))
                datetime.date(2022, 4, 2)
            """
            target_delta_int = target_weekday_int - base_date.weekday()  # Calculate the shift required
            target_delta_int += 7 if target_delta_int < 0 else 0  # If your target is Monday and the start_time =
            # Wednesday, target_delta_int shifts to the next future Monday (Not going back into a past Monday)

            return base_date + timedelta(days=target_delta_int)  # Shifted date

        return get_minimum_date_of_target_weekday(self.weekday_int, self.date_start)

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
