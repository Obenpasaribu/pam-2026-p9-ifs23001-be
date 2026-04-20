from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.extensions import Base

class RequestLog(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    theme = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)