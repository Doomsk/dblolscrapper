from sqlalchemy import (Column, BigInteger, Integer, Text, Boolean, DateTime,
                        ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BaseORM(Base):
    __abstract__ = True

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


class Champion(BaseORM):
    __tablename__ = 'champion'

    id = Column(BigInteger, primary_key=True)
    name = Column(Text)

    matches = relationship('PlayerMatchMap', back_populates='champion')


class Player(BaseORM):
    __tablename__ = 'player'

    id = Column(BigInteger, primary_key=True)
    username = Column(Text)
    main = Column(Boolean)

    matches = relationship('PlayerMatchMap', back_populates='player')


class Match(BaseORM):
    __tablename__ = 'match'

    id = Column(BigInteger, primary_key=True)
    version = Column(Text)
    creation = Column(DateTime)
    duration = Column(Integer)
    type = Column(Text)
    queue_type = Column(Text)

    players = relationship('PlayerMatchMap', back_populates='match')


class PlayerMatchMap(BaseORM):
    __tablename__ = 'player_match_map'

    player_id = Column(BigInteger, ForeignKey('player.id'), primary_key=True)
    match_id = Column(BigInteger, ForeignKey('match.id'), primary_key=True)
    champion_id = Column(Integer, ForeignKey('champion.id'))
    lane = Column(Text)
    role = Column(Text)
    queue = Column(Text)
    season = Column(Text)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    has_won = Column(Boolean)

    match = relationship('Match', back_populates='players')
    player = relationship('Player', back_populates='matches')
    champion = relationship('Champion', back_populates='matches')
