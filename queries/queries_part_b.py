from sqlalchemy import func, desc
from db_connection import session_maker, Event, Gname, Region, Targtype, Country


# Question 15
def get_favourites_target_types_per_group(group_name=None):
    with session_maker() as session:
        query = session.query(
            Gname.name.label('group_name'),
            Targtype.name.label('target_type'),
            func.count(Event.id).label('attack_count')) \
            .join(Event, Event.gname_id == Gname.id) \
            .join(Targtype, Event.targettype_id == Targtype.id) \
            .filter(Gname.name != 'Unknown')

        if group_name:
            query = query.filter(Gname.name == group_name)

        results = query \
            .group_by(Gname.name, Targtype.name) \
            .order_by(Gname.name, desc('attack_count')).all()

    group_targets = {}
    for result in results:

        if result.group_name not in group_targets:
            group_targets[result.group_name] = {}
        group_targets[result.group_name][result.target_type] = result.attack_count

    print(group_targets)


# Question 16 map
def get_unique_groups_by_area(model: str):
    if model == 'Country':
        model = Country
    else:
        model = Region

    with session_maker() as session:
        query = session.query(
            model.name, func.count(func.distinct(Gname.id)).label('unique_groups'), model.latitude, model.longitude) \
            .join(model.events).join(Event.gnames) \
            .group_by(model.id, model.latitude, model.longitude) \
            .order_by(desc('unique_groups')).all()

    return [{
        'region': i[0],
        'num_groups': i[1],
        'location': (i[2], i[3])
    } for i in query if i[2] is not None and i[3] is not None]
