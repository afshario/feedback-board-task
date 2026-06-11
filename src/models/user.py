from sqlalchemy import Column, Integer, String, DateTime, Boolean
import bcrypt
from sqlalchemy.sql import func
from db import Base

class User(Base):
      __tablename__ = "users"
    
      id = Column(Integer, primary_key=True, index=True)
      username = Column(String(50), unique=True, nullable=False, index=True)
      password = Column(String(255), nullable=False)
      is_admin = Column(Boolean, default= True) # this is temporary
      created_at = Column(DateTime, server_default=func.now())

      def set_password(self, password: str):
            self.password = bcrypt.hashpw(
                  password.encode(),
                  bcrypt.gensalt()
            ).decode()

      def check_password(self, password: str):
            return bcrypt.checkpw(
                  password.encode(),
                  self.password.encode()
            )
