from datetime import datetime, date
from typing import List, Optional
from sqlmodel import Session, select, func
from app.models.job_offer import JobOffer
from app.models.job_application import JobApplication
from app.schemas.job_offer import JobOfferCreate, JobOfferUpdate

class JobOfferService:
    """Servicio para gestionar ofertas de trabajo"""

    @staticmethod
    def create_job_offer(session: Session, job_offer_data: JobOfferCreate, user_id: int) -> JobOffer:
        """Crear una nueva oferta de trabajo"""
        job_offer = JobOffer(
            **job_offer_data.model_dump(),
            created_by=user_id,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        session.add(job_offer)
        session.commit()
        session.refresh(job_offer)
        return job_offer

    @staticmethod
    def get_job_offer_by_id(session: Session, job_offer_id: int) -> Optional[JobOffer]:
        """Obtener una oferta de trabajo por ID"""
        return session.get(JobOffer, job_offer_id)

    @staticmethod
    def get_all_job_offers(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[int] = None
    ) -> List[JobOffer]:
        """Obtener todas las ofertas de trabajo con paginación"""
        query = select(JobOffer)

        if is_active is not None:
            query = query.where(JobOffer.is_active == is_active)

        query = query.offset(skip).limit(limit).order_by(JobOffer.created_at.desc())
        return list(session.exec(query).all())

    @staticmethod
    def get_job_offers_by_user(
        session: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[JobOffer]:
        """Obtener ofertas de trabajo creadas por un usuario"""
        query = select(JobOffer).where(
            JobOffer.created_by == user_id
        ).offset(skip).limit(limit).order_by(JobOffer.created_at.desc())

        return list(session.exec(query).all())

    @staticmethod
    def update_job_offer(
        session: Session,
        job_offer_id: int,
        job_offer_data: JobOfferUpdate
    ) -> Optional[JobOffer]:
        """Actualizar una oferta de trabajo"""
        job_offer = session.get(JobOffer, job_offer_id)
        if not job_offer:
            return None

        update_data = job_offer_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(job_offer, key, value)

        job_offer.updated_at = datetime.now()
        session.add(job_offer)
        session.commit()
        session.refresh(job_offer)
        return job_offer

    @staticmethod
    def delete_job_offer(session: Session, job_offer_id: int) -> bool:
        """Eliminar una oferta de trabajo (soft delete)"""
        job_offer = session.get(JobOffer, job_offer_id)
        if not job_offer:
            return False

        job_offer.is_active = 0
        job_offer.updated_at = datetime.now()
        session.add(job_offer)
        session.commit()
        return True

    @staticmethod
    def get_applications_count(session: Session, job_offer_id: int) -> int:
        """Obtener el número de postulaciones de una oferta"""
        query = select(func.count(JobApplication.id)).where(
            JobApplication.job_offer_id == job_offer_id
        )
        return session.exec(query).one()

    @staticmethod
    def search_job_offers(
        session: Session,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[JobOffer]:
        """Buscar ofertas de trabajo por término"""
        query = select(JobOffer).where(
            (JobOffer.title.contains(search_term)) |
            (JobOffer.company.contains(search_term)) |
            (JobOffer.location.contains(search_term)) |
            (JobOffer.description.contains(search_term))
        ).where(JobOffer.is_active == 1).offset(skip).limit(limit).order_by(JobOffer.created_at.desc())

        return list(session.exec(query).all())

    @staticmethod
    def get_job_offers_by_date_range(
        session: Session,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[JobOffer]:
        """Obtener ofertas de trabajo filtradas por rango de fechas"""
        query = select(JobOffer).where(JobOffer.is_active == 1)

        if start_date:
            query = query.where(func.cast(JobOffer.created_at, func.DATE) >= start_date)

        if end_date:
            query = query.where(func.cast(JobOffer.created_at, func.DATE) <= end_date)

        query = query.offset(skip).limit(limit).order_by(JobOffer.created_at.desc())
        return list(session.exec(query).all())
