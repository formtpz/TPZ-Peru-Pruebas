# ----- Librerías ---- #
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

import Procesos, Historial, Capacitacion, Bonos_Extras, Salir
import historial_peru  # <-- NUEVO
from db_core import fetch_df, fetch_one, execute

# Constante para puestos peruanos
PUESTOS_PERUANOS = ("Supervisor Perú", "Operario Perú", "Coordinador Perú")

def obtener_modulo_historial(puesto):
    """Retorna el módulo de historial adecuado según el puesto."""
    if puesto in PUESTOS_PERUANOS:
        return historial_peru.Historial_Peru
    else:
        return Historial.Historial

def limpiar_placeholders(lista_placeholders):
    """Vacía todos los placeholders proporcionados."""
    for ph in lista_placeholders:
        if ph is not None:
            ph.empty()


def navegar_a_procesos(usuario, puesto):
    """Determina el perfil y redirige a la función correspondiente de Procesos."""
    usuario_activo = fetch_one(
        "SELECT perfil FROM usuarios WHERE usuario = %s",
        params=[usuario]
    )
    perfil = str(usuario_activo["perfil"]) if usuario_activo else "1"

    if perfil == "1":
        Procesos.Procesos1(usuario, puesto)
    elif perfil == "2":
        Procesos.Procesos2(usuario, puesto)
    else:
        Procesos.Procesos3(usuario, puesto)


def cargar_historial_otros(filtro, fecha_inicio, fecha_fin, usuario, nombre_usuario, puesto):
    """
    Carga el historial de 'otros_registros' según el filtro seleccionado.
    Versión adaptada para puestos peruanos.
    """
    base_query = """
        SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor,
               fecha, motivo, horas, observaciones, reporte
        FROM otros_registros
        WHERE fecha::date >= %s AND fecha::date <= %s
    """
    params = [fecha_inicio, fecha_fin]

    # Determinar si el usuario es peruano para ajustar los nombres de puestos
    es_peruano = puesto in PUESTOS_PERUANOS
    if es_peruano:
        # Si es peruano, usar puestos con sufijo " Perú"
        puesto_operario = "Operario Perú"
        puesto_profesional = "Profesional Jurídico Perú"
        # Nota: el filtro "Personal Asignado" sigue usando supervisor, pero solo mostrará peruanos
    else:
        puesto_operario = "Operario Catastral"
        puesto_profesional = "Profesional Jurídico"

    if filtro == "Todos":
        query = base_query
    elif filtro == "Operarios" or filtro == "Operarios Perú":
        # Si el filtro es "Operarios" o "Operarios Perú", usamos la variable dinámica
        query = base_query + f" AND puesto = %s"
        params.append(puesto_operario)
    elif filtro == "Profesional Jurídico" or filtro == "Profesional Jurídico Perú":
        query = base_query + f" AND puesto = %s"
        params.append(puesto_profesional)
    elif filtro == "Propio":
        query = base_query + " AND usuario = %s"
        params.append(usuario)
    elif filtro == "Personal Asignado":
        query = base_query + " AND supervisor = %s"
        params.append(nombre_usuario)
    elif filtro == "Reportados":
        query = base_query + " AND reporte = %s"
        params.append(nombre_usuario)
    elif filtro == "Personal Reciente":
        # Solo aplica para Supervisores (independientemente de si es peruano o no)
        supervisor_data = fetch_one(
            """
            SELECT proceso, subproceso 
            FROM usuarios 
            WHERE nombre = %s AND estado = 'Activo'
            """,
            params=[nombre_usuario]
        )
        
        if supervisor_data and supervisor_data["proceso"] and supervisor_data["subproceso"]:
            usuarios_recientes = fetch_df(
                """
                SELECT nombre 
                FROM usuarios 
                WHERE proceso_anterior = %s 
                  AND subproceso_anterior = %s 
                  AND activo_en_listas = 'activo'
                  AND usuario != %s
                  AND estado = 'Activo'
                """,
                params=[supervisor_data["proceso"], supervisor_data["subproceso"], usuario]
            )
            
            if not usuarios_recientes.empty:
                nombres_recientes = usuarios_recientes["nombre"].tolist()
                placeholders = ', '.join(['%s'] * len(nombres_recientes))
                query = base_query + f" AND nombre IN ({placeholders})"
                params.extend(nombres_recientes)
            else:
                return pd.DataFrame()
        else:
            return pd.DataFrame()
    else:
        return pd.DataFrame()

    return fetch_df(query, params=params)


