# Notificaciones.py - Versión simplificada

def mostrar_notificaciones_rechazos(usuario, nombre_operador):
    """
    Muestra panel de rechazos pendientes - Versión simplificada
    """
    
    df_rechazos = fetch_rechazos_pendientes(nombre_operador, dias=10)
    
    if df_rechazos.empty:
        st.success("✅ ¡No tienes rechazos pendientes en los últimos 10 días!")
        return
    
    total_rechazos = df_rechazos['rechazados'].sum()
    
    st.markdown(f"""
    <div style="background-color: #ffeb3b; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #d32f2f; margin: 0;">⚠️ ATENCIÓN: Tienes {len(df_rechazos)} rechazo(s) pendiente(s)</h3>
        <p style="color: #333; margin: 5px 0 0 0;">Total de unidades rechazadas: <strong>{total_rechazos}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar tabla simple
    st.dataframe(
        df_rechazos[['id', 'fecha', 'distrito', 'manzana', 'sector', 'numero_lote', 'rechazados', 'tipo_de_errores']],
        column_config={
            "id": "ID",
            "fecha": "Fecha",
            "distrito": "Distrito",
            "manzana": "Manzana",
            "sector": "Sector",
            "numero_lote": "Lote",
            "rechazados": "Cant. Rechazos",
            "tipo_de_errores": "Tipos de Error"
        },
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    
    # Selector simple para marcar como corregido
    st.subheader("✅ Marcar Rechazo como Corregido")
    
    # Crear opciones para el selectbox sin formateo complejo
    opciones = []
    for _, row in df_rechazos.iterrows():
        fecha_str = row['fecha']
        if isinstance(fecha_str, str) and len(fecha_str) >= 10:
            fecha_corta = fecha_str[5:10]  # "MM-DD"
        else:
            fecha_corta = str(fecha_str)[:10]
        opciones.append(f"{row['id']} - {fecha_corta} - {row['distrito']} - Lote {row['numero_lote']}")
    
    seleccion = st.selectbox("Seleccione el rechazo que ya fue corregido:", opciones, key="select_rechazo")
    
    if seleccion:
        id_seleccionado = int(seleccion.split(' - ')[0])
        
        if st.button("✓ Marcar como Corregido", type="primary"):
            if actualizar_estado_rechazo(id_seleccionado, 'corregido'):
                st.success(f"✅ ¡Rechazo ID {id_seleccionado} marcado como corregido!")
                st.rerun()
            else:
                st.error("❌ Error al actualizar")
