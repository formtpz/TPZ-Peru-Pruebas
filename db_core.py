import pandas as pd
import streamlit as st
import psycopg2
from urllib.parse import urlparse

uri = st.secrets.db_credentials.URI

result = urlparse(uri)
hostname = result.hostname
database = result.path[1:]
username = result.username
pwd = result.password
port_id = result.port


@st.cache_resource
def init_connection():
    return psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id,
    )


con = init_connection()


def fetch_df(query: str, params=None):
    return pd.read_sql_query(query, con=con, params=params)


def fetch_one(query: str, params=None):
    df = fetch_df(query, params=params)
    if df.empty:
        return None
    return df.iloc[0].to_dict()


def execute(query: str, params=None):
    cur = con.cursor()
    try:
        cur.execute(query, params)
        con.commit()
    finally:
        cur.close()

# Reemplaza las funciones en db_core.py con estas versiones actualizadas:

def fetch_operadores_cc(filtro_proceso=None, filtro_subproceso=None, filtro_proceso_anterior=None, filtro_subproceso_anterior=None):
    """
    Obtiene operadores para Control de Calidad con filtros específicos.
    
    Args:
        filtro_proceso: Valor para columna 'proceso'
        filtro_subproceso: Lista de valores para columna 'subproceso' (IN clause)
        filtro_proceso_anterior: Valor para columna 'proceso_anterior'
        filtro_subproceso_anterior: Lista de valores para columna 'subproceso_anterior' (IN clause)
    
    Returns:
        Lista de diccionarios con nombre y usuario
    """
    query = """
        SELECT DISTINCT nombre, usuario
        FROM usuarios
        WHERE estado = 'Activo'
          AND activo_en_listas = 'activo'
    """
    
    condiciones = []
    params = []
    
    # Filtro por proceso y subproceso
    if filtro_proceso and filtro_subproceso:
        condiciones.append("(proceso = %s AND subproceso IN %s)")
        params.extend([filtro_proceso, tuple(filtro_subproceso)])
    
    # Filtro por proceso_anterior y subproceso_anterior
    if filtro_proceso_anterior and filtro_subproceso_anterior:
        condiciones.append("(proceso_anterior = %s AND subproceso_anterior IN %s)")
        params.extend([filtro_proceso_anterior, tuple(filtro_subproceso_anterior)])
    
    # Combinar condiciones con OR
    if condiciones:
        query += " AND (" + " OR ".join(condiciones) + ")"
    
    query += " ORDER BY nombre"
    
    df = fetch_df(query, params=params)
    return df.to_dict('records') if not df.empty else []


def fetch_operadores_vinculacion():
    """
    Obtiene operadores para Control de Calidad Vinculación Precampo.
    Todos los usuarios activos que estén habilitados en listas.
    
    Returns:
        Lista de diccionarios con nombre y usuario
    """
    query = """
        SELECT DISTINCT nombre, usuario
        FROM usuarios
        WHERE estado = 'Activo'
          AND activo_en_listas = 'activo'
        ORDER BY nombre
    """
    df = fetch_df(query)
    return df.to_dict('records') if not df.empty else []
