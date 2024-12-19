from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.models.base import Base


class Attacktype(Base):
    __tablename__ = 'attacktypes'  # noqa

    id = Column(Integer, primary_key=True)
    name = Column(String)

    events = relationship('Event', back_populates='attacktypes')
