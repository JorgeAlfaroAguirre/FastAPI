from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import NVARCHAR, TEXT, DateTime, Enum as SQLEnum
import enum

class JobType(str, enum.Enum):
    """Tipos de trabajo disponibles"""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    REPLACEMENT = "replacement"
    URGENT = "urgent"

class JobOffer(SQLModel, table=True):
    """
    Modelo de oferta de trabajo.
    Una empresa publica ofertas de trabajo y los usuarios pueden postular.
    """
    __tablename__ = "job_offer"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(NVARCHAR(200), nullable=False))
    company: str = Field(sa_column=Column(NVARCHAR(200), nullable=False))
    location: str = Field(sa_column=Column(NVARCHAR(200), nullable=False))
    job_type: JobType = Field(sa_column=Column(SQLEnum(JobType), nullable=False))
    description: str = Field(sa_column=Column(TEXT, nullable=False))

    # Información adicional
    salary_range: Optional[str] = Field(default=None, sa_column=Column(NVARCHAR(100), nullable=True))
    requirements: Optional[str] = Field(default=None, sa_column=Column(TEXT, nullable=True))

    # Usuario que creó la oferta (puede ser un reclutador o admin)
    created_by: int = Field(foreign_key="app_user.id", nullable=False)

    # Estado de la oferta
    is_active: int = Field(default=1, nullable=False)
    created_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime, nullable=False))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime, nullable=False))
