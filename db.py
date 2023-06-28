import functools
from contextlib import contextmanager
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

engine = create_engine(
    "sqlite:///test.db",
    connect_args={"check_same_thread": False},
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


def get_db() -> Session:
    return SessionLocal()


def init_db():
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    session = get_db()
    try:
        yield session
    except SQLAlchemyError:
        session.rollback()
        raise
    finally:
        session.close()


def db_access(util: Callable):
    @functools.wraps(util)
    def inject_db(*args, **kwrags):
        with session_scope() as db:
            return util(*args, db=db, **kwrags)

    return inject_db
