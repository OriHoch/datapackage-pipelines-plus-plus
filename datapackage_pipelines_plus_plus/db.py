from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os


def get_engine(connection_string=None):
    if not connection_string:
        connection_string = os.environ.get("DPP_DB_ENGINE", "sqlite:///.data.db")
    return create_engine(connection_string)

def get_session(engine=None, connection_string=None):
    if not engine:
        engine = get_engine(connection_string)
    return sessionmaker(bind=engine)()
