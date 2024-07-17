from pydantic import BaseModel, EmailStr


class UserSignUpDTO(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str
