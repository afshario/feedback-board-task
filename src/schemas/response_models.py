from pydantic import BaseModel
from datetime import datetime

# Response schema after successful user registration
class RegisterResponse(BaseModel):
    id: int
    username: str

# Response schema for feedback data
class FeedBackResponse(BaseModel):
    id: int
    title: str
    content: str
    status: str
    created_at: datetime