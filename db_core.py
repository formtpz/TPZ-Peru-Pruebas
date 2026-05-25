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



# En db_core.py, mantenemos UNA SOLA función genérica:

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
        # Si filtro_subproceso es una lista, usar IN; si es string, usar =
        if isinstance(filtro_subproceso, list):
            cond1 = "(proceso = %s AND subproceso IN %s)"
            params.extend([filtro_proceso, tuple(filtro_subproceso)])
        else:
            cond1 = "(proceso = %s AND subproceso = %s)"
            params.extend([filtro_proceso, filtro_subproceso])
        condiciones.append(cond1)
    
    # Condición 2: proceso_anterior y subproceso_anterior cumplen filtros
    if filtro_proceso_anterior and filtro_subproceso_anterior:
        if isinstance(filtro_subproceso_anterior, list):
            cond2 = "(proceso_anterior = %s AND subproceso_anterior IN %s)"
            params.extend([filtro_proceso_anterior, tuple(filtro_subproceso_anterior)])
        else:
            cond2 = "(proceso_anterior = %s AND subproceso_anterior = %s)"
            params.extend([filtro_proceso_anterior, filtro_subproceso_anterior])
        condiciones.append(cond2)
    
    # Combinar condiciones con OR (cualquiera que cumpla alguna condición)
    if condiciones:
        query += " AND (" + " OR ".join(condiciones) + ")"
    
    query += " ORDER BY nombre"
    
    df = fetch_df(query, params=params)
    return df.to_dict('records') if not df.empty else []

# Agregar al final de db_core.py
# db_core.py - Versión que busca por usuario o por nombre

def fetch_rechazos_pendientes(identificador, tipo='nombre', dias=10):
    """
    Obtiene los rechazos pendientes para un operador.
    
    Args:
        identificador: Puede ser el nombre O el usuario
        tipo: 'nombre' o 'usuario' - indica qué columna buscar
        dias: Número de días hacia atrás
    """
    from datetime import datetime, timedelta
    
    fecha_limite = datetime.now() - timedelta(days=dias)
    fecha_limite_str = fecha_limite.strftime('%Y-%m-%d')
    
    # Determinar por qué columna buscar
    if tipo == 'usuario':
        # Buscar por usuario - necesitamos obtener el nombre real del operador
        query_nombre = """
            SELECT nombre FROM usuarios WHERE usuario = %s AND estado = 'Activo'
        """
        df_nombre = fetch_df(query_nombre, params=[identificador])
        if df_nombre.empty:
            return pd.DataFrame()
        nombre_buscar = df_nombre['nombre'].iloc[0]
    else:
        # Buscar directamente por nombre
        nombre_buscar = identificador
    
    # Ahora buscar en registro por el nombre
    query = """
        SELECT 
            id,
            fecha,
            proceso,
            distrito,
            manzana,
            sector,
            numero_lote,
            rechazados,
            tipo_de_errores,
            estado
        FROM registro
        WHERE operador_cc ILIKE %s
          AND estado = 'N/A'
          AND (rechazados::int)> 0
          AND fecha >= %s
        ORDER BY fecha DESC
    """
    return fetch_df(query, params=[nombre_buscar, fecha_limite_str])


def fetch_rechazos_pendientes_por_usuario(usuario, dias=10):
    """
    Versión simplificada: recibe el usuario y automáticamente busca su nombre.
    Esta es la que deberías usar desde Notificaciones.
    """
    import streamlit as st 
    from datetime import datetime, timedelta
    
    # Paso 1: Obtener el nombre del usuario desde la tabla usuarios
    query_nombre = """
        SELECT nombre FROM usuarios WHERE usuario = %s AND estado = 'Activo'
    """
    df_nombre = fetch_df(query_nombre, params=[usuario])
    
    if df_nombre.empty:
        st.warning(f"No se encontró el usuario '{usuario}' en la tabla de usuarios")
        return pd.DataFrame()
    
    nombre_operador = df_nombre['nombre'].iloc[0]
    
    # Paso 2: Buscar rechazos por ese nombre
    fecha_limite = datetime.now() - timedelta(days=dias)
    fecha_limite_str = fecha_limite.strftime('%Y-%m-%d')
    
    query = """
        SELECT 
            id,
            fecha,
            proceso,
            distrito,
            manzana,
            sector,
            numero_lote,
            rechazados,
            tipo_de_errores,
            estado
        FROM registro
        WHERE operador_cc ILIKE %s
          AND estado = 'N/A'
          AND (rechazados::int)> 0
          AND fecha >= %s
        ORDER BY fecha DESC
    """
    df_resultado = fetch_df(query, params=[nombre_operador, fecha_limite_str])
    
    # Diagnóstico silencioso (opcional)
    if df_resultado.empty:
        # Intentar búsqueda más flexible: cualquier coincidencia parcial
        query_flexible = """
            SELECT 
                id,
                fecha,
                proceso,
                distrito,
                manzana,
                sector,
                numero_lote,
                rechazados,
                tipo_de_errores,
                estado
            FROM registro
            WHERE operador_cc ILIKE %s
              AND estado = 'N/A'
              AND (rechazados::int)> 0
              AND fecha >= %s
            ORDER BY fecha DESC
        """
        # Buscar con porcentajes (ej: '%juan%' para encontrar 'juan perez')
        nombre_parcial = f"%{nombre_operador}%"
        df_resultado = fetch_df(query_flexible, params=[nombre_parcial, fecha_limite_str])
    
    return df_resultado


def actualizar_estado_rechazo(id_registro, nuevo_estado):
    """
    Actualiza el estado de un registro específico.
    Solo permite 'corregido'
    """
    if nuevo_estado != 'corregido':
        return False
    
    query = """
        UPDATE registro
        SET estado = %s
        WHERE id = %s
          AND estado = 'N/A'  # Solo actualizar si sigue pendiente
    """
    try:
        execute(query, params=[nuevo_estado, id_registro])
        return True
    except Exception as e:
        print(f"Error al actualizar: {e}")
        return False
