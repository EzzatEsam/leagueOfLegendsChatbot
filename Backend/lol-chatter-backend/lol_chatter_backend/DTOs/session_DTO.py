from datetime import datetime
from pydantic import BaseModel


class sessionDTO(BaseModel):
    id : int
    title : str
    date: datetime
