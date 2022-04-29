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

    Examples:
        Meeting(time_start=datetime.time(9, 40),
                time_end=datetime.time(11, 0),
                weekday_int=0,
                date_start=datetime.date(2022, 1, 17),
                date_end=datetime.date(2022, 4, 14),
                repeat_timedelta_days=7,
                location='UOW SYN SYN')
    """

    time_start: time = time.min
    time_end: time = time.max
    # In the event times are not specified, assume all day Meeting.
    weekday_int: int
    date_start: date
    date_end: date
    repeat_timedelta_days: int = 0
    location: str | None

    def get_actual_date_start(self) -> date:
        """Get the actual date of the first matching weekday_int.

        Returns:
            First datetime.date of the actual date which the meeting starts.

        Say a Meeting object has a self.weekday_int of 0 (representing a
        meeting on Monday), but has a self.date_start value that has a weekday
        (int) value that is not 0.
            Under certain circumstances a Meeting object can have a
            self.date_start that does not fall on the self.weekday_int. This
            commonly occurs with Courses running repeating meetings
            weekly/biweekly, due to the way schools might set their date start
            and end. They often set start and end dates of weekly courses with
            the start and end of the semester.
        """

        # Note I created/utilized this nested function since this is a really useful function that might one day be
        # needed outside this class structure.

        def forward_weekday_target(target_weekday_int: int, base_date: date) \
                -> date:
            """Get the first instance of a date that matches the target weekday
            in that falls on or after the base date.

            Args:
                target_weekday_int: Target weekday we want on the date.
                    Follows datetime.datetime.weekday() index convention.
                    (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
                base_date: Initial date to start on.

            Returns:
                New date with the correct target weekday.

            Examples:
                >>> forward_weekday_target(target_weekday_int=0,base_date=date(2022, 4, 1))
                datetime.date(2022, 4, 4)
                >>> forward_weekday_target(target_weekday_int=4,base_date=date(2022, 4, 1))
                datetime.date(2022, 4, 1)
                >>> forward_weekday_target(target_weekday_int=5,base_date=date(2022, 4, 1))
                datetime.date(2022, 4, 2)
            """
            target_delta_int = target_weekday_int - base_date.weekday()
            # Calculate the shift required
            target_delta_int += 7 if target_delta_int < 0 else 0  # If your
            # target is Monday and the start_time = Wednesday, target_delta_int
            # shifts to the next future Monday (Not going backwards to a past
            # Monday).

            return base_date + timedelta(days=target_delta_int)  # Shifted date

        return forward_weekday_target(self.weekday_int, self.date_start)

    def get_actual_date_end(self) -> date:
        """Get the actual date of the last matching weekday_int.

        Returns:
            Last datetime.date of the actual date which the meeting ends.

        This function need and behaviour is very similar to that of
        self.get_actual_date_start().
        """

        def backward_target_weekday(target_weekday_int: int, base_date: date) \
                -> date:
            """Get the last instance of a date that matches the target weekday
            in that falls on or before the base date.

            Args:
                target_weekday_int: Target weekday we want on the date.
                    Follows datetime.datetime.weekday() index convention.
                    (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
                base_date: Initial date to start on.

            Returns:
                New date with the correct target weekday.

            Examples:
                >>> backward_target_weekday(target_weekday_int=0,base_date=date(2022, 4, 30))
                datetime.date(2022, 4, 25)
                >>> backward_target_weekday(target_weekday_int=4,base_date=date(2022, 4, 30))
                datetime.date(2022, 4, 29)
                >>> backward_target_weekday(target_weekday_int=5,base_date=date(2022, 4, 30))
                datetime.date(2022, 4, 30)
            """
            target_delta_int = target_weekday_int - base_date.weekday()
            # Calculate the shift required
            target_delta_int -= 7 if target_delta_int > 0 else 0  # If your
            # target is Monday and the start_time = Wednesday, target_delta_int
            # shifts to the previous past Monday (Not going forward to the
            # future Monday).

            return base_date + timedelta(days=target_delta_int)  # Shifted date

        return backward_target_weekday(self.weekday_int, self.date_end)

    def num_actual_meetings(self) -> int:
        """Get the number of times a meeting actually occurs essentially is the
        sum of each reoccurrence.

        Returns:
            Number of times a class meets.

        Notes:
            Potential logic error due to bad data in of self.date_start and
            self.date_end. For example, courses are set to occur every week in
            a semester, but do not account for reading week which removes 1
            occurrence. Thus, 1 extra recurrence that does not actually exist
            is counted. To correct this behaviour courses would need to split
            meetings into 2 instances. One repeating each week till before
            reading week, then starting again after.
        """
        if self.repeat_timedelta_days > 0:  # Account for reoccurrence
            return ((self.get_actual_date_end()
                     - self.get_actual_date_start()).days
                    // self.repeat_timedelta_days + 1)

        return 1  # Single day, no reoccurrence

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


def meeting_time_conflict(meeting1: Meeting, meeting2: Meeting) -> bool:
    """Determines if 2 Meeting objects have time conflicts

    Args:
        meeting1:
        meeting2:

    Returns:
        True for a time conflict exists, False for no time conflict exists.
    """
    if (meeting1.weekday_int == meeting2.weekday_int and
            # Meetings occur on the same weekday

            # Meetings cross date intervals
            (meeting1.get_actual_date_start()
             <= meeting2.get_actual_date_start()
             <= meeting1.get_actual_date_end()
             or
             meeting1.get_actual_date_start()
             <= meeting2.get_actual_date_end()
             <= meeting1.get_actual_date_end()
             or
             meeting2.get_actual_date_start()
             <= meeting1.get_actual_date_start()
             <= meeting2.get_actual_date_end()
             or
             meeting2.get_actual_date_start()
             <= meeting1.get_actual_date_end()
             <= meeting2.get_actual_date_end()) and

            # Meetings cross time intervals
            (meeting1.time_start
             <= meeting2.time_start
             < meeting1.time_end
             or
             meeting1.time_start
             < meeting2.time_end
             <= meeting1.time_end
             or
             meeting2.time_start
             <= meeting1.time_start
             < meeting2.time_end
             or
             meeting2.time_start
             < meeting1.time_end
             <= meeting2.time_end)):
        return True

    return False
