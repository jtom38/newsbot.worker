from fastapi import APIRouter
from workerInfra.models import HealthModel
from workerService.api import HealthService


router = APIRouter(
    prefix='/health'
    ,tags=['health']
    
)

@router.get('/get')
def getHealth() -> HealthModel:
    hs = HealthService()
    return hs.health
