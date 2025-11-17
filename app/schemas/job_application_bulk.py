from typing import List
from pydantic import BaseModel, Field
from app.models.job_application import ApplicationStatus

# Schema para actualizar múltiples postulaciones
class BulkStatusUpdate(BaseModel):
    application_ids: List[int] = Field(..., min_length=1, description="IDs de las postulaciones a actualizar")
    status: ApplicationStatus = Field(..., description="Nuevo estado para todas las postulaciones")
    recruiter_notes: str | None = Field(None, description="Notas del reclutador")

# Schema para actualizar todas las postulaciones de una oferta
class JobOfferBulkUpdate(BaseModel):
    job_offer_id: int = Field(..., gt=0, description="ID de la oferta de trabajo")
    exclude_ids: List[int] = Field(default=[], description="IDs de postulaciones a excluir de la actualización")
    status: ApplicationStatus = Field(..., description="Nuevo estado para las postulaciones")
    recruiter_notes: str | None = Field(None, description="Notas del reclutador")

# Schema de respuesta para operaciones bulk
class BulkUpdateResponse(BaseModel):
    updated_count: int = Field(..., description="Número de postulaciones actualizadas")
    application_ids: List[int] = Field(..., description="IDs de las postulaciones actualizadas")
    status: ApplicationStatus = Field(..., description="Estado aplicado")
