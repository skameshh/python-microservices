from sqlalchemy import Column, Integer, String
from db import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True)
    full_name = Column(String(100))
    role = Column(String(50))
