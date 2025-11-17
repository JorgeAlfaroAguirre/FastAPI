from typing import Optional
from pydantic import BaseModel, Field

# Schema para actualizar CV
class CVUpdate(BaseModel):
    cv_full_name: Optional[str] = Field(None, max_length=200, description="Nombre completo")
    cv_phone: Optional[str] = Field(None, max_length=50, description="Teléfono")
    cv_summary: Optional[str] = Field(None, description="Resumen profesional")
    cv_experience: Optional[str] = Field(None, description="Experiencia laboral (JSON string)")
    cv_education: Optional[str] = Field(None, description="Educación (JSON string)")
    cv_skills: Optional[str] = Field(None, max_length=500, description="Habilidades separadas por comas")

# Schema de respuesta de CV
class CVResponse(BaseModel):
    cv_full_name: Optional[str]
    cv_phone: Optional[str]
    cv_summary: Optional[str]
    cv_experience: Optional[str]
    cv_education: Optional[str]
    cv_skills: Optional[str]

    class Config:
        from_attributes = True
