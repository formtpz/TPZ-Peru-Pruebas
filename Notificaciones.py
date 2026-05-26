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
    
    # Obtener rechazos pendientes
    df_rechazos = fetch_rechazos_pendientes(nombre_operador, dias=10)
    
    # Si NO hay rechazos: mostrar mensaje y redirigir DESPUÉS de la función
    if df_rechazos.empty:
        st.success("✅ ¡Inicio de sesión exitoso! Redirigiendo a la aplicación...")
        
        # Crear placeholder para el contador
        placeholder = st.empty()
        
        # Contador regresivo
        for i in range(3, 0, -1):
            placeholder.info(f"⏳ Abriendo aplicación en {i} segundo{'s' if i > 1 else ''}...")
            time.sleep(1)
        
        placeholder.success("🚀 ¡Redirigiendo ahora!")
        time.sleep(0.5)
        
        # Limpiar y guardar flag de redirección
        placeholder.empty()
        st.session_state['auto_redirect'] = True
        # NO llamar a st.rerun() aquí
        
        return  # Salir de la función, pero la redirección se manejará afuera
    
    # ==========================================
    # Si HAY rechazos: mostrar todo normalmente
    # ==========================================
    
    # Resetear flag de redirección
    st.session_state['auto_redirect'] = False
    
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
    
    # Formatear fechas correctamente
    def formatear_fecha(fecha_valor):
        """Convierte fecha en formato 'YYYY-MM-DD' a 'DD/MM/YYYY'"""
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
            def format_id_option(x):
                row = df_rechazos[df_rechazos['id'] == x].iloc[0]
                fecha_str = row['fecha']
                if isinstance(fecha_str, str) and '-' in fecha_str:
                    partes = fecha_str.split('-')
                    fecha_corta = f"{partes[2]}/{partes[1]}"
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
                time.sleep(1)
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
