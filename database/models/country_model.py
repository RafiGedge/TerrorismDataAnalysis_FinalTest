from sqlalchemy import Column, Integer, String, Index, Float
from sqlalchemy.orm import relationship

from database.models.base import Base


class Country(Base):
    __tablename__ = 'countries'  # noqa

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    latitude = Column(Float, nullable=True, default=None)
    longitude = Column(Float, nullable=True, default=None)

    events = relationship("Event", back_populates="countries")

    # __table_args__ = (Index('idx_name', 'name'),)
