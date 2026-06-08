from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Consultation(Base):
    __tablename__ = "consultations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), index=True)
    reason: Mapped[str] = mapped_column(String(200))
    symptoms: Mapped[str] = mapped_column(Text)
    diagnosis: Mapped[str | None] = mapped_column(String(200), nullable=True)
    treatment_plan: Mapped[str | None] = mapped_column(Text, nullable=True)
    smell_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    nasal_obstruction_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="consultations")
