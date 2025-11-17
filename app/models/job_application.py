from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, TEXT, NVARCHAR, Enum as SQLEnum
import enum

class ApplicationStatus(str, enum.Enum):
    """Estados del proceso de contratación"""
    PENDING = "pending"  # Postulación recibida, sin revisar
    UNDER_REVIEW = "under_review"  # En revisión por el reclutador
    INTERVIEW_SCHEDULED = "interview_scheduled"  # Entrevista programada
    INTERVIEWED = "interviewed"  # Entrevista realizada
    OFFERED = "offered"  # Oferta de trabajo enviada
    HIRED = "hired"  # Contratado
    REJECTED = "rejected"  # Rechazado

class JobApplication(SQLModel, table=True):
    """
    Modelo de postulación a oferta de trabajo.
    Relaciona un usuario con una oferta de trabajo.
    """
    __tablename__ = "job_application"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relación con oferta de trabajo
    job_offer_id: int = Field(foreign_key="job_offer.id", nullable=False)

    # Relación con usuario que postula
    user_id: int = Field(foreign_key="app_user.id", nullable=False)

    # Mensaje de presentación opcional
    cover_letter: Optional[str] = Field(default=None, sa_column=Column(TEXT, nullable=True))

    # Estado de la postulación (flujo completo de contratación)
    status: ApplicationStatus = Field(
        default=ApplicationStatus.PENDING,
        sa_column=Column(SQLEnum(ApplicationStatus), nullable=False)
    )

    # Notas del reclutador
    recruiter_notes: Optional[str] = Field(default=None, sa_column=Column(TEXT, nullable=True))

    # Timestamps
    applied_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime, nullable=False))
