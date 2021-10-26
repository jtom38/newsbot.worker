from fastapi import APIRouter
from newsbotWorker.infra.models import HealthModel
from newsbotWorker.service.api import HealthService

router = APIRouter(
    prefix='/health'
    ,tags=['health']
    
)

@router.get('/get')
def getHealth() -> HealthModel:
    hs = HealthService()
    return hs.health
