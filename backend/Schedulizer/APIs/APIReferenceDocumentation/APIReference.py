"""
Test functions for any external APIs used in the backend
"""

import json
from datetime import datetime

from backend.Schedulizer.APIs.MycampusAPI import get_json_course_data
from backend.Schedulizer.APIs.MycampusAPIDecoder import decode_api_json_to_course_obj as decode


def generate_api_file(course_code, mep_code, term_id):
    json_str = get_json_course_data(mep_code=mep_code, term_id=term_id, course_code=course_code)

    pull_datetime = datetime.now().strftime("%Y-%m-%d %H-%M")

    with open(f"{course_code} {pull_datetime}.json", "w") as file:
        json.dump(json_str, file, indent=4)


def print_decoded_objects_from_api(course_code, mep_code, term_id):
    yeet = decode(get_json_course_data(mep_code=mep_code, term_id=term_id, course_code=course_code))

    single = yeet[0]  # Printing first decoded Course object.
    print(single)

    for meeting in single.class_time:  # Printing all meetings within the course.class_time.
        print("-----")
        print(meeting)
