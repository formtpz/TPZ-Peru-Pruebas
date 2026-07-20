# ----- Librerías ---- #
import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import io
import Procesos, Historial, Capacitacion, Otros_Registros, Bonos_Extras, Salir
from Autenticacion import obtener_usuario_activo
from db_core import execute, fetch_operadores_cc

# Constante para puestos peruanos (se mantiene)
PUESTOS_PERUANOS = ("Supervisor Perú", "Operario Perú", "Coordinador Perú")

# ------------------------------------------------------------
# Funciones auxiliares para la carga masiva (adaptadas de CC_Postcampo)
# ------------------------------------------------------------
def formatear_sector_cc(valor):
    try:
        return str(int(float(valor))).zfill(2)
    except:
        return str(valor).zfill(2)

def formatear_manzana_cc(valor):
    try:
        return str(int(float(valor))).zfill(3)
    except:
        return str(valor).zfill(3)

def formatear_lote_cc(valor):
    try:
        valor_str = str(valor).strip()
        if not valor_str or valor_str.lower() == 'nan':
            return 'Todos'
        if valor_str.lower() == 'todos':
            return 'Todos'
        if ',' in valor_str:
            numeros = []
            for num in valor_str.split(','):
                num = num.strip()
                if num:
                    try:
                        numeros.append(str(int(float(num))).zfill(3))
                    except:
                        numeros.append(num)
            return ','.join(numeros) if numeros else 'Todos'
        else:
            return str(int(float(valor_str))).zfill(3)
    except:
        return str(valor)

def normalizar_horas_cc(valor):
    try:
        if isinstance(valor, str):
            valor = valor.replace(',', '.')
        return float(valor)
    except:
        return 0.0

def normalizar_texto_cc(valor, default="N/A"):
    if pd.isna(valor) or valor == '' or valor is None:
        return default
    return str(valor).strip()

def limpiar_espacios_extra(texto):
    """Elimina espacios dobles y espacios alrededor de comas, y deja un solo espacio entre palabras."""
    if not isinstance(texto, str):
        return texto
    # Reemplazar múltiples espacios por uno solo
    texto = ' '.join(texto.split())
    # Eliminar espacios alrededor de comas
    texto = ', '.join([part.strip() for part in texto.split(',')])
    return texto

def traducir_tipos_errores(valor):
    """Convierte números separados por comas a los nombres de errores según el mapa."""
    mapa = {
        '1': 'Atributos incompletos/erroneos',
        '2': 'Autoensamblado',
        '3': 'Diferencia de áreas',
        '4': 'Errores gráficos',
        '5': 'Puertas no coinciden',
        '6': 'Recapitulación errónea'
    }
    if pd.isna(valor) or valor == '':
        return ''
    texto = str(valor).strip()
    if not texto:
        return ''
    # Si el texto ya contiene nombres (no solo números), devolverlo limpio
    if any(c.isalpha() for c in texto):
        return limpiar_espacios_extra(texto)
    # Si son números separados por comas
    partes = [part.strip() for part in texto.split(',') if part.strip()]
    nombres = []
    for p in partes:
        if p in mapa:
            nombres.append(mapa[p])
        else:
            # Si no es número, intentar dejarlo tal cual (puede ser nombre parcial)
            nombres.append(p)
    return ', '.join(nombres)  # separados por coma y espacio

