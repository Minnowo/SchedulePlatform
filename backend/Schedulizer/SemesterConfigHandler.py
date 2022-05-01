"""SemesterConfig defines standard class structure for different available
program config modes.

Includes info like config name, api values, etc.
NOTE: Remember to update enabled configs in constants.py.
"""

import json
from datetime import datetime
from types import SimpleNamespace
from dotenv import load_dotenv
import os

from Schedulizer.NewEventClass import NewEvent

load_dotenv()


class SemesterConfig:
    def __init__(self, name: str, semester_start: datetime,
                 semester_end: datetime, api_mycampus_mep_code: str,
                 api_mycampus_term_id: str, api_ratemyprof_uni_id: str,
                 universal_events: list[NewEvent]):
        """Semester Config class, offers a standardized single object to
        represent all configs.

        Args:
            name:
            semester_start:
            semester_end:
            api_mycampus_mep_code:
            api_mycampus_term_id:
            api_ratemyprof_uni_id:
            universal_events: list of NewEvent objects
        """
        self.name = name
        self.semester_start = semester_start
        self.semester_end = semester_end
        self.api_mycampus_mep_code = api_mycampus_mep_code
        self.api_mycampus_term_id = api_mycampus_term_id
        self.api_ratemyprof_uni_id = api_ratemyprof_uni_id
        self.universal_events = universal_events

    def get_db_table(self):
        return (f"{os.getenv('SQL_CONFIG_TABLE_HEADER')}"
                f"{self.name.lower().replace(' ', '_')}")

    def to_json(self) -> str:
        """Converts a SemesterConfig object to json str.

        Returns:
            json string of the SemesterConfig object.
        """

        def default(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, int):
                return obj
            if isinstance(obj, list):  # list[NewEvent]
                return str([event.to_json for event in obj])
            else:
                return obj.__dict__

        return json.dumps(self, default=default)

    @staticmethod
    def from_json(json_str: str):  # -> SemesterConfig:
        """Converts a SemesterConfig object to json str.

        Returns:
            json string of the SemesterConfig object.
        """
        simple = json.loads(json_str, object_hook=lambda d: SimpleNamespace(**d))

        universal_events = [NewEvent(
            name=namespace.name,
            description=namespace.description,
            start_datetime=datetime.fromisoformat(namespace.start_datetime),
            end_datetime=datetime.fromisoformat(namespace.end_datetime))
            for namespace in simple.universal_events]
        # Universal events is a list of NewEvent objects that need to be
        # decoded accordingly.

        return SemesterConfig(
            name=simple.name,
            semester_start=datetime.fromisoformat(simple.semester_start),
            semester_end=datetime.fromisoformat(simple.semester_end),
            api_mycampus_mep_code=simple.api_mycampus_mep_code,
            api_mycampus_term_id=simple.api_mycampus_term_id,
            api_ratemyprof_uni_id=simple.api_ratemyprof_uni_id,
            universal_events=universal_events)

    def __str__(self):
        """For prototyping purposes only.

        Returns:
            Default str similar to regular __str__ methods.
        """
        universal_events_names = ", ".join([event.name for event in
                                            self.universal_events])

        return (f"name={self.name}\n"
                f"semester_start={self.semester_start}\n"
                f"semester_end={self.semester_end}\n"
                f"api_mycampus_mep_code={self.api_mycampus_mep_code}\n"
                f"api_mycampus_term_id={self.api_mycampus_term_id}\n"
                f"api_ratemyprof_uni_id={self.api_ratemyprof_uni_id}\n"
                f"universal_events.name={universal_events_names}")


def decode_config(json_file_path: str) -> SemesterConfig:
    """Acts as a decoder from a json config file to a SemesterConfig object.

    Potential FileNotFoundError raises!

    Args:
        json_file_path: Filepath of the json config file

    Returns:
        A SemesterConfig object with the dumped/decoded information from the
        given filepath
    """
    with open(json_file_path) as json_config_file:
        json_str = json_config_file.read()

    return SemesterConfig.from_json(json_str)
