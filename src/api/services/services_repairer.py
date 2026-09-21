from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.models import Application

#функция для работы(status_info)

def repair_info(application_id:int,db:Session):
    repair_id=db.query(Application).filter(Application.id==application_id).first()
    if not repair_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заявка с id={application_id} не найдена"
        )
    if repair_id.status_info is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Невозможно выполнить действие: у заявки с id={application_id} не задан статус",
        )
    elif repair_id.status_info < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Невозможно выполнить ремонт: заявка с id={application_id} не прошла этап диагностики",
        )
    else:
        repair_id.status_info+=1
    repair_id.status='Работы завершина. Ожидание выдачи клиенту'
    db.commit()
    db.refresh(repair_id)
    return repair_id