from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "postgresql://aleksandr@localhost:5432/apitest"

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass

#функция для обращение к сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()