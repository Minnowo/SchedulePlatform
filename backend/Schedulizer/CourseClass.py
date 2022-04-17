"""Course class module.

It holds universally common course values such as instructors and capacity count.
"""

import json
from datetime import date, time
from backend.Schedulizer.MeetingClass import Meeting


class Course:
    def __init__(self, fac: str, uid: str, crn: int, class_type: str, title: str, section: str,
                 class_time: list[Meeting], is_linked: bool, link_tag: str, seats_filled: int, max_capacity: int,
                 instructors: str, is_virtual: bool):
        """Course class defines a single general course identified by a CRN (course registration number).

        Args:
            fac: Faculty ID that identifies the c's faculty department. (Example: "MATH").
            uid: (UID = University ID). A course ID code that ends with the 'U'. (Example: "1020U").
            crn: (CRN = Course Registration Number). A unique int that represents each course. (Example: 12345).
            class_type: Identifies the type of class. (Example: "Lecture", "Tutorial" & "Laboratory").
            title: Title of the class. (Example: "Calculus II").
            section: Section identifier, usually a number with possible leading zeros. (Example: "001").
            class_time: List of Meeting objects. (MeetingClass.py).
            is_linked: Defines if the class has any linked classes that are required.
            link_tag: Identifies the link type for its c. (Example: "A1").
                For computation, links are made with matching tags from classes with the same fac and uid.
                Class with a link_tag="A1" needs to link with another class of link_tag="B#", where # is an integer.
            seats_filled: Number of seats filled.
            max_capacity: Maximum capacity of a course.
            instructors: Each instructors' information.
            is_virtual: Defines if the class is completely virtual/online.
        """

        self._fac = fac
        self._uid = uid
        self._crn = crn
        self._class_type = class_type
        self._title = title
        self._section = section
        self._class_time = class_time
        self._is_linked = is_linked
        self._link_tag = link_tag
        self._seats_filled = seats_filled
        self._max_capacity = max_capacity
        self._instructors = instructors
        self._is_virtual = is_virtual

    @property
    def fac(self):
        return self._fac

    @property
    def uid(self):
        return self._uid

    @property
    def crn(self):
        return self._crn

    @property
    def class_type(self):
        return self._class_type

    @property
    def title(self):
        return self._title

    @property
    def section(self):
        return self._section

    @property
    def class_time(self):
        return self._class_time

    def serialized_self_class_time(self):
        json_str = json.dumps(self._class_time, default=ClassTimeEncoder.default)
        return json_str

    @staticmethod
    def deserialize_to_class_time(json_str):
        class_obj = json.loads(json_str, cls=ClassTimeDecoder)
        return class_obj

    @property
    def is_linked(self):
        return self._is_linked

    @property
    def link_tag(self):
        return self._link_tag

    @property
    def seats_filled(self):
        return self._seats_filled

    @property
    def max_capacity(self):
        return self._max_capacity

    @property
    def instructors(self):
        return self._instructors

    @property
    def is_virtual(self):
        return self._is_virtual

    def get_raw_str(self):
        """For prototyping purposes only.

        Returns:
            Default str similar to regular __str__ methods.
        """
        return (f"fac={self._fac}\n"
                f"uid={self._uid}\n"
                f"crn={self._crn}\n"
                f"class_type={self._class_type}\n"
                f"title={self._title}\n"
                f"section={self._section}\n"
                f"class_time={self._class_time}\n"
                f"is_linked={self._is_linked}\n"
                f"link_tag={self._link_tag}\n"
                f"seats_filled={self._seats_filled}\n"
                f"max_capacity={self._max_capacity}\n"
                f"instructors={self._instructors}\n"
                f"is_virtual={self._is_virtual}")

    def __str__(self):
        return self.get_raw_str()


# vvv class_time encoders and decoders for serializing and deserializing vvv


class ClassTimeEncoder:
    """class_time encoders for serializing to json data
    """

    @staticmethod
    def default(obj):
        if isinstance(obj, date) or isinstance(obj, time):
            return obj.isoformat()
        if isinstance(obj, int):
            return obj
        else:
            return obj.__dict__


class ClassTimeDecoder(json.JSONDecoder):
    """class_time decoders from json for deserializing
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(dct):
        return Meeting(time_start=time.fromisoformat(dct["_time_start"]), time_end=time.fromisoformat(dct["_time_end"]),
                       weekday_int=dct["_weekday_int"], date_start=date.fromisoformat(dct["_date_start"]),
                       date_end=date.fromisoformat(dct["_date_end"]),
                       repeat_timedelta_days=dct["_repeat_timedelta_days"], location=dct["_location"])
