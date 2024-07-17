from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from lol_chatter_backend.DbOperations import UserManagement
from lol_chatter_backend.Dependencies.db_deps import get_db
from lol_chatter_backend.Models.User import User
from lol_chatter_backend.Security.tokens import get_token_data


async def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> str | None:
    if credentials and credentials.scheme == "Bearer":
        return credentials.credentials
    else:
        raise HTTPException(detail="Unauthorized", status_code=401)


async def get_current_user(token: str = Depends(get_bearer_token) , db=Depends(get_db)) -> User :

    token_data = get_token_data(token)

    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user , err = UserManagement.get_user_by_email(db , token_data.email)
    
    if err:
        raise HTTPException(status_code=400, detail=err)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
