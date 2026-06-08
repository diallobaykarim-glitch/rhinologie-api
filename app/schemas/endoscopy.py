from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EndoscopyExamBase(BaseModel):
    side: str = Field(pattern="^(left|right|bilateral)$")
    findings: str = Field(min_length=1)
    polyp_grade: int | None = Field(default=None, ge=0, le=4)
    septum_deviation: str | None = Field(default=None, max_length=120)
    conclusion: str | None = None


class EndoscopyExamCreate(EndoscopyExamBase):
    patient_id: int


class EndoscopyExamRead(EndoscopyExamBase):
    id: int
    patient_id: int
    performed_at: datetime

    model_config = ConfigDict(from_attributes=True)
