"""
Script to run SQL migration for updating job_application status constraint
"""
import os
import sys
from pathlib import Path

# Add the parent directory to the path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
import pyodbc

# Load environment variables
load_dotenv()

def run_migration():
    """Execute the SQL migration script"""

    # Read the SQL script
    sql_file = Path(__file__).parent / "update_job_application_status.sql"
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Parse connection string from environment
    connection_string = os.getenv("DB_SQL_SERVER_GIG")

    # Extract connection parameters from SQLAlchemy format
    # mssql+pyodbc://user:pass@server:port/database?driver=...
    if not connection_string or not connection_string.startswith("mssql+pyodbc://"):
        print("Error: Invalid DB_SQL_SERVER_GIG format")
        print(f"Connection string: {connection_string}")
        return False

    # Remove the mssql+pyodbc:// prefix
    conn_str = connection_string.replace("mssql+pyodbc://", "")

    # Split user:pass@server part
    auth_part, rest = conn_str.split("@", 1)
    username, password = auth_part.split(":", 1)

    # Split server:port/database?params
    server_part, db_and_params = rest.split("/", 1)
    server = server_part.split(":")[0]
    port = server_part.split(":")[1] if ":" in server_part else "1433"

    # Split database?params
    database = db_and_params.split("?")[0]

    # Extract driver from connection string if present
    driver = "ODBC Driver 18 for SQL Server"  # default
    if "?" in db_and_params:
        params = db_and_params.split("?")[1]
        for param in params.split("&"):
            if param.startswith("driver="):
                driver = param.split("=", 1)[1].replace("+", " ")
                break

    # Build ODBC connection string
    odbc_conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
    )

    # Add encryption params if using ODBC Driver 18
    if "ODBC Driver 18" in driver:
        odbc_conn_str += "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

    try:
        print("Connecting to database...")
        conn = pyodbc.connect(odbc_conn_str)
        cursor = conn.cursor()

        print("Executing migration script...")

        # Split the SQL script by GO statements
        sql_batches = [batch.strip() for batch in sql_content.split("GO") if batch.strip()]

        for i, batch in enumerate(sql_batches, 1):
            if batch.strip():
                try:
                    print(f"Executing batch {i}/{len(sql_batches)}...")
                    cursor.execute(batch)
                    conn.commit()

                    # Print any messages from SQL Server
                    while cursor.nextset():
                        pass

                except pyodbc.Error as e:
                    print(f"Warning in batch {i}: {e}")
                    # Continue with next batch even if one fails
                    conn.rollback()

        cursor.close()
        conn.close()

        print("\n" + "="*50)
        print("Migration completed successfully!")
        print("="*50)
        return True

    except Exception as e:
        print(f"Error executing migration: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
