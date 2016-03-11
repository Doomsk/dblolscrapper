from sqlalchemy import Column, BigInteger, Integer, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseORM(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @classmethod
    def get_or_create(cls, session, query, **kwargs):
        # Auto assign query parameters when creating/updating
        kwargs.update(query)

        obj = session.query(cls).filter_by(**query).first()
        if obj is not None:
            for key, value in kwargs.iteritems():
                setattr(obj, key, value)
            return obj
        obj = cls(**kwargs)
        session.add(obj)
        return obj


class Player(Base, BaseORM):
    __tablename__ = 'player'

    id = Column(BigInteger, primary_key=True)
    username = Column(Text)
    main = Column(Boolean)


class Match(Base, BaseORM):
    __tablename__ = 'match'

    id = Column(BigInteger, primary_key=True)
    version = Column(Text)
    start = Column(DateTime)
    type = Column(Text)
    queue_type = Column(Text)


class PlayerMatch(Base, BaseORM):
    __tablename__ = 'player_match'

    player_id = Column(BigInteger, primary_key=True)
    match_id = Column(BigInteger, primary_key=True)
    champion_id = Column(Integer)
    lane = Column(Text)
    role = Column(Text)
    queue = Column(Text)
    season = Column(Text)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
