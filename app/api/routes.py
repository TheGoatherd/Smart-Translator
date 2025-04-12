from fastapi import APIRouter
from .endpoints import chat_function as chat

app_router = APIRouter()

app_router.post("/chat")(chat)
