from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from db_connection.models.base import Base


class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    latitude = Column(Float, nullable=True, default=None)
    longitude = Column(Float, nullable=True, default=None)

    events = relationship("Event", back_populates="regions")
