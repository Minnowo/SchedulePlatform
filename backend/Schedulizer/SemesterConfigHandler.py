"""SemesterConfig defines standard class structure for different available program config modes.

Includes info like config name, api values, etc.
NOTE: Remember to update enabled configs in constants.py.
"""

import json
from datetime import datetime
from types import SimpleNamespace

from backend.Schedulizer.NewEventClass import NewEvent


class SemesterConfig:
    def __init__(self, name: str, semester_start: datetime, semester_end: datetime, api_mycampus_mep_code: str,
                 api_mycampus_term_id: str, api_ratemyprof_uni_id: str, universal_events: list[NewEvent]):
        """Semester Config class, offers a standardized single object to represent all configs.

        Args:
            name:
            semester_start:
            semester_end:
            api_mycampus_mep_code:
            api_mycampus_term_id:
            api_ratemyprof_uni_id:
            universal_events: list of NewEvent objects
        """
        self._name = name
        self._semester_start = semester_start
        self._semester_end = semester_end
        self._api_mycampus_mep_code = api_mycampus_mep_code
        self._api_mycampus_term_id = api_mycampus_term_id
        # _db_name is the equal of name but made safe for the SQL table name format rules
        self._db_name = self.__get_db_name()  # _db_name must be set after the attributes above as it may use the
        # value of other attributes
        self._api_ratemyprof_uni_id = api_ratemyprof_uni_id
        self._universal_events = universal_events

    @property
    def name(self):
        return self._name

    def __get_db_name(self):
        return "config_" + self._name.replace(" ", "_")

    @property
    def db_name(self):
        return self._db_name

    @property
    def semester_start(self):
        return self._semester_start

    @property
    def semester_end(self):
        return self._semester_end

    @property
    def api_mycampus_mep_code(self):
        return self._api_mycampus_mep_code

    @property
    def api_mycampus_term_id(self):
        return self._api_mycampus_term_id

    @property
    def api_ratemyprof_uni_id(self):
        return self._api_ratemyprof_uni_id

    @property
    def universal_events(self):
        return self._universal_events

    def __str__(self):
        """For prototyping purposes only.

        Returns:
            Default str similar to regular __str__ methods.
        """
        universal_events_names = ", ".join([event.name for event in self._universal_events])

        return (f"name={self._name}\n"
                f"db_name={self._db_name}\n"
                f"semester_start={self._semester_start}\n"
                f"semester_end={self._semester_end}\n"
                f"api_mycampus_mep_code={self._api_mycampus_mep_code}\n"
                f"api_mycampus_term_id={self._api_mycampus_term_id}\n"
                f"api_ratemyprof_uni_id={self._api_ratemyprof_uni_id}\n"
                f"universal_events.name={universal_events_names}")


def decode_config(json_file_path: str) -> SemesterConfig:
    """Acts as a decoder from a json config file to a SemesterConfig object.

    Potential FileNotFoundError raises!

    Args:
        json_file_path: Filepath of the json config file

    Returns:
        A SemesterConfig object with the dumped/decoded information from the given filepath
    """
    with open(json_file_path) as json_config_file:
        simple = json.load(json_config_file, object_hook=lambda d: SimpleNamespace(**d))

        # NOTE: This could be done with a custom json decoder class and object hook, but I couldn't get it working, so
        # it's decoded manually utilizing python types.SimpleNamespace here.

        universal_events = [NewEvent(name=namespace.event_name,
                                     description=namespace.event_description,
                                     start_datetime=datetime.fromisoformat(namespace.event_start),
                                     end_datetime=datetime.fromisoformat(namespace.event_end))
                            for namespace in simple.universal_events]
        # Universal events is a list of NewEvent objects that need to be decoded accordingly.

        config_object = SemesterConfig(name=simple.name,
                                       semester_start=datetime.fromisoformat(simple.semester_start),
                                       semester_end=datetime.fromisoformat(simple.semester_end),
                                       api_mycampus_mep_code=simple.api_mycampus_mep_code,
                                       api_mycampus_term_id=simple.api_mycampus_term_id,
                                       api_ratemyprof_uni_id=simple.api_ratemyprof_uni_id,
                                       universal_events=universal_events)

    return config_object
