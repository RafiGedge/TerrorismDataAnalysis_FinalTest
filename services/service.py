# import math
#
# from sqlalchemy import desc, func
#
# from database import session_maker, Event, Attacktype, Region, Gname
# from test import get_center_point
#
#
# def get_deadliest_attack_types(limit_five: bool = False):
#     with session_maker() as session:
#         result = session.query(
#             Attacktype.name, func.sum(Event.nkill * 2 + Event.nwound).label('total_score')) \
#             .join(Attacktype.events) \
#             .group_by(Attacktype.id) \
#             .order_by(desc('total_score'))
#
#     if limit_five:
#         result = result.limit(5)
#     else:
#         result = result.all()
#
#     [print(i) for i in result]
#
#
# def get_average1(region=None, limit_five: bool = False) -> list[dict]:
#     with session_maker() as session:
#         query = session.query(
#             Region.name, (func.sum(Event.nkill * 2 + Event.nwound) / func.count(Event.id)).label('average_score')) \
#             .join(Region.events)
#         if region:
#             query = query.filter(Region.name == region)
#         result = query.group_by(Region.id) \
#             .order_by(desc('average_score'))
#         if limit_five:
#             result = result.limit(5)
#         else:
#             result = result.all()
#
#     return [{'region': i[0], 'average': round(i[1], 4)} for i in result]
#
#
# def get_deadliest_groups():
#     with session_maker() as session:
#         result = session.query(
#             Gname.name, func.sum(Event.nkill * 2 + Event.nwound).label('total_score')) \
#             .join(Gname.events) \
#             .group_by(Gname.id) \
#             .order_by(desc('total_score')) \
#             .limit(5)
#
#     [print(i) for i in result]
#
#
# def get_average(region=None, limit_five: bool = False) -> list[dict]:
#     with (session_maker() as session):
#         query = session.query(
#             Region.name,
#             (func.sum(Event.nkill * 2 + Event.nwound) / func.count(Event.id)).label('average_score'),
#             func.array_agg(func.json_build_array(Event.latitude, Event.longitude)).filter(
#                 Event.latitude.isnot(None),
#                 Event.longitude.isnot(None)
#             ).label('coordinates')
#         ).join(Region.events)
#
#         if region:
#             query = query.filter(Region.name == region)
#
#         result = query.group_by(Region.id) \
#             .order_by(desc('average_score'))
#
#         if limit_five:
#             result = result.limit(5)
#         else:
#             result = result.all()
#
#     return [{
#         'region': row[0],
#         'average': round(row[1], 4),
#         'coordinates': get_center_point([tuple(coord) for coord in row[2]])
#     } for row in result]
#
# print(get_average())

# print(get_average(limit_five=True))

# with measure_block_time():
#     get_deadliest_attack_types(limit_five=True)
# get_average()

# query = text("""
#     SELECT attacktypes.name, SUM(events.nkill * 2 + events.nwound) AS total_score
#     FROM attacktypes
#     JOIN events ON events.attacktype_id = attacktypes.id
#     GROUP BY attacktypes.id
#     ORDER BY total_score DESC;
#                 """)
# result = session.execute(query).all()

# def measure_query_time(session, stmt):
#     start_time = time.time()  # זמן התחלה
#     result = session.execute(stmt).scalars().all()  # הרצת השאילתה
#     end_time = time.time()  # זמן סיום
#     return result, end_time - start_time

# SELECT attacktype.name, SUM(event.score) AS total_score
# FROM attacktype
# JOIN event ON event.attacktype_id = attacktype.id
# GROUP BY attacktype.id
# ORDER BY total_score DESC;

# [('Bombing/Explosion', 387445.0), ('Armed Assault', 263438.0), ('Assassination', 48821.0), ('Unknown', 37728.0), ('Hijacking', 24028.0), ('Hostage Taking (Kidnapping)', 12786.0), ('Unarmed Assault', 12330.0), ('Facility/Infrastructure Attack', 7772.0), ('Hostage Taking (Barricade Incident)', 5383.0)]
# from sqlalchemy.dialects.postgresql import insert
#
# # JSON של האירועים
# events_json = [
#     {"name": "Event1", "score": 10, "region_name": "USA"},
#     {"name": "Event2", "score": 20, "region_name": "Canada"},
#     {"name": "Event3", "score": 15, "region_name": "USA"}
# ]
#
# # שלב 1: שליפת כל האזורים הקיימים מראש
# region_names = {event["region_name"] for event in events_json}  # כל האזורים מה-JSON
# existing_regions = session.query(Region).filter(Region.name.in_(region_names)).all()
# existing_region_map = {region.name: region.id for region in existing_regions}
#
# # שלב 2: מציאת האזורים החדשים
# new_regions = [{"name": name} for name in region_names if name not in existing_region_map]
#
# # הכנסה מרוכזת של אזורים חדשים אם יש צורך
# if new_regions:
#     stmt = insert(Region).values(new_regions).on_conflict_do_nothing()
#     session.execute(stmt)
#     session.commit()
#
#     # עדכון המפה עם האזורים החדשים שנכנסו
#     updated_regions = session.query(Region).filter(Region.name.in_(region_names)).all()
#     existing_region_map.update({region.name: region.id for region in updated_regions})
#
# # שלב 3: הכנסת האירועים לטבלת Event
# events = [
#     {
#         "name": event["name"],
#         "score": event["score"],
#         "region_id": existing_region_map[event["region_name"]],
#     }
#     for event in events_json
# ]
#
# stmt = insert(Event).values(events)
# session.execute(stmt)
# session.commit()
#
# batch_size = 10000
# for i in range(0, len(events), batch_size):
#     batch = events[i:i + batch_size]
#     session.bulk_insert_mappings(Event, batch)
#     session.commit()

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
