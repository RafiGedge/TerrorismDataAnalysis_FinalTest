from sqlalchemy import desc, func
from database import session_maker, Event, Attacktype, Region, Gname
from services.calciualte_coorelation import get_correlation


# Question 1
def get_deadliest_attack_types(limit_five: bool = False):
    with session_maker() as session:
        result = session.query(
            Attacktype.name, func.sum(Event.score).label('total_score')) \
            .join(Attacktype.events) \
            .filter(Event.score.isnot(None), Attacktype.name != 'Unknown') \
            .group_by(Attacktype.id) \
            .order_by(desc('total_score'))

    if limit_five:
        result = result.limit(5)

    [print(i) for i in result]


# Question 2 map
def get_victims_average(region=None, limit_five: bool = False) -> list[dict]:
    with session_maker() as session:
        query = session.query(
            Region.name, func.avg(Event.score).label('average_score'), Region.latitude, Region.longitude) \
            .filter(Event.score.isnot(None), Region.latitude.isnot(None), Region.longitude.isnot(None)) \
            .join(Region.events)

    if region:
        query = query.filter(Region.name == region)

    result = query.group_by(Region.id).order_by(desc('average_score'))

    if limit_five is True:
        result = result.limit(5)

    return [{
        'region': i[0],
        'average': round(i[1], 4),
        'location': (i[2], i[3])
    } for i in result]


# Question 3
def get_deadliest_groups():
    with session_maker() as session:
        result = session.query(
            Gname.name, func.sum(Event.score).label('total_score')) \
            .join(Gname.events) \
            .filter(Event.score.isnot(None), Gname.name != 'Unknown') \
            .group_by(Gname.id) \
            .order_by(desc('total_score')) \
            .limit(5)

    [print(i) for i in result]


# Question 8 map
def get_most_active_groups(region=None):
    with session_maker() as session:
        query = session.query(
            Region.name.label('region_name'), Gname.name.label('group_name'),
            func.count(Event.id).label('event_count'), Region.latitude, Region.longitude) \
            .join(Event, Event.gname_id == Gname.id) \
            .join(Region, Event.region_id == Region.id) \
            .filter(Gname.name != 'Unknown') \
            .group_by('region_name', 'group_name', Region.latitude, Region.longitude) \
            .order_by(Region.name, desc('event_count')) \
            .all()

    if region:
        query = [i for i in query if i.region_name == region]

    result = {}
    for i in query:
        if i.region_name not in result:
            result[i.region_name] = {'groups': {}, 'location': (i.latitude, i.longitude)}
        if len(result[i.region_name]['groups']) < 5:
            result[i.region_name]['groups'][i.group_name] = i.event_count

    return result


# # Question 10 map
def get_correlation_victims_for_events(region=None):
    with session_maker() as session:
        query = session.query(
            Region.name, func.array_agg(Event.score), Region.latitude, Region.longitude) \
            .join(Region.events) \
            .filter(Event.score.isnot(None)) \
            .group_by(Region.id, Region.latitude, Region.longitude)

    if region:
        query = query.filter(Region.name == region)

    result = query.all()
    return [{
        'region': i[0],
        'correlation': round(get_correlation(i[1]), 5),
        'location': (i[2], i[3])}
        for i in result]