def buscar_columnas_por_coincidencia_cc(df):
    """Mapea columnas del Excel a los nombres esperados para CC Postcampo."""
    columnas_requeridas = {
        'distrito': ['distrito', 'DISTRITO', 'Distrito', 'Municipio', 'municipio'],
        'sector': ['sector', 'SECTOR', 'Sector', 'sec', 'SEC'],
        'manzana': ['manzana', 'MANZANA', 'Manzana', 'mz', 'MZ'],
        'tipo': ['tipo', 'TIPO', 'Tipo', 'tipo_cc'],
        'operador': ['operador', 'OPERADOR', 'Operador', 'operador_cc', 'Operador CC'],
        'numero_lote': ['numero_lote', 'numero lote', 'NÚMERO LOTE', 'N° Lote', 'lote', 'LOTE', 'n_lote', 'lotes'],
        'tipo_de_errores': ['tipo_de_errores', 'tipo errores', 'TIPO ERRORES', 'Error', 'errores'],
        'aprobados': ['aprobados', 'APROBADOS', 'Aprobados', 'aprob', 'APROB'],
        'rechazados': ['rechazados', 'RECHAZADOS', 'Rechazados', 'rechaz', 'RECHAZ'],
        'horas': ['horas', 'HORAS', 'Horas', 'horas trabajadas', 'horas_trabajadas']
    }
    mapeo = {}
    for nombre_requerido, posibles_nombres in columnas_requeridas.items():
        for posible in posibles_nombres:
            if posible in df.columns:
                mapeo[nombre_requerido] = posible
                break
    return mapeo

def procesar_dataframe_excel_cc(df, opciones_operadores):
    """
    Procesa el DataFrame del Excel, aplica transformaciones y mapea columnas.
    Retorna (df_procesado, columnas_faltantes, mapeo).
    """
    mapeo_columnas = buscar_columnas_por_coincidencia_cc(df)
    columnas_requeridas = [
        'distrito', 'sector', 'manzana', 'tipo', 'operador',
        'numero_lote', 'tipo_de_errores', 'aprobados', 'rechazados', 'horas'
    ]
    columnas_faltantes = [col for col in columnas_requeridas if col not in mapeo_columnas]
    if columnas_faltantes:
        return None, columnas_faltantes, mapeo_columnas

    df_procesado = pd.DataFrame()
    for nombre_requerido, nombre_real in mapeo_columnas.items():
        df_procesado[nombre_requerido] = df[nombre_real]

    # Transformaciones
    df_procesado['sector'] = df_procesado['sector'].apply(formatear_sector_cc)
    df_procesado['manzana'] = df_procesado['manzana'].apply(formatear_manzana_cc)
    df_procesado['numero_lote'] = df_procesado['numero_lote'].apply(
        lambda x: formatear_lote_cc(x) if str(x).strip().lower() != 'todos' else 'Todos'
    )
    df_procesado['horas'] = df_procesado['horas'].apply(normalizar_horas_cc)
    df_procesado['aprobados'] = pd.to_numeric(df_procesado['aprobados'], errors='coerce').fillna(0).astype(int)
    df_procesado['rechazados'] = pd.to_numeric(df_procesado['rechazados'], errors='coerce').fillna(0).astype(int)
    # Traducir tipo de errores: si son números, convertirlos a nombres
    df_procesado['tipo_de_errores'] = df_procesado['tipo_de_errores'].apply(traducir_tipos_errores)
    # Limpiar espacios en general
    for col in ['distrito', 'tipo', 'operador', 'numero_lote']:
        df_procesado[col] = df_procesado[col].apply(lambda x: limpiar_espacios_extra(str(x)) if pd.notna(x) else x)

    # Validar que el operador esté en la lista de opciones (si no, se marcará como error más adelante)
    # Pero en el data_editor se usará selectbox, así que dejamos tal cual.

    return df_procesado, [], mapeo_columnas

def validar_datos_masivos_cc(df, distritos_validos, tipos_validos, operadores_validos):
    """Valida el DataFrame procesado antes de insertar."""
    errores = []

    if df is None or df.empty:
        return False, "La tabla está vacía. No hay datos para procesar."

    # Quitar filas completamente vacías
    df_check = df.dropna(how="all")
    if df_check.empty:
        return False, "La tabla está vacía. No hay datos para procesar."

    if df['distrito'].isnull().any() or (df['distrito'] == '').any():
        errores.append("Hay filas sin 'Distrito' seleccionado.")
    else:
        invalidos = df[~df['distrito'].isin(distritos_validos)]
        if not invalidos.empty:
            errores.append(f"Distrito inválido en fila(s): {[i + 1 for i in invalidos.index.tolist()]}")

    if df['tipo'].isnull().any() or (df['tipo'] == '').any():
        errores.append("Hay filas sin 'Tipo' seleccionado.")
    else:
        invalidos = df[~df['tipo'].isin(tipos_validos)]
        if not invalidos.empty:
            errores.append(f"Tipo inválido en fila(s): {[i + 1 for i in invalidos.index.tolist()]}")

    if df['operador'].isnull().any() or (df['operador'] == '').any():
        errores.append("Hay filas sin 'Operador objeto de CC' seleccionado.")
    else:
        invalidos = df[~df['operador'].isin(operadores_validos)]
        if not invalidos.empty:
            errores.append(f"Operador inválido en fila(s): {[i + 1 for i in invalidos.index.tolist()]} (verifica que el nombre coincida exactamente)")

    if (df['horas'] < 0).any():
        errores.append("Hay filas con 'Horas' negativas.")

    if (df['aprobados'] < 0).any():
        errores.append("Hay filas con 'Aprobados' negativos.")

    if (df['rechazados'] < 0).any():
        errores.append("Hay filas con 'Rechazados' negativos.")

    if errores:
        return False, "\n".join(errores)
    return True, "Datos válidos"

