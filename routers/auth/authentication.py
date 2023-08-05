from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.models import users
from dependencies.db.users import UsersDriver
from .password_handler import PasswordHandler
from dependencies.token_handler import TokenHandler

router = APIRouter(
    prefix="/user-auth",
    tags=["auth"]
)

password_handler = PasswordHandler()
token_handler = TokenHandler()
users_driver = UsersDriver()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/user-auth/login")


@router.post(
    "/signup",
    summary="create a new user",
    description="add user to the database and send email to verify",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "user is added to the database",
            "content": {
                "text/plain": {
                    "example": "User is created"
                },
            }
        },
        status.HTTP_406_NOT_ACCEPTABLE: {
            "description": "email already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "email already exists"
                    }
                }
            }
        }
    }
)
async def signup(user: users.UserInSignup) -> PlainTextResponse:
    users_driver.handle_existing_email(user.email)
    user.password = password_handler.get_password_hash(user.password)
    users_driver.create_user(user)
    return PlainTextResponse("User is created successfully", status_code=status.HTTP_200_OK)


@router.post(
    "/login",
    summary="login for exited user",
    description="login and get access token",
    response_model=users.UserOutLogin,
    responses={
        status.HTTP_200_OK: {
            "description": "login successfully",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                                        "eyJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIiwiaWF0IjoxNjIyNjQyNjQyLCJleHAiOjE",
                        "token_type": "bearer"
                    }
                }
            }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "wrong password or email is not verified",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "wrong password or email is not verified"
                    }
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "email not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "email not found"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "invalid email",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid email"
                    }
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "wrong domain name",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "invalid domain name for the email"
                    }
                }
            }
        }
    }
)
async def login(user_in: Annotated[OAuth2PasswordRequestForm, Depends()]) -> users.UserOutLogin:
    users_driver.validate(user_in.username)
    user_in = users.UserInLogin(email=user_in.username, password=user_in.password)

    users_driver.handle_nonexistent_email(user_in.email)
    user_db: users.UserOut = users_driver.get_user_by_email(user_in.email)

    if not password_handler.verify_password(user_in.password, user_db.password):
        raise HTTPException(detail="wrong password", status_code=status.HTTP_401_UNAUTHORIZED)

    encoded_token = token_handler.encode_token(users.UserToken(**user_db.dict()))
    return users.UserOutLogin(access_token=encoded_token)

