from fastapi_login import LoginManager
from authConstants import SECRET

manager = LoginManager(SECRET, token_url="/auth/token")