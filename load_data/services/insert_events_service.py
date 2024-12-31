from more_itertools import chunked
from db_connection import Event, session_maker


def insert_events_to_db(df):
    df_as_dicts = df.to_dict(orient='records')
    records = [Event(**record) for record in df_as_dicts]
    count = 0
    for chunk in chunked(records, 1000):
        count += len(chunk)
        with session_maker() as session:
            session.add_all(chunk)
            session.commit()
            print(f'\rInserted records: {count}', end='')
    print()
