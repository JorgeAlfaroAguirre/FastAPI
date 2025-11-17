from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.job_offer import JobType

# Schema para crear una oferta de trabajo
class JobOfferCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Título de la oferta")
    company: str = Field(..., min_length=1, max_length=200, description="Nombre de la empresa")
    location: str = Field(..., min_length=1, max_length=200, description="Ubicación del trabajo")
    job_type: JobType = Field(..., description="Tipo de trabajo")
    description: str = Field(..., min_length=10, description="Descripción detallada del trabajo")
    salary_range: Optional[str] = Field(None, max_length=100, description="Rango salarial")
    requirements: Optional[str] = Field(None, description="Requisitos del trabajo")

# Schema para actualizar una oferta de trabajo
class JobOfferUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    company: Optional[str] = Field(None, min_length=1, max_length=200)
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    job_type: Optional[JobType] = None
    description: Optional[str] = Field(None, min_length=10)
    salary_range: Optional[str] = Field(None, max_length=100)
    requirements: Optional[str] = None
    is_active: Optional[int] = Field(None, ge=0, le=1)

# Schema de respuesta
class JobOfferResponse(BaseModel):
    id: int
    title: str
    company: str
    location: str
    job_type: JobType
    description: str
    salary_range: Optional[str]
    requirements: Optional[str]
    created_by: int
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema de respuesta con información de aplicaciones
class JobOfferWithApplications(JobOfferResponse):
    applications_count: int = 0
