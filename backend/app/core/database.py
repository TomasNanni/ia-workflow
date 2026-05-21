from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# Primary Engine (SQLite for sessions/auth)
connect_args = {}
if settings.sessions_db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.sessions_db_url,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Secondary Engine (Postgres for read-only analytics)
analytics_engine = None
if settings.analytics_db_url:
    # Fix for potential postgres:// vs postgresql:// issue
    analytics_url = settings.analytics_db_url
    if analytics_url.startswith("postgres://"):
        analytics_url = analytics_url.replace("postgres://", "postgresql://", 1)
    analytics_engine = create_engine(analytics_url)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
