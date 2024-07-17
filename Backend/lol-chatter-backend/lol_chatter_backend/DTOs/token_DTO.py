from pydantic import BaseModel


class TokenDTO(BaseModel):
    accessToken: str
    tokenType: str