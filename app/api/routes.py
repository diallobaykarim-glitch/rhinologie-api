from fastapi import APIRouter

from app.api import consultations, endoscopy, patients, statistics

api_router = APIRouter()
api_router.include_router(patients.router)
api_router.include_router(consultations.router)
api_router.include_router(endoscopy.router)
api_router.include_router(statistics.router)
