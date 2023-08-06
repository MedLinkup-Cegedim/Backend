from datetime import datetime
from typing import Annotated, List, Dict

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


password_type = Annotated[str, Field(
        example="password",
        title="New password",
        description="New password of the user",
    )]
email_type = Annotated[EmailStr, Field(
        example="user@gmail.com",
        title="Email",
        description="Email of the user",
    )]
firstname_type = Annotated[str, Field(
        example="John",
        title="First name",
        description="First name of the user",
    )]
lastname_type = Annotated[str, Field(
        example="Doe",
        title="Last name",
        description="Last name of the user",
    )]
user_id_type = Annotated[str, Field(
        example="60b6d8b3e3f4f3b3f0a3f3b3",
        title="User ID",
        description="ID of the user",
    )]
case_type = Annotated[List[Dict], Field(
        title="Cases List",
        description="List of cases associated with the user",
    )]

class UserInSignup(BaseModel):
    email: email_type
    password: password_type
    firstname: firstname_type
    lastname: lastname_type

class UserInfo(BaseModel):
    id: user_id_type
    email: email_type
    firstname: firstname_type
    lastname: lastname_type

class UserInLogin(BaseModel):
    email: email_type
    password: password_type

class UserDB(UserInSignup):
    cases: case_type = []

class UserOut(UserDB):
    id: user_id_type


class UserOutLogin(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserToken(BaseModel):
    id: user_id_type
    email: email_type

#######################################

class OrgInSignup(UserInSignup):
    org_flag = 1

class OrgDB(UserInSignup):
    Organization_status: str = "active"

class OrgOut(OrgDB):
    id: user_id_type

    class Config:
        arbitrary_types_allowed = True

