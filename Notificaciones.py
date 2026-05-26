# Notificaciones.py
import streamlit as st
import pandas as pd
from datetime import datetime
import time
from db_core import fetch_rechazos_pendientes, actualizar_estado_rechazo


def mostrar_notificaciones_rechazos(usuario, nombre_operador):
    """
    Muestra panel de rechazos pendientes
    """
    
    # Inicializar contador en session_state si no existe
    if 'redirect_counter' not in st.session_state:
        st.session_state.redirect_counter = 3
    
    # Obtener rechazos pendientes
    df_rechazos = fetch_rechazos_pendientes(nombre_operador, dias=10)
    
    # Si NO hay rechazos: auto-avance con contador
    if df_rechazos.empty:
        # Si ya tenemos un contador activo, mostrarlo y decrementar
        if st.session_state.redirect_counter > 0:
            st.success("✅ ¡Inicio de sesión exitoso! Redirigiendo a la aplicación...")
            
            # Mostrar contador
            placeholder = st.empty()
            placeholder.info(f"⏳ Abriendo aplicación en {st.session_state.redirect_counter} segundo{'s' if st.session_state.redirect_counter > 1 else ''}...")
            
            # Decrementar el contador
            st.session_state.redirect_counter -= 1
            
            # Pequeña pausa
            time.sleep(1)
            st.rerun()
            
        else:
            # Contador llegó a 0, redirigir
            st.session_state.redirect_counter = 3  # Reset para próximas veces
            st.session_state['auto_redirect'] = True
            st.rerun()
            return
    
    else:
        # Si HAY rechazos, resetear el contador y mostrar todo normalmente
        st.session_state.redirect_counter = 3
        
        # Contar total de rechazos
        total_rechazos = df_rechazos['rechazados'].sum() if 'rechazados' in df_rechazos.columns else len(df_rechazos)
        
        # Mostrar encabezado
        st.markdown(f"""
        <div style="background-color: #ffeb3b; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: #d32f2f; margin: 0;">⚠️ ATENCIÓN: Tienes {len(df_rechazos)} rechazo(s) pendiente(s) por corregir</h3>
            <p style="color: #333; margin: 5px 0 0 0;">Total de unidades rechazadas: <strong>{total_rechazos}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Crear copia para mostrar
        df_display = df_rechazos.copy()
        
        # Formatear fechas correctamente (MANEJO DE STRING)
        def formatear_fecha(fecha_valor):
            """Convierte fecha en formato 'YYYY-MM-DD' a 'DD/MM/YYYY'"""
            try:
                # Si ya es datetime
                if hasattr(fecha_valor, 'strftime'):
                    return fecha_valor.strftime('%d/%m/%Y')
                # Si es string
                elif isinstance(fecha_valor, str):
                    # Intentar parsear el string
                    if '-' in fecha_valor:
                        partes = fecha_valor.split('-')
                        if len(partes) == 3:
                            return f"{partes[2]}/{partes[1]}/{partes[0]}"
                    return fecha_valor
                else:
                    return str(fecha_valor)
            except:
                return str(fecha_valor)
        
        df_display['fecha_display'] = df_display['fecha'].apply(formatear_fecha)
        
        # Renombrar columnas
        df_display = df_display.rename(columns={
            'id': 'ID',
            'fecha_display': 'Fecha',
            'proceso': 'Proceso',
            'distrito': 'Distrito',
            'manzana': 'Manzana',
            'sector': 'Sector',
            'numero_lote': 'Lote',
            'rechazados': 'Cant. Rechazos',
            'tipo_de_errores': 'Tipos de Error',
            'estado': 'Estado'
        })
        
        # Seleccionar columnas a mostrar
        columnas_mostrar = ['ID', 'Fecha', 'Proceso', 'Distrito', 'Manzana', 'Sector', 'Lote', 'Cant. Rechazos', 'Tipos de Error']
        columnas_existentes = [col for col in columnas_mostrar if col in df_display.columns]
        
        # Mostrar tabla
        st.dataframe(
            df_display[columnas_existentes],
            use_container_width=True,
            hide_index=True,
            height=300
        )
        
        st.divider()
        
        # Sección para marcar como corregido
        st.subheader("✅ Marcar Rechazo como Corregido")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            opciones_ids = df_rechazos['id'].tolist()
            if opciones_ids:
                # Función para formatear la opción del selectbox
                def format_id_option(x):
                    # Obtener la fila correspondiente
                    row = df_rechazos[df_rechazos['id'] == x].iloc[0]
                    fecha_str = row['fecha']
                    # Formatear fecha para el selectbox
                    if isinstance(fecha_str, str) and '-' in fecha_str:
                        partes = fecha_str.split('-')
                        fecha_corta = f"{partes[2]}/{partes[1]}"  # Solo día/mes
                    else:
                        fecha_corta = str(fecha_str)[:10]
                    return f"ID {x} - {fecha_corta} - {row['distrito']} - Lote {row['numero_lote']} ({row['rechazados']} rechazos)"
                
                id_a_corregir = st.selectbox(
                    "Seleccione el ID del rechazo que ya fue corregido:",
                    options=opciones_ids,
                    format_func=format_id_option,
                    key="select_rechazo"
                )
            else:
                id_a_corregir = None
                st.info("🎉 ¡Todos los rechazos han sido corregidos!")
        
        with col2:
            if id_a_corregir and st.button("✓ Marcar como Corregido", type="primary", key="btn_corregir"):
                if actualizar_estado_rechazo(id_a_corregir, 'corregido'):
                    st.success(f"✅ ¡Rechazo ID {id_a_corregir} marcado como corregido!")
                    st.balloons()
                    time.sleep(1)  # Pequeña pausa para ver el mensaje
                    st.rerun()
                else:
                    st.error("❌ No se pudo actualizar. Intente nuevamente.")
        
        # Mostrar detalles del seleccionado
        if id_a_corregir:
            registro = df_rechazos[df_rechazos['id'] == id_a_corregir].iloc[0]
            fecha_original = registro['fecha']
            if isinstance(fecha_original, str) and '-' in fecha_original:
                partes = fecha_original.split('-')
                fecha_mostrar = f"{partes[2]}/{partes[1]}/{partes[0]}"
            else:
                fecha_mostrar = str(fecha_original)
            
            st.info(f"""
            📌 **Detalle del rechazo seleccionado:**  
            - **Fecha:** {fecha_mostrar}  
            - **Distrito:** {registro['distrito']}  
            - **Manzana:** {registro['manzana']}  
            - **Sector:** {registro['sector']}  
            - **Lote:** {registro['numero_lote']}  
            - **Unidades rechazadas:** {registro['rechazados']}  
            - **Errores:** {registro['tipo_de_errores']}
            """)
