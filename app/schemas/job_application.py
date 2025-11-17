from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.job_application import ApplicationStatus

# Schema para crear una postulación
class JobApplicationCreate(BaseModel):
    job_offer_id: int = Field(..., gt=0, description="ID de la oferta de trabajo")
    cover_letter: Optional[str] = Field(None, description="Carta de presentación")

# Schema para actualizar estado de postulación (solo reclutador)
class JobApplicationUpdateStatus(BaseModel):
    status: ApplicationStatus = Field(..., description="Estado de la postulación")
    recruiter_notes: Optional[str] = Field(None, description="Notas del reclutador")

# Schema de respuesta básico
class JobApplicationResponse(BaseModel):
    id: int
    job_offer_id: int
    user_id: int
    cover_letter: Optional[str]
    status: ApplicationStatus
    recruiter_notes: Optional[str]
    applied_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True

# Schema de respuesta con información del usuario
class JobApplicationWithUser(JobApplicationResponse):
    user_name: str
    user_email: str
    user_cv_summary: Optional[str] = None

# Schema de respuesta con información de la oferta
class JobApplicationWithOffer(JobApplicationResponse):
    job_title: str
    company: str
    location: str
