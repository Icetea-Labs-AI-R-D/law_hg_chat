import pydantic

class ChatRequest(pydantic.BaseModel):
    conversation_id: str
    message: str
    
class ChatResponse(pydantic.BaseModel):
    message: str