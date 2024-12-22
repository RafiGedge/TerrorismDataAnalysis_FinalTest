from database import session_maker, Region


def get_regions():
    with session_maker() as session:
        result = session.query(Region.name).all()
    return [i[0] for i in result]
