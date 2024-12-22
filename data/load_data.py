import math
from datetime import date
import numpy as np
import pandas as pd
from itertools import islice
from sqlalchemy import text
from database import session_maker, Country, Region, Attacktype, Targtype, Event, Gname
from check_times import measure_block_time

file_path = 'files/globalterrorismdb_0718dist.csv'

df: pd.DataFrame = pd.DataFrame()
gnames_foreignkeys: dict = dict()


def load_csv():
    global df
    columns = [
        'iyear', 'imonth', 'iday', 'country', 'country_txt', 'region', 'region_txt', 'attacktype1', 'attacktype1_txt',
        'targtype1', 'targtype1_txt', 'latitude', 'longitude', 'gname', 'nperps', 'nkill', 'nwound'
    ]
    df = pd.read_csv(file_path, encoding='latin1', usecols=columns)
    df.rename(columns={
        'region': 'region_id', 'country': 'country_id', 'attacktype1': 'attacktype_id', 'targtype1': 'targettype_id',
        'gname': 'gname_id'}, inplace=True)
    df = df.replace({np.nan: None})


def return_as_dicts(*args) -> list[dict]:
    is_two_params = len(args) == 2
    params = list(args)
    keys = {params[0]: 'name'} if not is_two_params else {params[0]: 'id', params[1]: 'name'}
    result = (df[params]
              .drop_duplicates()
              .rename(columns=keys)
              .to_dict('records'))
    if is_two_params:
        result.sort(key=lambda x: x['id'])
    return result


def insert_to_db(o_list, model):
    with session_maker() as session:
        for o in o_list:
            session.add(model(**o))
        session.commit()
    print(f'records inserted: {len(o_list)} at table: {model.__name__}')


def insert_foreign_keys():
    insert_to_db(return_as_dicts('country_id', 'country_txt'), Country)
    insert_to_db(return_as_dicts('region_id', 'region_txt'), Region)
    insert_to_db(return_as_dicts('attacktype_id', 'attacktype1_txt'), Attacktype)
    insert_to_db(return_as_dicts('targettype_id', 'targtype1_txt'), Targtype)
    insert_to_db(return_as_dicts('gname_id'), Gname)


def before_insert(event: dict):
    try:
        event['date'] = date(event['iyear'], event['imonth'], event['iday'])
    except ValueError:
        event['date'] = date(event['iyear'], 1, 1)
        event['is_year_only'] = True
    del event['iyear'], event['imonth'], event['iday']
    event['gname_id'] = gnames_foreignkeys[event['gname_id']]
    return event


def get_gnames_foreignkeys():
    global gnames_foreignkeys
    query = text("SELECT * FROM gnames")
    with session_maker() as session:
        result = session.execute(query).mappings().all()
    gnames_foreignkeys = {o['name']: o['id'] for o in result}


def insert_events():
    row_iterator = df.drop(['country_txt', 'region_txt', 'attacktype1_txt', 'targtype1_txt'], axis=1).iterrows()
    get_gnames_foreignkeys()
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
    insert_foreign_keys()
    insert_events()
