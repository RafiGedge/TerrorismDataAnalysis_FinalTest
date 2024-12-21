from sqlalchemy import desc, func

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


def get_average():
    with session_maker() as session:
        result = session.query(
            Region.name, (func.sum(Event.nkill * 2 + Event.nwound) / func.count(Event.id)).label('average_score')) \
            .join(Region.events) \
            .group_by(Region.id) \
            .order_by(desc('average_score')) \
            .all()

    [print(f'{i[0]}: {i[1]:.4f}') for i in result]


def get_deadliest_groups():
    with session_maker() as session:
        result = session.query(
            Gname.name, func.sum(Event.nkill * 2 + Event.nwound).label('total_score')) \
            .join(Gname.events) \
            .group_by(Gname.id) \
            .order_by(desc('total_score')) \
            .limit(5)

    [print(i) for i in result]
