from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.services.services import get_all_applications
from src.auth.auth import require_role
from src.databases.database import get_db
from src.shemas import ApplicationShema
from src.api.services.services_repairer import repair_info

router_repair=APIRouter(prefix='/repairer',tags=["Мастер по ремонту"])

# @router_repair.get("/dashboard", dependencies=[Depends(require_role("repairer"))], summary='Вход')
# def get_engineer_dashboard():
#     return {"message": "Добро пожаловать в панель управления Мастера по ремонту! Желаем вам приятной смены<3"}

#получаем список заявок
@router_repair.get("/",response_model=list[ApplicationShema],dependencies=[Depends(require_role("repairer"))],summary="Список заявок")
def get_application_repairer(db: Session = Depends(get_db)):
    return get_all_applications(db=db)

@router_repair.post('/{application_id}/repair', dependencies=[Depends(require_role("repairer"))], response_model=ApplicationShema, summary='Отметка о готовности ремонта')
def status_repair(application_id: int, db: Session = Depends(get_db)):
    return repair_info(application_id=application_id, db=db)


