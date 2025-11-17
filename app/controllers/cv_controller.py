from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import datetime
from app.services.db.sql_server_connection import get_session
from app.models.user import AppUser
from app.schemas.cv import CVUpdate, CVResponse

router = APIRouter(prefix="/cv", tags=["CV"])

@router.get("/{user_id}", response_model=CVResponse)
def get_user_cv(
    user_id: int,
    session: Session = Depends(get_session)
):
    """
    Obtener el CV de un usuario.
    """
    try:
        user = session.get(AppUser, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        return CVResponse(
            cv_full_name=user.cv_full_name,
            cv_phone=user.cv_phone,
            cv_summary=user.cv_summary,
            cv_experience=user.cv_experience,
            cv_education=user.cv_education,
            cv_skills=user.cv_skills
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener CV: {str(e)}"
        )

@router.put("/{user_id}", response_model=CVResponse)
def update_user_cv(
    user_id: int,
    cv_data: CVUpdate,
    session: Session = Depends(get_session)
):
    """
    Actualizar el CV de un usuario.

    Los campos de experiencia y educación deben enviarse como JSON string:
    - **cv_experience**: [{"company": "...", "position": "...", "years": "..."}]
    - **cv_education**: [{"institution": "...", "degree": "...", "year": "..."}]
    - **cv_skills**: Lista separada por comas
    """
    try:
        user = session.get(AppUser, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        # Actualizar solo los campos proporcionados
        update_data = cv_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        user.updated_at = datetime.now()
        session.add(user)
        session.commit()
        session.refresh(user)

        return CVResponse(
            cv_full_name=user.cv_full_name,
            cv_phone=user.cv_phone,
            cv_summary=user.cv_summary,
            cv_experience=user.cv_experience,
            cv_education=user.cv_education,
            cv_skills=user.cv_skills
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar CV: {str(e)}"
        )
