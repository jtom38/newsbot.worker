from fastapi import APIRouter
from newsbotWorkerApiInfra.models import HealthModel
from newsbotWorkerApiService.api import HealthService


router = APIRouter(
    prefix='/health'
    ,tags=['health']
    
)

@router.get('/get')
def getHealth() -> HealthModel:
    hs = HealthService()
    return hs.health
