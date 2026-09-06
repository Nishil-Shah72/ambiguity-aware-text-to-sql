from sqlalchemy import create_engine, text
from app.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    result = connection.execute(text("SELECT DATABASE();"))
    print("Connected to:", result.fetchone()[0])