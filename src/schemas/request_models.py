from pydantic import BaseModel, Field
from enum import Enum

# Enum for feedback status tracking
class FeedbackStatus(Enum):
      SUBMITTED = "submitted"
      UNDER_REVIEW = "under_review"
      PROCESSED = "processed"

# Request validation for user registration
class RegisterRequest(BaseModel):
      username: str = Field(..., min_length=3, max_length=50)
      password: str = Field(..., min_length=8)

# Request validation for user login
class LoginRequest(BaseModel):
      username: str = Field(..., min_length=3, max_length=50)
      password: str = Field(..., min_length=8)

# Request validation for creating new feedback
class FeedBackCreate(BaseModel):
      title: str
      content: str

# Request validation for updating existing feedback
class FeedBackUpdate(BaseModel):
      title: str = None
      content: str = None
      status: FeedbackStatus