from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraper.settings import Config

_session = None


def get_session():
    global _session
    if _session is not None:
        return _session

    uri = '{}://{}:{}@{}/{}'.format(Config.RDBMS, Config.DB_USER,
                                    Config.DB_PASS, Config.DB_HOST,
                                    Config.DB_NAME)
    engine = create_engine(uri)
    Session = sessionmaker(bind=engine)
    _session = Session()
    return _session
