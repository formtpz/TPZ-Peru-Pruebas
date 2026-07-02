# ----- historial_peru.py (sin botón de Bonos y Horas Extras) -----
import numpy as np
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

import Procesos, Capacitacion, Otros_Registros, Salir  # <-- Bonos_Extras eliminado
from db_core import fetch_df

# -------------------------------------------------------------------
# FUNCIONES AUXILIARES DE DATOS (con filtro por puesto peruano)
# -------------------------------------------------------------------

def convertir_lotes(df):
    """Convierte la columna 'lotes' (texto) a conteo numérico."""
    if 'lotes' not in df.columns:
        return df
    def contar_lotes(valor):
        if pd.isna(valor) or valor == '':
            return 0
        if isinstance(valor, str):
            partes = [p.strip() for p in valor.split(',') if p.strip()]
            return len(partes)
        try:
            return int(float(valor))
        except:
            return 0
    df['lotes'] = df['lotes'].apply(contar_lotes)
    return df

def cargar_datos_supervisor_peru(fecha_inicio, fecha_fin, personal, proceso, tipo, nombre_usuario):
    """Carga datos solo de los puestos peruanos."""
    puestos_peru = ("'Operario Perú'", "'Supervisor Perú'", "'Coordinador Perú'")
    filtro_puesto = f"puesto IN ({', '.join(puestos_peru)})"

    base_r = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, proceso, fecha, semana, año,
               distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,
               lotes, estado, cast(aprobados as float), cast(rechazados as float), operador_cc,
               tipo_de_errores, conteo_de_errores, numero_lote, observaciones, cast(horas as float)
        FROM registro
        WHERE {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
        """,
        params=[fecha_inicio, fecha_fin]
    )
    base_c = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, fecha, tema,
               cast(horas as float), observaciones, reporte
        FROM capacitaciones
        WHERE {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
        """,
        params=[fecha_inicio, fecha_fin]
    )
    base_o = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, fecha, motivo,
               cast(horas as float), observaciones, reporte
        FROM otros_registros
        WHERE {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
        """,
        params=[fecha_inicio, fecha_fin]
    )

    data_r = base_r.copy() if base_r is not None else pd.DataFrame()
    data_c = base_c.copy() if base_c is not None else pd.DataFrame()
    data_o = base_o.copy() if base_o is not None else pd.DataFrame()

    if not data_r.empty:
        data_r = convertir_lotes(data_r)

    if personal == "Operarios Perú":
        data_r = data_r[data_r["puesto"] == "Operario Perú"] if not data_r.empty else data_r
        data_c = data_c[data_c["puesto"] == "Operario Perú"] if not data_c.empty else data_c
        data_o = data_o[data_o["puesto"] == "Operario Perú"] if not data_o.empty else data_o
    elif personal == "Profesional Jurídico Perú":
        data_r = data_r[data_r["puesto"] == "Profesional Jurídico Perú"] if not data_r.empty else data_r
        data_c = data_c[data_c["puesto"] == "Profesional Jurídico Perú"] if not data_c.empty else data_c
        data_o = data_o[data_o["puesto"] == "Profesional Jurídico Perú"] if not data_o.empty else data_o
    elif personal == "Propio":
        data_r = data_r[data_r["nombre"] == nombre_usuario] if not data_r.empty else data_r
        data_c = data_c[data_c["nombre"] == nombre_usuario] if not data_c.empty else data_c
        data_o = data_o[data_o["nombre"] == nombre_usuario] if not data_o.empty else data_o
    elif personal == "Personal Asignado":
        data_r = data_r[data_r["supervisor"] == nombre_usuario] if not data_r.empty else data_r
        data_c = data_c[data_c["supervisor"] == nombre_usuario] if not data_c.empty else data_c
        data_o = data_o[data_o["supervisor"] == nombre_usuario] if not data_o.empty else data_o

    if proceso != "Todos" and not data_r.empty:
        data_r = data_r[data_r["proceso"] == proceso]
    if tipo != "Todos" and not data_r.empty:
        data_r = data_r[data_r["tipo"] == tipo]

    return data_r, data_c, data_o

def cargar_datos_operario_peru(usuario, fecha_inicio, fecha_fin, proceso, tipo, nombre_completo):
    """Carga datos para operario peruano."""
    puestos_peru = ("'Operario Perú'",)
    filtro_puesto = f"puesto IN ({', '.join(puestos_peru)})"

    condiciones = [f"usuario = %s", filtro_puesto]
    params_where = [usuario]
    if proceso != "Todos":
        condiciones.append("proceso = %s")
        params_where.append(proceso)
    if tipo != "Todos":
        condiciones.append("tipo = %s")
        params_where.append(tipo)

    where_clause = " AND ".join(condiciones)
    params = params_where + [fecha_inicio, fecha_fin]

    data_1_r = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, proceso, fecha, semana, año,
               distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,
               lotes, cast(aprobados as float), cast(rechazados as float), operador_cc,
               tipo_de_errores, conteo_de_errores, numero_lote, observaciones, cast(horas as float)
        FROM registro
        WHERE {where_clause} AND fecha::date >= %s AND fecha::date <= %s
        """,
        params=params
    )

    data_8_r = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, proceso, fecha, semana, año,
               distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,
               lotes, cast(aprobados as float), cast(rechazados as float), operador_cc,
               tipo_de_errores, conteo_de_errores, numero_lote, observaciones, cast(horas as float)
        FROM registro
        WHERE usuario = %s AND {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
          AND tipo NOT IN ('Producción Horas Extras', 'Inspección Horas Extras', 'Reproceso Horas Extras')
        """,
        params=[usuario, fecha_inicio, fecha_fin]
    )
    data_6_r = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, proceso, fecha, semana, año,
               distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,
               lotes, cast(aprobados as float), cast(rechazados as float), operador_cc,
               tipo_de_errores, conteo_de_errores, numero_lote, observaciones, cast(horas as float)
        FROM registro
        WHERE usuario = %s AND {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
          AND tipo IN ('Producción Horas Extras', 'Inspección Horas Extras', 'Reproceso Horas Extras')
        """,
        params=[usuario, fecha_inicio, fecha_fin]
    )
    data_5_r = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, proceso, fecha, semana, año,
               distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,
               lotes, cast(aprobados as float), cast(rechazados as float), operador_cc,
               tipo_de_errores, conteo_de_errores, numero_lote, observaciones, cast(horas as float)
        FROM registro
        WHERE operador_cc = %s AND {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
        """,
        params=[nombre_completo, fecha_inicio, fecha_fin]
    )

    data_1_r = convertir_lotes(data_1_r) if not data_1_r.empty else data_1_r
    data_8_r = convertir_lotes(data_8_r) if not data_8_r.empty else data_8_r
    data_6_r = convertir_lotes(data_6_r) if not data_6_r.empty else data_6_r
    data_5_r = convertir_lotes(data_5_r) if not data_5_r.empty else data_5_r

    data_1_c = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, fecha, tema,
               cast(horas as float), observaciones, reporte
        FROM capacitaciones
        WHERE usuario = %s AND {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
        """,
        params=[usuario, fecha_inicio, fecha_fin]
    )
    data_1_o = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, fecha, motivo,
               cast(horas as float), observaciones, reporte
        FROM otros_registros
        WHERE usuario = %s AND {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
        """,
        params=[usuario, fecha_inicio, fecha_fin]
    )
    data_6_o = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, fecha, motivo,
               cast(horas as float), observaciones, reporte
        FROM otros_registros
        WHERE usuario = %s AND {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
          AND motivo IN ('Horas Extra', 'Horas Extra Apoyo Otros Proyectos', 'Horas Extras')
        """,
        params=[usuario, fecha_inicio, fecha_fin]
    )
    data_9_o = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, fecha, motivo,
               cast(horas as float), observaciones, reporte
        FROM otros_registros
        WHERE usuario = %s AND {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
          AND motivo NOT IN ('Reposición de tiempo', 'Horas Extra', 'Horas Extra Apoyo Otros Proyectos', 'Horas Extras')
        """,
        params=[usuario, fecha_inicio, fecha_fin]
    )
    data_7_o = fetch_df(
        f"""
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor, fecha, motivo,
               cast(horas as float), observaciones, reporte
        FROM otros_registros
        WHERE usuario = %s AND {filtro_puesto} AND fecha::date >= %s AND fecha::date <= %s
          AND motivo = 'Reposición de tiempo'
        """,
        params=[usuario, fecha_inicio, fecha_fin]
    )

    data_1_r = data_1_r if data_1_r is not None else pd.DataFrame()
    data_8_r = data_8_r if data_8_r is not None else pd.DataFrame()
    data_6_r = data_6_r if data_6_r is not None else pd.DataFrame()
    data_5_r = data_5_r if data_5_r is not None else pd.DataFrame()
    data_1_c = data_1_c if data_1_c is not None else pd.DataFrame()
    data_1_o = data_1_o if data_1_o is not None else pd.DataFrame()
    data_6_o = data_6_o if data_6_o is not None else pd.DataFrame()
    data_9_o = data_9_o if data_9_o is not None else pd.DataFrame()
    data_7_o = data_7_o if data_7_o is not None else pd.DataFrame()

    return data_1_r, data_8_r, data_6_r, data_5_r, data_1_c, data_1_o, data_6_o, data_9_o, data_7_o

# -------------------------------------------------------------------
# FUNCIONES DE PROCESAMIENTO
# -------------------------------------------------------------------

def generar_resumen_horas(data_r, data_c, data_o):
    data_r = data_r if data_r is not None else pd.DataFrame()
    data_c = data_c if data_c is not None else pd.DataFrame()
    data_o = data_o if data_o is not None else pd.DataFrame()

    if data_r.empty and data_c.empty and data_o.empty:
        return pd.DataFrame()

    data_8_r = data_r[~data_r["tipo"].isin(["Producción Horas Extras", "Inspección Horas Extras", "Reproceso Horas Extras"])].copy() if not data_r.empty else pd.DataFrame()
    data_6_r = data_r[data_r["tipo"].isin(["Producción Horas Extras", "Inspección Horas Extras", "Reproceso Horas Extras"])].copy() if not data_r.empty else pd.DataFrame()
    data_6_o = data_o[data_o["motivo"].isin(["Horas Extra", "Horas Extra Apoyo Otros Proyectos", "Horas Extras"])].copy() if not data_o.empty else pd.DataFrame()
    data_7_o = data_o[data_o["motivo"] == "Reposición de tiempo"].copy() if not data_o.empty else pd.DataFrame()
    data_9_o = data_o[~data_o["motivo"].isin(["Reposición de tiempo", "Horas Extra", "Horas Extra Apoyo Otros Proyectos", "Horas Extras"])].copy() if not data_o.empty else pd.DataFrame()

    def agrupar_o_vacio(df, group_cols, agg_col, rename_dict):
        if df is not None and not df.empty:
            res = df.groupby(group_cols, as_index=False)[[agg_col]].agg(np.sum)
            res.rename(columns=rename_dict, inplace=True)
            return res
        else:
            return pd.DataFrame(columns=group_cols + list(rename_dict.values()))

    prod_normal = agrupar_o_vacio(data_8_r, ["nombre", "fecha"], "horas", {"horas": "horas_produccion"})
    prod_extra = agrupar_o_vacio(data_6_r, ["nombre", "fecha"], "horas", {"horas": "horas_extra_produccion"})
    cap = agrupar_o_vacio(data_c, ["nombre", "fecha"], "horas", {"horas": "horas_capacitacion"})
    otros = agrupar_o_vacio(data_9_o, ["nombre", "fecha"], "horas", {"horas": "horas_otros_registros"})
    otros_extra = agrupar_o_vacio(data_6_o, ["nombre", "fecha"], "horas", {"horas": "horas_extra_otros_registros"})
    reposicion = agrupar_o_vacio(data_7_o, ["nombre", "fecha"], "horas", {"horas": "reposicion"})

    datos_horas = pd.concat([prod_normal, prod_extra, cap, otros, otros_extra], axis=0)
    if datos_horas.empty:
        return pd.DataFrame()

    keys = datos_horas[["nombre", "fecha"]].drop_duplicates()
    merged = keys.merge(prod_normal, on=["nombre", "fecha"], how="left")
    merged = merged.merge(prod_extra, on=["nombre", "fecha"], how="left")
    merged = merged.merge(cap, on=["nombre", "fecha"], how="left")
    merged = merged.merge(otros, on=["nombre", "fecha"], how="left")
    merged = merged.merge(otros_extra, on=["nombre", "fecha"], how="left")
    merged = merged.merge(reposicion, on=["nombre", "fecha"], how="left")
    merged = merged.fillna(0)

    cols_numeric = ["horas_produccion", "horas_extra_produccion", "horas_capacitacion",
                    "horas_otros_registros", "horas_extra_otros_registros", "reposicion"]
    for col in cols_numeric:
        if col in merged.columns:
            merged[col] = pd.to_numeric(merged[col], errors="coerce").fillna(0)

    merged["Total"] = merged["horas_produccion"] + merged["horas_capacitacion"] + merged["horas_otros_registros"]
    return merged

def generar_resumen_produccion(data_r, modo_supervisor=False):
    data_r = data_r if data_r is not None else pd.DataFrame()
    if data_r.empty:
        return pd.DataFrame(), pd.DataFrame()

    diario = data_r.groupby(["nombre", "fecha"], as_index=False)[["lotes", "edificas", "horas"]].agg(np.sum)
    diario["rendimiento"] = (diario["edificas"] / diario["horas"]) * 8.5

    semanal = data_r.groupby(["nombre", "semana", "proceso"], as_index=False)[["edificas", "unidades_catastrales", "horas"]].agg(np.sum)

    if modo_supervisor:
        valor_esperado_map = {
            'Precampo': 340,
            'Control de Calidad Precampo': 510,
            'Postcampo': 340,
            'Control de Calidad Postcampo': 765
        }
        semanal["valor esperado"] = semanal["proceso"].map(valor_esperado_map).fillna(0)
        semanal["diferencia"] = semanal["edificas"] - semanal["valor esperado"]
    else:
        tasa_por_hora = {
            'Precampo': 8,
            'Control de Calidad Precampo': 10,
            'Postcampo': 7,
            'Control de Calidad Postcampo': 10,
            'Vinculación Precampo': 8,
            'Control de Calidad Vinculación Precampo': 10
        }
        semanal["valor esperado"] = semanal["proceso"].map(tasa_por_hora).fillna(0) * semanal["horas"]
        semanal["diferencia"] = semanal["edificas"] + semanal["unidades_catastrales"] - semanal["valor esperado"]
        semanal["ratio bruto"] = (semanal["edificas"] + semanal["unidades_catastrales"]) / semanal["horas"]

    return diario, semanal

def generar_resumen_calidad(data_r):
    data_r = data_r if data_r is not None else pd.DataFrame()
    if data_r.empty:
        return pd.DataFrame()

    data_filtrada = data_r[(data_r["tipo"] == "Inspección") & (data_r["operador_cc"].notna()) & (data_r["operador_cc"] != "N/A")]
    if data_filtrada.empty:
        return pd.DataFrame()

    resumen = data_filtrada.groupby(["operador_cc", "semana"], as_index=False)[["edificas", "aprobados", "rechazados"]].agg(np.sum)
    resumen["porcentaje_aprobacion"] = ((resumen["aprobados"] / resumen["edificas"]) * 100).round(2).astype(str) + "%"
    return resumen

def generar_resumen_calidad_operario(data_5_r):
    data_5_r = data_5_r if data_5_r is not None else pd.DataFrame()
    if data_5_r.empty:
        return pd.DataFrame()

    data_filtrada = data_5_r[data_5_r["tipo"] == "Inspección"]
    if data_filtrada.empty:
        return pd.DataFrame()

    resumen = data_filtrada.groupby(["operador_cc", "semana"], as_index=False)[["edificas", "unidades_catastrales", "aprobados", "rechazados"]].agg(np.sum)
    resumen["porcentaje_aprobacion"] = ((resumen["aprobados"] / (resumen["edificas"] + resumen["unidades_catastrales"])) * 100).round(2).astype(str) + "%"
    return resumen

# -------------------------------------------------------------------
# FUNCIONES DE VISUALIZACIÓN
# -------------------------------------------------------------------

def limpiar_placeholders(lista_placeholders):
    for ph in lista_placeholders:
        if ph is not None:
            ph.empty()

def mostrar_reporte_base(data, placeholder):
    data = data if data is not None else pd.DataFrame()
    if data.empty:
        placeholder.error("No existen reportes para mostrar")
    else:
        placeholder.dataframe(data)

def mostrar_resumen_horas(datos_horas, placeholder_tabla, placeholder_error):
    datos_horas = datos_horas if datos_horas is not None else pd.DataFrame()
    if datos_horas.empty:
        placeholder_error.error("No existen horas para mostrar")
    else:
        placeholder_tabla.dataframe(datos_horas)

def mostrar_resumen_produccion(diario, semanal, data_r, placeholder_diario, placeholder_semanal_titulo,
                               placeholder_semanal, placeholder_error):
    data_r = data_r if data_r is not None else pd.DataFrame()
    if data_r.empty:
        placeholder_error.error("No existe producción para mostrar")
        return

    diario = diario if diario is not None else pd.DataFrame()
    semanal = semanal if semanal is not None else pd.DataFrame()

    if not diario.empty:
        placeholder_diario.dataframe(diario)
    else:
        placeholder_diario.info("No hay datos diarios")

    placeholder_semanal_titulo.subheader("Resumen Semanal")
    if not semanal.empty:
        placeholder_semanal.dataframe(semanal)
    else:
        placeholder_semanal.info("No hay datos semanales")

# -------------------------------------------------------------------
# FUNCIÓN PRINCIPAL Historial_Peru (sin botón Bonos)
# -------------------------------------------------------------------

def Historial_Peru(usuario, puesto):
    nombre_df = fetch_df("SELECT nombre FROM usuarios WHERE usuario = %s", params=[usuario])
    nombre_7 = nombre_df.loc[0, 'nombre'] if not nombre_df.empty else ""

    default_date = datetime.now(pytz.timezone('America/Guatemala'))

    # --- Sidebar (sin Bonos) ---
    ph_sidebar = []
    ph_titulo = st.sidebar.empty()
    ph_titulo.title("Menú")
    ph_sidebar.append(ph_titulo)

    btn_procesos = st.sidebar.empty()
    ph_sidebar.append(btn_procesos)
    btn_capacitacion = st.sidebar.empty()
    ph_sidebar.append(btn_capacitacion)
    btn_otros = st.sidebar.empty()
    ph_sidebar.append(btn_otros)
    # btn_bonos eliminado
    btn_salir = st.sidebar.empty()
    ph_sidebar.append(btn_salir)

    # --- Contenido principal ---
    ph_main = []
    titulo_historial = st.empty()
    ph_main.append(titulo_historial)
    titulo_historial.title("Historial Perú")

    fecha_inicio = st.empty()
    ph_main.append(fecha_inicio)
    fecha_fin = st.empty()
    ph_main.append(fecha_fin)

    fecha_inicio_val = fecha_inicio.date_input("Fecha de Inicio", value=default_date, key="fecha_inicio_peru")
    fecha_fin_val = fecha_fin.date_input("Fecha de Finalización", value=default_date, key="fecha_fin_peru")

    placeholders_contenido = []

    # Filtros según perfil
    if puesto in ["Supervisor Perú", "Técnico SIG Perú", "Coordinador Perú"]:
        filtro_personal = st.empty()
        placeholders_contenido.append(filtro_personal)
        filtro_proceso = st.empty()
        placeholders_contenido.append(filtro_proceso)
        filtro_tipo = st.empty()
        placeholders_contenido.append(filtro_tipo)

        personal_sel = filtro_personal.selectbox("Personal", options=("Todos", "Operarios Perú", "Profesional Jurídico Perú", "Propio", "Personal Asignado"), key="filtro_personal_peru")
        proceso_sel = filtro_proceso.selectbox("Proceso", options=("Todos","Postcampo Folios de Matricula Inmobiliaria","Postcampo Control de Calidad FMI","Control de Calidad Folios de Matricula Inmobiliaria","Calidad Externa XTF","Consultas de Campo","Folios de Matricula Inmobiliaria","Precampo","Control de Calidad Precampo","Preparación de Insumos","Entregas Postcampo","Postcampo","Control de Calidad Postcampo","Restitución de Tierras","Revisión de Predios Segregados","Vinculación Precampo","Control de Calidad Vinculación Precampo"), key="proceso_sup_peru")
        tipo_sel = filtro_tipo.selectbox("Tipo", options=("Todos","Ordinario","Corrección","Corrección Inspección","Corrección Primera Reinspección","Reproceso Ordinario","Reproceso Corrección Inspección","Reproceso Corrección Primera Reinspección","Inspección","Reinspección","Primera Reinspección","Segunda Reinspección","Reproceso Inspección","Reproceso Primera Reinspección","Reproceso Segunda Reinspección"), key="tipo_sup_peru")

        data_r, data_c, data_o = cargar_datos_supervisor_peru(fecha_inicio_val, fecha_fin_val, personal_sel, proceso_sel, tipo_sel, nombre_7)
    else:
        filtro_proceso_op = st.empty()
        placeholders_contenido.append(filtro_proceso_op)
        filtro_tipo_op = st.empty()
        placeholders_contenido.append(filtro_tipo_op)

        proceso_sel = filtro_proceso_op.selectbox("Proceso", options=("Todos","Control de Calidad Folios de Matricula Inmobiliaria","Postcampo Control de Calidad FMI","Consultas de Campo","Postcampo Folios de Matricula Inmobiliaria","Folios de Matricula Inmobiliaria","Precampo", "Control de Calidad Precampo","Preparación de Insumos","Entregas Postcampo","Postcampo","Control de Calidad Postcampo","Restitución de Tierras","Revisión de Predios Segregados","Vinculación Precampo","Control de Calidad Vinculación Precampo"), key="proceso_op_peru")
        tipo_sel = filtro_tipo_op.selectbox("Tipo", options=("Todos","Ordinario","Corrección","Corrección Inspección","Correccion Primera Reinspección","Inspección","Reinspección","Primera Reinspección","Segunda Reinspección","Reproceso Inspección","Reproceso Primera Reinspección"), key="tipo_op_peru")

        data_1_r, data_8_r, data_6_r, data_5_r, data_1_c, data_1_o, data_6_o, data_9_o, data_7_o = cargar_datos_operario_peru(
            usuario, fecha_inicio_val, fecha_fin_val, proceso_sel, tipo_sel, nombre_7
        )
        data_r = data_1_r
        data_c = data_1_c
        data_o = data_1_o

    # --- Placeholders para resultados ---
    ph_reporte_titulo = st.empty()
    placeholders_contenido.append(ph_reporte_titulo)
    ph_reporte_data = st.empty()
    placeholders_contenido.append(ph_reporte_data)

    ph_horas_titulo = st.empty()
    placeholders_contenido.append(ph_horas_titulo)
    ph_horas_data = st.empty()
    placeholders_contenido.append(ph_horas_data)
    ph_horas_error = st.empty()
    placeholders_contenido.append(ph_horas_error)

    ph_prod_titulo = st.empty()
    placeholders_contenido.append(ph_prod_titulo)
    ph_prod_diario = st.empty()
    placeholders_contenido.append(ph_prod_diario)
    ph_prod_semanal_titulo = st.empty()
    placeholders_contenido.append(ph_prod_semanal_titulo)
    ph_prod_semanal = st.empty()
    placeholders_contenido.append(ph_prod_semanal)
    ph_prod_error = st.empty()
    placeholders_contenido.append(ph_prod_error)

    if puesto in ["Supervisor Perú", "Técnico SIG Perú", "Coordinador Perú"]:
        ph_calidad_titulo = st.empty()
        placeholders_contenido.append(ph_calidad_titulo)
        ph_calidad_data = st.empty()
        placeholders_contenido.append(ph_calidad_data)
    else:
        ph_calidad_titulo_op = st.empty()
        placeholders_contenido.append(ph_calidad_titulo_op)
        ph_calidad_data_op = st.empty()
        placeholders_contenido.append(ph_calidad_data_op)

    # --- Procesamiento y visualización ---
    ph_reporte_titulo.subheader("Reportes")
    mostrar_reporte_base(data_r, ph_reporte_data)

    ph_horas_titulo.subheader("Resumen de Horas")
    if puesto in ["Supervisor Perú", "Técnico SIG Perú", "Coordinador Perú"]:
        datos_horas = generar_resumen_horas(data_r, data_c, data_o)
    else:
        def generar_horas_operario():
            d8 = data_8_r if data_8_r is not None else pd.DataFrame()
            d6 = data_6_r if data_6_r is not None else pd.DataFrame()
            c1 = data_1_c if data_1_c is not None else pd.DataFrame()
            o9 = data_9_o if data_9_o is not None else pd.DataFrame()
            o6 = data_6_o if data_6_o is not None else pd.DataFrame()
            o7 = data_7_o if data_7_o is not None else pd.DataFrame()

            prod_normal = d8.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum).rename(columns={"horas": "horas_produccion"}) if not d8.empty else pd.DataFrame(columns=["nombre","fecha","horas_produccion"])
            prod_extra = d6.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum).rename(columns={"horas": "horas_extra_produccion"}) if not d6.empty else pd.DataFrame(columns=["nombre","fecha","horas_extra_produccion"])
            cap = c1.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum).rename(columns={"horas": "horas_capacitacion"}) if not c1.empty else pd.DataFrame(columns=["nombre","fecha","horas_capacitacion"])
            otros = o9.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum).rename(columns={"horas": "horas_otros_registros"}) if not o9.empty else pd.DataFrame(columns=["nombre","fecha","horas_otros_registros"])
            otros_extra = o6.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum).rename(columns={"horas": "horas_extra_otros_registros"}) if not o6.empty else pd.DataFrame(columns=["nombre","fecha","horas_extra_otros_registros"])
            reposicion = o7.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum).rename(columns={"horas": "reposicion"}) if not o7.empty else pd.DataFrame(columns=["nombre","fecha","reposicion"])

            combined = pd.concat([prod_normal, prod_extra, cap, otros, otros_extra], axis=0)
            if combined.empty:
                return pd.DataFrame()
            keys = combined[["nombre","fecha"]].drop_duplicates()
            merged = keys.merge(prod_normal, on=["nombre","fecha"], how="left").merge(prod_extra, on=["nombre","fecha"], how="left").merge(cap, on=["nombre","fecha"], how="left").merge(otros, on=["nombre","fecha"], how="left").merge(otros_extra, on=["nombre","fecha"], how="left").merge(reposicion, on=["nombre","fecha"], how="left").fillna(0)
            for col in ["horas_produccion","horas_capacitacion","horas_otros_registros"]:
                if col in merged.columns:
                    merged[col] = pd.to_numeric(merged[col], errors="coerce").fillna(0)
            merged["Total"] = merged["horas_produccion"] + merged["horas_capacitacion"] + merged["horas_otros_registros"]
            return merged

        datos_horas = generar_horas_operario()

    mostrar_resumen_horas(datos_horas, ph_horas_data, ph_horas_error)

    ph_prod_titulo.subheader("Resumen de Producción")
    if puesto in ["Supervisor Perú", "Técnico SIG Perú", "Coordinador Perú"]:
        diario, semanal = generar_resumen_produccion(data_r, modo_supervisor=True)
        mostrar_resumen_produccion(diario, semanal, data_r, ph_prod_diario, ph_prod_semanal_titulo,
                                   ph_prod_semanal, ph_prod_error)
    else:
        diario, semanal = generar_resumen_produccion(data_r, modo_supervisor=False)
        if data_r.empty:
            ph_prod_error.error("No existe producción para mostrar")
        else:
            ph_prod_semanal_titulo.subheader("Resumen de Producción por Proceso")
            ph_prod_semanal.dataframe(semanal)

    # Calidad
    if puesto in ["Supervisor Perú", "Técnico SIG Perú", "Coordinador Perú"]:
        ph_calidad_titulo.subheader("Resumen Calidad")
        calidad = generar_resumen_calidad(data_r)
        if calidad.empty:
            ph_calidad_data.error("No existen reportes para mostrar")
        else:
            calidad_vista = calidad.rename(columns={"edificas": "muestra"})
            ph_calidad_data.dataframe(calidad_vista)
    else:
        ph_calidad_titulo_op.subheader("Resumen Calidad")
        calidad_op = generar_resumen_calidad_operario(data_5_r)
        if calidad_op.empty:
            ph_calidad_data_op.error("No existen reportes para mostrar")
        else:
            calidad_vista = calidad_op.rename(columns={"unidades_catastrales": "muestra unidades catastrales", "edificas": "muestra edificas"})
            ph_calidad_data_op.dataframe(calidad_vista)

    # --- Navegación (sin Bonos) ---
    if btn_procesos.button("Procesos", key="procesos_hist_peru"):
        limpiar_placeholders(ph_sidebar + ph_main + placeholders_contenido)
        st.session_state.Historial = False
        perfil_df = fetch_df("SELECT perfil FROM usuarios WHERE usuario = %s", params=[usuario])
        perfil = str(perfil_df.loc[0, 'perfil']) if not perfil_df.empty else "1"
        if perfil == "1":
            Procesos.Procesos1(usuario, puesto)
        elif perfil == "2":
            Procesos.Procesos2(usuario, puesto)
        else:
            Procesos.Procesos3(usuario, puesto)

    elif btn_capacitacion.button("Capacitaciones", key="capacitacion_hist_peru"):
        limpiar_placeholders(ph_sidebar + ph_main + placeholders_contenido)
        st.session_state.Historial = False
        st.session_state.Capacitacion = True
        Capacitacion.Capacitacion(usuario, puesto)

    elif btn_otros.button("Otros Registros", key="otros_hist_peru"):
        limpiar_placeholders(ph_sidebar + ph_main + placeholders_contenido)
        st.session_state.Historial = False
        st.session_state.Otros_Registros = True
        Otros_Registros.Otros_Registros(usuario, puesto)

    # El botón de Bonos ha sido eliminado

    elif btn_salir.button("Salir", key="salir_hist_peru"):
        limpiar_placeholders(ph_sidebar + ph_main + placeholders_contenido)
        st.session_state.Ingreso = False
        st.session_state.Historial = False
        st.session_state.Salir = True
        Salir.Salir()
