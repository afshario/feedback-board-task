from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
import enum
from sqlalchemy.sql import func
from db import Base

# Enum for feedback status tracking
class FeedbackStatus(str,enum.Enum):
      SUBMITTED = "submitted"
      UNDER_REVIEW = "under_review"
      PROCESSED = "processed"

class FeedBack(Base):
      __tablename__ = "feedbacks"
    
      id = Column(Integer, primary_key=True, index=True)
      title = Column(String(100), nullable=False)
      content = Column(Text, nullable=False)
      status = Column(
            Enum(FeedbackStatus),
            default=FeedbackStatus.SUBMITTED,  
            nullable=False,  
            index=True
      )
      created_at = Column(DateTime, server_default=func.now())
      updated_at = Column(DateTime, onupdate=func.now())   