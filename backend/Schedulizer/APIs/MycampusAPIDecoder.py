"""Decodes json dict pulled via the MycampusAPI.py into the main Course class (CourseClass.py).

Uses the Meeting class (MeetingClass) to populate the class_times properly/attribute in the course class.
"""

from datetime import datetime

from backend.Schedulizer.constants import CLASS_INSTRUCTION_IN_PERSON_KEYS
from backend.Schedulizer.CourseClass import Course
from backend.Schedulizer.MeetingClass import Meeting


def decode_api_json_to_course_obj(json_dict: dict) -> list[Course]:
    """

    Args:
        json_dict: JSON dict pulled by the MycampusAPI.py module.

    Returns:
        List of decoded Course objects.
    """

    def is_virtual(instructional_method_description: str) -> bool:
        """Compares instructional_method_description to CLASS_INSTRUCTION_IN_PERSON_KEYS to see if a course is virtual.

        Args:
            instructional_method_description:

        Returns:
            True = is virtual, False = not virtual/in person
        """
        for key in CLASS_INSTRUCTION_IN_PERSON_KEYS:
            if key.lower() in instructional_method_description.lower():
                return False
        return True

    course_list = []  # Master list to return

    for data in json_dict["data"]:  # Loop through all courses
        meetings = data["meetingsFaculty"]
        meeting_list = []

        for meeting in meetings:  # Loop through all meet times
            m_fac = meeting["meetingTime"]

            # Weekday int calculation
            try:
                weekday_int = [m_fac["monday"], m_fac["tuesday"], m_fac["wednesday"], m_fac["thursday"],
                               m_fac["friday"], m_fac["saturday"], m_fac["sunday"]].index(True)
                # ^^^ Following datetime convention of monday = 0, tuesday = 1, ... , sunday = 6
            except ValueError:
                weekday_int = -1  # Negative 1 denotes no class on a day (async class/course)

            date_start = datetime.strptime(m_fac["startDate"], "%m/%d/%Y").date()
            date_end = datetime.strptime(m_fac["endDate"], "%m/%d/%Y").date()

            if date_start is not None and date_end is not None and weekday_int >= 0:  # Course is not async

                # repeat_timedelta calculation
                if date_start == date_end:  # Single day meetings:
                    repeat_timedelta_days = 0

                    # TODO POSSIBLE IMPROVED REPEATING QOL IMPROVEMENT.
                    #  New logic needed to require to parse biweekly. (School structures/formats biweekly as individual
                    #  non repeating events)
                    """
                    elif meeting["category"] != "01" and m_fac["category"] != "01":  # Biweekly meetings:
                        # Usually meeting["category"] = m_fac["category"], for redundancy purposes they're both here...
                        repeat_timedelta_days = 14
                    """

                else:  # Weekly meetings:
                    repeat_timedelta_days = 7

                # Create Meeting object
                m = Meeting(time_start=datetime.strptime(m_fac["beginTime"], "%H%M").time(),
                            time_end=datetime.strptime(m_fac["endTime"], "%H%M").time(),
                            weekday_int=weekday_int,
                            date_start=date_start,
                            date_end=date_end,
                            repeat_timedelta_days=repeat_timedelta_days,
                            location=f"{m_fac['campus']} {m_fac['building']} {m_fac['room']}")

                meeting_list.append(m)  # Append Meeting object to meeting list

        # Create Course object
        c = Course(fac=data["subject"],
                   uid=data["courseNumber"],
                   crn=int(data["courseReferenceNumber"]),
                   class_type=data["scheduleTypeDescription"],
                   title=data["courseTitle"],
                   section=data["sequenceNumber"],
                   class_time=meeting_list,
                   is_linked=bool(data["isSectionLinked"]),
                   link_tag=data["linkIdentifier"],
                   seats_filled=int(data["enrollment"]),
                   max_capacity=int(data["maximumEnrollment"]),
                   instructors=", ".join([f"{fac['displayName']} ({fac['emailAddress']})" for fac in data["faculty"]]),
                   is_virtual=is_virtual(data["instructionalMethodDescription"]))

        course_list.append(c)  # Append Course object to course list

    return course_list  # Return the master list
