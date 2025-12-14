"""
Conexión a la Base de Datos - Onsen Coffee
"""

import os
import sqlite3
import tempfile
import threading

# Ruta en /tmp para funcionar en entornos serverless de solo lectura
DB_PATH = os.path.join(tempfile.gettempdir(), 'onsen-coffee.db')

# Lock para evitar condiciones de carrera al inicializar
_init_lock = threading.Lock()
_initialized = False


def _ensure_initialized():
    """Crea la base de datos y datos seed si no existe"""
    global _initialized
    
    # Doble verificación con lock para thread-safety
    if _initialized:
        return
        
    with _init_lock:
        if _initialized:
            return
            
        if not os.path.exists(DB_PATH):
            from db.schema import create_tables, insert_seed_data
            create_tables()
            insert_seed_data()
        
        _initialized = True

def get_connection():
    """
    Obtiene una conexión a la base de datos SQLite.
    Retorna resultados como diccionario para fácil acceso.
    """
    _ensure_initialized()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    conn.execute("PRAGMA foreign_keys = ON")  # Habilita foreign keys
    return conn

def get_cursor():
    """Obtiene un cursor para ejecutar queries"""
    conn = get_connection()
    return conn, conn.cursor()

def init_database():
    """Inicializa la base de datos creando las tablas"""
    global _initialized
    _initialized = False
    _ensure_initialized()

# Conexión legacy para compatibilidad
connection = None

def get_legacy_connection():
    """Obtiene conexión legacy - deprecado, usar get_connection()"""
    global connection
    if connection is None:
        connection = get_connection()
    return connection
