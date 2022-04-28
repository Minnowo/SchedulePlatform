from curses.ascii import HT
from fastapi import HTTPException, status

API_404_USER_NOT_FOUND = HTTPException(
    status_code = status.HTTP_404_NOT_FOUND,
    detail = "This user doesn't exist."
)

API_406_USERNAME_INVALID = HTTPException(
    status_code = status.HTTP_406_NOT_ACCEPTABLE,
    detail = "This username isn't acceptable."
)

API_406_PASSWORD_INVALID = HTTPException(
    status_code = status.HTTP_406_NOT_ACCEPTABLE,
    detail = "This password isn't acceptable."
)

API_409_EMAIL_CONFLICT = HTTPException(
    status_code = status.HTTP_409_CONFLICT,
    detail = "This email is already in use."
)

API_409_USERNAME_CONFLICT = HTTPException(
    status_code= status.HTTP_409_CONFLICT,
    detail = "This user already exists."
)