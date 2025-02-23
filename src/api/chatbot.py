from fastapi import APIRouter

chatbot_router = APIRouter()

@chatbot_router.post("/chatbot/message")
async def chatbot():
    pass

@chatbot_router.post("/chatbot/message/stream")
async def chatbot_stream():
    pass