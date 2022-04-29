"""FastAPI

Normally to run FastAPI manually using uvicorn you use: "uvicorn main:app --reload" in the terminal from the directory
of this file (main.py). However, here uvicorn is called so FastAPI should run when main is run.

Remember to get to the docs it looks like this: http://localhost:8000/docs
"""
import time

from fastapi import FastAPI, Request, Depends
from DBController import UserAccounts
from Util.Authentication import auth
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm 
import uvicorn

from SchedulizerCalls import general_crn_build, generate_crn_download_path

app = FastAPI()

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"Hello": "World"}


@app.post('/auth/token')
async def login(req: Request, data: OAuth2PasswordRequestForm = Depends()):


    username = data.username
    password = data.password

    user = auth.auth_user(username, password)

    if user == False:
        print("NOPE!")
        return

    access_token = auth.manager.create_access_token(
        data = {
            "username" : username,
        }
    )

    return {
        'access_token': access_token, 
        'token_type': 'bearer',
        'username'  : username,
    }


@app.post('/create/user')
async def create_user(username: str, password: str, name: str, email: str):
    tic = time.perf_counter()
    UserAccounts.create_user(username,password,name,email)
    toc = time.perf_counter()
    
    print(f"A user was created in {toc-tic:0.4f} seconds")

    return {"Hello" : "World"}

@app.post('/c')
async def c():
    queriedUser = UserAccounts.search_user('test@gmail.com')
    print(queriedUser)


    return {'suc':'ces'}


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
    uvicorn.run("main:app", host="localhost", port=8000)
