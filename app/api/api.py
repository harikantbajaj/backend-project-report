from fastapi import APIRouter
from app.api.v1 import users, reports, auth

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
