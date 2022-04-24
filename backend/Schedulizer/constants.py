"""Constants related to program computation
"""

from datetime import timedelta

from backend.Schedulizer.SemesterConfigHandler import decode_config

# Cache file directory
CACHE_DIRECTORY_PATH = "cache/"

# ICS Calendar base file name
ICS_CALENDAR_FILENAME = "calendar.ics"

# Keywords to check if a course is in person based on API data
# Called in MyCampusAPIDecoder.py
CLASS_INSTRUCTION_IN_PERSON_KEYS = ["in-class", "in-person"]  # API data at .instructionalMethodDescription

# Course record metadata outdated timedelta
OUTDATED_COURSE_METADATA_TIMEDELTA = timedelta(days=0, hours=0, minutes=30, seconds=0)

# Enabled semester config templates
ENABLED_CONFIGS_FILE_PATH = "Schedulizer/configs/0_enabledConfigs.json"
