from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base

class Motivation(Base):
    __tablename__ = "motivations"

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))