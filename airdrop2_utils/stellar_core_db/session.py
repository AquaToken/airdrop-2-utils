from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def make_session(db_url: str) -> Session:
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)

    return Session.begin()
