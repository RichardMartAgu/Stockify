from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.config import settings
from app.utils.logger import logger

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

try:
    with engine.connect() as connection:
        logger.info("Successful connection to the database!")
except Exception as e:
    logger.error(f"Error connecting to the database: {e}")


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
