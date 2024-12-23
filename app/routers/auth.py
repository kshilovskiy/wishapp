from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.config import settings
from app.routers.security import authenticate_user, create_access_token, get_jwt_payload, get_active_user
from app.models.token import Token, RefreshToken
from app.database import DbSession

router = APIRouter()

TOKEN_TYPE_REFRESH = "refresh"

@router.post("/token")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: DbSession
) -> Token:
    if len(form_data.username) <= 1:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    access_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_access_token(
        data={"sub": user.email, "token_type": TOKEN_TYPE_REFRESH}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@router.post("/refresh")
async def refresh(token_data: RefreshToken, db: DbSession) -> Token:
    try:
        payload = get_jwt_payload(token_data.token)
        token_type = payload.get("token_type")
        if token_type != TOKEN_TYPE_REFRESH:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )
        email = payload.get("sub")
        user = get_active_user(email, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No such user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        new_refresh_token = create_access_token(
            data={"sub": email, "token_type": TOKEN_TYPE_REFRESH},
            expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        )
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
