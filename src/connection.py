# db_connection.py
import sqlite3

from src.utils import parse_datetime
from src.config import DATABASE_PATH

# Registrar o conversor para o tipo DATETIME
sqlite3.register_converter("DATETIME", parse_datetime)


def get_connection():
    """Estabelece e retorna a conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(
        DATABASE_PATH,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
    )
    conn.row_factory = sqlite3.Row  
    return conn