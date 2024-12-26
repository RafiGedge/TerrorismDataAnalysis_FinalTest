import pandas as pd
from pathlib import Path
from datetime import date
from data.services.insert_events_service import insert_events_to_db
from data.services.load_csv_service import load_csv
from database import session_maker, Country, Region, Attacktype, Targtype, Gname, City
from queries.queries_service import get_average_by_area

df: pd.DataFrame = pd.DataFrame()
gnames_foreignkeys: dict = dict()
cities_foreignkeys: dict = dict()


def get_csv():
    file_path = Path(__file__).parent / 'files' / 'globalterrorismdb_0718dist.csv'
    columns = [1, 2, 3, 7, 8, 9, 10, 12, 13, 14, 28, 29, 34, 35, 58, 69, 98, 101]
    renames = {'region': 'region_id', 'country': 'country_id', 'attacktype1': 'attacktype_id',
               'targtype1': 'targettype_id'}
    global df
    df = load_csv(file_path, columns, renames)


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
    return result


def insert_keys_to_db(params: list, model):
    converted_data = convert_to_instances(params, model)
    with session_maker() as session:
        session.add_all(converted_data)
        session.commit()
    print(f'records inserted: {len(converted_data)} at table: {model.__tablename__}')


def insert_foreign_keys():
    data_to_insert = [
        (['country_id', 'country_txt'], Country),
        (['region_id', 'region_txt'], Region),
        (['attacktype_id', 'attacktype1_txt'], Attacktype),
        (['targettype_id', 'targtype1_txt'], Targtype),
        (['gname'], Gname),
        (['city'], City)
    ]
    for params, model in data_to_insert:
        insert_keys_to_db(params, model)


def before_insert(event: dict) -> dict:
    month, day = event['imonth'], event['iday']
    if 0 in (month, day):
        month, day = 1, 1
        event['is_year_only'] = True
    event['date'] = date(event['iyear'], month, day)
    event['gname_id'] = gnames_foreignkeys[event['gname']]
    event['city_id'] = cities_foreignkeys[event['city']]
    if None not in (event['nkill'], event['nwound']):
        event['score'] = event['nkill'] * 2 + event['nwound']
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
    insert_events_to_db(row_iterator, before_insert)


def insert_coordinates(model):
    with session_maker() as session:
        for key, value in get_average_by_area(model).items():
            session.query(model).filter(model.id == key).update(
                {model.latitude: value[0], model.longitude: value[1]}, synchronize_session=False
            )
        session.commit()
    print(f'Coordinates updated for {model.__tablename__}')


def load_data():
    get_csv()
    insert_foreign_keys()
    insert_events()
    insert_coordinates(Region)
    insert_coordinates(Country)
