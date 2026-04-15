# ----- Librerías ---- #
import streamlit as st
import time

import Historial, Capacitacion, Otros_Registros, Correcciones, Bonos_Extras, Salir
import Precampo_Juridico, Descarga_Partidas_Juridico, Asignacion_Partidas
import CC_Precampo_Juridico, Estado_UIT_Hito
import Precampo, CC_Precampo, Preparacion_Insumos
import Entregas_Postcampo, Postcampo, CC_Postcampo, CC_Vinculacion_Precampo
import Vinculacion_Precampo

from Autenticacion import obtener_usuario_activo

# ------------------- AUTO REFRESH (igual que original) ------------------- #
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if time.time() - st.session_state.start_time > 29 * 60:
    st.session_state.clear()
    st.rerun()

def auto_refresh(seconds=30600):
    st.markdown(
        f'<meta http-equiv="refresh" content="{seconds}">',
        unsafe_allow_html=True
    )
auto_refresh(30600)

# ------------------- UTILIDAD COMÚN ------------------- #
def limpiar(placeholders):
    """Vacía una lista de placeholders de Streamlit."""
    for p in placeholders:
        p.empty()

# =========================================================
# ===================== PROCESOS 1 (Campo) =================
# =========================================================
def Procesos1(usuario, puesto):
    st.session_state.Ingreso = True
    obtener_usuario_activo(usuario)  # opcional: cachea el usuario activo

    if not st.session_state.Procesos:
        # ---------- Sidebar ----------
        ph1 = st.sidebar.empty(); ph1.title("Menú")
        ph2 = st.sidebar.empty(); btn_historial = ph2.button("Historial", key="historial_2")
        ph3 = st.sidebar.empty(); btn_capacitacion = ph3.button("Capacitaciones", key="capacitacion_2")
        ph4 = st.sidebar.empty(); btn_otros = ph4.button("Otros Registros", key="otros_registros_2")
        ph5 = st.sidebar.empty(); btn_bonos = ph5.button("Bonos y Horas Extras", key="bonos_extras_2")
        ph_corr = st.sidebar.empty(); btn_correcciones = ph_corr.button("Solicitud Correcciones", key="correcciones")
        ph6 = st.sidebar.empty(); btn_salir = ph6.button("Salir", key="salir_2")

        # ---------- Main: botones de procesos ----------
        ph7 = st.empty(); ph7.title("Procesos")
        ph8 = st.empty(); btn_pj = ph8.button(":orange[Precampo Jurídico]", key="precampo_juridico_2")
        ph9 = st.empty(); btn_dp = ph9.button(":orange[Descarga Partidas Jurídico]", key="descarga_partidas_juridico_2")
        ph10 = st.empty(); btn_ccpj = ph10.button(":orange[Control de Calidad Precampo Jurídico]", key="cc_precampo_juridico_2")
        ph11 = st.empty(); btn_asig = ph11.button(":orange[Asignación de Partidas]", key="asignacion_partidas")
        ph12 = st.empty(); btn_precampo = ph12.button(":green[Precampo]", key="precampo_2")
        ph13 = st.empty(); btn_cc_pre = ph13.button(":green[Control de Calidad Precampo]", key="cc_precampo_2")
        ph14 = st.empty(); btn_vin = ph14.button(":blue[Vinculación Precampo]", key="vinculacion_precampo_2")
        ph15 = st.empty(); btn_prep = ph15.button(":gray[Preparación de Insumos]", key="preparacion_insumos_2")
        ph16 = st.empty(); btn_ent = ph16.button(":gray[Entregas Postcampo]", key="entregas_2")
        ph17 = st.empty(); btn_post = ph17.button(":blue[Postcampo]", key="postcampo_2")
        ph18 = st.empty(); btn_cc_post = ph18.button(":blue[Control de Calidad Postcampo]", key="cc_postcampo_2")
        ph19 = st.empty(); btn_cc_vin = ph19.button(":green[Control de Calidad Vinculación Precampo]", key="cc_vinculacion_precampo_2")
        ph20 = st.empty(); btn_estado = ph20.button("Calidad Interna XTF", key="estado_uit_hito_2")

        placeholders = [ph1,ph2,ph3,ph4,ph5,ph_corr,ph6,ph7,ph8,ph9,ph10,ph11,ph12,ph13,ph14,ph15,ph16,ph17,ph18,ph19,ph20]

        # ---------- Navegación ----------
        if btn_historial:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Historial = True
            Historial.Historial(usuario, puesto)

        elif btn_capacitacion:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Capacitacion = True
            Capacitacion.Capacitacion(usuario, puesto)

        elif btn_otros:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Otros_Registros = True
            Otros_Registros.Otros_Registros(usuario, puesto)

        elif btn_bonos:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Bonos_Extras = True
            Bonos_Extras.Bonos_Extras(usuario, puesto)

        elif btn_correcciones:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Correcciones = True
            Correcciones.Correcciones(usuario, puesto)

        elif btn_salir:
            limpiar(placeholders)
            st.session_state.Ingreso = False
            st.session_state.Procesos = True
            st.session_state.Salir = True
            Salir.Salir()

        elif btn_pj:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Precampo_Juridico = True
            Precampo_Juridico.Precampo_Juridico(usuario, puesto)

        elif btn_dp:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Descarga_Partidas_Juridico = True
            Descarga_Partidas_Juridico.Descarga_Partidas_Juridico(usuario, puesto)

        elif btn_ccpj:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.CC_Precampo_Juridico = True
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario, puesto)

        elif btn_asig:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Asignacion_Partidas = True
            Asignacion_Partidas.Asignacion_Partidas(usuario, puesto)

        elif btn_precampo:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Precampo = True
            Precampo.Precampo(usuario, puesto)

        elif btn_cc_pre:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.CC_Precampo = True
            CC_Precampo.CC_Precampo(usuario, puesto)

        elif btn_vin:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Vinculacion_Precampo = True
            Vinculacion_Precampo.Vinculacion_Precampo(usuario, puesto)

        elif btn_prep:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Preparacion_Insumos = True
            Preparacion_Insumos.Preparacion_Insumos(usuario, puesto)

        elif btn_ent:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Entregas_Postcampo = True
            Entregas_Postcampo.Entregas_Postcampo(usuario, puesto)

        elif btn_post:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Postcampo = True
            Postcampo.Postcampo(usuario, puesto)

        elif btn_cc_post:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.CC_Postcampo = True
            CC_Postcampo.CC_Postcampo(usuario, puesto)

        elif btn_cc_vin:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.CC_Vinculacion_Precampo = True
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario, puesto)

        elif btn_estado:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Estado_UIT_Hito = True
            Estado_UIT_Hito.Estado_UIT_Hito(usuario, puesto)

    else:
        # Restauración del submódulo activo (evita volver a mostrar el menú)
        if st.session_state.Historial:
            Historial.Historial(usuario, puesto)
        elif st.session_state.Capacitacion:
            Capacitacion.Capacitacion(usuario, puesto)
        elif st.session_state.Otros_Registros:
            Otros_Registros.Otros_Registros(usuario, puesto)
        elif st.session_state.Bonos_Extras:
            Bonos_Extras.Bonos_Extras(usuario, puesto)
        elif st.session_state.Correcciones:
            Correcciones.Correcciones(usuario, puesto)
        elif st.session_state.Precampo_Juridico:
            Precampo_Juridico.Precampo_Juridico(usuario, puesto)
        elif st.session_state.Descarga_Partidas_Juridico:
            Descarga_Partidas_Juridico.Descarga_Partidas_Juridico(usuario, puesto)
        elif st.session_state.CC_Precampo_Juridico:
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario, puesto)
        elif st.session_state.Asignacion_Partidas:
            Asignacion_Partidas.Asignacion_Partidas(usuario, puesto)
        elif st.session_state.Precampo:
            Precampo.Precampo(usuario, puesto)
        elif st.session_state.CC_Precampo:
            CC_Precampo.CC_Precampo(usuario, puesto)
        elif st.session_state.Vinculacion_Precampo:
            Vinculacion_Precampo.Vinculacion_Precampo(usuario, puesto)
        elif st.session_state.Preparacion_Insumos:
            Preparacion_Insumos.Preparacion_Insumos(usuario, puesto)
        elif st.session_state.Entregas_Postcampo:
            Entregas_Postcampo.Entregas_Postcampo(usuario, puesto)
        elif st.session_state.Postcampo:
            Postcampo.Postcampo(usuario, puesto)
        elif st.session_state.CC_Postcampo:
            CC_Postcampo.CC_Postcampo(usuario, puesto)
        elif st.session_state.CC_Vinculacion_Precampo:
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario, puesto)
        elif st.session_state.Estado_UIT_Hito:
            Estado_UIT_Hito.Estado_UIT_Hito(usuario, puesto)

