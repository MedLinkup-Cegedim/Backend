import pydantic

from dependencies.models import cases
from dependencies.db.client import Client
from pymongo import errors as mongo_errors
from bson.objectid import ObjectId
from dependencies.utils.bson import convert_to_object_id
from fastapi import HTTPException
from fastapi import status


class CasesDriver:
    def __init__(self):
        self.db = Client().get_instance().get_db()
        self.collection = self.db["cases"]

    def add_case(self, case):
        try:
            case_dict = case.dict()
            inserted_id = self.collection.insert_one(case_dict).inserted_id

            # Retrieve the inserted document to get the case_id
            inserted_doc = self.collection.find_one({"_id": inserted_id})
            case_db = cases.CaseOut(case_id=str(inserted_id), **inserted_doc)
            return case_db
        except mongo_errors.PyMongoError:
            raise HTTPException(detail="database error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except pydantic.ValidationError as e:
            raise HTTPException(detail="validation error", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                headers={"X-Error": str(e)})
