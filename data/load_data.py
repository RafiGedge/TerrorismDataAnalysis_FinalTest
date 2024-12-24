import numpy as np
import pandas as pd
from datetime import date
from itertools import islice
from database import session_maker, Country, Region, Attacktype, Targtype, Event, Gname, City
from check_times import measure_block_time

file_path = 'files/globalterrorismdb_0718dist.csv'

df: pd.DataFrame = pd.DataFrame()
gnames_foreignkeys: dict = dict()
cities_foreignkeys: dict = dict()


def load_csv():
    global df
    columns = [
        'iyear', 'imonth', 'iday', 'country', 'country_txt', 'city', 'region', 'region_txt', 'attacktype1',
        'attacktype1_txt',
        'targtype1', 'targtype1_txt', 'latitude', 'longitude', 'gname', 'nperps', 'nkill', 'nwound'
    ]
    df = pd.read_csv(file_path, encoding='latin1', usecols=columns)
    df.rename(columns={
        'region': 'region_id', 'country': 'country_id', 'attacktype1': 'attacktype_id', 'targtype1': 'targettype_id'},
        inplace=True)
    df = df.replace({np.nan: None})


def convert_to_instances(params: list, model) -> list[dict]:
    is_two_params = len(params) == 2
    keys = {params[0]: 'name'} if not is_two_params else {params[0]: 'id', params[1]: 'name'}
    result = (df[params]
              .drop_duplicates()
              .rename(columns=keys)
              .to_dict('records'))
    if is_two_params:
        result.sort(key=lambda x: x['id'])
    result = [model(**i) for i in result]
    print(result)
    return result


def insert_keys_to_db(o_list):
    with session_maker() as session:
        session.add_all(o_list)
        session.commit()
    print(f'records inserted: {len(o_list)} at table: {o_list[0].__tablename__}')


def insert_foreign_keys():
    insert_keys_to_db(convert_to_instances(['country_id', 'country_txt'], Country))
    insert_keys_to_db(convert_to_instances(['region_id', 'region_txt'], Region))
    insert_keys_to_db(convert_to_instances(['attacktype_id', 'attacktype1_txt'], Attacktype))
    insert_keys_to_db(convert_to_instances(['targettype_id', 'targtype1_txt'], Targtype))
    insert_keys_to_db(convert_to_instances(['gname'], Gname))
    insert_keys_to_db(convert_to_instances(['city'], City))


def before_insert(event: dict) -> dict:
    try:
        event['date'] = date(event['iyear'], event['imonth'], event['iday'])
    except ValueError:
        event['date'] = date(event['iyear'], 1, 1)
        event['is_year_only'] = True
    del event['iyear'], event['imonth'], event['iday']
    event['gname_id'] = gnames_foreignkeys[event['gname']]
    event['city_id'] = cities_foreignkeys[event['city']]
    if event['nkill'] is None:
        event['nkill'] = -1
    if event['nwound'] is None:
        event['nwound'] = -1
    event['score'] = event['nkill'] * 2 + event['nwound'] if -1 not in (event['nkill'], event['nwound']) else None
    return event


def get_foreignkeys():
    global gnames_foreignkeys, cities_foreignkeys
    with session_maker() as session:
        gnames_query = session.query(Gname).all()
        cities_query = session.query(City).all()
    gnames_foreignkeys = {o.name: o.id for o in gnames_query}
    cities_foreignkeys = {o.name: o.id for o in cities_query}


def insert_events():
    row_iterator = df.drop(['country_txt', 'region_txt', 'attacktype1_txt', 'targtype1_txt'], axis=1).iterrows()
    get_foreignkeys()
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


with measure_block_time():
    load_csv()
    # insert_foreign_keys()
    # insert_events()
    # insert_coordinates(Region)
    # insert_coordinates(Country)
    # insert_coordinates(City)
