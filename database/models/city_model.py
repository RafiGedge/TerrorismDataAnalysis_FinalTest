from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from database.models.base import Base


class City(Base):
    __tablename__ = 'cities'  # noqa
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    latitude = Column(Float, nullable=True, default=None)
    longitude = Column(Float, nullable=True, default=None)

    events = relationship('Event', back_populates='cities')
