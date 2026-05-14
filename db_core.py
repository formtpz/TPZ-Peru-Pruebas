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
    
    # Condición 1: proceso y subproceso actuales cumplen filtros
    if filtro_proceso and filtro_subproceso:
        cond1 = "(proceso = %s AND subproceso IN %s)"
        condiciones.append(cond1)
        params.extend([filtro_proceso, tuple(filtro_subproceso)])
    
    # Condición 2: proceso_anterior y subproceso_anterior cumplen filtros
    if filtro_proceso_anterior and filtro_subproceso_anterior:
        cond2 = "(proceso_anterior = %s AND subproceso_anterior IN %s)"
        condiciones.append(cond2)
        params.extend([filtro_proceso_anterior, tuple(filtro_subproceso_anterior)])
    
    # Combinar condiciones con OR (cualquiera que cumpla alguna condición)
    if condiciones:
        query += " AND (" + " OR ".join(condiciones) + ")"
    
    query += " ORDER BY nombre"
    
    print(f"DEBUG - Query: {query}")  # Para debugging
    print(f"DEBUG - Params: {params}")  # Para debugging
    
    df = fetch_df(query, params=params)
    return df.to_dict('records') if not df.empty else []
