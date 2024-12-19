import math
import pandas as pd
from itertools import islice
from database import session_maker, Country, Region, Attacktype, Targtype, Event
from check_times import measure_block_time

columns = [
    'iyear', 'imonth', 'iday',
    'country', 'country_txt',
    'region', 'region_txt',
    'attacktype1', 'attacktype1_txt',
    'targtype1', 'targtype1_txt',
    'city',
    'latitude', 'longitude',
    'gname', 'nperps',
    'nkill', 'nwound'
]

file_path = 'data_files/globalterrorismdb_0718dist.csv'

df = pd.read_csv(file_path, encoding='latin1', usecols=columns)
df.rename(columns={
    'region': 'region_id', 'country': 'country_id', 'attacktype1': 'attackType_id', 'targtype1': 'targetType_id'},
    inplace=True)


def return_as_dicts(o_id, o_name) -> list[dict[int, str]]:
    result = (df[[o_id, o_name]]
              .drop_duplicates()
              .rename(columns={o_id: 'id', o_name: 'name'})
              .to_dict('records'))
    return result.sort(key=lambda x: x['id'])


def insert_to_db(o_list, model):
    with session_maker() as session:
        for o in o_list:
            session.add(model(**o))
        session.commit()
    return len(o_list)


def insert_foreign_keys():
    insert_to_db(return_as_dicts('country_id', 'country_txt'), Country)
    insert_to_db(return_as_dicts('region_id', 'region_txt'), Region)
    insert_to_db(return_as_dicts('attackType_id', 'attacktype1_txt'), Attacktype)
    insert_to_db(return_as_dicts('targetType_id', 'targtype1_txt'), Targtype)


def before_insert(event: dict):
    if math.isnan(event['nkill']):
        event['nkill'] = 0
    if math.isnan(event['nwound']):
        event['nwound'] = 0
    event['score'] = event['nkill'] * 2 + event['nwound']
    return event


def insert_events():
    row_iterator = df.drop(['country_txt', 'region_txt', 'attacktype1_txt', 'targtype1_txt', 'city'], axis=1).iterrows()
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
    # insert_foreign_keys()
    insert_events()

# for _, row in row_iterator:
#     row_dict = row.to_dict()
#     print(row_dict)
#     break

# unique_values = df['column_name'].unique().tolist()

# unique_values = df[['column1', 'column2']].drop_duplicates().values.tolist()
