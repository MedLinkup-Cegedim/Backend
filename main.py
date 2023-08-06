"""
created by: Ahmed Maher
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from routers.auth import authentication
from routers.cases import cases

app = FastAPI(
    title="Cegedim",
    description="Cegedim project APIs",
    version="1.0",
    docs_url="/"

)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(cases.router)
add_pagination(app)

