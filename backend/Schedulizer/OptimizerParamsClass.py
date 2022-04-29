"""CourseOptimizerCriteria defines the criteria for the optimizer to calculate
the rating value of a single Course object.
"""

import json
from datetime import time

from Schedulizer.CourseClass import Course


class CourseOptimizerCriteria:
    def __init__(self,
                 times_start: list[
                     time | None, time | None, time | None, time | None,
                     time | None, time | None, time | None] = None,
                 times_start_weight: float = 0.0,
                 times_end: list[
                     time | None, time | None, time | None, time | None,
                     time | None, time | None, time | None] = None,
                 times_end_weight: float = 0.0,
                 is_virtual: bool | None = None,
                 is_virtual_weight: float = 0.0,
                 min_prof_rating: float | None = None,
                 min_prof_rating_weight: float = 0.0,
                 min_seats_open: int | None = None,
                 min_seats_open_weight: float = 0.0,
                 max_capacity: int | None = None,
                 max_capacity_weight: float = 0.0):
        """
        Args:
            times_start: List of the earliest allowed start time per day.
                Follows datetime.datetime.weekday() index convention.
                (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
                Use case: User wants to ensure they start school after a
                certain time each day.
            times_start_weight:
            times_end: List of the latest allowed end time per day.
                Follows datetime.datetime.weekday() index convention.
                (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
                Use case: User wants to ensure they get off from school by a
                certain time each day.
            times_end_weight:
            is_virtual: True = prioritize virtual classes, False = prioritize
                in-person classes.
                Use case: User wants more virtual (or in-person) classes.
            is_virtual_weight:
            min_prof_rating: Minimum professor rating.
                Should be within range [0, 1], logically a 0 rating would be
                the same as None.
                Use case: User wants to get actually decent profs.
            min_prof_rating_weight:
            min_seats_open: Minimum number of seats open for registration.
                Use case: User wants to ensure they will have open seats to be
                able to register.
            min_seats_open_weight:
            max_capacity: Maximum capacity size.
                Use case: User wants smaller class sizes.
            max_capacity_weight:

        Notes:
            The None state means that no criteria specified.
        """
        self.times_start = times_start
        self.times_start_weight = times_start_weight
        self.times_end = times_end
        self.times_end_weight = times_end_weight
        self.is_virtual = is_virtual
        self.is_virtual_weight = is_virtual_weight
        self.min_prof_rating = min_prof_rating
        self.min_prof_rating_weight = min_prof_rating_weight
        self.min_seats_open = min_seats_open
        self.min_seats_open_weight = min_seats_open_weight
        self.max_capacity = max_capacity
        self.max_capacity_weight = max_capacity_weight

    def course_eval(self, course: Course) -> float:
        """Evaluates the rating of a Course object for schedule optimizer.
        Higher rating means a more favourable course.

        Args:
            course: Course object of which to calculate the rating/weight for.

        Returns:
            Rating/weight float.
        """
        rating = 0.0

        if self.times_start is not None:
            for meeting in course.class_time:
                if meeting.time_start > self.times_start[meeting.weekday_int]:
                    # Meeting starts later, as requested
                    rating += (1 * meeting.num_actual_meetings()
                               * self.times_start_weight)
                else:
                    rating -= (1 * meeting.num_actual_meetings()
                               * self.times_start_weight)

        if self.times_end is not None:
            for meeting in course.class_time:
                if meeting.time_end < self.times_end[meeting.weekday_int]:
                    # Meeting ends earlier, as requested
                    rating += (1 * meeting.num_actual_meetings()
                               * self.times_end_weight)
                else:
                    rating -= (1 * meeting.num_actual_meetings()
                               * self.times_end_weight)

        if self.is_virtual is not None:
            if self.is_virtual == course.is_virtual:
                rating += (1 * course.num_actual_meetings()
                           * self.is_virtual_weight)
            else:
                rating -= (1 * course.num_actual_meetings()
                           * self.is_virtual_weight)

        # Notice times_start, times_end and is_virtual ratings depend on the
        # actual meetings count. This is to help account for variations of
        # meeting counts. For example, a user wants virtual classes (Optimizer
        # criteria is_virtual=True) as they don't want to commute to campus as
        # much. Suppose the optimizer is forced to decide between a biweekly
        # in-person lab versus a weekly in-person lecture. It will rate the
        # biweekly lab to be higher (more favourable) than the weekly lecture
        # because it has more meetings.

        if self.min_prof_rating is not None:
            pass  # TODO(Daniel): FUTURE WIP

        if self.min_seats_open is not None:
            if self.min_seats_open <= (course.max_capacity
                                       - course.seats_filled):
                rating += 1 * self.min_seats_open_weight
            else:
                rating -= 1 * self.min_seats_open_weight

        if self.max_capacity is not None:
            if self.max_capacity >= course.max_capacity:
                rating += 1 * self.max_capacity_weight
            else:
                rating -= 1 * self.max_capacity_weight

        return rating

    def to_json(self) -> str:
        """Converts a CourseOptimizerCriteria object to json str.

        Returns:
            json string of the CourseOptimizerCriteria object.
        """
        return json.dumps(self, default=CourseOptimizerCriteriaEncoder.default)

    @staticmethod
    def from_json(json_str: str):
        """Converts a json str to CourseOptimizerCriteria object.

        Args:
            json_str: json string of the Course object to decode from.

        Returns:
            CourseOptimizerCriteria from the decoded json string.
        """
        return json.loads(json_str, cls=CourseOptimizerCriteriaDecoder)

    def __str__(self):
        return (f"times_start={self.times_start}\n"
                f"times_start_weight={self.times_start_weight}\n"
                f"times_end={self.times_end}\n"
                f"times_end_weight={self.times_end_weight}\n"
                f"is_virtual={self.is_virtual}\n"
                f"is_virtual_weight={self.is_virtual_weight}\n"
                f"min_prof_rating={self.min_prof_rating}\n"
                f"min_prof_rating_weight={self.min_prof_rating_weight}\n"
                f"min_seats_open={self.min_seats_open}\n"
                f"min_seats_open_weight={self.min_seats_open_weight}\n"
                f"max_capacity={self.max_capacity}\n"
                f"max_capacity_weight={self.max_capacity_weight}\n")


