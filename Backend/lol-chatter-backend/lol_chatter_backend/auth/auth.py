from datetime import timedelta
from typing import Union
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from lol_chatter_backend.DTOs import (
    ErrorDTO,
    UserSignUpDTO,
    TokenDTO,
    UserLoginDTO,
    UserDataDTO,
)
from lol_chatter_backend.DbOperations import UserManagement
from lol_chatter_backend.Dependencies.db_deps import get_db
from lol_chatter_backend.Dependencies.token_deps import get_current_user
from lol_chatter_backend.Models.token_data import TokenData
from lol_chatter_backend.Security.tokens import create_access_token

router = APIRouter()


@router.post("/signup", responses={400: {"model": ErrorDTO}}, status_code=201)
async def signup(signup_data: UserSignUpDTO, db=Depends(get_db)):

    user, err = UserManagement.create_user(db, signup_data)
    if err:
        return JSONResponse(status_code=400, content=err.model_dump())
    return {}


@router.post(
    "/login",
    responses={400: {"model": ErrorDTO}},
    status_code=200,
    response_model=TokenDTO,
)
async def login(login_data: UserLoginDTO, db=Depends(get_db)):
    usr, err = UserManagement.login_user(db, login_data)
    if err:
        return JSONResponse(status_code=400, content=err.model_dump())
    if usr:
        tokenData = TokenData(email=usr.email, userId=usr.id)
        token = create_access_token(data=tokenData, expires_delta=timedelta(days=7))
        return TokenDTO(accessToken=token, tokenType="bearer")


@router.get("/me", response_model=UserDataDTO)
async def get_me(user=Depends(get_current_user)):
    return UserDataDTO(
        firstName=user.first_name, lastName=user.last_name, email=user.email
    )
