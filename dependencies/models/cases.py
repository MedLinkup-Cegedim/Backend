from typing import Annotated,Optional
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field

from enum import Enum

# Define an Enum class for categories of the cases
class Category(Enum):
    Heart = "heart"
    Burn = "burn"
    Cancer = "cancer"


name_type = Annotated[str, Field(
    description="first/last Name of the user(patient)",
    example="John",
)]

email_type = Annotated[str, Field(
    description="Email of the user(patient)",
    example="ahmed@gmail.com",
)]

Category_type = Annotated[Category, Field(
    description="case type in db",
    example=Category.Heart.value
)]

creation_date_type = Annotated[datetime, Field(
    description="Creation date of the order",
    example="2023-05-01T00:00:00",
)]
case_id_type = Annotated[str, Field(
    example="60b6d8b3e3f4f3b3f0a3f3b3",
    title="Case ID",
    description="ID of the case in the database",
)]
class Case(BaseModel):
    first_name: name_type
    last_name: name_type
    email: email_type
    category: str
    status: str
    created_date: creation_date_type


class CaseOut(Case):
    case_id: case_id_type

