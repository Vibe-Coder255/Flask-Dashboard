from typing import Any

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DATABASE = "test_db"


def check_mysql_connection() -> dict[str, Any]:
    """Check MySQL connection and return status."""
    try:
        import mysql.connector
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        connection.close()
        return {
            "status": "success",
            "database": MYSQL_DATABASE,
            "host": MYSQL_HOST,
            "port": MYSQL_PORT
        }
    except ImportError:
        return {
            "status": "error",
            "error": "mysql-connector-python not installed"
        }
    except Exception as error:
        return {
            "status": "error",
            "error": str(error)
        }


def get_mysql_tables() -> list[dict[str, Any]]:
    """Get list of tables from MySQL database."""
    try:
        import mysql.connector
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [{"name": table[0]} for table in cursor.fetchall()]
        cursor.close()
        connection.close()
        return tables
    except Exception as error:
        return [{"error": str(error)}]


def get_mysql_table_data(table_name: str, limit: int = 100) -> list[dict[str, Any]]:
    """Get data from a specific MySQL table."""
    try:
        import mysql.connector
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
    except Exception as error:
        return [{"error": str(error)}]
