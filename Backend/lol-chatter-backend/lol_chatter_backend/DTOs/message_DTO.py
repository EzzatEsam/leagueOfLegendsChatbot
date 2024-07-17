from datetime import datetime
from pydantic import BaseModel


class messageDTO(BaseModel):
    id: int
    content: str
    date: datetime
    role : str