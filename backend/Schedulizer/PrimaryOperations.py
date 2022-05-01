"""Primary program logic functions.
"""

import json

from Schedulizer.SemesterConfigHandler import SemesterConfig
from Schedulizer.APIs.MycampusAPI import get_json_course_data
from Schedulizer.APIs.MycampusAPIDecoder import decode_api_json_to_course_obj \
    as decode
from Schedulizer.ICSManipulation import create_ics_calendar
from DBController.Courses import update_course_record, get_course_via_crn, \
    is_up_to_date
from Schedulizer.SemesterConfigHandler import decode_config
from Schedulizer.constants import ENABLED_CONFIGS_FILE_PATH


def __course_code_is_valid_possible(course_code: str) -> bool:
    """Check if a course code string could be turned into valid form.

    Args:
        course_code: Course code defined by the school. (MATH1010U)

    Returns:
        True if valid, False if not.

    Notes:
        All given course codes are turned to uppercase here. The function here
        does not determine if the exact format is valid, rather if its core
        values could be made into a valid course code.
            For proper validation returns see: op_course_code_valid_format().

    Examples:
        >>> __course_code_is_valid_possible("MATH1010U")
        True
        >>> __course_code_is_valid_possible("Math1010u")
        True
        >>> __course_code_is_valid_possible("Phy1010u")
        True
        >>> __course_code_is_valid_possible("m a t h   1 0 1 0 u")
        True
        >>> __course_code_is_valid_possible("maths1010u")
        False
        >>> __course_code_is_valid_possible("ma1010u")
        False
    """
    if not isinstance(course_code, str):
        return False

    course_code = course_code.replace(" ", "").upper()

    # MATHS1010U -> fac = MATHS, uid = 1010U
    fac = course_code[:-5]
    uid = course_code[-5:]

    if not ((3 <= len(fac) <= 4) and (not fac.isdigit()) and uid[:-1].isdigit()
            and uid[-1] == "U"):
        return False

    return True


def op_course_code_valid_format(course_code: str) -> str | None:
    """Returns the clean valid form (should be valid for all purposes in code)
    of a course code, None if not possible.

    Args:
        course_code: Course code defined by the school. (MATH1010U)

    Returns:
        Cleaned up valid course code or None if not possible.

    Examples:
        >>> op_course_code_valid_format("MATH1010U")
        'MATH1010U'
        >>> op_course_code_valid_format("Math1010u")
        'MATH1010U'
        >>> op_course_code_valid_format("m a t h   1 0 1 0 u")
        'MATH1010U'
        >>> op_course_code_valid_format("maths1010u")
        None
    """
    if __course_code_is_valid_possible(course_code):
        return course_code.replace(" ", "").upper()

    return None


def op_update_courses_with_overhead(config_object: SemesterConfig,
                                    course_codes: list[str]):
    """Update all course records of matching specified course codes if deemed
    out of date.

    Args:
        config_object: SemesterConfig object holding semester calendar info.
            (Typically = SemesterConfig.name).
        course_codes: list of course codes to update for.
    """
    if not isinstance(course_codes, list) \
            and not isinstance(course_codes, tuple):
        raise TypeError("course_codes should be a list of course codes (str).")

    # Validate and remove duplicates
    course_codes = [op_course_code_valid_format(code) for code in course_codes
                    if op_course_code_valid_format(code) is not None]
    course_codes = list(set(course_codes))

    for course_code in course_codes:
        if not is_up_to_date(course_table=config_object.get_db_table(),
                             fac=course_code[:-5],
                             uid=course_code[-5:]):
            __update_course(config_object=config_object,
                            course_code=course_code)


def __update_course(config_object: SemesterConfig, course_code: str):
    """Pull course data from my MyCampus API and update/add new records of all
    the courses matching the course code.

    Args:
        config_object: SemesterConfig object holding semester calendar info.
            (Typically = SemesterConfig.get_db_table()).
        course_code: course to search by API for and update on internal
            DBController.

    Raises:
        ValueError: If no course of the given course code was returned from the
            MyCampus API.
    """
    course_code = op_course_code_valid_format(course_code)

    if course_code is not None:
        course_objects = decode(
            get_json_course_data(mep_code=config_object.api_mycampus_mep_code,
                                 term_id=config_object.api_mycampus_term_id,
                                 course_code=course_code))

        if len(course_objects) > 0:
            for course_obj in course_objects:
                update_course_record(course_table=config_object.get_db_table(),
                                     c=course_obj)
                # TODO: Should make this multi threaded maybe. Takes a long time
                #  updating records of each course individually.
        else:
            raise ValueError(f"Course code {course_code} not found!")


def op_generate_ics(config_object: SemesterConfig, crn_codes: list[int],
                    cache_id: str = None) -> str:
    """Generate an .ics calendar file saved to a specified (cache) file path
    and return that path.

    Args:
        config_object: SemesterConfig object holding semester calendar info.
            (Typically = SemesterConfig.get_db_table()).
        crn_codes: List of crn codes to find matching crn codes for.
        cache_id: cache id, default None.

    Returns:
        Cache file path of the created ics file.
    """
    if not isinstance(crn_codes, list) and not isinstance(crn_codes, tuple):
        raise TypeError("crn_codes should be a list of crn codes (int).")

    # Validate and remove duplicates
    crn_codes = [crn for crn in crn_codes if isinstance(crn, int)]
    crn_codes = list(set(crn_codes))  # Remove duplicates

    courses_list = []

    for crn in crn_codes:
        course = get_course_via_crn(course_table=config_object.get_db_table(),
                                    crn=crn)

        if course is None:
            raise RuntimeError(f"CRN {crn} not found!")

        courses_list.append(course)

    file_path = create_ics_calendar(config_object=config_object,
                                    course_list=courses_list,
                                    cache_id=cache_id)

    return file_path


def op_get_config(config_id: str) -> SemesterConfig | None:
    """Get the matching SemesterConfig by id which is defined by
    ENABLED_CONFIGS_FILE_PATH.

    Args:
        config_id: Config ID specified in ENABLED_CONFIGS_FILE_PATH.

    Returns:
        SemesterConfig or None if no matching enabled config was found.
    """
    with open(ENABLED_CONFIGS_FILE_PATH) as file:
        config_filepath = json.load(file)

    try:
        semester_config = decode_config(config_filepath[config_id])
    except KeyError:
        return None

    return semester_config
