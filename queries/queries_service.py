from sqlalchemy import func
from services.calculate_location import get_centroid
from database import session_maker, Region, Event


def get_regions():
    with session_maker() as session:
        result = session.query(Region.name).all()
    return [i[0] for i in result]


def get_average_by_area(model):
    with session_maker() as session:
        query = session.query(
            model.id, func.array_agg(func.json_build_array(Event.latitude, Event.longitude)).
            filter(Event.latitude.isnot(None), Event.longitude.isnot(None))) \
            .join(model.events) \
            .group_by(model.id).all()
    return {i[0]: get_centroid(i[1]) for i in query}
