# Notificaciones.py
import streamlit as st
import pandas as pd
from datetime import datetime
import time
from db_core import fetch_rechazos_pendientes, actualizar_estado_rechazo


def mostrar_notificaciones_rechazos(usuario, nombre_operador):
    """
    Muestra panel de rechazos pendientes o redirige directamente a procesos.
    Retorna True si debe redirigir a procesos, False si el usuario está en el panel.
    """
    
    # Obtener rechazos pendientes
    df_rechazos = fetch_rechazos_pendientes(nombre_operador, dias=10)
    
    # ==========================================
    # CASO 1: NO HAY RECHAZOS - Redirección directa
    # ==========================================
    if df_rechazos.empty:
        st.success("✅ ¡Inicio de sesión exitoso!")
        
        # Mensaje breve y redirección inmediata
        with st.spinner("🚀 Accediendo a la aplicación..."):
            time.sleep(0.5)  # Solo para dar feedback visual mínimo
        
        # Marcar sesión como lista para procesos
        st.session_state['pantalla_actual'] = 'procesos'
        st.rerun()
        return True  # Redirección exitosa
    
    # ==========================================
    # CASO 2: HAY RECHAZOS - Mostrar panel
    # ==========================================
    
    # Contar total de rechazos
    total_rechazos = df_rechazos['rechazados'].sum() if 'rechazados' in df_rechazos.columns else len(df_rechazos)
    
    # Mostrar encabezado con diseño mejorado
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fff3e0, #ffe0b2); 
                padding: 20px; 
                border-radius: 15px; 
                margin-bottom: 25px;
                border-left: 5px solid #ff6f00;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <h2 style="color: #e65100; margin: 0 0 10px 0;">⚠️ Rechazos Pendientes</h2>
        <p style="color: #333; font-size: 16px; margin: 0;">
            Tienes <strong style="color: #d32f2f;">{len(df_rechazos)} rechazo(s)</strong> sin corregir | 
            Total unidades: <strong style="color: #d32f2f;">{total_rechazos}</strong>
        </p>
        <p style="color: #666; font-size: 14px; margin: 10px 0 0 0;">
            ⚡ Debes corregirlos en el sistema de origen para continuar
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear copia para mostrar
    df_display = df_rechazos.copy()
    
    # Formatear fechas (tu función original está bien)
    def formatear_fecha(fecha_valor):
        try:
            if hasattr(fecha_valor, 'strftime'):
                return fecha_valor.strftime('%d/%m/%Y')
            elif isinstance(fecha_valor, str):
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
    
    # Renombrar columnas para mejor visualización
    df_display = df_display.rename(columns={
        'id': 'ID',
        'fecha_display': 'Fecha',
        'proceso': 'Proceso',
        'distrito': 'Distrito',
        'manzana': 'Manzana',
        'sector': 'Sector',
        'numero_lote': 'Lote',
        'rechazados': 'Cant. Rechazos',
        'tipo_de_errores': 'Tipos de Error'
    })
    
    # Mostrar tabla con estilo mejorado
    columnas_mostrar = ['ID', 'Fecha', 'Proceso', 'Distrito', 'Manzana', 'Sector', 'Lote', 'Cant. Rechazos', 'Tipos de Error']
    columnas_existentes = [col for col in columnas_mostrar if col in df_display.columns]
    
    st.markdown("### 📋 Listado de Rechazos")
    st.dataframe(
        df_display[columnas_existentes],
        use_container_width=True,
        hide_index=True,
        height=350
    )
    
    st.divider()
    
    # Sección para marcar como corregido (mejorada)
    st.markdown("### ✅ Marcar como Corregido")
    
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        opciones_ids = df_rechazos['id'].tolist()
        if opciones_ids:
            def format_id_option(x):
                row = df_rechazos[df_rechazos['id'] == x].iloc[0]
                fecha_str = row['fecha']
                if isinstance(fecha_str, str) and '-' in fecha_str:
                    partes = fecha_str.split('-')
                    fecha_corta = f"{partes[2]}/{partes[1]}"
                else:
                    fecha_corta = str(fecha_str)[:10]
                return f"ID {x} - {fecha_corta} - {row['distrito']} - Lote {row['numero_lote']} ({row['rechazados']} rech.)"
            
            id_a_corregir = st.selectbox(
                "Selecciona el rechazo corregido:",
                options=opciones_ids,
                format_func=format_id_option,
                key="select_rechazo"
            )
        else:
            id_a_corregir = None
            st.success("🎉 ¡Todos los rechazos han sido corregidos!")
    
    with col2:
        if id_a_corregir and st.button("✓ Corregido", type="primary", use_container_width=True, key="btn_corregir"):
            if actualizar_estado_rechazo(id_a_corregir, 'corregido'):
                st.success(f"✅ ¡Rechazo ID {id_a_corregir} marcado como corregido!")
                st.balloons()
                time.sleep(0.8)
                
                # Verificar si ya no hay más rechazos
                df_check = fetch_rechazos_pendientes(nombre_operador, dias=10)
                if df_check.empty:
                    st.success("🎊 ¡Todos los rechazos corregidos! Accediendo a la aplicación...")
                    time.sleep(1)
                    st.session_state['pantalla_actual'] = 'procesos'
                    st.rerun()
                else:
                    st.rerun()
            else:
                st.error("❌ Error al actualizar. Intenta nuevamente.")
    
    with col3:
        if st.button("Continuar sin corregir →", type="secondary", use_container_width=True, key="btn_continuar"):
            st.warning("⚠️ Recuerda corregir los rechazos pendientes")
            st.session_state['pantalla_actual'] = 'procesos'
            st.rerun()
    
    # Panel de detalles expandible
    if id_a_corregir:
        with st.expander("📌 Detalles del rechazo seleccionado", expanded=True):
            registro = df_rechazos[df_rechazos['id'] == id_a_corregir].iloc[0]
            fecha_original = registro['fecha']
            if isinstance(fecha_original, str) and '-' in fecha_original:
                partes = fecha_original.split('-')
                fecha_mostrar = f"{partes[2]}/{partes[1]}/{partes[0]}"
            else:
                fecha_mostrar = str(fecha_original)
            
            col_det1, col_det2 = st.columns(2)
            with col_det1:
                st.metric("📅 Fecha", fecha_mostrar)
                st.metric("🏘️ Distrito", registro['distrito'])
                st.metric("📍 Manzana", registro['manzana'])
            with col_det2:
                st.metric("🔢 Sector", registro['sector'])
                st.metric("🏠 Lote", registro['numero_lote'])
                st.metric("❌ Unidades rechazadas", registro['rechazados'])
            
            st.error(f"**Errores detectados:** {registro['tipo_de_errores']}")
    
    return False  # El usuario está en el panel de rechazos
