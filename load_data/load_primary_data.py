import pandas as pd
import numpy as np
from datetime import date
from pathlib import Path
from load_data.services.insert_events_service import insert_events_to_db
from load_data.services.load_csv_service import load_csv
from db_connection import Country, Region, Attacktype, Targtype, Gname, City, session_maker
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


def insert_foreign_keys():
    data_to_insert = [
        (['country_id', 'country_txt'], Country),
        (['region_id', 'region_txt'], Region),
        (['attacktype_id', 'attacktype1_txt'], Attacktype),
        (['targettype_id', 'targtype1_txt'], Targtype),
        (['gname'], Gname),
        (['city'], City)
    ]
    for columns, model in data_to_insert:
        converted_data = convert_to_instances(columns, model)
        with session_maker() as session:
            session.add_all(converted_data)
            session.commit()
        print(f'records inserted: {len(converted_data)} at table: {model.__tablename__}')


def get_foreignkeys():
    global gnames_foreignkeys, cities_foreignkeys
    with session_maker() as session:
        gnames_query = session.query(Gname).all()
        cities_query = session.query(City).all()
    gnames_foreignkeys = {o.name: o.id for o in gnames_query}
    cities_foreignkeys = {o.name: o.id for o in cities_query}


def formating_date(row):
    month, day = row['imonth'], row['iday']
    if 0 in (month, day):
        return {'date': date(row['iyear'], 1, 1), 'is_year_only': True}
    return {'date': date(row['iyear'], month, day), 'is_year_only': False}


def preparing_events():
    global df
    results = df.apply(formating_date, axis=1)
    df['date'] = results.map(lambda x: x['date'])
    df['is_year_only'] = results.map(lambda x: x['is_year_only'])
    get_foreignkeys()
    df['city_id'] = df['city'].map(cities_foreignkeys)
    df['gname_id'] = df['gname'].map(gnames_foreignkeys)
    df['score'] = np.where(df['nkill'].isna() | df['nwound'].isna(), None, df['nkill'] * 2 + df['nwound'])
    df = df[['date', 'is_year_only', 'region_id', 'country_id', 'city_id', 'latitude', 'longitude', 'attacktype_id',
             'targettype_id', 'gname_id', 'nperps', 'nkill', 'nwound', 'score']]


def insert_events():
    preparing_events()
    insert_events_to_db(df)


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


if __name__ == '__main__':
    load_data()
