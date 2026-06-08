from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.endoscopy import EndoscopyExam
from app.models.patient import Patient
from app.schemas.endoscopy import EndoscopyExamCreate, EndoscopyExamRead

router = APIRouter(prefix="/endoscopy", tags=["endoscopy"])


@router.post("", response_model=EndoscopyExamRead, status_code=status.HTTP_201_CREATED)
def create_endoscopy_exam(payload: EndoscopyExamCreate, db: Session = Depends(get_db)):
    if not db.get(Patient, payload.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    exam = EndoscopyExam(**payload.model_dump())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


@router.get("", response_model=list[EndoscopyExamRead])
def list_endoscopy_exams(
    db: Session = Depends(get_db),
    patient_id: int | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    statement = select(EndoscopyExam).order_by(EndoscopyExam.performed_at.desc()).limit(limit).offset(offset)
    if patient_id is not None:
        statement = (
            select(EndoscopyExam)
            .where(EndoscopyExam.patient_id == patient_id)
            .order_by(EndoscopyExam.performed_at.desc())
            .limit(limit)
            .offset(offset)
        )
    return db.execute(statement).scalars().all()
