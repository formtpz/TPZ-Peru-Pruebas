# ----- Librerías ---- #

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import Procesos, Historial, Capacitacion, Otros_Registros, Bonos_Extras, Salir
import historial_peru  # <-- NUEVO
from Autenticacion import obtener_usuario_activo
from db_core import execute, fetch_operadores_cc, fetch_registros_corregidos_pendientes, actualizar_estado_revision

# Constante para puestos peruanos
PUESTOS_PERUANOS = ("Supervisor Perú", "Operario Perú", "Coordinador Perú")

def obtener_modulo_historial(puesto):
    if puesto in PUESTOS_PERUANOS:
        return historial_peru.Historial_Peru
    else:
        return Historial.Historial

def CC_Vinculacion_Precampo(usuario, puesto):
    
    # ----- Sidebar con botones condicionales ----- #
    ph_sidebar = st.sidebar.empty()
    
    with ph_sidebar.container():
        st.title("Menú")
        procesos_btn = st.button("Procesos", key="procesos_3")
        historial_btn = st.button("Historial", key="historial_3")
        capacitacion_btn = st.button("Capacitaciones", key="capacitacion_3")
        otros_registros_btn = st.button("Otros Registros", key="otros_registros_3")
        
        # Botón de Bonos solo si NO es peruano
        if puesto not in PUESTOS_PERUANOS:
            bonos_extras_btn = st.button("Bonos y Horas Extras", key="bonos_extras_3")
        else:
            bonos_extras_btn = False  # No se muestra
        
        salir_btn = st.button("Salir", key="salir_3")
    
    # ----- Contenido Principal ----- #
    ph_main = st.empty()
    
    with ph_main.container():
        st.title(":blue[Control de Calidad Vinculación Precampo]")
        
        # Checkbox para marcar como corregido por QC
        corregido_qc = st.checkbox(
            "Marcar como Corregido por QC",
            value=False,
            key="corregido_qc_toggle",
            help="Active esta opción si el reporte ya fue corregido por Control de Calidad y NO debe enviarse al operador"
        )
        
        if corregido_qc:
            st.warning(
                "⚠️ ATENCIÓN: Este reporte no se enviará al operador para ser corregido. "
                "Se marcará como 'Corregido por QC' directamente."
            )
        
        estado_reporte = "Corregido por QC" if corregido_qc else "N/A"
        
        default_date = datetime.now(pytz.timezone('America/Guatemala'))
        
        fecha = st.date_input("Fecha", value=default_date, key="fecha_3")
        
        distrito = st.selectbox(
            "Distrito", 
            options=("Chorrillos", "San Juan De Miraflores", "Villa el Salvador"),
            key="distrito_3"
        )
        
        manzana = st.selectbox(
            "Manzana", 
            options=("001","002","003","004","005","006","007","008","009","010",
                    "011","012","013","014","015","016","017","018","019","020",
                    "021","022","023","024","025","026","027","028","029","030",
                    "031","032","033","034","035","036","037","038","039","040",
                    "041","042","043","044","045","046","047","048","049","050",
                    "051","052","053","054","055","056","057","058","058","059",
                    "060","061","062","063","064","065","066","067","068","069",
                    "070","071","072","073","074","075","076","077","078","079",
                    "080","081","082","083","084","085","086","087","088","089",
                    "090","091","092","093","094","095","096","097","098","099",
                    "100","101","102","103","104","105","106","107","108","109",
                    "110","111","112","113","114","115","116","117","118","119","120"),
            key="manzana_3"
        )
        
        sector = st.selectbox(
            "Sector", 
            options=("01","02","03","04","05","06","07","08","09","10",
                    "11","12","13","14","15","16","17","18","19","20",
                    "21","22","23","24","25","26","27","28","29","30",
                    "31","32","33","34","35","36","37","38","39","40",
                    "41","42","43","44","45","46","47","48","49","50",
                    "51","52","53","54","55","56","57","58","59","60",
                    "61","62","63","64","65","66","67","68","69","70",
                    "71","72","73","74","75","76","77","78","79","80",
                    "81","82","83","84","85","86","87","88","89","90",
                    "91","92","93","94","95","96","97","98","99","100",
                    "101","102","103","104","105","106","107","108","109",
                    "110","111","112","113","114","115","116","117","118","119","120"),
            key="sector_3"
        )
        
        lotes = ["Todos"] + [f"{i:03d}" for i in range(1, 249)]
        numero_lote = st.multiselect(
            "Número de Lote",
            options=lotes,
            key="numero_lote_3"
        )
        if "Todos" in numero_lote:
            numero_lote = ["Todos"]
        numero_lote_str = ",".join(numero_lote)
        
        operadores_disponibles = fetch_operadores_cc(
            filtro_proceso='Precampo',
            filtro_subproceso='Vinculación',
            filtro_proceso_anterior='Precampo',
            filtro_subproceso_anterior='Vinculación'
        )
        if operadores_disponibles:
            opciones_operadores = [op['nombre'] for op in operadores_disponibles]
        else:
            opciones_operadores = ["No hay operadores disponibles"]
        
        operador = st.selectbox(
            "Operador objeto de CC",
            options=opciones_operadores,
            key="operador_3"
        )
        
        tipo = st.selectbox(
            "Tipo", 
            options=("Inspección", "Primera Reinspección", "Inspección Horas Extras", "Control de Calidad Supervisión"),
            key="tipo_3"
        )
        
        tipo_de_errores = st.multiselect(
            "Tipo Errores", 
            options=("Numeración errónea o incompleta", "Errores geométricos y/o de forma", 
                    "Polígonos y/o puntos duplicados", "Omisión/Comisión de polígonos", 
                    "Polígonos no se ajustan a ortofoto", "Omisión/Comisión de puertas"),
            key="tipo_de_errores_3"
        )
        
        aprobados = st.number_input("Cantidad de Unidades Catastrales Aprobados", min_value=0, step=1, key="aprobados_3")
        rechazados = st.number_input("Cantidad de Unidades Catastrales Rechazados", min_value=0, step=1, key="rechazados_3")
        horas = st.number_input("Cantidad de Horas Trabajadas en el Proceso", min_value=0.0, key="horas_3")
        
        reporte_btn = st.button("Generar Reporte", key="reporte_3")
    
    # ----- Navegación ----- #
    if procesos_btn:
        ph_main.empty()
        ph_sidebar.empty()
        st.session_state.CC_Vinculacion_Precampo = False
        st.session_state.Procesos = True
        
        usuario_activo = obtener_usuario_activo(usuario)
        perfil = str(usuario_activo["perfil"]) if usuario_activo else ""
        
        if perfil == "1":
            Procesos.Procesos1(usuario, puesto)
        elif perfil == "2":
            Procesos.Procesos2(usuario, puesto)
        elif perfil == "3":
            Procesos.Procesos3(usuario, puesto)
    
    elif historial_btn:
        ph_main.empty()
        ph_sidebar.empty()
        st.session_state.CC_Vinculacion_Precampo = False
        st.session_state.Historial = True
        # Llamar al módulo de historial adecuado
        modulo_hist = obtener_modulo_historial(puesto)
        modulo_hist(usuario, puesto)
    
    elif capacitacion_btn:
        ph_main.empty()
        ph_sidebar.empty()
        st.session_state.CC_Vinculacion_Precampo = False
        st.session_state.Capacitacion = True
        Capacitacion.Capacitacion(usuario, puesto)
    
    elif otros_registros_btn:
        ph_main.empty()
        ph_sidebar.empty()
        st.session_state.CC_Vinculacion_Precampo = False
        st.session_state.Otros_Registros = True
        Otros_Registros.Otros_Registros(usuario, puesto)
    
    elif bonos_extras_btn:  # Solo existe si no es peruano
        ph_main.empty()
        ph_sidebar.empty()
        st.session_state.CC_Vinculacion_Precampo = False
        st.session_state.Bonos_Extras = True
        Bonos_Extras.Bonos_Extras(usuario, puesto)
    
    elif salir_btn:
        ph_main.empty()
        ph_sidebar.empty()
        st.session_state.CC_Vinculacion_Precampo = False
        st.session_state.Ingreso = False
        st.session_state.Salir = True
        Salir.Salir()
    
    elif reporte_btn:
        # Generar reporte (código original sin cambios, solo se incluye la parte de guardado)
        marca = datetime.now(pytz.timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M:%S")
        
        usuario_activo = obtener_usuario_activo(usuario)
        if not usuario_activo:
            st.error("No se encontró un usuario activo para generar el reporte.")
            return
        
        nombre = usuario_activo["nombre"]
        supervisor = usuario_activo["supervisor"]
        
        unidades_catastrales = aprobados + rechazados
        semana = fecha.isocalendar()[1]
        año = fecha.isocalendar()[0]
        horas_bi = float(horas)
        tipos_de_errores_str = ','.join(tipo_de_errores)
        conteo = len(tipo_de_errores)
        
        execute(
            """
            INSERT INTO registro (
                marca, usuario, nombre, puesto, supervisor, proceso, fecha, semana, año, 
                distrito, tipo, lotes, aprobados, rechazados, horas,
                manzana, sector, numero_lote, estado, area, unidades_catastrales, 
                edificas, partida, con_fmi, sin_fmi, observaciones, zona,
                tipo_calidad, horas_bi, area_bi, operador_cc, total_de_errores, 
                errores_por_excepciones, tipo_de_errores, conteo_de_errores
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, 
                %s, %s, %s
            )
            """,
            params=[
                marca, usuario, nombre, puesto, supervisor, "Control de Calidad Vinculación Precampo", 
                fecha, semana, año, distrito, tipo, 0, aprobados, rechazados, horas,
                manzana, sector, numero_lote_str, estado_reporte, 0.0, unidades_catastrales, 
                0, "N/A", 0, 0, "N/A", "N/A",
                "N/A", horas_bi, 0, operador, 0, 
                0, tipos_de_errores_str, conteo
            ],
        )
        
        st.success('✅ Reporte enviado correctamente')
        
        # ============ TABLA DE REGISTROS PENDIENTES (sin cambios) ============ #
        st.markdown("---")
        st.subheader("📋 Registros pendientes de revisión")
        
        df_pendientes = fetch_registros_corregidos_pendientes(usuario)
        
        if not df_pendientes.empty:
            df_pendientes['marcar_revisado'] = False
            st.info(f"Se encontraron {len(df_pendientes)} registro(s) pendiente(s) de revisión")
            
            edited_df = st.data_editor(
                df_pendientes,
                column_config={
                    "id": st.column_config.NumberColumn("ID", disabled=True),
                    "marca": st.column_config.DatetimeColumn("Fecha Registro", disabled=True),
                    "fecha": st.column_config.DateColumn("Fecha", disabled=True),
                    "distrito": st.column_config.TextColumn("Distrito", disabled=True),
                    "manzana": st.column_config.TextColumn("Manzana", disabled=True),
                    "sector": st.column_config.TextColumn("Sector", disabled=True),
                    "numero_lote": st.column_config.TextColumn("Lotes", disabled=True),
                    "operador_cc": st.column_config.TextColumn("Operador CC", disabled=True),
                    "tipo_de_errores": st.column_config.TextColumn("Tipo de Errores", disabled=True),
                    "estado": st.column_config.TextColumn("Estado Actual", disabled=True),
                    "marcar_revisado": st.column_config.CheckboxColumn(
                        "Marcar como Revisado",
                        help="Seleccione para cambiar el estado a 'revisado'"
                    )
                },
                hide_index=True,
                key="tabla_revision_cc"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("💾 Guardar cambios de estado", key="guardar_revision_cc", use_container_width=True):
                    registros_a_actualizar = edited_df[edited_df['marcar_revisado'] == True]
                    if len(registros_a_actualizar) > 0:
                        actualizaciones_exitosas = 0
                        actualizaciones_fallidas = 0
                        for _, row in registros_a_actualizar.iterrows():
                            if actualizar_estado_revision(row['id']):
                                actualizaciones_exitosas += 1
                            else:
                                actualizaciones_fallidas += 1
                        if actualizaciones_fallidas == 0:
                            st.success(f'✅ {actualizaciones_exitosas} registro(s) actualizado(s) a "revisado" exitosamente')
                        else:
                            st.warning(f'⚠️ {actualizaciones_exitosas} exitoso(s), {actualizaciones_fallidas} fallido(s)')
                        st.rerun()
                    else:
                        st.warning("⚠️ No se seleccionó ningún registro para actualizar.")
        else:
            st.info("ℹ️ No hay registros pendientes de revisión con estado 'corregido' en este momento.")
