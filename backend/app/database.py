from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from app.config import get_settings

settings = get_settings()

database_url = URL.create(
    drivername="mysql+pymysql",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=2,
    pool_recycle=1800,
)


def check_database_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))