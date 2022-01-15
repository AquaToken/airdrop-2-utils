from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def make_session(db_url: str) -> Session:
    db_url = db_url.replace('postgres://', 'postgresql+psycopg2://')
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)

    return Session.begin()
