from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import date
from app.services.db.sql_server_connection import get_session
from app.services.db.job_offer_service import JobOfferService
from app.schemas.job_offer import (
    JobOfferCreate,
    JobOfferUpdate,
    JobOfferResponse,
    JobOfferWithApplications
)

router = APIRouter(prefix="/job-offers", tags=["Job Offers"])

@router.post("/", response_model=JobOfferResponse, status_code=status.HTTP_201_CREATED)
def create_job_offer(
    job_offer: JobOfferCreate,
    user_id: int = Query(..., description="ID del usuario que crea la oferta"),
    session: Session = Depends(get_session)
):
    """
    Crear una nueva oferta de trabajo.

    - **title**: Título de la oferta
    - **company**: Nombre de la empresa
    - **location**: Ubicación del trabajo
    - **job_type**: Tipo de trabajo (full_time, part_time, replacement, urgent)
    - **description**: Descripción detallada
    - **salary_range**: Rango salarial (opcional)
    - **requirements**: Requisitos (opcional)
    """
    try:
        new_offer = JobOfferService.create_job_offer(session, job_offer, user_id)
        return new_offer
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear oferta de trabajo: {str(e)}"
        )

@router.get("/", response_model=List[JobOfferResponse])
def get_all_job_offers(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros"),
    is_active: Optional[int] = Query(None, ge=0, le=1, description="Filtrar por estado activo"),
    session: Session = Depends(get_session)
):
    """
    Obtener todas las ofertas de trabajo con paginación.

    - **skip**: Número de registros a saltar (por defecto 0)
    - **limit**: Número máximo de registros a devolver (por defecto 100)
    - **is_active**: Filtrar por estado activo (0 o 1)
    """
    try:
        offers = JobOfferService.get_all_job_offers(session, skip, limit, is_active)
        return offers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ofertas: {str(e)}"
        )

@router.get("/search", response_model=List[JobOfferResponse])
def search_job_offers(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """
    Buscar ofertas de trabajo por término.
    Busca en: título, empresa, ubicación y descripción.
    """
    try:
        offers = JobOfferService.search_job_offers(session, q, skip, limit)
        return offers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar ofertas: {str(e)}"
        )

@router.get("/by-date", response_model=List[JobOfferResponse])
def get_job_offers_by_date(
    start_date: Optional[date] = Query(None, description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Fecha de fin (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=100, description="Número máximo de registros"),
    session: Session = Depends(get_session)
):
    """
    Buscar ofertas de trabajo por rango de fechas.

    - **start_date**: Fecha de inicio (YYYY-MM-DD). Ejemplo: 2025-01-01
    - **end_date**: Fecha de fin (YYYY-MM-DD). Ejemplo: 2025-12-31
    - Si no se especifica start_date, se obtienen todas hasta end_date
    - Si no se especifica end_date, se obtienen todas desde start_date
    - Si no se especifica ninguna, se obtienen todas las ofertas activas

    Ejemplos:
    - /job-offers/by-date?start_date=2025-01-01&end_date=2025-01-31  # Ofertas de enero 2025
    - /job-offers/by-date?start_date=2025-01-01  # Ofertas desde enero 2025 hasta hoy
    - /job-offers/by-date?end_date=2025-12-31  # Ofertas hasta diciembre 2025
    """
    try:
        offers = JobOfferService.get_job_offers_by_date_range(
            session, start_date, end_date, skip, limit
        )
        return offers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar ofertas por fecha: {str(e)}"
        )

@router.get("/{job_offer_id}", response_model=JobOfferWithApplications)
def get_job_offer(
    job_offer_id: int,
    session: Session = Depends(get_session)
):
    """
    Obtener una oferta de trabajo por ID, incluyendo el número de postulaciones.
    """
    try:
        offer = JobOfferService.get_job_offer_by_id(session, job_offer_id)
        if not offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Oferta de trabajo no encontrada"
            )

        applications_count = JobOfferService.get_applications_count(session, job_offer_id)

        return {
            **offer.model_dump(),
            "applications_count": applications_count
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener oferta: {str(e)}"
        )

@router.get("/user/{user_id}", response_model=List[JobOfferResponse])
def get_job_offers_by_user(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """
    Obtener todas las ofertas de trabajo creadas por un usuario.
    """
    try:
        offers = JobOfferService.get_job_offers_by_user(session, user_id, skip, limit)
        return offers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener ofertas del usuario: {str(e)}"
        )

@router.put("/{job_offer_id}", response_model=JobOfferResponse)
def update_job_offer(
    job_offer_id: int,
    job_offer_data: JobOfferUpdate,
    session: Session = Depends(get_session)
):
    """
    Actualizar una oferta de trabajo.
    Solo se actualizan los campos proporcionados.
    """
    try:
        updated_offer = JobOfferService.update_job_offer(session, job_offer_id, job_offer_data)
        if not updated_offer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Oferta de trabajo no encontrada"
            )
        return updated_offer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar oferta: {str(e)}"
        )

@router.delete("/{job_offer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job_offer(
    job_offer_id: int,
    session: Session = Depends(get_session)
):
    """
    Eliminar (desactivar) una oferta de trabajo.
    Esto es un soft delete, la oferta se marca como inactiva.
    """
    try:
        success = JobOfferService.delete_job_offer(session, job_offer_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Oferta de trabajo no encontrada"
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar oferta: {str(e)}"
        )
