from datetime import datetime
from pydantic import BaseModel


class TokenData(BaseModel):
    email: str 
    userId : int

