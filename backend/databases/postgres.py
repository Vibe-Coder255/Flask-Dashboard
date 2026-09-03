from typing import Any

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = ""
POSTGRES_DATABASE = "test_db"


def check_postgres_connection() -> dict[str, Any]:
    """Check PostgreSQL connection and return status."""
    try:
        import psycopg2
        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DATABASE
        )
        connection.close()
        return {
            "status": "success",
            "database": POSTGRES_DATABASE,
            "host": POSTGRES_HOST,
            "port": POSTGRES_PORT
        }
    except ImportError:
        return {
            "status": "error",
            "error": "psycopg2 not installed"
        }
    except Exception as error:
        return {
            "status": "error",
            "error": str(error)
        }


def get_postgres_tables() -> list[dict[str, Any]]:
    """Get list of tables from PostgreSQL database."""
    try:
        import psycopg2
        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DATABASE
        )
        cursor = connection.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [{"name": table[0]} for table in cursor.fetchall()]
        cursor.close()
        connection.close()
        return tables
    except Exception as error:
        return [{"error": str(error)}]


def get_postgres_table_data(table_name: str, limit: int = 100) -> list[dict[str, Any]]:
    """Get data from a specific PostgreSQL table."""
    try:
        import psycopg2
        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DATABASE
        )
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        
        # Get column names
        column_names = [desc[0] for desc in cursor.description]
        
        # Fetch data and convert to list of dictionaries
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
        
        cursor.close()
        connection.close()
        return data
    except Exception as error:
        return [{"error": str(error)}]
