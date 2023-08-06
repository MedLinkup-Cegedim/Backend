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

user_id_type = Annotated[str, Field(
    description="user ID(owner) in db",
    example="2dg3f4g5h6j7k8l9",
)]

class AddCase(BaseModel):
    first_name: name_type
    last_name: name_type
    email: email_type
    Category: Category_type
    created_date: creation_date_type
    user_id: user_id_type = 0


