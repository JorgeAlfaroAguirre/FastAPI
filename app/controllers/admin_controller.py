"""
Admin endpoints for database migrations and maintenance
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.services.db.sql_server_connection import get_session
from app.utils.migrate_db import run_status_migration, run_setup_job_system

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/migrate/job-application-status")
def migrate_job_application_status(
    session: Session = Depends(get_session)
):
    """
    Run migration to update job_application status constraint.

    This adds new status values:
    - pending
    - under_review
    - interview_scheduled
    - interviewed
    - offered
    - hired
    - rejected

    **WARNING**: This endpoint modifies database schema. Use with caution.
    """
    try:
        result = run_status_migration(session)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["message"]
            )

        return {
            "message": "Migration completed successfully",
            "details": result.get("details", [])
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running migration: {str(e)}"
        )


@router.post("/setup/job-system")
def setup_job_system(
    session: Session = Depends(get_session)
):
    """
    Run initial setup for job system (create tables).

    This creates:
    - job_offer table
    - job_application table
    - Adds CV fields to app_user table

    **WARNING**: This endpoint modifies database schema. Run only once during initial setup.
    """
    try:
        result = run_setup_job_system(session)

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["message"]
            )

        return {
            "message": "Setup completed successfully",
            "details": result.get("details", [])
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error running setup: {str(e)}"
        )
