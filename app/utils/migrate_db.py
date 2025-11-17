"""
Database migration utilities
"""
from pathlib import Path
from sqlmodel import Session, text


def run_sql_file(session: Session, sql_filename: str) -> dict:
    """
    Run a SQL script file
    Returns dict with success status and message
    """
    try:
        # Read the SQL script
        sql_file = Path(__file__).parent.parent.parent / "scripts" / sql_filename

        if not sql_file.exists():
            return {
                "success": False,
                "message": f"SQL file not found: {sql_file}"
            }

        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Split by GO statements and filter out comments, empty lines, and problematic commands
        batches = []
        current_batch = []

        for line in sql_content.split('\n'):
            stripped = line.strip()

            # Skip empty lines, comment-only lines, USE statements, and PRINT statements
            if (not stripped or
                stripped.startswith('--') or
                stripped.upper().startswith('USE ') or
                stripped.upper().startswith('PRINT ')):
                continue

            # Check if this is a GO statement
            if stripped.upper() == 'GO':
                if current_batch:
                    batch_text = '\n'.join(current_batch).strip()
                    if batch_text:
                        batches.append(batch_text)
                    current_batch = []
            else:
                current_batch.append(line)

        # Add the last batch if there is one
        if current_batch:
            batch_text = '\n'.join(current_batch).strip()
            if batch_text:
                batches.append(batch_text)

        # Execute each batch
        results = []
        for i, batch in enumerate(batches, 1):
            if batch.strip():
                try:
                    session.exec(text(batch))
                    session.commit()
                    results.append(f"Batch {i} executed successfully")
                except Exception as e:
                    # Log the error but continue
                    results.append(f"Batch {i} error: {str(e)}")
                    session.rollback()

        return {
            "success": True,
            "message": "Migration completed",
            "details": results
        }

    except Exception as e:
        session.rollback()
        return {
            "success": False,
            "message": f"Migration failed: {str(e)}"
        }


def run_status_migration(session: Session) -> dict:
    """Run the job_application status migration"""
    return run_sql_file(session, "update_job_application_status.sql")


def run_setup_job_system(session: Session) -> dict:
    """Run the job system setup (create tables)"""
    return run_sql_file(session, "setup_job_system.sql")
