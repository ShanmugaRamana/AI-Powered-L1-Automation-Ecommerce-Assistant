# /backend/app/models/chat_models.py
from pydantic import BaseModel
from typing import List, Dict, Any

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, Any]]