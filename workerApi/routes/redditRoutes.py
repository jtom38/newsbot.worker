from fastapi import APIRouter


router = APIRouter(prefix='/reddit', tags=['Reddit'])


@router.get('/get/errors')
def getErrors() -> None:
    return None
