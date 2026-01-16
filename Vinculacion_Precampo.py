# ----- Librerías ---- #

import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import pytz
from urllib.parse import urlparse
import Procesos,Historial,Capacitacion,Otros_Registros,Bonos_Extras,Salir
from Autenticacion import hostname, database, username, pwd, port_id, con


def Vinculacion_Precampo(usuario, puesto):

    # ----- Conexión, Botones y Memoria ---- #
    uri = st.secrets.db_credentials.URI

    placeholder1_3 = st.sidebar.empty()
    placeholder1_3.title("Menú")

    placeholder2_3 = st.sidebar.empty()
    procesos_3 = placeholder2_3.button("Procesos", key="procesos_3")

    placeholder3_3 = st.sidebar.empty()
    historial_3 = placeholder3_3.button("Historial", key="historial_3")

    placeholder4_3 = st.sidebar.empty()
    capacitacion_3 = placeholder4_3.button("Capacitaciones", key="capacitacion_3")

    placeholder5_3 = st.sidebar.empty()
    otros_registros_3 = placeholder5_3.button("Otros Registros", key="otros_registros_3")

    placeholder6_3 = st.sidebar.empty()
    bonos_extras_3 = placeholder6_3.button("Bonos y Hoas Extras", key="bonos_extras_3")

    placeholder7_3 = st.sidebar.empty()
    salir_3 = placeholder7_3.button("Salir", key="salir_3")

    placeholder8_3 = st.empty()
    placeholder8_3.title("Vinculación Precampo")

    default_date_3 = datetime.now(pytz.timezone('America/Guatemala'))

    placeholder9_3 = st.empty()
    fecha_3 = placeholder9_3.date_input("Fecha", value=default_date_3, key="fecha_3")

    placeholder10_3 = st.empty()
    distrito_3 = placeholder10_3.selectbox(
        "Distrito",
        options=("Chorrillos", "San Juan De Miraflores", "Villa el Salvador"),
        key="distrito_3"
    )

    placeholder12_3 = st.empty()
    sector_3 = placeholder12_3.selectbox(
        "Sector",
        options=[f"{i:02d}" for i in range(1, 121)],
        key="sector_3"
    )

    placeholder13_3 = st.empty()
    manzana_3 = placeholder13_3.selectbox(
        "Manzana",
        options=[f"{i:03d}" for i in range(1, 121)],
        key="manzana_3"
    )

    placeholder15_3 = st.empty()
    tipo_3 = placeholder15_3.selectbox(
        "Tipo",
        options=(
            "Ordinario",
            "Reproceso Ordinario",
            "Corrección de Calidad",
            "Corrección de Calidad Extraordinaria",
            "Producción Horas Extras"
        ),
        key="tipo_3"
    )

    placeholder16_3 = st.empty()
    estado_3 = placeholder16_3.selectbox(
        "Estado",
        options=("Finalizado", "En Conflicto"),
        key="estado_3"
    )

    placeholder18_3 = st.empty()
    numero_lote_3 = placeholder18_3.selectbox(
        "Número de lote",
        options=[f"{i:03d}" for i in range(1, 249)],
        key="numero_lote_3"
    )

    # ===== NUEVO SELECTOR EXCLUSIVO =====
    placeholder19a_3 = st.empty()
    modo_proceso_3 = placeholder19a_3.radio(
        "Tipo de Vinculación",
        options=("Vinculación Precampo", "Puntos Jurídicos"),
        index=0,
        key="modo_proceso_3"
    )

    # ===== UNIDADES CATASTRALES (CONDICIONAL) =====
    placeholder20_3 = st.empty()

    if modo_proceso_3 == "Puntos Jurídicos":
        placeholder20_3.empty()
        unidades_catastrales_3 = 0
    else:
        unidades_catastrales_3 = placeholder20_3.number_input(
            "Cantidad de Unidades Catrastales",
            min_value=0,
            step=1,
            key="unidades_catastrales_3"
        )

    placeholder21_3 = st.empty()
    horas_3 = placeholder21_3.number_input(
        "Cantidad de Horas Trabajadas en el Proceso",
        min_value=0.0,
        key="horas_3"
    )

    placeholder22_3 = st.empty()
    observaciones_3 = placeholder22_3.text_input(
        "Observaciones",
        value="N/A",
        max_chars=60,
        key="observaciones_3"
    )

    placeholder23_3 = st.empty()
    reporte_3 = placeholder23_3.button("Generar Reporte", key="reporte_3")

    # ===================== PROCESOS ===================== #

    if procesos_3 or historial_3 or capacitacion_3 or otros_registros_3 or bonos_extras_3 or salir_3:
        for p in [
            placeholder1_3, placeholder2_3, placeholder3_3, placeholder4_3,
            placeholder5_3, placeholder6_3, placeholder7_3, placeholder8_3,
            placeholder9_3, placeholder10_3, placeholder12_3, placeholder13_3,
            placeholder15_3, placeholder16_3, placeholder18_3, placeholder19a_3,
            placeholder20_3, placeholder21_3, placeholder22_3, placeholder23_3
        ]:
            p.empty()

    if procesos_3:
        perfil = pd.read_sql(f"select perfil from usuarios where usuario='{usuario}'", uri).loc[0, 'perfil']
        if perfil == "1":
            Procesos.Procesos1(usuario, puesto)
        elif perfil == "2":
            Procesos.Procesos2(usuario, puesto)
        elif perfil == "3":
            Procesos.Procesos3(usuario, puesto)

    elif historial_3:
        Historial.Historial(usuario, puesto)

    elif capacitacion_3:
        Capacitacion.Capacitacion(usuario, puesto)

    elif otros_registros_3:
        Otros_Registros.Otros_Registros(usuario, puesto)

    elif bonos_extras_3:
        Bonos_Extras.Bonos_Extras(usuario, puesto)

    elif salir_3:
        Salir.Salir()

    # ===================== INSERT ===================== #

    elif reporte_3:

        cursor01 = con.cursor()

        marca_3 = datetime.now(pytz.timezone('America/Guatemala')).strftime("%Y-%m-%d %H:%M:%S")

        nombre_3 = pd.read_sql(f"select nombre from usuarios where usuario='{usuario}'", uri).loc[0, 'nombre']
        supervisor_3 = pd.read_sql(f"select supervisor from usuarios where usuario='{usuario}'", uri).loc[0, 'supervisor']

        semana_3 = fecha_3.isocalendar()[1]
        año_3 = fecha_3.isocalendar()[0]
        horas_bi = float(horas_3)

        # ===== PROCESO FINAL =====
        if modo_proceso_3 == "Puntos Jurídicos":
            proceso_final_3 = "Vinculación Precampo Puntos Juridicos"
        else:
            proceso_final_3 = "Vinculación Precampo"

        cursor01.execute(f"""
            INSERT INTO registro (
                marca, usuario, nombre, puesto, supervisor, proceso, fecha,
                semana, año, distrito, tipo, lotes, aprobados, rechazados,
                horas, manzana, sector, numero_lote, estado, area,
                unidades_catastrales, edificas, partida, con_fmi, sin_fmi,
                observaciones, zona, tipo_calidad, horas_bi, area_bi,
                operador_cc, total_de_errores, errores_por_excepciones,
                tipo_de_errores, conteo_de_errores
            ) VALUES (
                '{marca_3}', '{usuario}', '{nombre_3}', '{puesto}', '{supervisor_3}',
                '{proceso_final_3}', '{fecha_3}', '{semana_3}', '{año_3}',
                '{distrito_3}', '{tipo_3}', '0', '0', '0', '{horas_3}',
                '{manzana_3}', '{sector_3}', '{numero_lote_3}', '{estado_3}',
                '0.0', '{unidades_catastrales_3}', '0', 'N/A', '0', '0',
                '{observaciones_3}', 'N/A', 'N/A', '{horas_bi}', '0.0',
                'N/A', '0', '0', 'N/A', '0'
            )
        """)

        con.commit()
        st.success("Reporte enviado correctamente")
