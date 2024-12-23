from sqlalchemy import func
from check_times import measure_block_time
from data.service.service import get_centroid
from database import session_maker, Region, Event, Country, City


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


def insert_coordinates(model):
    with session_maker() as session:
        for key, value in get_average_by_area(model).items():
            session.query(model).filter(model.id == key).update(
                {model.latitude: value[0], model.longitude: value[1]}, synchronize_session=False
            )
        session.commit()

# with measure_block_time():
#     insert_coordinates(Region)
# insert_coordinates(Country)
# insert_coordinates(City)
