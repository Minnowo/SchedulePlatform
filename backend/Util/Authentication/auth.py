import bcrypt
import hashlib # hashlib is actually built-into python
import base64
import json

from DBController import UserAccounts
from fastapi_login import LoginManager

SECRET = 'your-secret-key'

manager = LoginManager(SECRET, token_url="/auth/token")

# def authenticate_user(username : str, password : str) -> models.UserAuthIn:

def hashPassword(password: str) -> str:

    # This turns the password string into bytes

    if isinstance(password, str):
        password.encode()

    #Taken from the bcrypt docs (Work arround for 72 char limit)

    return bcrypt.hashpw( 
    base64.b64encode(hashlib.sha256(password.encode()).digest()), 
    bcrypt.gensalt(15)
    ).decode()

def verifyPassword(password : str, hashed_password: str) -> bool:

    if isinstance(password,str):
        password = password.encode()
    
    return bcrypt.checkpw(
        base64.b64encode(
            hashlib.sha256(
                password
            )
        ),
        hashed_password.encode()
    )


@manager.user_loader()
def authUser(userQuery: str, password: str) -> json:

    UserAccounts.searchUser(userQuery)

    return

