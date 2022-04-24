"""Functions called by FastAPI app relating to Schedulizer logic.
"""

import json

from backend.Schedulizer.DBController.Courses import get_course_via_crn
from backend.Schedulizer.SemesterConfigHandler import decode_config
from backend.Schedulizer.constants import ENABLED_CONFIGS_FILE_PATH
from backend.Schedulizer.PrimaryOperations import op_update_courses_with_overhead, op_generate_ics


def general_crn_build(config_id: str, course_codes: list[str], crn_codes: list[int]):
    """json string data of given CRN codes pulled from the backend DB.

    Args:
        config_id: Semester config id determines what semester is being processed.
        course_codes: List of course codes which the given crn codes belong to. The program will update the backend DB
            (with overhead). These course codes are not necessary to function, but should be given to ensure the DB has
            the data for the requested CRNs.
        crn_codes: List of crn codes of each specific class to process.

    Returns:
        Course data in json form.
    """
    with open(ENABLED_CONFIGS_FILE_PATH) as file:
        config_filepath = json.load(file)

    config_obj = decode_config(config_filepath[config_id])

    op_update_courses_with_overhead(config_object=config_obj, course_codes=course_codes)

    result = ", ".join(
        get_course_via_crn(course_table=config_obj.db_table_name, crn=crn).to_json() for crn in crn_codes)

    return result


def generate_crn_download_path(config_id: str, course_codes: list[str], crn_codes: list[int]):
    """Generates an ics calendar file given a list of crn codes.

    Args:
        config_id: Semester config id determines what semester is being processed.
        course_codes: List of course codes which the given crn codes belong to. The program will update the backend DB
            (with overhead). These course codes are not necessary to function, but should be given to ensure the DB has
            the data for the requested CRNs.
        crn_codes: List of crn codes of each specific class to process.

    Returns:
        Cache file path of the created ics file.
    """
    with open(ENABLED_CONFIGS_FILE_PATH) as file:
        config_filepath = json.load(file)

    config_obj = decode_config(config_filepath[config_id])

    op_update_courses_with_overhead(config_object=config_obj, course_codes=course_codes)

    result = op_generate_ics(config_object=config_obj, crn_codes=crn_codes, cache_id="test")

    return result
