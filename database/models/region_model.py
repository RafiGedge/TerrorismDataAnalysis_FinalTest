from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.models.base import Base


class Region(Base):
    __tablename__ = 'regions'  # noqa

    id = Column(Integer, primary_key=True)
    name = Column(String)

    events = relationship("Event", back_populates="regions")
