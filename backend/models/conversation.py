from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime
import pymongo

class Message(BaseModel):
    role: str
    content: str

class Conversation(Document):
    chat_id: str
    messages: List[Message]
    documents: List[Dict]
    create_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)
    
    class Settings:
        name = "conversation"
        indexes = [
            [
                ("chat_id", pymongo.TEXT),
                ("create_at", pymongo.DESCENDING)
            ]
        ]
        
class ConversationModel(BaseModel):
    chat_id: str
    messages: List[Message]
    documents: List[Dict]