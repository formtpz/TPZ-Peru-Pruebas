# ----- Librerías -----
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

import Procesos
from db_core import fetch_df, fetch_one, execute


def limpiar_placeholders(lista_placeholders):
    """Vacía todos los placeholders proporcionados."""
    for ph in lista_placeholders:
        if ph is not None:
            ph.empty()


def navegar_a_procesos(usuario, puesto):
    """Determina el perfil y redirige a la función correspondiente de Procesos."""
    perfil_info = fetch_one(
        "SELECT perfil FROM usuarios WHERE usuario = %s",
        params=[usuario]
    )
    perfil = str(perfil_info["perfil"]) if perfil_info else "1"

    if perfil == "1":
        Procesos.Procesos1(usuario, puesto)
    elif perfil == "2":
        Procesos.Procesos2(usuario, puesto)
    else:
        Procesos.Procesos3(usuario, puesto)


def Capacitacion(usuario, puesto):
    # Obtener nombre completo del usuario
    nombre_df = fetch_df("SELECT nombre FROM usuarios WHERE usuario = %s", params=[usuario])
    nombre_completo = nombre_df.loc[0, 'nombre'] if not nombre_df.empty else ""

    # --- Sidebar ---
    ph_sidebar = []
    ph_titulo = st.sidebar.empty()
    ph_titulo.title("Menú")
    ph_sidebar.append(ph_titulo)

    btn_procesos = st.sidebar.empty()
    ph_sidebar.append(btn_procesos)
    btn_historial = st.sidebar.empty()
    ph_sidebar.append(btn_historial)
    btn_otros = st.sidebar.empty()
    ph_sidebar.append(btn_otros)
    btn_bonos = st.sidebar.empty()
    ph_sidebar.append(btn_bonos)
    btn_salir = st.sidebar.empty()
    ph_sidebar.append(btn_salir)

    # --- Contenido principal ---
    ph_main = []
    titulo = st.empty()
    ph_main.append(titulo)
    titulo.title("Registro de Capacitaciones")

    # Formulario de registro
    with st.form(key="form_capacitacion", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input(
                "Fecha",
                value=datetime.now(pytz.timezone("America/Guatemala")),
                key="fecha_cap"
            )
        with col2:
            tema = st.text_input("Tema de la capacitación", max_chars=100, key="tema_cap")

        horas = st.number_input("Horas", min_value=0.0, step=0.25, key="horas_cap")
        observaciones = st.text_area("Observaciones", value="N/A", max_chars=200, key="obs_cap")
        enviar = st.form_submit_button("Registrar Capacitación")

        if enviar:
            if tema.strip() == "":
                st.error("Debe ingresar el tema de la capacitación.")
            elif horas <= 0:
                st.error("Las horas deben ser mayores a 0.")
            else:
                marca = datetime.now(pytz.timezone("America/Guatemala")).strftime("%Y-%m-%d %H:%M:%S")
                execute(
                    """
                    INSERT INTO capacitaciones (
                        marca, usuario, nombre, puesto, supervisor,
                        fecha, tema, horas, observaciones
                    )
                    VALUES (%s, %s, %s, %s, (SELECT supervisor FROM usuarios WHERE usuario = %s), %s, %s, %s, %s)
                    """,
                    params=[
                        marca, usuario, nombre_completo, puesto, usuario,
                        fecha, tema.strip(), horas, observaciones
                    ]
                )
                st.success("Capacitación registrada correctamente.")
                st.rerun()

    # Historial de capacitaciones del usuario (últimos 30 días)
    st.subheader("📋 Mis capacitaciones recientes")
    fecha_limite = datetime.now().date() - pd.Timedelta(days=30)
    historial = fetch_df(
        """
        SELECT fecha, tema, horas, observaciones
        FROM capacitaciones
        WHERE usuario = %s AND fecha::date >= %s
        ORDER BY fecha DESC
        """,
        params=[usuario, fecha_limite]
    )
    if historial.empty:
        st.info("No hay capacitaciones registradas en los últimos 30 días.")
    else:
        st.dataframe(historial, use_container_width=True)

    # --- Navegación ---
    if btn_procesos.button("Procesos", key="procesos_cap"):
        limpiar_placeholders(ph_sidebar + ph_main)
        st.session_state.Capacitacion = False
        navegar_a_procesos(usuario, puesto)

    elif btn_historial.button("Historial", key="historial_cap"):
        limpiar_placeholders(ph_sidebar + ph_main)
        st.session_state.Capacitacion = False
        st.session_state.Historial = True
        import Historial
        Historial.Historial(usuario, puesto)

    elif btn_otros.button("Otros Registros", key="otros_cap"):
        limpiar_placeholders(ph_sidebar + ph_main)
        st.session_state.Capacitacion = False
        st.session_state.Otros_Registros = True
        import Otros_Registros
        Otros_Registros.Otros_Registros(usuario, puesto)

    elif btn_bonos.button("Bonos y Horas Extras", key="bonos_cap"):
        limpiar_placeholders(ph_sidebar + ph_main)
        st.session_state.Capacitacion = False
        st.session_state.Bonos_Extras = True
        import Bonos_Extras
        Bonos_Extras.Bonos_Extras(usuario, puesto)

    elif btn_salir.button("Salir", key="salir_cap"):
        limpiar_placeholders(ph_sidebar + ph_main)
        st.session_state.Ingreso = False
        st.session_state.Capacitacion = False
        st.session_state.Salir = True
        import Salir
        Salir.Salir()
