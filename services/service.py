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

from sqlalchemy.dialects.postgresql import insert


countries = ["USA", "Canada", "France"]


stmt = insert(Country).values([{"name": country} for country in countries]) \
    .on_conflict_do_nothing()

with session_maker() as session:
    session.execute(stmt)
    session.commit()