def Otros_Registros(usuario, puesto):
    # Obtener nombre completo del usuario
    nombre_df = fetch_df("SELECT nombre FROM usuarios WHERE usuario = %s", params=[usuario])
    nombre_13 = nombre_df.loc[0, 'nombre'] if not nombre_df.empty else ""

    # Fecha por defecto
    default_date = datetime.now(pytz.timezone('America/Guatemala'))

    # --- Sidebar ---
    ph_sidebar = []
    ph_titulo = st.sidebar.empty()
    ph_titulo.title("Menú")
    ph_sidebar.append(ph_titulo)

    btn_procesos = st.sidebar.empty()
    ph_sidebar.append(btn_procesos)
    btn_historial = st.sidebar.empty()
    ph_sidebar.append(btn_historial)
    btn_capacitacion = st.sidebar.empty()
    ph_sidebar.append(btn_capacitacion)
    
    # Botón de Bonos solo si NO es peruano
    if puesto not in PUESTOS_PERUANOS:
        btn_bonos = st.sidebar.empty()
        ph_sidebar.append(btn_bonos)
    else:
        btn_bonos = None  # No se muestra

    btn_salir = st.sidebar.empty()
    ph_sidebar.append(btn_salir)

    # --- Contenido principal ---
    ph_main = []
    titulo = st.empty()
    ph_main.append(titulo)
    titulo.title("Otros Registros")

    # Placeholders que se usarán condicionalmente
    placeholders_contenido = []

    # Variables que se usarán en la navegación
    personal_13 = []
    fecha_13 = default_date
    motivo_13 = ""
    horas_13 = 0.0
    observaciones_13 = ""
    data_historial = pd.DataFrame()

    # ---------------------------
    # PERFIL COORDINADOR / SUPERVISOR (incluyendo peruanos)
    # ---------------------------
    # Vamos a considerar que tanto "Coordinador" como "Coordinador Perú" y "Supervisor" como "Supervisor Perú"
    # deben tener el mismo comportamiento de registro y filtros.
    es_supervisor_peru = puesto in ["Supervisor Perú", "Supervisor"]
    es_coordinador_peru = puesto in ["Coordinador Perú", "Coordinador"]
    es_peruano = puesto in PUESTOS_PERUANOS

    if puesto in ["Coordinador", "Supervisor"] or es_peruano:
        # Registro
        ph_sub_registro = st.empty()
        placeholders_contenido.append(ph_sub_registro)
        ph_sub_registro.subheader("Registro")

        # Obtener lista de personal (adaptado para peruanos)
        if es_coordinador_peru or puesto == "Coordinador":
            # Para Coordinador (normal o Perú): mostrar todos los activos, pero si es Perú, filtrar por puestos peruanos
            if es_peruano:
                data_personal = fetch_df(
                    "SELECT nombre FROM usuarios WHERE estado = 'Activo' AND puesto IN %s",
                    params=[PUESTOS_PERUANOS]
                )
            else:
                data_personal = fetch_df("SELECT nombre FROM usuarios WHERE estado = 'Activo'")
        else:  # Supervisor (normal o Perú)
            # Base: personal asignado al supervisor (supervisor = nombre_usuario) o el mismo supervisor
            data_personal = fetch_df(
                "SELECT nombre FROM usuarios WHERE estado = 'Activo' AND (supervisor = %s OR usuario = %s)",
                params=[nombre_13, usuario]
            )
            # Si es Supervisor Perú, además filtrar por puestos peruanos
            if es_peruano:
                # Filtramos después de obtener para mantener solo los peruanos
                data_personal = data_personal[data_personal["puesto"].isin(PUESTOS_PERUANOS)]
            
            # Agregar "Personal Reciente" si existe (para Supervisores, sin importar si es peruano)
            supervisor_data = fetch_one(
                """
                SELECT proceso, subproceso 
                FROM usuarios 
                WHERE nombre = %s AND estado = 'Activo'
                """,
                params=[nombre_13]
            )
            if supervisor_data and supervisor_data["proceso"] and supervisor_data["subproceso"]:
                personal_reciente = fetch_df(
                    """
                    SELECT nombre 
                    FROM usuarios 
                    WHERE proceso_anterior = %s 
                      AND subproceso_anterior = %s 
                      AND activo_en_listas = 'activo'
                      AND usuario != %s
                      AND estado = 'Activo'
                    """,
                    params=[supervisor_data["proceso"], supervisor_data["subproceso"], usuario]
                )
                if not personal_reciente.empty:
                    # Si es Perú, también filtrar por puestos peruanos
                    if es_peruano:
                        personal_reciente = personal_reciente[personal_reciente["puesto"].isin(PUESTOS_PERUANOS)]
                    data_personal = pd.concat([data_personal, personal_reciente]).drop_duplicates()
        
        nombres_personal = data_personal["nombre"].tolist() if not data_personal.empty else []

        ph_personal = st.empty()
        placeholders_contenido.append(ph_personal)
        personal_13 = ph_personal.multiselect("Personal", nombres_personal, key="personal_13")

        ph_fecha = st.empty()
        placeholders_contenido.append(ph_fecha)
        fecha_13 = ph_fecha.date_input("Fecha", value=default_date, key="fecha_13")

        ph_motivo = st.empty()
        placeholders_contenido.append(ph_motivo)
        motivo_13 = ph_motivo.selectbox(
            "Motivo",
            options=(
                "Reposición de tiempo", "Cita CCSS", "Entregas", "Incapacidad",
                "Control de Calidad Masivos", "Fallos en Aplicativo o Conexión", "Horas Extras",
                "Licencia por Fallecimiento de Familiar", "Licencia por Maternidad, Paternidad o Lactancia",
                "Reunión", "Supervisión", "Vacaciones", "Horas Extra Apoyo Otros Proyectos",
                "Horas Ordinarias Apoyo a Otros Proyectos", "Otros"
            ),
            key="motivo_13"
        )

        ph_horas = st.empty()
        placeholders_contenido.append(ph_horas)
        horas_13 = ph_horas.number_input("Cantidad de Horas Individuales", min_value=0.0, step=0.25, key="horas_13")

        ph_observaciones = st.empty()
        placeholders_contenido.append(ph_observaciones)
        observaciones_13 = ph_observaciones.text_input("Observaciones", max_chars=60, key="observaciones_13")

        ph_reporte = st.empty()
        placeholders_contenido.append(ph_reporte)
        reporte_btn = ph_reporte.button("Generar Reporte", key="reporte_13")
        
        ph_mensaje = st.empty()
        placeholders_contenido.append(ph_mensaje)
        
        if reporte_btn:
            if not personal_13:
                ph_mensaje.error("Favor ingresar el nombre de alguna persona")
            else:
                try:
                    for nombre in personal_13:
                        marca = datetime.now(pytz.timezone('America/Guatemala')).strftime("%Y-%m-%d %H:%M:%S")
                        persona = fetch_one(
                            "SELECT usuario, puesto, supervisor FROM usuarios WHERE nombre = %s LIMIT 1",
                            params=[nombre]
                        )
                        if not persona:
                            continue

                        execute(
                            """
                            INSERT INTO otros_registros (
                                marca, usuario, nombre, puesto, supervisor,
                                fecha, motivo, horas, observaciones, reporte, horas_bi
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """,
                            params=[
                                marca, persona["usuario"], nombre, persona["puesto"], persona["supervisor"],
                                fecha_13, motivo_13, horas_13, observaciones_13, nombre_13, float(horas_13)
                            ]
                        )
                    ph_mensaje.success("✅ Registro enviado correctamente")
                except Exception as e:
                    ph_mensaje.error(f"❌ Error al guardar: {str(e)}")

        ph_separador = st.empty()
        placeholders_contenido.append(ph_separador)
        ph_separador.markdown("_____")

        # Historial
        ph_sub_historial = st.empty()
        placeholders_contenido.append(ph_sub_historial)
        ph_sub_historial.subheader("Historial")

        ph_fecha_inicio = st.empty()
        placeholders_contenido.append(ph_fecha_inicio)
        fecha_inicio_val = ph_fecha_inicio.date_input("Fecha de Inicio", value=default_date, key="fecha_inicio_13")

        ph_fecha_fin = st.empty()
        placeholders_contenido.append(ph_fecha_fin)
        fecha_fin_val = ph_fecha_fin.date_input("Fecha de Finalización", value=default_date, key="fecha_fin_13")

        ph_filtro = st.empty()
        placeholders_contenido.append(ph_filtro)
        
        # Construir opciones de filtro según el puesto
        # Si es peruano, usamos etiquetas con "Perú"
        if es_peruano:
            sufijo = " Perú"
            op_base = ["Todos", "Operarios" + sufijo, "Profesional Jurídico" + sufijo]
        else:
            op_base = ["Todos", "Operarios", "Profesional Jurídico"]
        
        opciones_filtro = op_base + ["Propio", "Personal Asignado", "Reportados"]
        
        # Solo Supervisores (normales o peruanos) tienen "Personal Reciente"
        if puesto in ["Supervisor", "Supervisor Perú"]:
            opciones_filtro.append("Personal Reciente")
        
        filtro_val = ph_filtro.selectbox(
            "Filtro",
            options=opciones_filtro,
            key="filtro_13"
        )
        
        # Mostrar información sobre "Personal Reciente"
        if filtro_val == "Personal Reciente":
            supervisor_info = fetch_one(
                """
                SELECT proceso, subproceso 
                FROM usuarios 
                WHERE nombre = %s AND estado = 'Activo'
                """,
                params=[nombre_13]
            )
            if supervisor_info:
                ph_info_reciente = st.empty()
                placeholders_contenido.append(ph_info_reciente)
                ph_info_reciente.info(
                    f"📋 Mostrando personal que anteriormente estuvo en: "
                    f"Proceso '{supervisor_info['proceso']}' - "
                    f"Subproceso '{supervisor_info['subproceso']}'"
                )

        # Cargar historial según filtros, pasando el puesto para determinar los puestos peruanos
        data_historial = cargar_historial_otros(
            filtro_val, fecha_inicio_val, fecha_fin_val, usuario, nombre_13, puesto
        )

    # ---------------------------
    # PERFIL OPERARIO / PROFESIONAL JURÍDICO / QC (incluyendo peruanos)
    # ---------------------------
    else:
        ph_sub_historial = st.empty()
        placeholders_contenido.append(ph_sub_historial)
        ph_sub_historial.subheader("Historial")

        ph_fecha_inicio = st.empty()
        placeholders_contenido.append(ph_fecha_inicio)
        fecha_inicio_val = ph_fecha_inicio.date_input("Fecha de Inicio", value=default_date, key="fecha_inicio_13")

        ph_fecha_fin = st.empty()
        placeholders_contenido.append(ph_fecha_fin)
        fecha_fin_val = ph_fecha_fin.date_input("Fecha de Finalización", value=default_date, key="fecha_fin_13")

        data_historial = fetch_df(
            """
            SELECT cast(id as integer), marca, usuario, nombre, puesto, supervisor,
                   fecha, motivo, horas, observaciones, reporte
            FROM otros_registros
            WHERE usuario = %s AND fecha::date >= %s AND fecha::date <= %s
            ORDER BY fecha DESC
            """,
            params=[usuario, fecha_inicio_val, fecha_fin_val]
        )

    # Mostrar DataFrame de historial
    ph_dataframe = st.empty()
    placeholders_contenido.append(ph_dataframe)
    if data_historial.empty:
        ph_dataframe.info("No hay registros para el período seleccionado.")
    else:
        ph_dataframe.dataframe(data_historial, use_container_width=True)

    # ---------------------------
    # Navegación
    # ---------------------------
    if btn_procesos.button("Procesos", key="procesos_13"):
        limpiar_placeholders(ph_sidebar + ph_main + placeholders_contenido)
        st.session_state.Otros_Registros = False
        navegar_a_procesos(usuario, puesto)

    elif btn_historial.button("Historial", key="historial_13"):
        limpiar_placeholders(ph_sidebar + ph_main + placeholders_contenido)
        st.session_state.Otros_Registros = False
        st.session_state.Historial = True
        # Llamar al módulo de historial adecuado
        modulo_hist = obtener_modulo_historial(puesto)
        modulo_hist(usuario, puesto)

    elif btn_capacitacion.button("Capacitaciones", key="capacitacion_13"):
        limpiar_placeholders(ph_sidebar + ph_main + placeholders_contenido)
        st.session_state.Otros_Registros = False
        st.session_state.Capacitacion = True
        Capacitacion.Capacitacion(usuario, puesto)

    # Botón de Bonos solo existe si no es peruano
    elif btn_bonos is not None and btn_bonos.button("Bonos y Horas Extra", key="bonos_13"):
        limpiar_placeholders(ph_sidebar + ph_main + placeholders_contenido)
        st.session_state.Otros_Registros = False
        st.session_state.Bonos_Extras = True
        Bonos_Extras.Bonos_Extras(usuario, puesto)

    elif btn_salir.button("Salir", key="salir_13"):
        limpiar_placeholders(ph_sidebar + ph_main + placeholders_contenido)
        st.session_state.Ingreso = False
        st.session_state.Otros_Registros = False
        st.session_state.Salir = True
        Salir.Salir()
