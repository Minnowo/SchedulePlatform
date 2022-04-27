"""Primary program logic functions.

TODO: Warning! Unsafe usage of variables identifying SQL table names which are called in queries executed by the
 connector. Security fix needed!
"""

import json

from Schedulizer.SemesterConfigHandler import SemesterConfig
from Schedulizer.APIs.MycampusAPI import get_json_course_data
from Schedulizer.APIs.MycampusAPIDecoder import decode_api_json_to_course_obj as decode
from Schedulizer.ICSManipulation import create_ics_calendar
from Schedulizer.DBController.Courses import update_course_record, get_course_via_crn, is_up_to_date
from Schedulizer.SemesterConfigHandler import decode_config
from Schedulizer.constants import ENABLED_CONFIGS_FILE_PATH


def op_update_courses_with_overhead(config_object: SemesterConfig, course_codes: list[str]):
    """Update all course records of matching specified course codes if deemed out of date.

    Args:
        config_object: SemesterConfig object holding semester calendar info. (Typically = SemesterConfig.name).
        course_codes: list of course codes to update for.
    """
    course_codes = list(set(course_codes))  # Remove duplicates

    if not isinstance(course_codes, list) and not isinstance(course_codes, tuple):
        raise TypeError("course_codes should be a list of course codes (str).")

    for course_code in course_codes:
        if not is_up_to_date(course_table=config_object.name, fac=course_code[:-5], uid=course_code[-5:]):
            __op_update_course(config_object=config_object, course_code=course_code)


def __op_update_course(config_object: SemesterConfig, course_code: str):
    """Pull course data from my MyCampus API and update/add new records of all the courses matching the course code.

    Args:
        config_object: SemesterConfig object holding semester calendar info. (Typically = SemesterConfig.name).
        course_code: course to search by API for and update on internal DBController.

    Raises:
        ValueError: If no course of the given course code was returned from the MyCampus API.
    """
    course_objects = decode(get_json_course_data(mep_code=config_object.api_mycampus_mep_code,
                                                 term_id=config_object.api_mycampus_term_id,
                                                 course_code=course_code))

    if len(course_objects) > 0:
        for course_obj in course_objects:
            update_course_record(course_table=config_object.name, c=course_obj)
            # TODO: Should make this multi threaded maybe. Takes a long time updating records of each course
            #  individually.
    else:
        raise ValueError(f"Course code {course_code} not found!")


def op_generate_ics(config_object: SemesterConfig, crn_codes: list[int], cache_id: str = None) -> str:
    """Generate an .ics calendar file saved to a specified (cache) file path and return that path.

    Args:
        config_object: SemesterConfig object holding semester calendar info. (Typically = SemesterConfig.name).
        crn_codes: List of crn codes to find matching crn codes for.
        cache_id: cache id, default None.

    Returns:
        Cache file path of the created ics file.
    """
    if not isinstance(crn_codes, list) and not isinstance(crn_codes, tuple):
        raise TypeError("crn_codes should be a list of crn codes (int).")

    crn_codes = list(set(crn_codes))  # Remove duplicates

    courses_list = []

    for crn in crn_codes:
        course = get_course_via_crn(course_table=config_object.name, crn=crn)

        if course is None:
            raise RuntimeError(f"CRN {crn} not found!")

        courses_list.append(course)

    file_path = create_ics_calendar(config_object=config_object, course_list=courses_list, cache_id=cache_id)

    return file_path


def op_get_config(config_id: str) -> SemesterConfig | None:
    """Get the matching SemesterConfig by id which is defined by ENABLED_CONFIGS_FILE_PATH.

    Args:
        config_id: Config ID specified in ENABLED_CONFIGS_FILE_PATH.

    Returns:
        SemesterConfig object or None if a matching enabled config was not found.
    """
    with open(ENABLED_CONFIGS_FILE_PATH) as file:
        config_filepath = json.load(file)

    try:
        semester_config = decode_config(config_filepath[config_id])
    except KeyError:
        return None

    return semester_config
