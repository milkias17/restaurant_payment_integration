import functools
from contextlib import contextmanager
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

engine = create_engine(
    "sqlite:///anony_handler.db",
    connect_args={"check_same_thread": False},
    echo=True,
)

SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)


def get_db() -> Session:
    return SessionLocal()


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
    async def inject_db(*args, **kwrags):
        with session_scope() as db:
            return await util(*args, db=db, **kwrags)

    return inject_db
