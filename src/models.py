from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.databases.database import Base

#таблица с заявками
class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)

    FIO: Mapped[str] = mapped_column(String(255), nullable=False)

    number: Mapped[str] = mapped_column(String(50),nullable=False)

    email: Mapped[str] = mapped_column(String(255),nullable=False)

    info: Mapped[str] = mapped_column(Text,nullable=False)

    status_info: Mapped[int]=mapped_column(Integer,default=0)

    status:Mapped[str]=mapped_column(String(400),default='Заявка создана,Ожидание диагностки')


#таблица авторизация
class AccessCode(Base):
    __tablename__ = 'access_codes'
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)

    FIO: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    code_hash: Mapped[str] = mapped_column(String(255),nullable=False,unique=True)

    role: Mapped[str] = mapped_column(String(50),nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True,nullable=False)

