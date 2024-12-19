from sqlalchemy import Column, Integer, String, ForeignKey, Index, Float
from sqlalchemy.orm import relationship

from database.models.base import Base


class Event(Base):
    __tablename__ = 'events'  # noqa

    id = Column(Integer, primary_key=True)
    iyear = Column(Integer, nullable=True)
    imonth = Column(Integer, nullable=True)
    iday = Column(Integer, nullable=True)
    region_id = Column(Integer, ForeignKey('regions.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))
    # city = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    attackType_id = Column(Integer, ForeignKey('attacktypes.id'))
    targetType_id = Column(Integer, ForeignKey('targtypes.id'))
    gname = Column(String, nullable=True)
    nperps = Column(Float, nullable=True)
    nkill = Column(Float, nullable=True)
    nwound = Column(Float, nullable=True)
    score = Column(Float, nullable=True)

    countries = relationship("Country", back_populates="events")
    regions = relationship("Region", back_populates="events")
    attacktypes = relationship("Attacktype", back_populates="events")
    targtypes = relationship("Targtype", back_populates="events")

    # __table_args__ = (Index('iyear', 'iyear'))
