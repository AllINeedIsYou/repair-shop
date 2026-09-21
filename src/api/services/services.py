from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
import secrets
import hashlib
import string
from src.databases.database import get_db, Base, engine
from src.models import Application,AccessCode
from src.shemas import ApplicationShema, AccessCodeCreateSchema, AccessCodeCreateSchema, AccessCodeResponseSchema


router_services = APIRouter(prefix='/services', tags=["Сервер"])

#ФУНКЦИЯ ХЕШИРОВАНИЯ
def hash_code(code: str) -> str:
    return hashlib.sha256(code.encode('utf-8')).hexdigest()

# ЧИСТАЯ ФУНКЦИЯ ДЛЯ БД
def get_all_applications(db: Session):
    return db.query(Application).all()

# ЭНДПОИНТ ДЛЯ СЕРВЕРА
@router_services.get("/", response_model=list[ApplicationShema], summary="Список заявок")
def get_application_endpoint(db: Session = Depends(get_db)):
    return get_all_applications(db)

# СОЗДАНИЕ ФАЙЛА С БД
@router_services.post('/database_create', summary='Создание базы данных')
def create_bd():
    Base.metadata.create_all(bind=engine)
    return {"status": "database created"}

# ГЕНЕРИРУЕМ КОД
def generate_access_code(length: int = 12):
    alphabet = string.ascii_uppercase + string.digits

    return ''.join(
        secrets.choice(alphabet)
        for _ in range(length)
    )


def create_unique_access_code(db: Session, role: str) -> tuple[AccessCode, str]:

    while True:
        new_code = generate_access_code()
        hashed = hash_code(new_code)

        # Проверка на дубликат
        existing = db.query(AccessCode).filter(AccessCode.code_hash == hashed).first()
        if not existing:
            break

    db_access_code = AccessCode(
        code_hash=hashed,
        role=role,
        is_active=True
    )
#мы сохраняем в бд хэш, не сам код, но код отдаем в return,
# чтобы вывести его в эндпоинте ниже, чтобы пользователь мох сохранить его и передать работнику
    db.add(db_access_code)
    db.commit()
    db.refresh(db_access_code)

    return db_access_code,new_code



@router_services.post("/access-codes",response_model=AccessCodeResponseSchema,summary="Сгенерировать и сохранить новый код доступа")
def generate_code_endpoint(data: AccessCodeCreateSchema,db: Session = Depends(get_db)):
    allowed_roles = ["operator", "engineer", "repairer"]
    if data.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимая роль. Допустимые роли: {','.join(allowed_roles)}"
        )

    db_entry, raw_code = create_unique_access_code(db=db, role=data.role)

    return AccessCodeResponseSchema(
        id=db_entry.id,
        code=raw_code,
        role=db_entry.role,
        is_active=db_entry.is_active
    )
