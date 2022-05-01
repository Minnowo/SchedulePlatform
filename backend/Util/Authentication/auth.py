import bcrypt
import hashlib  # hashlib is actually built-into python
import base64
import json
import fastapi.security as FA_security
from fastapi import Depends, HTTPException, status

from DBController import UserAccounts
from fastapi_login import LoginManager


SECRET = 'your-secret-key'

OAUTH2_PASS_SCHEMA = FA_security.OAuth2PasswordBearer(tokenUrl="/auth/token")

manager = LoginManager(SECRET, token_url="/auth/token", use_cookie=True)


# def authenticate_user(username : str, password : str) -> models.UserAuthIn:

def hash_password(password: str) -> str:
    # This turns the password string into bytes

    if isinstance(password, str):
        password.encode()

    # Taken from the bcrypt docs (Work around for 72 char limit)

    return bcrypt.hashpw(
        base64.b64encode(hashlib.sha256(password.encode()).digest()),
        bcrypt.gensalt(15)
    ).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    if isinstance(password, str):
        password = password.encode()

    check_hash = base64.b64encode(
            hashlib.sha256(
                password
            ).digest()
        )


    return bcrypt.checkpw(
       check_hash,
        hashed_password.encode()
    )


@manager.user_loader()
def load_user(user_query: str) -> json:

    user = UserAccounts.search_user(user_query)

    if user is None:
        return 
    
    return user

async def get_current_user(token: str = Depends(OAUTH2_PASS_SCHEMA)):
    

    return token

