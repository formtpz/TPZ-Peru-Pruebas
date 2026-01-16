import pandas as pd
import streamlit as st
import psycopg2
from urllib.parse import urlparse

# --- Cargar URI desde secrets ---
uri = st.secrets.db_credentials.URI

# --- Parsear URI ---
result = urlparse(uri)
hostname = result.hostname
database = result.path[1:]
username = result.username
pwd = result.password
port_id = result.port

# --- Función para recuperar contraseña ---
def contraseña(usuario):
    query = f"""
        SELECT contraseña 
        FROM usuarios 
        WHERE usuario = '{usuario}' 
          AND estado = 'Activo'
    """
    return pd.read_sql(query, con)

# --- Crear una sola conexión global (cacheada) ---
@st.cache_resource
def init_connection():
    return psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )

# --- Abrir conexión compartida ---
con = init_connection()

