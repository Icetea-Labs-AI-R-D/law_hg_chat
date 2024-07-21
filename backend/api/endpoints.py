from fastapi import APIRouter
from api.routes.chat import router as chat

router = APIRouter()

router.include_router(router=chat)