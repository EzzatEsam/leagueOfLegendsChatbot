from datetime import datetime, timedelta
from typing import Union

import jwt

from lol_chatter_backend.Models.token_data import TokenData
from lol_chatter_backend.config import ENCODING_ALGORITHM, SECRET_KEY


def create_access_token(data: TokenData , expires_delta: timedelta) -> str:
    """
    Creates a JSON Web Token (JWT) with the provided data and expiration time.

    Args:
        data (TokenData): The data to be encoded in the JWT.
        expires_delta (timedelta): The time duration after which the JWT will expire.

    Returns:
        str: The encoded JWT.

    """
    to_encode = data.model_dump()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ENCODING_ALGORITHM)
    return encoded_jwt

def get_token_data(token: str) -> TokenData | None:
    """
    Decodes a given token using the provided SECRET_KEY and ENCODING_ALGORITHM.
    
    Args:
        token (str): The token to decode.
    
    Returns:
        TokenData | None: The decoded token data if successful, None if an InvalidTokenError occurs.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ENCODING_ALGORITHM])
        token_data = TokenData(**decoded_token)
        return token_data
    except jwt.exceptions.InvalidTokenError as e:        
        return None
    
