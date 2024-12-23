from datetime import datetime
from itertools import islice

import pandas as pd
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

from database import Country, session_maker, Attacktype, Gname, City, Targtype, Event

# from main import get_coordinates

file_path = 'files/RAND_Database_of_Worldwide_Terrorism_Incidents - 5000 rows.csv'

df: pd.DataFrame = pd.DataFrame()
countries_foreignkeys: dict = dict()
cities_foreignkeys: dict = dict()
attacktypes_foreignkeys: dict = dict()
gnames_foreignkeys: dict = dict()


def load_csv():
    global df
    columns = ['Date', 'City', 'Country', 'Perpetrator', 'Weapon', 'Injuries', 'Fatalities']
    df = pd.read_csv(file_path, encoding='latin1', usecols=columns)
    df.rename(columns={'Date': 'date', 'Fatalities': 'nkill', 'Injuries': 'nwound'}, inplace=True)


def insert_keys_to_db(unique_list: list, model):
    with session_maker() as session:
        before_count = session.query(func.count(model.id)).scalar()
        for i in range(4):
            session.execute(insert(model).values([{'name': i} for i in unique_list]).on_conflict_do_nothing())
            session.commit()
        after_count = session.query(func.count(model.id)).scalar()
    records_inserted = after_count - before_count
    print(f'records inserted: {records_inserted} at table: {model.__tablename__}')


def complete_foreignkeys():
    insert_keys_to_db(df['Country'].unique().tolist(), Country)
    insert_keys_to_db(df['City'].unique().tolist(), City)
    insert_keys_to_db(df['Weapon'].unique().tolist(), Attacktype)
    insert_keys_to_db(df['Perpetrator'].unique().tolist(), Gname)


def convert_date(date_string: str) -> datetime:
    date_object = datetime.strptime(date_string, "%d-%b-%y")
    if date_object.year > 2024:
        date_object = date_object.replace(year=date_object.year - 100)
    return date_object


def get_foreignkeys():
    global countries_foreignkeys, cities_foreignkeys, attacktypes_foreignkeys, gnames_foreignkeys
    with session_maker() as session:
        countries_query = session.query(Country).all()
        cities_query = session.query(City).all()
        attacktypes_query = session.query(Attacktype).all()
        gnames_query = session.query(Gname).all()
        countries_foreignkeys = {o.name: o.id for o in countries_query}
        cities_foreignkeys = {o.name: o.id for o in cities_query}
        attacktypes_foreignkeys = {o.name: o.id for o in attacktypes_query}
        gnames_foreignkeys = {o.name: o.id for o in gnames_query}


def before_insert(event: dict) -> dict:
    event['date'] = convert_date(event['date'])
    event['county_id'] = countries_foreignkeys[event['Country']]
    try:
        event['city_id'] = cities_foreignkeys[event['City']]
    except KeyError:
        event['city_id'] = 3
    event['attacktype_id'] = attacktypes_foreignkeys[event['Weapon']]
    event['gname_id'] = gnames_foreignkeys[event['Perpetrator']]
    del event['Country'], event['City'], event['Weapon'], event['Perpetrator']
    return event


def insert_events():
    get_foreignkeys()
    row_iterator = df.iterrows()
    count = 0
    while True:
        chunk = list(islice((before_insert(row.to_dict()) for _, row in row_iterator), 1000))
        count += len(chunk)
        if not chunk:
            break
        with session_maker() as session:
            session.bulk_insert_mappings(Event, chunk)
            session.commit()
            print(f'\rInserted records: {count}', end='')


# load_csv()
# # complete_foreignkeys()
# # unique_cities = df['City'].unique().tolist()
# result = []
# for city in unique_cities:
#     answer = get_coordinates(city)
#     result.append(answer)
# print(result)
# print(len(result))
# print(result.count(None))
load_csv()
complete_foreignkeys()
# insert_events()
# print(df['Weapon'].unique().tolist())
# get_foreignkeys()
# print(attacktypes_foreignkeys)

# insert_events()
