from sqlalchemy import desc, func
from database import session_maker, Event, Attacktype, Region, Country


def get_deadliest_attack_types(num: int = None):
    with session_maker() as session:
        result = session.query(
            Attacktype.name, func.sum(Event.score).label('total_score')) \
            .join(Attacktype.events) \
            .group_by(Attacktype.id) \
            .order_by(desc('total_score')) \
            .all()
    if num:
        result = result[:num]
    [print(i) for i in result]


def get_average():
    with (session_maker() as session):
        result = session.query(
            Region.name, (func.sum(Event.score) / func.count(Event.id)).label('average_score')) \
            .join(Region.events) \
            .group_by(Region.id) \
            .order_by(desc('average_score')) \
            .all()

    [print(f'{i[0]}: {i[1]:.4f}') for i in result]















from sqlalchemy.dialects.postgresql import insert

# JSON של האירועים
events_json = [
    {"name": "Event1", "score": 10, "region_name": "USA"},
    {"name": "Event2", "score": 20, "region_name": "Canada"},
    {"name": "Event3", "score": 15, "region_name": "USA"}
]

# שלב 1: שליפת כל האזורים הקיימים מראש
region_names = {event["region_name"] for event in events_json}  # כל האזורים מה-JSON
existing_regions = session.query(Region).filter(Region.name.in_(region_names)).all()
existing_region_map = {region.name: region.id for region in existing_regions}

# שלב 2: מציאת האזורים החדשים
new_regions = [{"name": name} for name in region_names if name not in existing_region_map]

# הכנסה מרוכזת של אזורים חדשים אם יש צורך
if new_regions:
    stmt = insert(Region).values(new_regions).on_conflict_do_nothing()
    session.execute(stmt)
    session.commit()

    # עדכון המפה עם האזורים החדשים שנכנסו
    updated_regions = session.query(Region).filter(Region.name.in_(region_names)).all()
    existing_region_map.update({region.name: region.id for region in updated_regions})

# שלב 3: הכנסת האירועים לטבלת Event
events = [
    {
        "name": event["name"],
        "score": event["score"],
        "region_id": existing_region_map[event["region_name"]],
    }
    for event in events_json
]

stmt = insert(Event).values(events)
session.execute(stmt)
session.commit()

batch_size = 10000
for i in range(0, len(events), batch_size):
    batch = events[i:i + batch_size]
    session.bulk_insert_mappings(Event, batch)
    session.commit()


# get_deadliest_attack_types()
# get_average()

from sqlalchemy import select

# countries = ["USA", "Canada", "France"]  # רשימת המדינות
#
# for country in countries:
#     # בדיקה אם המדינה קיימת
#     exists = session.query(Region).filter_by(name=country).first()
#     if not exists:
#         # הוספה אם המדינה לא קיימת
#         session.add(Region(name=country))
#
# # שמירה למסד הנתונים
# session.commit()

# from sqlalchemy.dialects.postgresql import insert
#
#
# countries = ["USA", "Canada", "France"]
#
#
# stmt = insert(Country).values([{"name": country} for country in countries]) \
#     .on_conflict_do_nothing()
#
# with session_maker() as session:
#     session.execute(stmt)
#     session.commit()
