from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SessionDuration(Base):
    __tablename__ = 'session_duration'
    
    userId = Column(String(10), primary_key=True)
    sessionDuration = Column(Integer, nullable=False)

