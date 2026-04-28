from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ChatRequest(BaseModel):
    ticker: str
    message: str
    history: List[dict] = []

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Allows the user to chat with the system regarding a specific ticker.
    """
    # Mock data for boilerplate
    return {
        "response": f"I see you're asking about {request.ticker}. The model identified an oversold RSI on the daily chart combined with highly positive sentiment."
    }
