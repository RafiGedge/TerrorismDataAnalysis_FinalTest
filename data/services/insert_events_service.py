from itertools import islice

from database import session_maker, Event


def insert_events_to_db(row_iterator, before_insert):
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
    print()
