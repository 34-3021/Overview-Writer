from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginSuccessResponse(BaseModel):
    token: str
    message: str

class LoginFailedResponse(BaseModel):
    message: str
