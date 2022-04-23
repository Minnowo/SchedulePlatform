"""Create ics file intended to be used as a calendar from a list of Course objects.

Able to utilize a Config object universal event data to generate universal event.
"""
import icalendar
from icalendar import Calendar, Event
from datetime import datetime, time, timedelta

from backend.Schedulizer.constants import ICS_CALENDAR_FILENAME
from backend.Schedulizer.CacheFilePathManipulation import get_cache_path
from backend.Schedulizer.CourseClass import Course
from backend.Schedulizer.MeetingClass import Meeting
from backend.Schedulizer.SemesterConfigHandler import SemesterConfig


def create_ics_calendar(config_object: SemesterConfig, course_list: list[Course], cache_id: str = None):
    """Create ics file given a list of course objects.

    Args:
        config_object: SemesterConfig object holding semester calendar info.
        course_list: list -> Course -> List of Course objects to translate into ics calendar.
        cache_id: Cache id, default None.
    """
    calendar = Calendar()

    events = __build_course_event_list(config_object=config_object, course_list=course_list)
    events += __build_universal_event_list(config_object=config_object)

    for event in events:
        calendar.add_component(event)

    with open(get_cache_path(ICS_CALENDAR_FILENAME, cache_id), "wb") as file:
        file.write(calendar.to_ical())


def __build_course_event_list(config_object: SemesterConfig, course_list: list[Course]) -> list[icalendar.Event]:
    """

    Args:
        config_object: SemesterConfig object holding semester calendar info.
        course_list: List of Course or single Course to turn into an event(s).

    Returns:
        List of all Course object(s) translated into icalendar.Event(s).
    """
    # Ensure type instance
    if isinstance(course_list, Course):
        course_list = [course_list]
    elif not isinstance(course_list, list) and not isinstance(course_list, tuple):
        raise TypeError(f"Expected list, tuple of Course objects or Course type")

    # Compute/create/translate events
    events_list = []

    for course in course_list:
        for meeting in course.class_time:
            events_list += __build_meeting_events(config_object, course, meeting)

    return events_list


def __base_event(course: Course) -> icalendar.Event:
    """

    Args:
        course: class object to translate to event.

    Returns:
        icalendar.Event() -> class translated to event.
    """
    event = Event()

    # Summary setting
    summary = f"{course.title} {course.class_type[:3].upper()} ({course.fac}{course.uid})"
    event.add("summary", summary)

    # Description setting
    description = (
        f"Instructor: {course.instructors}\n"
        f"CRN: {course.crn}\n"
        f"Section: {course.section}\n"
    )
    event.add("description", description)

    return event


def __build_meeting_events(config_object: SemesterConfig, course: Course, meeting: Meeting) -> list[icalendar.Event]:
    """

    Args:
        config_object: SemesterConfig object holding semester calendar info.
        course: Basic event details.
        meeting: Meeting specific details.

    Returns:
        list of icalendar.Event(s) of translated Course.
    """
    events_list = []  # List of events being added to the icalendar

    base_event = __base_event(course)  # Base event, build upon this event moving forward

    # Location setting
    if course.is_virtual:  # Completely virtual course:
        base_event.add("location", "SYNCHRONOUS/VIRTUAL")
    else:  # Handle each meeting individually:
        base_event.add("location", meeting.location)

    if meeting.repeat_timedelta_days == 0:  # No recurrence, period. Assume no shifting required
        # Datetime start and end setting.
        start = datetime.combine(meeting.date_start, meeting.time_start)
        end = datetime.combine(meeting.date_start, meeting.time_end)

        if start > config_object.semester_start and end < config_object.semester_end:
            base_event.add("dtstart", start)  # Event start and date datetime.
            base_event.add("dtend", end)

        events_list.append(base_event)

    elif meeting.repeat_timedelta_days > 0 and meeting.repeat_timedelta_days % 7 == 0:  # Repeats in multiples of 7 days
        # Event start and date datetime. Create first event start and end by shifting.
        if meeting.date_start.weekday() != meeting.weekday_int:  # If the current start_datetime isn't matching the
            # target weekday_data
            target_delta_int = meeting.weekday_int - meeting.date_start.weekday()  # Calculate the shift required
            target_delta_int += 7 if target_delta_int < 0 else 0  # If your target is Monday and the start_time =
            # Wednesday, target_delta_int shifts to the next future Monday (Not going back into a past Monday)
            start_date = meeting.date_start + timedelta(days=target_delta_int)  # Shifted date
        else:  # No shift required.
            start_date = meeting.date_start

        base_event.add("dtstart", datetime.combine(start_date, meeting.time_start))  # Event start and date datetime.
        base_event.add("dtend", datetime.combine(start_date, meeting.time_end))

        # Recurrence/Repeating frequency rule setting - Docs:
        #  https://icalendar.org/iCalendar-RFC-5545/3-8-5-3-recurrence-rule.html
        day_dict = {0: "MO", 1: "TU", 2: "WE", 3: "TH", 4: "FR", 5: "SA", 6: "SU"}
        # ^^^ Heads up: datetime uses Monday = 0 VS icalendar uses Sunday = 0. This acts as a conversion.
        day = day_dict[meeting.weekday_int]  # Match proper representation via dict
        interval = (meeting.repeat_timedelta_days / 7)
        # Recurrence rule:
        base_event.add("rrule", {"FREQ": "WEEKLY",
                                 "INTERVAL": interval,
                                 "UNTIL": datetime.combine(meeting.date_end, time.max),
                                 "BYDAY": day})

        events_list.append(base_event)

    else:  # Some crazy recurrence rule
        pass  # Currently program assumes no crazy recurrence rules

    return events_list


def __build_universal_event_list(config_object: SemesterConfig) -> list[icalendar.Event]:
    """Add all enabled exclusions as events to all schedules.

    Args:
        config_object: SemesterConfig object holding semester calendar info.

    Returns:
        icalendar.Event(s).
    """
    universal_events = config_object.universal_events

    exclusion_event_list = []

    for event in universal_events:
        single_event = Event()

        single_event.add("summary", event.name)  # Summary setting
        single_event.add("description", event.description)  # Description setting

        single_event.add("dtstart", event.start_datetime)  # Event time setting
        single_event.add("dtend", event.end_datetime)

        exclusion_event_list.append(single_event)

    return exclusion_event_list
