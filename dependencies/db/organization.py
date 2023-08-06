from datetime import datetime

import email_validator
from fastapi import HTTPException
from fastapi import status

from pymongo import errors as mongo_errors
from email_validator import validate_email

from dependencies.models import users
from dependencies.db.client import Client
from dependencies.utils.bson import convert_to_object_id

class OrganizationDriver:
    def __init__(self):
        self.db = Client.get_instance().get_db()
        self.collection = self.db["organizations"]

    def handle_existing_email(self, email: str):
        if self.email_exists(email):
            raise HTTPException(detail="email already exists", status_code=status.HTTP_400_BAD_REQUEST)

    def handle_nonexistent_email(self, email: str):
        if not self.email_exists(email):
            raise HTTPException(detail="email not found", status_code=status.HTTP_404_NOT_FOUND)

    def create_user(self, user: users.UserInSignup) -> users.UserOut:
        try:
            org_db = users.OrgDB(last_password_update=datetime.utcnow(), **user.dict())
            inserted_id = self.collection.insert_one(org_db.dict()).inserted_id
            org_out = users.OrgOut(**org_db.dict(), id=str(inserted_id))
            return org_out
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def email_exists(self, email: str):
        try:
            return self.collection.find_one({"email": email}) is not None
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_user_by_email(self, email: str) -> users.OrgOut:
        try:
            user = self.collection.find_one({"email": email})
            return users.OrgOut(**user, id=str(user["_id"]))
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
