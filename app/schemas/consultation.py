from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ConsultationBase(BaseModel):
    reason: str = Field(min_length=1, max_length=200)
    symptoms: str = Field(min_length=1)
    diagnosis: str | None = Field(default=None, max_length=200)
    treatment_plan: str | None = None
    smell_score: int | None = Field(default=None, ge=0, le=10)
    nasal_obstruction_score: int | None = Field(default=None, ge=0, le=10)


class ConsultationCreate(ConsultationBase):
    patient_id: int


class ConsultationRead(ConsultationBase):
    id: int
    patient_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
