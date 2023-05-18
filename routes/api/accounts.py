import passlib
from fastapi import Request

from utils.classes import APIRouter

router = APIRouter(logger_name=__name__, logger_level=0) # logger level will later be changed when including

@router.post("/register")
async def index(request: Request):
    ...