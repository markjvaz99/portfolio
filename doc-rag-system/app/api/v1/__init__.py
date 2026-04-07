from fastapi import APIRouter
from . import  routes_query

api_router = APIRouter()

api_router.include_router(routes_query.router, prefix="/query", tags=["Query"])
