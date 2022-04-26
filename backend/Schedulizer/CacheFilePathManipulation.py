"""Cache is used to manage internal temporary files made the on machine during runtime.

cache_id or similar verbiage is used to describe a cache key value used to identify specific use cases for each cached
file. For example, it might be the unique identifier for a user's generated ics file.
"""

import os
import errno

from Schedulizer.constants import CACHE_DIRECTORY_PATH


def get_cache_path(file_name: str, cache_id: str = None) -> str:
    __make_sure_path_exists(CACHE_DIRECTORY_PATH)

    path, extension = os.path.splitext(file_name)

    cache_id = "" if cache_id is None else cache_id

    combined_path = f"{CACHE_DIRECTORY_PATH}{path}{cache_id}{extension}"  # Combine paths

    return combined_path


def remove_file_path(path: str):
    if os.path.exists(path):
        os.remove(path)
    else:
        raise RuntimeError(f"File path \"{path}\" does not exist!")


def remove_cache_path(file_name: str, cache_id: str = None):
    cache_path = get_cache_path(file_name=file_name, cache_id=cache_id)
    remove_file_path(cache_path)


def clear_cache_directory():
    remove_file_path(CACHE_DIRECTORY_PATH)


def __make_sure_path_exists(path: str):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
