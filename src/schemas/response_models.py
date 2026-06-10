from pydantic import BaseModel
from datetime import datetime
from request_models import FeedbackStatus

# Response schema after successful user registration
class RegisterResponse(BaseModel):
    id: int
    username: str

# Response schema for feedback data
class FeedBackResponse(BaseModel):
      id: int
      author: str
      title: str
      content: str
      status: FeedbackStatus
      created_at: datetime