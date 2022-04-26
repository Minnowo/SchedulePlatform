"""Course class module.

It holds universally common course values such as instructors and capacity count.
"""

from pydantic import BaseModel
import json
from datetime import date, time
from types import SimpleNamespace

from Schedulizer.MeetingClass import Meeting


class Course(BaseModel):
    """Course class defines a single general course identified by a CRN (course registration number).

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

    fac: str
    uid: str
    crn: int
    class_type: str
    title: str
    section: str
    class_time: list[Meeting] = []
    is_linked: bool
    link_tag: str | None
    seats_filled: int
    max_capacity: int
    instructors: str | None = None
    is_virtual: bool = False

    def get_serialized_self_class_time(self) -> str:
        """Returns a short json class time (short form used for database storage) of self.class_time.

        Returns:
            json string of the converted self.class_time.
        """
        json_str = json.dumps(self.class_time, default=CourseClassEncoder.default)
        return json_str

    @staticmethod
    def deserialize_to_class_time(json_str: str) -> list[Meeting]:
        """Converts a short json class time (short form used for database storage) to appropriate format for
        Course.class_time.

        Args:
            json_str: json string of the Course object to decode from.

        Returns:
            List of Meeting objects (Format for Course.class_time).
        """
        class_time = json.loads(json_str, cls=ClassTimeDecoder)
        return class_time

    def to_json(self) -> str:
        """Converts a Course object to json str.

        Returns:
            json string of the Course object.
        """
        return json.dumps(self, default=CourseClassEncoder.default)

    @staticmethod
    def from_json(json_str: str):
        """Converts a json str to Course object.

        Args:
            json_str: json string of the Course object to decode from.

        Returns:
            Course from the decoded object.
        """
        class_time_str = json.dumps(json.loads(json_str)["class_time"])

        simple = json.loads(json_str, object_hook=lambda d: SimpleNamespace(**d))

        return Course(fac=simple.fac,
                      uid=simple.uid,
                      crn=simple.crn,
                      class_type=simple.class_type,
                      title=simple.title,
                      section=simple.section,
                      class_time=Course.deserialize_to_class_time(class_time_str),
                      is_linked=simple.is_linked,
                      link_tag=simple.link_tag,
                      seats_filled=simple.seats_filled,
                      max_capacity=simple.max_capacity,
                      instructors=simple.instructors,
                      is_virtual=simple.is_virtual)

    def get_raw_str(self):
        """For prototyping purposes only.

        Returns:
            Default str similar to regular __str__ methods.
        """
        return (f"fac={self.fac}\n"
                f"uid={self.uid}\n"
                f"crn={self.crn}\n"
                f"class_type={self.class_type}\n"
                f"title={self.title}\n"
                f"section={self.section}\n"
                f"class_time={self.class_time}\n"
                f"is_linked={self.is_linked}\n"
                f"link_tag={self.link_tag}\n"
                f"seats_filled={self.seats_filled}\n"
                f"max_capacity={self.max_capacity}\n"
                f"instructors={self.instructors}\n"
                f"is_virtual={self.is_virtual}")

    def __str__(self):
        return self.get_raw_str()


# vvv json encoders and decoders for serializing and deserializing vvv

class CourseClassEncoder:
    """class_time encoders for serializing to json data.

    This is only really required to handle datetime.date, datetime.time and datetime.datetime as iso format and the
    rest is just handled as expected (dict and ints).
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
    """Course.class_time decoder from json for deserializing.
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(dct) -> Meeting:
        return Meeting(time_start=time.fromisoformat(dct["time_start"]),
                       time_end=time.fromisoformat(dct["time_end"]),
                       weekday_int=dct["weekday_int"],
                       date_start=date.fromisoformat(dct["date_start"]),
                       date_end=date.fromisoformat(dct["date_end"]),
                       repeat_timedelta_days=dct["repeat_timedelta_days"],
                       location=dct["location"])
