from pydantic import BaseModel, EmailStr


class AuthRegistration(BaseModel):
    email: EmailStr
    password: str
    

class AuthRegistrationResponse(BaseModel):
     id: int
     email: EmailStr
     username: str
     is_staff: bool
     is_superuser: bool

class AuthLogin(BaseModel):
    email: EmailStr
    password: str


class AuthRegistrationResponse(AuthRegistration):
    id: int
    email: EmailStr
    username: str
    is_staff: bool
    is_superuser: bool