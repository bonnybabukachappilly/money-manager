# app/api/v1/router/auth.py

from typing import Annotated

from fastapi import APIRouter, Depends, status, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import (
    UserResponseSchema,
    UserRegisterSchema,
    TokenResponseSchema
)
from app.api.dependencies import SessionDeps, UserRepoDeps
from app.application.user import RegisterUser, LoginUser
from app.domain import User
from app.exceptions.application import (
    EmailAlreadyExistsError,
    InvalidCredentialException,
    InactiveUserException
)

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post(
    path='/register',
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary='Register new user')
async def register(
        _: Request, body: UserRegisterSchema, session: SessionDeps,
        user_repo: UserRepoDeps) -> User:

    use_case = RegisterUser(
        user_repo=user_repo,
        session=session
    )

    try:
        user: User = await use_case.execute(
            fname=body.first_name,
            lname=body.last_name,
            email=body.email,
            password=body.password
        )

        await session.commit()

    except EmailAlreadyExistsError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='A user with this email already exists'
        ) from e

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='unknown error occurred.'
        ) from e

    return user


@router.post(
    path='/login',
    response_model=TokenResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary='Authenticate and obtain a JWT')
async def login(
        _: Request, form: Annotated[OAuth2PasswordRequestForm, Depends()],
        repo: UserRepoDeps) -> TokenResponseSchema:

    use_case = LoginUser(user_repo=repo)

    try:
        token: str = await use_case.execute(
            email=form.username,
            password=form.password
        )  # type: ignore

    except (InvalidCredentialException, InactiveUserException) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    return TokenResponseSchema(access_token=token)
