from sqlalchemy import Column, Integer, ForeignKey, Float, Date, Boolean, Index
from sqlalchemy.orm import relationship

from database.models.base import Base


class Event(Base):
    __tablename__ = 'events'  # noqa

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=True)
    is_year_only = Column(Boolean, default=False)
    region_id = Column(Integer, ForeignKey('regions.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))
    # city = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    attacktype_id = Column(Integer, ForeignKey('attacktypes.id'))
    targettype_id = Column(Integer, ForeignKey('targtypes.id'))
    gname_id = Column(Integer, ForeignKey('gnames.id'))
    nperps = Column(Float, nullable=True)
    nkill = Column(Float, nullable=True)
    nwound = Column(Float, nullable=True)

    countries = relationship("Country", back_populates="events")
    regions = relationship("Region", back_populates="events")
    attacktypes = relationship("Attacktype", back_populates="events")
    targtypes = relationship("Targtype", back_populates="events")
    gnames = relationship("Gname", back_populates="events")

    # __table_args__ = (Index('iyear', 'iyear'))
