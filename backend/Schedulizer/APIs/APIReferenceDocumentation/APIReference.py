"""A few test functions for the external mycampus API used in the backend.

These files should under no conditions be used in production. Only to be used as reference and test code. There is
basically no overhead, redundancies, input production, etc.
"""

import json
from datetime import datetime

from Schedulizer.APIs.MycampusAPI import get_json_course_data
from Schedulizer.APIs.MycampusAPIDecoder import decode_api_json_to_course_obj as decode


def generate_api_file(mep_code: str, term_id: str, course_code: str, save_to_filepath: str | None = None):
    """
    Generates a .json file of the api response from the mycampus api. The data matches that of the given course_code.

    Args:
        mep_code: School mep code. Example: Ontario Tech University = "UOIT".
        term_id: Term id used by api.
            Examples: Fall 2021 = "202109", Winter 2022 = "202201", Spring/Summer 2022 = "202205".
        course_code: Course code.
            Examples: "PHY1010U", "CHEM1800U", "MATH1850U".
        save_to_filepath: File path + name to save to, defaults None (in which case, uses course and now datetime as
            filename saved to the current directory).

    Note: There is overhead to add a ".json" if needed to the given filepath.

    Examples:
        generate_api_file("UOIT", "202201", "PHY1020U", "test")
            This will save the response for "PHY1020U in the term "202201" at "UOIT", saved to "test.json" (in the
            current directory).

        generate_api_file("UOIT", "202201", "PHY1020U")
            This will save the response for "PHY1020U in the term "202201" at "UOIT", saved to
            "PHY1020U %Y-%m-%d %H-%M.json" (current datetime.strftime) (in the current directory).
    """
    json_str = get_json_course_data(mep_code=mep_code, term_id=term_id, course_code=course_code)

    save_to_filepath = save_to_filepath if not None else f"{course_code} {datetime.now().strftime('%Y-%m-%d %H-%M')}"
    save_to_filepath = save_to_filepath + ".json" if save_to_filepath[-5:] != ".json" else save_to_filepath

    with open(f"{save_to_filepath}", "w") as file:
        json.dump(json_str, file, indent=4)


def print_decoded_objects_local_json(read_from_filepath: str):
    """
    Prints the first instance of a Course object of all decoded courses from a locally saved .json file. This file
    should be identical to that of a json response from the mycampus api.

    Args:
        read_from_filepath: File path of the json file to decode.

    Examples:
        print_decoded_objects_local_json("APIS/APIReferenceDocumentation/PHY1020U 2022-01-15 13-32.json")

        print_decoded_objects_local_json("test.json")
    """
    with open(read_from_filepath, "r") as file:
        json_dict = json.load(file)

    decoded_courses = decode(json_dict)

    first_course = decoded_courses[0]  # Printing first decoded Course object.
    print(first_course)

    for meeting in first_course.class_time:  # Printing all meetings within the course.class_time.
        print("-----")
        print(meeting)
