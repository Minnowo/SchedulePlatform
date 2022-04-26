"""A few test functions for the external ratemyprofessor API used in the backend.

These files should under no conditions be used in production. Only to be used as reference and test code. There is
basically no overhead, redundancies, input production, etc.
"""

import json
from datetime import datetime

from Schedulizer.APIs.RatemyprofessorAPI import get_prof_list


def ratemyprofessor_api_save_as_json_file(uni_id: int, save_to_filepath: str | None = None):
    """
    Generates a .json file of the api response from the ratemyprofessor api. The data matches that of the given uni_id.

    Args:
        uni_id: University ID. Example: Ontario Tech University = 4714.
        save_to_filepath: File path + name to save to, defaults None (in which case, uses course and now datetime as
            filename saved to the current directory).

    Examples:
        ratemyprofessor_api_save_as_json_file(4714, "test")
            This will save the response for professor ratings at university ID 4714, saved to "test.json" (in the
            current directory).

        ratemyprofessor_api_save_as_json_file(4714)
            This will save the response for professor ratings at university ID 4714, saved to
            "4714 %Y-%m-%d %H-%M.json" (current datetime.strftime) (in the current directory).
    """
    save_to_filepath = save_to_filepath if save_to_filepath is not None \
        else f"{uni_id} {datetime.now().strftime('%Y-%m-%d %H-%M')}"
    save_to_filepath = save_to_filepath + ".json" if save_to_filepath[-5:] != ".json" else save_to_filepath

    with open(f"{save_to_filepath}", "w") as file:
        json.dump(get_prof_list(uni_id), file, indent=4)
