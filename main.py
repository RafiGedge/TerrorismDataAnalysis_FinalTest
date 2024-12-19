import math
import pandas as pd
from sqlalchemy import event

from check_times import measure_block_time
from database import session_maker, Country, Region, Attacktype, Targtype, Event

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

    result.sort(key=lambda x: x['id'])
    return result


def insert_to_db(o_list, model):
    with session_maker() as session:
        for o in o_list:
            session.add(model(**o))
        session.commit()
    return len(o_list)


@event.listens_for(Event, 'before_insert')
def receive_before_insert(mapper, connection, target):
    if math.isnan(target.nkill):
        target.nkill = 0
    if math.isnan(target.nwound):
        target.nwound = 0
    target.score = target.nkill * 2 + target.nwound


def insert_foreign_keys():
    regions = return_as_dicts('region_id', 'region_txt')
    counties = return_as_dicts('country_id', 'country_txt')
    attacktypes = return_as_dicts('attackType_id', 'attacktype1_txt')
    targtypes = return_as_dicts('targetType_id', 'targtype1_txt')

    print(f'{insert_to_db(counties, Country)} records, countries.')
    print(f'{insert_to_db(regions, Region)} records, regions.')
    print(f'{insert_to_db(attacktypes, Attacktype)} records, attacktypes.')
    print(f'{insert_to_db(targtypes, Targtype)} records, targtypes.')


def insert_events():
    row_iterator = df.drop(['country_txt', 'region_txt', 'attacktype1_txt', 'targtype1_txt', 'city'], axis=1).iterrows()
    count = 0
    while True:
        with session_maker() as session:
            try:
                for i in range(1000):
                    _, row = next(row_iterator)
                    row_dict = row.to_dict()
                    session.add(Event(**row_dict))
                    count += 1
                session.commit()
                print(f'\rInserted records: {count}', end='')
            except StopIteration:
                session.commit()
                print(f'\rInserted records: {count}', end='')
                break
    return

# with measure_block_time():
# insert_foreign_keys()
# insert_events()



# for _, row in row_iterator:
#     row_dict = row.to_dict()
#     print(row_dict)
#     break

# unique_values = df['column_name'].unique().tolist()

# unique_values = df[['column1', 'column2']].drop_duplicates().values.tolist()
