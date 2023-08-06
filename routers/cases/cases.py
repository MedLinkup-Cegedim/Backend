from fastapi.responses import PlainTextResponse
from typing import List, Annotated
from fastapi import APIRouter, HTTPException, status, Body
from dependencies.models.cases import Case, CaseOut
from dependencies.db.users import UsersDriver
from dependencies.db.cases import CasesDriver
from dependencies.token_handler import TokenHandler
from fastapi.security import OAuth2PasswordBearer
from dependencies.models.users import UserToken
from fastapi import Depends


router = APIRouter(
    prefix="/cases",
    tags=["cases"]
)
db_handler = CasesDriver()
users_driver = UsersDriver()

token_handler = TokenHandler()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user-auth/login")

@router.post(
    "/add_case",
    summary="Add case",
    description="This endpoint allows you to add case for a user(patient)",
    responses={
        status.HTTP_200_OK: {
            "description": "Order added successfully.",
            "content": {
                    "first_name":"John",
                    "last_name":"Doe",
                    "email":"ahmed@gmail.com",
                    "category":"heart",
                    "created_date":"2021-08-12T12:00:00.000Z",
                    "user_id":"jhv868753v5y3u74t"
                    }
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User is not authorized",
        },
    },
)
async def add_case(
    token: Annotated[str, Depends(oauth2_scheme)],
    case: Case = Body(..., description="Case model",
    example={
        "first_name": "John",
        "last_name": "Doe",
        "email": "user@gmail.com",
        "category": "heart",
        "status": "active",
        "created_date": "2021-08-12T12:00:00.000Z",
    })
) -> CaseOut:
    user: UserToken = token_handler.get_user(token)
    users_driver.handle_nonexistent_user(user.id)
    users_driver.handle_nonexistent_email(case.email)
    new_case_data = {
        "category": case.category,
        "status": case.status,
        "severity": 1
    }
    user_in_db = users_driver.get_user_by_email(case.email)
    user_in_db.cases.append(new_case_data)
    users_driver.edit_info(user.id, new_case_data)
    return db_handler.add_case(case)