# =========================================================
# ===================== PROCESOS 2 (Gabinete) ==============
# =========================================================
def Procesos2(usuario, puesto):
    st.session_state.Ingreso = True
    obtener_usuario_activo(usuario)

    if not st.session_state.Procesos:
        # Sidebar común
        ph1 = st.sidebar.empty(); ph1.title("Menú")
        ph2 = st.sidebar.empty(); btn_historial = ph2.button("Historial", key="historial_2_gab")
        ph3 = st.sidebar.empty(); btn_capacitacion = ph3.button("Capacitaciones", key="capacitacion_2_gab")
        ph4 = st.sidebar.empty(); btn_otros = ph4.button("Otros Registros", key="otros_registros_2_gab")
        ph5 = st.sidebar.empty(); btn_bonos = ph5.button("Bonos y Horas Extras", key="bonos_extras_2_gab")
        ph_corr = st.sidebar.empty(); btn_correcciones = ph_corr.button("Solicitud Correcciones", key="correcciones_gab")
        ph6 = st.sidebar.empty(); btn_salir = ph6.button("Salir", key="salir_2_gab")

        # Main: solo procesos de gabinete
        ph7 = st.empty(); ph7.title("Procesos - Gabinete")
        ph8 = st.empty(); btn_precampo = ph8.button("Precampo", key="precampo_2_gab")
        ph9 = st.empty(); btn_cc_pre = ph9.button("Control de Calidad Precampo", key="cc_precampo_2_gab")
        ph10 = st.empty(); btn_ent = ph10.button("Entregas Postcampo", key="entregas_2_gab")
        ph11 = st.empty(); btn_post = ph11.button("Postcampo", key="postcampo_2_gab")
        ph12 = st.empty(); btn_vin = ph12.button("Vinculación Precampo", key="vinculacion_precampo_2_gab")
        ph13 = st.empty(); btn_cc_post = ph13.button("Control de Calidad Postcampo", key="cc_postcampo_2_gab")
        ph14 = st.empty(); btn_cc_vin = ph14.button("Control de Calidad Vinculación Precampo", key="cc_vinculacion_precampo_2_gab")

        placeholders = [ph1,ph2,ph3,ph4,ph5,ph_corr,ph6,ph7,ph8,ph9,ph10,ph11,ph12,ph13,ph14]

        if btn_historial:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Historial = True
            Historial.Historial(usuario, puesto)

        elif btn_capacitacion:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Capacitacion = True
            Capacitacion.Capacitacion(usuario, puesto)

        elif btn_otros:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Otros_Registros = True
            Otros_Registros.Otros_Registros(usuario, puesto)

        elif btn_bonos:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Bonos_Extras = True
            Bonos_Extras.Bonos_Extras(usuario, puesto)

        elif btn_correcciones:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Correcciones = True
            Correcciones.Correcciones(usuario, puesto)

        elif btn_salir:
            limpiar(placeholders)
            st.session_state.Ingreso = False
            st.session_state.Procesos = True
            st.session_state.Salir = True
            Salir.Salir()

        elif btn_precampo:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Precampo = True
            Precampo.Precampo(usuario, puesto)

        elif btn_cc_pre:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.CC_Precampo = True
            CC_Precampo.CC_Precampo(usuario, puesto)

        elif btn_ent:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Entregas_Postcampo = True
            Entregas_Postcampo.Entregas_Postcampo(usuario, puesto)

        elif btn_post:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Postcampo = True
            Postcampo.Postcampo(usuario, puesto)

        elif btn_vin:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Vinculacion_Precampo = True
            Vinculacion_Precampo.Vinculacion_Precampo(usuario, puesto)

        elif btn_cc_post:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.CC_Postcampo = True
            CC_Postcampo.CC_Postcampo(usuario, puesto)

        elif btn_cc_vin:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.CC_Vinculacion_Precampo = True
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario, puesto)

    else:
        # Restaurar submódulo activo
        if st.session_state.Historial:
            Historial.Historial(usuario, puesto)
        elif st.session_state.Capacitacion:
            Capacitacion.Capacitacion(usuario, puesto)
        elif st.session_state.Otros_Registros:
            Otros_Registros.Otros_Registros(usuario, puesto)
        elif st.session_state.Bonos_Extras:
            Bonos_Extras.Bonos_Extras(usuario, puesto)
        elif st.session_state.Correcciones:
            Correcciones.Correcciones(usuario, puesto)
        elif st.session_state.Precampo:
            Precampo.Precampo(usuario, puesto)
        elif st.session_state.CC_Precampo:
            CC_Precampo.CC_Precampo(usuario, puesto)
        elif st.session_state.Entregas_Postcampo:
            Entregas_Postcampo.Entregas_Postcampo(usuario, puesto)
        elif st.session_state.Postcampo:
            Postcampo.Postcampo(usuario, puesto)
        elif st.session_state.Vinculacion_Precampo:
            Vinculacion_Precampo.Vinculacion_Precampo(usuario, puesto)
        elif st.session_state.CC_Postcampo:
            CC_Postcampo.CC_Postcampo(usuario, puesto)
        elif st.session_state.CC_Vinculacion_Precampo:
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario, puesto)

