from sqlalchemy import inspect, text
from langchain_community.utilities import SQLDatabase

def get_db_info(db: SQLDatabase) -> dict:
    """
    Get detailed information about the database including tables, columns, and relationships.
    
    Args:
        db: SQLDatabase instance connected to a PostgreSQL database
        
    Returns:
        dict: Dictionary containing database schema information
    """
    inspector = inspect(db._engine)
    tables = inspector.get_table_names()
    
    db_info = {
        "tables": {},
        "relationships": []
    }
    
    # Get table information including columns and primary keys
    for table in tables:
        columns = []
        for column in inspector.get_columns(table):
            columns.append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column.get("nullable", True),
                "default": str(column.get("default", "")) if column.get("default") else None,
            })
        
        primary_keys = inspector.get_pk_constraint(table).get("constrained_columns", [])
        indexes = []
        for index in inspector.get_indexes(table):
            indexes.append({
                "name": index["name"],
                "columns": index["column_names"],
                "unique": index["unique"]
            })
        
        db_info["tables"][table] = {
            "columns": columns,
            "primary_keys": primary_keys,
            "indexes": indexes
        }
    
    # Get foreign key relationships
    for table in tables:
        for fk in inspector.get_foreign_keys(table):
            relationship = {
                "table": table,
                "columns": fk["constrained_columns"],
                "references_table": fk["referred_table"],
                "references_columns": fk["referred_columns"],
                "name": fk.get("name")
            }
            db_info["relationships"].append(relationship)
    
    return db_info


def execute_sample_query(db: SQLDatabase, table_name: str, limit: int = 5) -> list:
    """
    Execute a sample query to show a few rows from a specific table.
    
    Args:
        db: SQLDatabase instance
        table_name: Name of the table to query
        limit: Maximum number of rows to return
        
    Returns:
        list: Sample data from the specified table
    """
    query = f"SELECT * FROM {table_name} LIMIT {limit}"
    with db._engine.connect() as conn:
        result = conn.execute(text(query))
        columns = result.keys()
        data = [dict(zip(columns, row)) for row in result.fetchall()]
    return data


def test_connection(db: SQLDatabase) -> bool:
    """
    Test database connection by executing a simple query.
    
    Args:
        db: SQLDatabase instance
        
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        with db._engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False 