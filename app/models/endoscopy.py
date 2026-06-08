from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class EndoscopyExam(Base):
    __tablename__ = "endoscopy_exams"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id", ondelete="CASCADE"), index=True)
    side: Mapped[str] = mapped_column(String(20))
    findings: Mapped[str] = mapped_column(Text)
    polyp_grade: Mapped[int | None] = mapped_column(Integer, nullable=True)
    septum_deviation: Mapped[str | None] = mapped_column(String(120), nullable=True)
    conclusion: Mapped[str | None] = mapped_column(Text, nullable=True)
    performed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    patient = relationship("Patient", back_populates="endoscopy_exams")
