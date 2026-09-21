from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from src.databases.database import get_db
from src.models import Application

#функция для диагностки(status_info)

def perform_diagnostics(aplication_id:int, db:Session)->Application:
    application=db.query(Application).filter(Application.id==aplication_id).first()
    if not application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Заявка с id={aplication_id} не найдена"
        )

    if application.status_info is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Невозможно выполнить действие: у заявки с id={aplication_id} не задан статус",
        )
    else:
        application.status_info+=1
    application.status='Диагностика завершена, Ожидание выполнения работы...'
    db.commit()
    db.refresh(application)
    return application
