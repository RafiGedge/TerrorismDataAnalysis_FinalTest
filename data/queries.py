from sqlalchemy import desc, func
from data.service.service import get_centroid
from database import session_maker, Event, Attacktype, Region, Gname


def get_deadliest_attack_types(limit_five: bool = False):
    with session_maker() as session:
        result = session.query(
            Attacktype.name, func.sum(Event.nkill * 2 + Event.nwound).label('total_score')) \
            .join(Attacktype.events) \
            .group_by(Attacktype.id) \
            .order_by(desc('total_score'))

    if limit_five:
        result = result.limit(5)
    else:
        result = result.all()

    [print(i) for i in result]


def get_average(region=None, limit_five: bool = False) -> list[dict]:
    with session_maker() as session:
        query = session.query(
            Region.name, func.avg(Event.nkill * 2 + Event.nwound).label('average_score'),
            func.array_agg(func.json_build_array(Event.latitude, Event.longitude)).
            filter(Event.latitude.isnot(None), Event.longitude.isnot(None))
        ).join(Region.events)

        if region:
            query = query.filter(Region.name == region)

        result = query.group_by(Region.id) \
            .order_by(desc('average_score'))

        if limit_five is True:
            result = result.limit(5)

        result = result.all()

    return [{
        'region': i[0],
        'average': round(i[1], 4),
        'location': get_centroid(i[2])
    } for i in result]


def get_deadliest_groups():
    with session_maker() as session:
        result = session.query(
            Gname.name, func.sum(Event.nkill * 2 + Event.nwound).label('total_score')) \
            .join(Gname.events) \
            .group_by(Gname.id) \
            .order_by(desc('total_score')) \
            .limit(5)

    [print(i) for i in result]
