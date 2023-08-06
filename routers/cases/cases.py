from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from dependencies.models import users
from dependencies.db.users import UsersDriver
from dependencies.token_handler import TokenHandler


router = APIRouter(
    prefix="/cases",
    tags=["cases"]
)