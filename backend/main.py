"""FastAPI

Normally to run FastAPI manually using uvicorn you use: "uvicorn main:app --reload" in the terminal from the directory
of this file (main.py). However, here uvicorn is called so FastAPI should run when main is run.

Remember to get to the docs it looks like this: http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

from backend.SchedulizerCalls import general_crn_build, generate_crn_download_path

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.post("/crn/{config_id}")
async def crn(config_id: str, course_codes: list[str], crn_codes: list[int]) -> str:
    """json string data of given CRN codes pulled from the backend DB.

    Args:
        config_id: Semester config id determines what semester is being processed.
        course_codes: List of course codes which the given crn codes belong to. The program will update the backend DB
            (with overhead). These course codes are not necessary to function, but should be given to ensure the DB has
            the data for the requested CRNs.
        crn_codes: List of crn codes of each specific class to process.

    Returns:
        Course data in a json string form from the backend DB based on CRN codes.
    """
    return general_crn_build(config_id=config_id, course_codes=course_codes, crn_codes=crn_codes)


@app.post("/crn/{config_id}/download")
async def crn_download(config_id: str, course_codes: list[str], crn_codes: list[int]) -> FileResponse:
    """Download calendar generated from given CRN codes pulled from the backend DB.

    Args:
        config_id: Semester config id determines what semester is being processed.
        course_codes: List of course codes which the given crn codes belong to. The program will update the backend DB
            (with overhead). These course codes are not necessary to function, but should be given to ensure the DB has
            the data for the requested CRNs.
        crn_codes: List of crn codes of each specific class to process.

    Returns:
        Download for the created ics calendar file
    """
    cache_path = generate_crn_download_path(config_id=config_id, course_codes=course_codes, crn_codes=crn_codes)
    return FileResponse(path=cache_path, filename="calendar.ics", media_type='text/ics')


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
