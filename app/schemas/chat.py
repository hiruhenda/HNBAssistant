from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_name: str = Field(..., description="Name of the user", example="Hiruka")
    message: str = Field(..., description="Message for the assistant", example="Hello! What can you help me with?")

class ChatResponse(BaseModel):
    user_name: str
    reply: str
    status: str = "success"