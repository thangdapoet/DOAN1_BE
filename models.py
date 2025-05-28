from sqlalchemy import Column, Integer, String, Double, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    data_entries = relationship("Data", back_populates="session")


class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    doam = Column(Double, index=True)
    nhietdo = Column(Double)
    co2 = Column(Double)
    co = Column(Double)
    nh3 = Column(Double)
    toluen = Column(Double)
    c6h6 = Column(Double)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    
    session_id = Column(Integer, ForeignKey("session.id"))

    
    session = relationship("Session", back_populates="data_entries")
