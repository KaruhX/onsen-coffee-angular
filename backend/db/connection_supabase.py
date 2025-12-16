"""
Conexión a Supabase - Onsen Coffee
Base de datos PostgreSQL serverless con toda la potencia de Supabase
"""

import os
from supabase import create_client, Client

# Cargar variables de entorno (solo en desarrollo local)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass  # En producción (Vercel) las variables vienen del dashboard

# Configuración de Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL', '')

# Soportar nuevas API keys (publishable/secret) y legacy (anon/service_role)
SUPABASE_KEY = (
    os.environ.get('SUPABASE_PUBLISHABLE_KEY') or 
    os.environ.get('SUPABASE_ANON_KEY', '')
)
SUPABASE_SERVICE_KEY = (
    os.environ.get('SUPABASE_SECRET_KEY') or 
    os.environ.get('SUPABASE_SERVICE_KEY', '')
)

# Cliente Supabase global
_supabase_client: Client = None


def get_supabase_client(use_service_key: bool = False) -> Client:
    """
    Obtiene el cliente de Supabase.
    
    Args:
        use_service_key: Si True, usa la service key (para operaciones admin).
                        Si False, usa la anon key (para operaciones públicas).
    
    Returns:
        Cliente de Supabase configurado
    """
    global _supabase_client
    
    if not SUPABASE_URL:
        raise Exception("SUPABASE_URL no está configurado")
    
    key = SUPABASE_SERVICE_KEY if use_service_key and SUPABASE_SERVICE_KEY else SUPABASE_KEY
    
    if not key:
        raise Exception("SUPABASE_PUBLISHABLE_KEY o SUPABASE_ANON_KEY no está configurado")
    
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, key)
    
    return _supabase_client


def get_db_connection():
    """
    Obtiene conexión directa a PostgreSQL usando psycopg2.
    Útil para queries complejas o migraciones.
    """
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    # Supabase provee la URL de conexión directa
    postgres_url = os.environ.get('SUPABASE_DB_URL', '')
    
    if not postgres_url:
        raise Exception("SUPABASE_DB_URL no está configurado")
    
    conn = psycopg2.connect(
        postgres_url,
        cursor_factory=RealDictCursor,
        sslmode='require'
    )
    return conn


def init_database():
    """Inicializa la base de datos creando las tablas si no existen"""
    from . import schema
    schema.create_tables()


# Funciones helper para operaciones comunes

def query_table(table_name: str, filters: dict = None, select: str = "*"):
    """
    Query simplificado a una tabla.
    
    Args:
        table_name: Nombre de la tabla
        filters: Diccionario con filtros (ej: {"status": "active"})
        select: Campos a seleccionar (default: "*")
    
    Returns:
        Lista de registros
    """
    client = get_supabase_client()
    query = client.table(table_name).select(select)
    
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    
    response = query.execute()
    return response.data


def insert_record(table_name: str, data: dict):
    """
    Inserta un registro en una tabla.
    
    Args:
        table_name: Nombre de la tabla
        data: Diccionario con los datos a insertar
    
    Returns:
        Registro insertado
    """
    client = get_supabase_client(use_service_key=True)
    response = client.table(table_name).insert(data).execute()
    return response.data[0] if response.data else None


def update_record(table_name: str, record_id: int, data: dict):
    """
    Actualiza un registro por ID.
    
    Args:
        table_name: Nombre de la tabla
        record_id: ID del registro
        data: Datos a actualizar
    
    Returns:
        Registro actualizado
    """
    client = get_supabase_client(use_service_key=True)
    response = client.table(table_name).update(data).eq('id', record_id).execute()
    return response.data[0] if response.data else None


def delete_record(table_name: str, record_id: int):
    """
    Elimina un registro por ID.
    
    Args:
        table_name: Nombre de la tabla
        record_id: ID del registro
    
    Returns:
        True si se eliminó correctamente
    """
    client = get_supabase_client(use_service_key=True)
    response = client.table(table_name).delete().eq('id', record_id).execute()
    return True if response.data else False
