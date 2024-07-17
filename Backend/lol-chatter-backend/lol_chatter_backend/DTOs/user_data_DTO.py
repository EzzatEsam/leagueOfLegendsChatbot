from pydantic import BaseModel


class UserDataDTO(BaseModel) :
    firstName : str
    lastName : str
    email : str