# Notificaciones.py
import streamlit as st
import pandas as pd
from db_core import fetch_rechazos_pendientes, actualizar_estado_rechazo


def mostrar_notificaciones_rechazos(usuario, nombre_operador):
    """
    Muestra un panel con los rechazos pendientes del operador.
    NO interrumpe el flujo - se muestra y permite acciones in-situ.
    """
    
    # Obtener rechazos pendientes de los últimos 10 días
    df_rechazos = fetch_rechazos_pendientes(nombre_operador, dias=10)
    
    if df_rechazos.empty:
        st.success("✅ ¡No tienes rechazos pendientes en los últimos 10 días!")
        return
    
    # Mostrar contador y título con diseño llamativo
    st.markdown(f"""
    <div style="background-color: #ffeb3b; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #d32f2f; margin: 0;">⚠️ ATENCIÓN: Tienes {len(df_rechazos)} rechazo(s) pendiente(s) por corregir</h3>
        <p style="color: #333; margin: 5px 0 0 0;">Por favor, revisa los siguientes casos y márcalos como corregidos una vez resueltos.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear una copia para mostrar
    df_display = df_rechazos.copy()
    
    # Formatear fechas
    df_display['fecha'] = pd.to_datetime(df_display['fecha']).dt.strftime('%d/%m/%Y')
    
    # Renombrar columnas para mejor presentación
    df_display = df_display.rename(columns={
        'id': 'ID',
        'fecha': 'Fecha',
        'proceso': 'Proceso',
        'distrito': 'Distrito',
        'manzana': 'Manzana',
        'sector': 'Sector',
        'numero_lote': 'Lote',
        'rechazados': 'Cant. Rechazos',
        'tipo_de_errores': 'Tipos de Error',
        'estado': 'Estado'
    })
    
    # Mostrar tabla
    st.dataframe(
        df_display[['ID', 'Fecha', 'Proceso', 'Distrito', 'Manzana', 'Sector', 'Lote', 'Cant. Rechazos', 'Tipos de Error']],
        use_container_width=True,
        hide_index=True,
        height=300
    )
    
    st.divider()
    
    # Sección para marcar como corregido (compacta)
    st.subheader("✅ Marcar Rechazo como Corregido")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        # Selector de ID
        opciones_ids = df_rechazos['id'].tolist()
        if opciones_ids:
            id_a_corregir = st.selectbox(
                "Seleccione el ID del rechazo que ya fue corregido:",
                options=opciones_ids,
                format_func=lambda x: f"ID {x} - {df_rechazos[df_rechazos['id'] == x]['fecha'].iloc[0].strftime('%d/%m')} - {df_rechazos[df_rechazos['id'] == x]['distrito'].iloc[0]} - Lote {df_rechazos[df_rechazos['id'] == x]['numero_lote'].iloc[0]}",
                key="select_rechazo"
            )
        else:
            id_a_corregir = None
            st.info("🎉 ¡Todos los rechazos han sido corregidos!")
    
    with col2:
        if id_a_corregir and st.button("✓ Marcar como Corregido", type="primary", key="btn_corregir"):
            if actualizar_estado_rechazo(id_a_corregir, 'corregido'):
                st.success(f"✅ ¡Rechazo ID {id_a_corregir} marcado como corregido!")
                st.balloons()  # Efecto visual divertido
                st.rerun()  # Recargar para actualizar la lista
            else:
                st.error("❌ No se pudo actualizar. Intente nuevamente.")
    
    with col3:
        if id_a_corregir:
            # Mostrar detalles del seleccionado
            registro_seleccionado = df_rechazos[df_rechazos['id'] == id_a_corregir].iloc[0]
            st.info(f"📌 **Detalle:** {registro_seleccionado['rechazados']} unidad(es) rechazada(s) - {registro_seleccionado['tipo_de_errores']}")
