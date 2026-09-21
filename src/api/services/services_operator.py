from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.models import Application

#функция для удаление заявки
def del_elements_aplication_by_id(aplication_id:int,db:Session):
    app_to_del=db.query(Application).filter(Application.id==aplication_id).first()
    if not app_to_del:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заявка с id={aplication_id} не найдена"
        )
    db.delete(app_to_del)
    db.commit()
    return {'status':'success', 'massage': f"Заявка с id={aplication_id} успешно удалена"}