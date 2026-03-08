import logging
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from capstone.backend.config import settings
from capstone.backend.database.models import DATABASE_MODEL

logger = logging.getLogger(__name__)

# Create Engine
engine = create_engine(
    settings.sqlalchemy_database_url,
    connect_args={"check_same_thread": False} if settings.sqlalchemy_database_url.startswith("sqlite") else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create tables if they don't exist."""
    try:
        DATABASE_MODEL.metadata.create_all(bind=engine)
        logger.info("Database tables initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def get_db() -> Generator[Session, None, None]:
    """Dependency for FastAPI to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Keep DBConnection for backward compatibility if needed, but refactored to use settings
class DBConnection:
    def __init__(self):
        self.engine = engine
        self.session = SessionLocal()
        init_db()

    def query(self, table, limit=None, offset=None, filters=None, order_by=None):
        try:
            query = self.session.query(table)
            if filters:
                query = query.filter(*filters)
            if order_by:
                query = query.order_by(*order_by)
            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)
            return query.all()
        except Exception as e:
            logger.error(f"Query error: {e}")
            return []

    def insert(self, table, **kwargs):
        try:
            # We use a new session for insert to ensure it's closed correctly if using this wrapper
            with SessionLocal() as session:
                obj = table(**kwargs)
                session.add(obj)
                session.commit()
                logger.debug(f"Insert Success: {kwargs}")
        except Exception as e:
            logger.error(f"Insert error: {e}")
            raise

    def delete(self, table, **kwargs):
        try:
            with SessionLocal() as session:
                session.query(table).filter_by(**kwargs).delete()
                session.commit()
                logger.debug(f"Delete Success: {kwargs}")
        except Exception as e:
            logger.error(f"Delete error: {e}")
            raise