# =========================================================
# ===================== PROCESOS 3 (Jurídico) ==============
# =========================================================
def Procesos3(usuario, puesto):
    st.session_state.Ingreso = True
    obtener_usuario_activo(usuario)

    if not st.session_state.Procesos:
        ph1 = st.sidebar.empty(); ph1.title("Menú")
        ph2 = st.sidebar.empty(); btn_historial = ph2.button("Historial", key="historial_2_jur")
        ph3 = st.sidebar.empty(); btn_capacitacion = ph3.button("Capacitaciones", key="capacitacion_2_jur")
        ph4 = st.sidebar.empty(); btn_otros = ph4.button("Otros Registros", key="otros_registros_2_jur")
        ph5 = st.sidebar.empty(); btn_bonos = ph5.button("Bonos y Horas Extras", key="bonos_extras_2_jur")
        ph_corr = st.sidebar.empty(); btn_correcciones = ph_corr.button("Solicitud Correcciones", key="correcciones_jur")
        ph6 = st.sidebar.empty(); btn_salir = ph6.button("Salir", key="salir_2_jur")

        ph7 = st.empty(); ph7.title("Procesos - Jurídico")
        ph8 = st.empty(); btn_pj = ph8.button("Precampo Jurídico", key="precampo_juridico_2_jur")
        ph9 = st.empty(); btn_dp = ph9.button("Descarga Partidas Jurídico", key="descarga_partidas_juridico_2_jur")
        ph10 = st.empty(); btn_ccpj = ph10.button("Control de Calidad Precampo Jurídico", key="cc_precampo_juridico_2_jur")
        ph11 = st.empty(); btn_asig = ph11.button("Asignación de Partidas", key="asignacion_partidas_jur")

        placeholders = [ph1,ph2,ph3,ph4,ph5,ph_corr,ph6,ph7,ph8,ph9,ph10,ph11]

        if btn_historial:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Historial = True
            Historial.Historial(usuario, puesto)

        elif btn_capacitacion:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Capacitacion = True
            Capacitacion.Capacitacion(usuario, puesto)

        elif btn_otros:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Otros_Registros = True
            Otros_Registros.Otros_Registros(usuario, puesto)

        elif btn_bonos:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Bonos_Extras = True
            Bonos_Extras.Bonos_Extras(usuario, puesto)

        elif btn_correcciones:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Correcciones = True
            Correcciones.Correcciones(usuario, puesto)

        elif btn_salir:
            limpiar(placeholders)
            st.session_state.Ingreso = False
            st.session_state.Procesos = True
            st.session_state.Salir = True
            Salir.Salir()

        elif btn_pj:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Precampo_Juridico = True
            Precampo_Juridico.Precampo_Juridico(usuario, puesto)

        elif btn_dp:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Descarga_Partidas_Juridico = True
            Descarga_Partidas_Juridico.Descarga_Partidas_Juridico(usuario, puesto)

        elif btn_ccpj:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.CC_Precampo_Juridico = True
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario, puesto)

        elif btn_asig:
            limpiar(placeholders)
            st.session_state.Procesos = True
            st.session_state.Asignacion_Partidas = True
            Asignacion_Partidas.Asignacion_Partidas(usuario, puesto)

    else:
        if st.session_state.Historial:
            Historial.Historial(usuario, puesto)
        elif st.session_state.Capacitacion:
            Capacitacion.Capacitacion(usuario, puesto)
        elif st.session_state.Otros_Registros:
            Otros_Registros.Otros_Registros(usuario, puesto)
        elif st.session_state.Bonos_Extras:
            Bonos_Extras.Bonos_Extras(usuario, puesto)
        elif st.session_state.Correcciones:
            Correcciones.Correcciones(usuario, puesto)
        elif st.session_state.Precampo_Juridico:
            Precampo_Juridico.Precampo_Juridico(usuario, puesto)
        elif st.session_state.Descarga_Partidas_Juridico:
            Descarga_Partidas_Juridico.Descarga_Partidas_Juridico(usuario, puesto)
        elif st.session_state.CC_Precampo_Juridico:
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario, puesto)
        elif st.session_state.Asignacion_Partidas:
            Asignacion_Partidas.Asignacion_Partidas(usuario, puesto)
