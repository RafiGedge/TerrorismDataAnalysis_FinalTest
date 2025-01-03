from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from settings.postgres_config import DATABASE_URL
from db_connection.models import *

engine = create_engine(f'{DATABASE_URL}/terrorism_data')

if not database_exists(engine.url):
    create_database(engine.url)
    print("Database created")

Base.metadata.create_all(engine)

session_maker = sessionmaker(bind=engine)
