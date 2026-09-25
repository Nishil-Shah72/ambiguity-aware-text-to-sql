from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from app.config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


DATABASE_URL = URL.create(
    drivername="mysql+mysqlconnector",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME
)

engine = create_engine(DATABASE_URL)


with engine.connect() as connection:
    result = connection.execute(text("SELECT DATABASE();"))
    print("Connected to:", result.fetchone()[0])