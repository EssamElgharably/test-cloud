from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import Engine
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost:5432/clinic_db")

logger.info(f"Connecting to database at: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, echo=True)  # echo=True will log all SQL statements
    # Test the connection
    with engine.connect() as conn:
        logger.info("Successfully connected to the database")
except Exception as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    raise

# Use scoped_session for thread safety (good for Flask apps)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    logger.debug(f"Executing SQL: {statement}")

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
