"""MyCampus API used to pull schedule data in json formats via http get requests.

3 http request in single session. Send following 3 requests in sequential order:
    1)  https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/term/termSelection?mode=search&mepCode=UOIT
    2)  https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/term/search?mode=search&term=202201
    3)  https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/searchResults/searchResults?mepCode=UOIT&txt_term=202201&txt_subjectcoursecombo=CHEM1800U

If you want to check the course registration website in guest mode:
    https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/term/termSelection?mode=search&mepCode=UOIT

Error raising:
    1)  In the event a get request cannot be fulfilled (MyCampus/Banner is down) a requests.exceptions.ConnectionError
        exception is raised.
"""

import requests


def get_json_course_codes(mep_code: str, term_id: str, search_code: str, max_count: int = 10) -> dict:
    """http request for course code based on a search key.

    Args:
        mep_code: School mep code. Example: Ontario Tech University = "UOIT".
        term_id: Term id used by api.
            Examples: Fall 2021 = "202109", Winter 2022 = "202201", Spring/Summer 2022 = "202205".
        search_code: Search course code.
            Examples: "PHY1010U", "CHEM1800U", "MATH1850U".
        max_count: Number of course results to search. Default = 10.

    Returns:
        Course codes of matching search_code as json dict response from API

        Example:
            Given search_code = PHY
            Return = ["PHY1010U", "PHY1020U", etc]
    """
    if not isinstance(mep_code, str):
        raise TypeError(f"mep_code expected {str}, received {type(mep_code)}")
    elif not isinstance(search_code, str):
        raise TypeError(f"course_code expected {str}, received {type(search_code)}")
    elif not isinstance(term_id, str):
        raise TypeError(f"term_id expected {str}, received {type(term_id)}")
    elif not isinstance(max_count, int):
        raise TypeError(f"max_count expected {int}, received {type(max_count)}")

    session = requests.Session()

    session.get(url=f"https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/term/termSelection?mode=search&"
                    f"mepCode={mep_code}", timeout=5)
    session.get(url=f"https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/term/search?mode=search&term={term_id}",
                timeout=5)
    return session.get(url=f"https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/classSearch/get_subjectcoursecombo?"
                           f"searchTerm={search_code}&term={term_id}&offset=1&max={max_count}", timeout=5).json()


def get_json_course_data(mep_code: str, term_id: str, course_code: str, max_count=999) -> dict:
    """http API request for course data

    Args:
        mep_code: School mep code. Example: Ontario Tech University = "UOIT".
        term_id: Term id used by api.
            Examples: Fall 2021 = "202109", Winter 2022 = "202201", Spring/Summer 2022 = "202205".
        course_code: Course code.
            Examples: "PHY1010U", "CHEM1800U", "MATH1850U".
        max_count: Number of course results to search. Default = 999.

    Returns:
        Course data json dict response from API

        Example:
            Given course_code = PHY1020U
            Return = json responce from API
    """
    if not isinstance(mep_code, str):
        raise TypeError(f"mep_code expected {str}, received {type(mep_code)}")
    elif not isinstance(course_code, str):
        raise TypeError(f"course_code expected {str}, received {type(course_code)}")
    elif not isinstance(term_id, str):
        raise TypeError(f"term_id expected {str}, received {type(term_id)}")
    elif not isinstance(max_count, int):
        raise TypeError(f"max_count expected {int}, received {type(max_count)}")

    course_code = course_code.upper()

    session = requests.Session()

    session.get(url=f"https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/term/termSelection?mode=search&"
                    f"mepCode={mep_code}", timeout=5)
    session.get(url=f"https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/term/search?mode=search&term={term_id}",
                timeout=5)
    return session.get(url=f"https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/searchResults/searchResults?"
                           f"mepCode={mep_code}&txt_term={term_id}&txt_subjectcoursecombo={course_code}&"
                           f"pageMaxSize={max_count}", timeout=5).json()


def get_terms(mep_code: str, max_count: int = 999) -> dict:
    """http API request for term ids of a given mep_code.

    Args:
        mep_code: School mep code. Example: Ontario Tech University = "UOIT".
        max_count: Number of course's class results to search. Default = 999.

    Returns:
        Term data json dict response from API

        Return example:
            [{'code': '202205', 'description': 'Spring/Summer 2022'},
             {'code': '202201', 'description': 'Winter 2022 (View Only)'},
             ...
            ]
    """
    session = requests.Session()

    session.get(url=f"https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/term/termSelection?mode=search&"
                    f"mepCode={mep_code}", timeout=5)
    return session.get(url=f"https://ssp.mycampus.ca/StudentRegistrationSsb/ssb/classSearch/getTerms?searchTerm"
                           f"=&offset=1&max={max_count}",
                       timeout=5).json()