class CourseOptimizerCriteriaEncoder:
    """CourseOptimizerCriteria encoders for serializing to json data.
    """

    @staticmethod
    def default(obj):
        if isinstance(obj, time):
            return obj.isoformat()
        if isinstance(obj, int):
            return obj
        if isinstance(obj, float):
            return obj
        else:
            return obj.__dict__


class CourseOptimizerCriteriaDecoder(json.JSONDecoder):
    """CourseOptimizerCriteria decoder from json for deserializing.
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args,
                                  **kwargs)

    @staticmethod
    def object_hook(dct) -> CourseOptimizerCriteria:
        times_start = ([time.fromisoformat(t) for t in dct["times_start"]]
                       if dct["times_start"] is not None else None)
        times_end = ([time.fromisoformat(t) for t in dct["times_end"]]
                     if dct["times_end"] is not None else None)

        return CourseOptimizerCriteria(
            times_start=times_start,
            times_start_weight=dct["times_start_weight"],
            times_end=times_end,
            times_end_weight=dct["times_end_weight"],
            is_virtual=dct["is_virtual"],
            is_virtual_weight=dct["is_virtual_weight"],
            min_prof_rating=dct["min_prof_rating"],
            min_prof_rating_weight=dct["min_prof_rating_weight"],
            min_seats_open=dct["min_seats_open"],
            min_seats_open_weight=dct["min_seats_open_weight"],
            max_capacity=dct["max_capacity"],
            max_capacity_weight=dct["max_capacity_weight"])
