"""
Conexión a la Base de Datos - Onsen Coffee
"""

import os
import sqlite3
import tempfile

# Ruta en /tmp para funcionar en entornos serverless de solo lectura
DB_PATH = os.path.join(tempfile.gettempdir(), 'onsen-coffee.db')


def _ensure_initialized():
    """Crea la base de datos y datos seed si no existe"""
    if os.path.exists(DB_PATH):
        return
    from db.schema import create_tables, insert_seed_data
    create_tables()
    insert_seed_data()

def get_connection():
    """
    Obtiene una conexión a la base de datos SQLite.
    Retorna resultados como diccionarioCreame las tablas necesarioas para un proyecto profesional de eccomerce de cafe de especialidads para fácil acceso.
    """
    _ensure_initialized()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON")  # Habilita foreign keys
    return conn

def get_cursor():
    """Obtiene un cursor para ejecutar queries"""
    conn = get_connection()
    return conn, conn.cursor()

def init_database():
    """Inicializa la base de datos creando las tablas"""
    from db.schema import create_tables, insert_seed_data
    create_tables()
    insert_seed_data()

# Conexión legacy para compatibilidad
connection = get_connection()
