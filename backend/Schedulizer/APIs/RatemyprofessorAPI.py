"""RateMyProfessor API used to pull schedule data in json formats via http get requests.

https://www.ratemyprofessors.com
"""

import requests
import json
import math


def get_prof_list(uni_id: int) -> list[str]:
    """

    Args:
        uni_id: University id.

    Returns:
        List of prof data.
    """
    prof_list = []
    num_of_prof = get_num_of_profs(uni_id)
    pages_count = math.ceil(num_of_prof / 20)

    for i in range(1, pages_count + 1):
        page = requests.get(f"http://www.ratemyprofessors.com/filter/professor/?&page={i}&"
                            f"filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&"
                            f"sid={uni_id}", timeout=5)
        prof_list.extend(json.loads(page.content)['professors'])

    return prof_list


def get_num_of_profs(uni_id: int) -> int:
    """

    Args:
        uni_id: University id

    Returns:
        Number of professor records at the given university id.
    """
    page = requests.get(f"http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&"
                        f"query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid={uni_id}", timeout=5)
    temp_json = json.loads(page.content)

    return temp_json["remaining"] + 20  # TODO: If there is less than 20 (less than 1 page) this count doesnt work.