def insertar_registros_masivos_cc(df, fecha_seleccionada, usuario, usuario_activo, puesto):
    """Inserta fila por fila en la tabla `registro` para CC Postcampo."""
    marca = datetime.now(pytz.timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M:%S")
    nombre = usuario_activo["nombre"]
    supervisor = usuario_activo["supervisor"]
    semana = fecha_seleccionada.isocalendar()[1]
    año = fecha_seleccionada.isocalendar()[0]
    registros_insertados = 0

    try:
        for _, row in df.iterrows():
            aprobados = int(row['aprobados'])
            rechazados = int(row['rechazados'])
            unidades_catastrales = aprobados + rechazados
            horas = float(row['horas'])

            tipos_de_errores = normalizar_texto_cc(row.get('tipo_de_errores', ''), default="")
            # Ya viene limpio y traducido del procesamiento
            lista_errores = [t.strip() for t in tipos_de_errores.split(',') if t.strip()]
            tipos_de_errores_str = ','.join(lista_errores)
            conteo_errores = len(lista_errores)

            manzana = formatear_manzana_cc(row['manzana'])
            sector = formatear_sector_cc(row['sector'])
            numero_lote = formatear_lote_cc(row.get('numero_lote', 'Todos'))

            execute(
                """
                INSERT INTO registro (
                  marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito,tipo,lotes,aprobados,rechazados,horas,
                  manzana,sector,numero_lote,estado,area,unidades_catastrales,edificas,partida,con_fmi,sin_fmi,observaciones,zona,
                  tipo_calidad,horas_bi,area_bi,operador_cc,total_de_errores,errores_por_excepciones,tipo_de_errores,conteo_de_errores
                )
                VALUES (
                  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                  %s,%s,%s,%s,%s,%s,%s,%s
                )
                """,
                params=[
                  marca, usuario, nombre, puesto, supervisor, "Control de Calidad Postcampo", fecha_seleccionada, semana, año,
                  row['distrito'], row['tipo'], 0, aprobados, rechazados, horas,
                  manzana, sector, numero_lote, "N/A", 0.0, unidades_catastrales, 0, "N/A", 0, 0, "N/A", "N/A",
                  "N/A", horas, 0, row['operador'], 0, 0, tipos_de_errores_str, conteo_errores
                ],
            )
            registros_insertados += 1
        return True, registros_insertados, f"Se insertaron {registros_insertados} registro(s) exitosamente."
    except Exception as e:
        return False, registros_insertados, f"Error al insertar registros: {str(e)}"

def obtener_modulo_historial(puesto):
    """Retorna la función del módulo de historial adecuada según el puesto (igual que antes)."""
    if puesto in PUESTOS_PERUANOS:
        import historial_peru
        return historial_peru.Historial_Peru
    else:
        return Historial.Historial

# ------------------------------------------------------------
# Función principal del módulo CC_Postcampo (renovada)
# ------------------------------------------------------------
def CC_Postcampo(usuario, puesto):

    # ----- Inicializar contador de versión (para el editor masivo) -----
    if "version_tabla_cc" not in st.session_state:
        st.session_state.version_tabla_cc = 0

    # ----- Placeholders del sidebar -----
    placeholder1 = st.sidebar.empty()
    placeholder1.title("Menú")
    placeholder2 = st.sidebar.empty()
    procesos_btn = placeholder2.button("Procesos", key="procesos_cc")
    placeholder3 = st.sidebar.empty()
    historial_btn = placeholder3.button("Historial", key="historial_cc")
    placeholder4 = st.sidebar.empty()
    capacitacion_btn = placeholder4.button("Capacitaciones", key="capacitacion_cc")
    placeholder5 = st.sidebar.empty()
    otros_btn = placeholder5.button("Otros Registros", key="otros_cc")
    # Botón de Bonos solo si NO es peruano
    if puesto not in PUESTOS_PERUANOS:
        placeholder6 = st.sidebar.empty()
        bonos_btn = placeholder6.button("Bonos y Horas Extras", key="bonos_cc")
    else:
        placeholder6 = None
        bonos_btn = False
    placeholder7 = st.sidebar.empty()
    salir_btn = placeholder7.button("Salir", key="salir_cc")

    # ----- Selector de modo de carga -----
    placeholder_modo = st.empty()
    modo_carga = placeholder_modo.radio(
        "Selecciona el modo de carga:",
        options=["📝 Carga Manual (Formulario)", "📋 Carga Masiva (Subir Excel)"],
        key="modo_cc_postcampo"
    )

    # ----- Título -----
    placeholder_titulo = st.empty()
    placeholder_titulo.title(":blue[Control de Calidad Postcampo]")

    # ----- Listas de valores válidos (se usan en ambos modos) -----
    distritos_opciones = ("Chorrillos", "San Juan De Miraflores", "Villa el Salvador")
    tipo_opciones = ("Inspección", "Inspección Reproceso", "Primera Reinspección",
                     "Inspección Horas Extras", "Control de Calidad Supervisión")
    tipo_errores_opciones = ("Atributos incompletos/erroneos", "Autoensamblado", "Diferencia de áreas",
                             "Errores gráficos", "Puertas no coinciden", "Recapitulación errónea")
    # Obtener operadores desde la base de datos
    operadores_disponibles = fetch_operadores_cc(
        filtro_proceso='Postcampo',
        filtro_subproceso='Productivo',
        filtro_proceso_anterior='Postcampo',
        filtro_subproceso_anterior='Productivo'
    )
    if operadores_disponibles:
        opciones_operadores = [op['nombre'] for op in operadores_disponibles]
    else:
        opciones_operadores = ["No hay operadores disponibles"]

    # ---- Inicialización de placeholders del formulario manual ----
    placeholder_fecha = None
    placeholder_distrito = None
    placeholder_manzana = None
    placeholder_sector = None
    placeholder_numero_lote = None
    placeholder_operador = None
    placeholder_tipo = None
    placeholder_tipo_errores = None
    placeholder_aprobados = None
    placeholder_rechazados = None
    placeholder_horas = None
    placeholder_reporte = None

    # Variables del formulario manual
    fecha_manual = None
    distrito_manual = None
    manzana_manual = None
    sector_manual = None
    numero_lote_manual = None
    operador_manual = None
    tipo_manual = None
    tipo_errores_manual = None
    aprobados_manual = None
    rechazados_manual = None
    horas_manual = None
    reporte_btn = None

    # ----- Modo manual (idéntico al original) -----
    if modo_carga == "📝 Carga Manual (Formulario)":
        default_date = datetime.now(pytz.timezone('America/Guatemala'))

        placeholder_fecha = st.empty()
        fecha_manual = placeholder_fecha.date_input("Fecha", value=default_date, key="fecha_cc_manual")

        placeholder_distrito = st.empty()
        distrito_manual = placeholder_distrito.selectbox("Distrito", options=distritos_opciones, key="distrito_cc_manual")

        placeholder_manzana = st.empty()
        manzana_manual = placeholder_manzana.selectbox(
            "Manzana",
            options=tuple(f"{i:03d}" for i in range(1, 121)),
            key="manzana_cc_manual"
        )

        placeholder_sector = st.empty()
        sector_manual = placeholder_sector.selectbox(
            "Sector",
            options=tuple(f"{i:02d}" for i in range(1, 121)),
            key="sector_cc_manual"
        )

        # Multiselect de lotes
        lotes = ["Todos"] + [f"{i:03d}" for i in range(1, 249)]
        placeholder_numero_lote = st.empty()
        numero_lote_seleccion = placeholder_numero_lote.multiselect(
            "Número de Lote",
            options=lotes,
            key="lote_cc_manual"
        )
        if "Todos" in numero_lote_seleccion:
            numero_lote_seleccion = ["Todos"]
        numero_lote_manual = ",".join(numero_lote_seleccion)

        placeholder_operador = st.empty()
        operador_manual = placeholder_operador.selectbox(
            "Operador objeto de CC",
            options=opciones_operadores,
            key="operador_cc_manual"
        )

        placeholder_tipo = st.empty()
        tipo_manual = placeholder_tipo.selectbox("Tipo", options=tipo_opciones, key="tipo_cc_manual")

        placeholder_tipo_errores = st.empty()
        tipo_errores_manual = placeholder_tipo_errores.multiselect(
            "Tipo Errores",
            options=tipo_errores_opciones,
            key="tipo_errores_cc_manual"
        )

        placeholder_aprobados = st.empty()
        aprobados_manual = placeholder_aprobados.number_input(
            "Cantidad de Unidades Catastrales Aprobados",
            min_value=0,
            step=1,
            key="aprobados_cc_manual"
        )

        placeholder_rechazados = st.empty()
        rechazados_manual = placeholder_rechazados.number_input(
            "Cantidad de Unidades Catastrales Rechazados",
            min_value=0,
            step=1,
            key="rechazados_cc_manual"
        )

        placeholder_horas = st.empty()
        horas_manual = placeholder_horas.number_input(
            "Cantidad de Horas Trabajadas en el Proceso",
            min_value=0.0,
            key="horas_cc_manual"
        )

        placeholder_reporte = st.empty()
        reporte_btn = placeholder_reporte.button("Generar Reporte", key="reporte_cc_manual")

    # ----- Modo masivo (subir Excel) -----
    else:
        # Fecha para todos los registros
        placeholder_fecha_masiva = st.empty()
        fecha_masiva = placeholder_fecha_masiva.date_input(
            "📅 Fecha para todos los registros",
            value=datetime.now(pytz.timezone('America/Guatemala')),
            key="fecha_masiva_cc"
        )

        # Instrucciones y plantilla
        placeholder_instrucciones = st.empty()
        with placeholder_instrucciones.container():
            st.info("""
            📋 **Instrucciones:**
            1. Descarga la plantilla Excel oficial (abajo).
            2. Llena tus datos en la **Hoja1** del Excel.
            3. Los nombres de columna pueden variar ligeramente (se detectan por coincidencia).
            4. Sube el archivo Excel.
            5. Revisa la vista previa antes de confirmar.

            **Transformaciones automáticas:**
            - Sector: 1 → 01
            - Manzana: 5 → 005
            - N° Lote: 1 → 001 (o '1,2,3' → '001,002,003')
            - Horas: 8,5 → 8.5
            - Tipo de errores: puedes escribir números separados por comas (ej. 1,3,5) y se traducirán a los nombres correspondientes.
            - Campos vacíos → "N/A" o "Todos".
            """)

        placeholder_descarga_plantilla = st.empty()
        with placeholder_descarga_plantilla.container():
            st.markdown("### 📥 Plantilla oficial")
            # URL de la plantilla para CC Postcampo (debes subirla a tu repositorio)
            url_plantilla = "https://raw.githubusercontent.com/formtpz/Reportes_Peru_V2/main/docs/controlcalidadpostcampo.xlsx"
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f'''
                <a href="{url_plantilla}" download>
                    <button style="background-color: #4CAF50; color: white; padding: 10px 20px;
                    border: none; border-radius: 5px; cursor: pointer; font-size: 16px;">
                        📥 Descargar Plantilla
                    </button>
                </a>
                ''', unsafe_allow_html=True)
            with col2:
                st.caption("Descarga el machote oficial `controlcalidadpostcampo.xlsx`")
                st.caption(f"🔗 [Enlace directo]({url_plantilla})")

        placeholder_archivo = st.empty()
        archivo_excel = placeholder_archivo.file_uploader(
            "📁 Subir archivo Excel con datos",
            type=['xlsx', 'xls'],
            key="archivo_cc_masivo",
            help="Selecciona el archivo Excel con los datos a cargar (Hoja1)"
        )

        df_editado = None
        placeholder_tabla = st.empty()
        placeholder_estadisticas = st.empty()

        if archivo_excel is not None:
            try:
                df_excel = pd.read_excel(archivo_excel, sheet_name=0)
                if df_excel.empty:
                    with placeholder_tabla.container():
                        st.error("❌ El archivo Excel está vacío")
                else:
                    df_procesado, columnas_faltantes, mapeo = procesar_dataframe_excel_cc(df_excel, opciones_operadores)
                    if columnas_faltantes:
                        with placeholder_tabla.container():
                            st.error(f"❌ No se encontraron las siguientes columnas: {', '.join(columnas_faltantes)}")
                            st.info(f"Columnas detectadas en el Excel: {', '.join(df_excel.columns.tolist())}")
                            st.info("💡 Puedes usar nombres similares. Revisa la plantilla oficial para ver los nombres exactos.")
                    else:
                        with placeholder_tabla.container():
                            with st.expander("🔍 Ver mapeo de columnas detectadas"):
                                for nombre_requerido, nombre_real in mapeo.items():
                                    st.write(f"  • '{nombre_real}' → **{nombre_requerido}**")
                        with placeholder_tabla.container():
                            st.subheader("📊 Vista previa de datos procesados")
                            st.caption("✏️ Los datos ya fueron transformados. Puedes editarlos antes de subir.")

                            # Configurar columnas para el data_editor
                            column_config = {
                                "distrito": st.column_config.SelectboxColumn(
                                    "Distrito",
                                    options=list(distritos_opciones),
                                    required=True
                                ),
                                "sector": st.column_config.TextColumn(
                                    "Sector",
                                    help="Formateado a 2 dígitos",
                                    required=True
                                ),
                                "manzana": st.column_config.TextColumn(
                                    "Manzana",
                                    help="Formateado a 3 dígitos",
                                    required=True
                                ),
                                "tipo": st.column_config.SelectboxColumn(
                                    "Tipo",
                                    options=list(tipo_opciones),
                                    required=True
                                ),
                                "operador": st.column_config.SelectboxColumn(
                                    "Operador objeto de CC",
                                    options=opciones_operadores,
                                    required=True
                                ),
                                "numero_lote": st.column_config.TextColumn(
                                    "N° Lote",
                                    help="Ej: 1,2,3 o 'Todos'"
                                ),
                                "tipo_de_errores": st.column_config.TextColumn(
                                    "Tipo Errores",
                                    help="Puedes ingresar números (1,3,5) o nombres separados por coma"
                                ),
                                "aprobados": st.column_config.NumberColumn(
                                    "Aprobados",
                                    min_value=0,
                                    step=1,
                                    required=True
                                ),
                                "rechazados": st.column_config.NumberColumn(
                                    "Rechazados",
                                    min_value=0,
                                    step=1,
                                    required=True
                                ),
                                "horas": st.column_config.NumberColumn(
                                    "Horas",
                                    min_value=0.0,
                                    format="%.2f",
                                    required=True
                                )
                            }

                            df_editado = st.data_editor(
                                df_procesado,
                                num_rows="dynamic",
                                use_container_width=True,
                                hide_index=True,
                                column_config=column_config,
                                key=f"editor_masivo_cc_{st.session_state.version_tabla_cc}"
                            )

                            # Reforzar transformaciones después de la edición
                            if df_editado is not None and not df_editado.empty:
                                df_editado['sector'] = df_editado['sector'].apply(formatear_sector_cc)
                                df_editado['manzana'] = df_editado['manzana'].apply(formatear_manzana_cc)
                                df_editado['numero_lote'] = df_editado['numero_lote'].apply(
                                    lambda x: formatear_lote_cc(x) if str(x).strip().lower() != 'todos' else 'Todos'
                                )
                                df_editado['horas'] = df_editado['horas'].apply(normalizar_horas_cc)
                                df_editado['aprobados'] = pd.to_numeric(df_editado['aprobados'], errors='coerce').fillna(0).astype(int)
                                df_editado['rechazados'] = pd.to_numeric(df_editado['rechazados'], errors='coerce').fillna(0).astype(int)
                                # Traducir tipo de errores nuevamente (por si el usuario editó)
                                df_editado['tipo_de_errores'] = df_editado['tipo_de_errores'].apply(traducir_tipos_errores)
                                # Limpiar espacios en campos de texto
                                for col in ['distrito', 'tipo', 'operador', 'numero_lote']:
                                    df_editado[col] = df_editado[col].apply(lambda x: limpiar_espacios_extra(str(x)) if pd.notna(x) else x)

                        if not df_editado.empty:
                            with placeholder_estadisticas.container():
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("📊 Registros", len(df_editado))
                                with col2:
                                    st.metric("🏘️ Sectores", df_editado['sector'].nunique())
                                with col3:
                                    st.metric("🏠 Manzanas", df_editado['manzana'].nunique())

            except Exception as e:
                with placeholder_tabla.container():
                    st.error(f"❌ Error al leer el archivo Excel: {str(e)}")
                    st.info("💡 Asegúrate de que el archivo sea un Excel válido (.xlsx o .xls) y que los datos estén en la Hoja1")

        placeholder_boton_masivo = st.empty()
        subir_masivo = placeholder_boton_masivo.button(
            "🚀 Subir Registros Masivos",
            type="primary",
            use_container_width=True,
            key="subir_masivo_cc",
            disabled=(df_editado is None or df_editado.empty)
        )

        if subir_masivo and df_editado is not None:
            with st.spinner("⏳ Validando datos..."):
                es_valido, mensaje_validacion = validar_datos_masivos_cc(
                    df_editado, list(distritos_opciones), list(tipo_opciones), opciones_operadores
                )
                if not es_valido:
                    st.error(f"❌ Error de validación:\n{mensaje_validacion}")
                    st.warning("⚠️ No se subió ningún registro. Corrige los errores e intenta de nuevo.")
                else:
                    st.success("✅ Validación exitosa")
                    usuario_activo = obtener_usuario_activo(usuario)
                    if not usuario_activo:
                        st.error("No se encontró un usuario activo para generar el reporte.")
                        return
                    with st.spinner("💾 Insertando registros en la base de datos..."):
                        exito, insertados, mensaje = insertar_registros_masivos_cc(
                            df_editado, fecha_masiva, usuario, usuario_activo, puesto
                        )
                        if exito:
                            st.success(f"✅ {mensaje}")
                            st.balloons()
                            # Reiniciar el estado para un nuevo lote (opcional)
                            st.session_state.version_tabla_cc += 1
                            st.rerun()
                        else:
                            st.error(f"❌ {mensaje}")
                            st.error(f"Se insertaron {insertados} registro(s) antes del error.")

    # ------------------------------------------------------------
    # Función para limpiar todos los placeholders
    # ------------------------------------------------------------
    def limpiar():
        for p in [placeholder1, placeholder2, placeholder3, placeholder4,
                  placeholder5, placeholder6, placeholder7, placeholder_titulo,
                  placeholder_modo,
                  placeholder_fecha, placeholder_distrito, placeholder_manzana,
                  placeholder_sector, placeholder_numero_lote, placeholder_operador,
                  placeholder_tipo, placeholder_tipo_errores,
                  placeholder_aprobados, placeholder_rechazados, placeholder_horas,
                  placeholder_reporte]:
            if p: p.empty()
        # Limpiar placeholders del modo masivo
        if 'placeholder_fecha_masiva' in locals() and placeholder_fecha_masiva:
            placeholder_fecha_masiva.empty()
        if 'placeholder_instrucciones' in locals() and placeholder_instrucciones:
            placeholder_instrucciones.empty()
        if 'placeholder_descarga_plantilla' in locals() and placeholder_descarga_plantilla:
            placeholder_descarga_plantilla.empty()
        if 'placeholder_archivo' in locals() and placeholder_archivo:
            placeholder_archivo.empty()
        if 'placeholder_tabla' in locals() and placeholder_tabla:
            placeholder_tabla.empty()
        if 'placeholder_estadisticas' in locals() and placeholder_estadisticas:
            placeholder_estadisticas.empty()
        if 'placeholder_boton_masivo' in locals() and placeholder_boton_masivo:
            placeholder_boton_masivo.empty()

    # ------------------------------------------------------------
    # Navegación
    # ------------------------------------------------------------
    if procesos_btn:
        limpiar()
        st.session_state.Procesos = False
        st.session_state.CC_Postcampo = False
        usuario_activo = obtener_usuario_activo(usuario)
        perfil = str(usuario_activo["perfil"]) if usuario_activo else ""
        if perfil == "1":
            Procesos.Procesos1(usuario, puesto)
        elif perfil == "2":
            Procesos.Procesos2(usuario, puesto)
        elif perfil == "3":
            Procesos.Procesos3(usuario, puesto)

    elif historial_btn:
        limpiar()
        st.session_state.CC_Postcampo = False
        st.session_state.Historial = True
        modulo_hist = obtener_modulo_historial(puesto)
        modulo_hist(usuario, puesto)

    elif capacitacion_btn:
        limpiar()
        st.session_state.CC_Postcampo = False
        st.session_state.Capacitacion = True
        Capacitacion.Capacitacion(usuario, puesto)

    elif otros_btn:
        limpiar()
        st.session_state.CC_Postcampo = False
        st.session_state.Otros_Registros = True
        Otros_Registros.Otros_Registros(usuario, puesto)

    elif bonos_btn:
        limpiar()
        st.session_state.CC_Postcampo = False
        st.session_state.Bonos_Extras = True
        Bonos_Extras.Bonos_Extras(usuario, puesto)

    elif salir_btn:
        limpiar()
        st.session_state.Ingreso = False
        st.session_state.CC_Postcampo = False
        st.session_state.Salir = True
        Salir.Salir()

    # ----- Generar Reporte (manual) -----
    elif modo_carga == "📝 Carga Manual (Formulario)" and reporte_btn:
        marca = datetime.now(pytz.timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M:%S")
        usuario_activo = obtener_usuario_activo(usuario)
        if not usuario_activo:
            st.error("No se encontró un usuario activo para generar el reporte.")
            return

        nombre = usuario_activo["nombre"]
        supervisor = usuario_activo["supervisor"]
        unidades_catastrales = aprobados_manual + rechazados_manual
        semana = fecha_manual.isocalendar()[1]
        año = fecha_manual.isocalendar()[0]
        horas_bi = float(horas_manual)
        tipos_de_errores_str = ','.join(tipo_errores_manual)
        conteo = len(tipo_errores_manual)

        execute(
            """
            INSERT INTO registro (
              marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito,tipo,lotes,aprobados,rechazados,horas,
              manzana,sector,numero_lote,estado,area,unidades_catastrales,edificas,partida,con_fmi,sin_fmi,observaciones,zona,
              tipo_calidad,horas_bi,area_bi,operador_cc,total_de_errores,errores_por_excepciones,tipo_de_errores,conteo_de_errores
            )
            VALUES (
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
              %s,%s,%s,%s,%s,%s,%s,%s
            )
            """,
            params=[
              marca, usuario, nombre, puesto, supervisor, "Control de Calidad Postcampo", fecha_manual, semana, año,
              distrito_manual, tipo_manual, 0, aprobados_manual, rechazados_manual, horas_manual,
              manzana_manual, sector_manual, numero_lote_manual, "N/A", 0.0, unidades_catastrales, 0, "N/A", 0, 0, "N/A", "N/A",
              "N/A", horas_bi, 0, operador_manual, 0, 0, tipos_de_errores_str, conteo
            ],
        )
        st.success('Reporte enviado correctamente')
