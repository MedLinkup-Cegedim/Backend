from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.models import users
from dependencies.db.users import UsersDriver
from dependencies.db.organization import OrganizationDriver
from .password_handler import PasswordHandler
from dependencies.token_handler import TokenHandler

router = APIRouter(
    prefix="/org-auth",
    tags=["org-auth"]
)

password_handler = PasswordHandler()
token_handler = TokenHandler()
users_driver = UsersDriver()
org_driver = OrganizationDriver()
oath2_scheme = OAuth2PasswordBearer(tokenUrl="/user-auth/login")


@router.post(
    "/org-signup",
    summary="create a new organization",
    description="add user to the database and send email to verify",
    response_class=PlainTextResponse,
    responses={
        status.HTTP_200_OK: {
            "description": "organization is added to the database",
            "content": {
                "text/plain": {
                    "example": "organization is created"
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
async def signup(org: users.UserInSignup) -> PlainTextResponse:
    org_driver.handle_existing_email(org.email)
    org.password = password_handler.get_password_hash(org.password)
    org_driver.create_user(org)
    return PlainTextResponse("organization is created successfully", status_code=status.HTTP_200_OK)



@router.post(
    "/org-login",
    summary="login for exited organization",
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
            "description": "wrong password",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "wrong password"
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
async def login(org_in: Annotated[OAuth2PasswordRequestForm, Depends()]) -> users.UserOutLogin:
    users_driver.validate(org_in.username)
    org_in = users.UserInLogin(email=org_in.username, password=org_in.password)

    org_driver.handle_nonexistent_email(org_in.email)
    org_db: users.OrgOut = org_driver.get_user_by_email(org_in.email)

    if not password_handler.verify_password(org_in.password, org_db.password):
        raise HTTPException(detail="wrong password", status_code=status.HTTP_401_UNAUTHORIZED)

    encoded_token = token_handler.encode_token(users.UserToken(**org_db.dict()))
    return users.UserOutLogin(access_token=encoded_token)

