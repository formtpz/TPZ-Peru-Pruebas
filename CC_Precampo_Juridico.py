# ----- Librerías ---- #

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import io
import Procesos, Historial, Capacitacion, Otros_Registros, Bonos_Extras, Salir
from Autenticacion import obtener_usuario_activo
from db_core import execute, fetch_operadores_cc

def formatear_sector(valor):
    """Asegura que el sector tenga 2 dígitos (01, 02, etc.)"""
    try:
        return str(int(float(valor))).zfill(2)
    except:
        return str(valor).zfill(2)

def formatear_manzana(valor):
    """Asegura que la manzana tenga 3 dígitos (001, 002, etc.)"""
    try:
        return str(int(float(valor))).zfill(3)
    except:
        return str(valor).zfill(3)

def formatear_lote(valor):
    """
    Asegura que cada número de lote tenga 3 dígitos (001, 002, etc.)
    Soporta:
    - Número individual: "2" → "002"
    - Múltiples lotes: "2, 3, 112, 113" → "002, 003, 112, 113"
    - "Todos" → "Todos"
    """
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
            return ', '.join(numeros) if numeros else 'Todos'
        else:
            return str(int(float(valor_str))).zfill(3)
            
    except:
        return str(valor)

def normalizar_horas(valor):
    """Convierte comas a puntos en horas y asegura que sea float"""
    try:
        if isinstance(valor, str):
            valor = valor.replace(',', '.')
        return float(valor)
    except:
        return 0.0

def normalizar_texto(valor, default="N/A"):
    """Convierte valores nulos o vacíos al valor por defecto"""
    if pd.isna(valor) or valor == '' or valor is None:
        return default
    return str(valor)

def buscar_columnas_por_coincidencia(df):
    """
    Busca las columnas requeridas por coincidencia de nombres
    Retorna un diccionario mapeando nombre_requerido -> nombre_real_en_excel
    
    NOTA: 'estado' NO se busca en el Excel, se asigna "N/A" automáticamente
    """
    columnas_requeridas = {
        'distrito': ['distrito', 'DISTRITO', 'Distrito'],
        'sector': ['sector', 'SECTOR', 'Sector'],
        'manzana': ['manzana', 'MANZANA', 'Manzana', 'mz', 'MZ'],
        'tipo': ['tipo', 'TIPO', 'Tipo'],
        'numero_lote': ['numero_lote', 'numero lote', 'NÚMERO LOTE', 'N° Lote', 'lote', 'LOTE', 'n_lote', 'n° lote'],
        'partida': ['partida', 'PARTIDA', 'Partida', 'n° partida', 'n_partida'],
        'aprobados': ['aprobados', 'APROBADOS', 'Aprobados', 'registros_aprobados', 'aprob'],
        'rechazados': ['rechazados', 'RECHAZADOS', 'Rechazados', 'registros_rechazados', 'rech'],
        'horas': ['horas', 'HORAS', 'Horas', 'horas trabajadas', 'horas_trabajadas'],
        'observaciones': ['observaciones', 'OBSERVACIONES', 'Observaciones', 'obs', 'OBS'],
        'tipo_errores': ['tipo_errores', 'tipo de errores', 'TIPO DE ERRORES', 'TIPO_ERRORES', 
                         'tipo_errores', 'errores_tipo', 'tipo_error']
    }
    
    mapeo = {}
    for nombre_requerido, posibles_nombres in columnas_requeridas.items():
        for posible in posibles_nombres:
            if posible in df.columns:
                mapeo[nombre_requerido] = posible
                break
    
    return mapeo

def procesar_dataframe_excel(df):
    """
    Procesa el DataFrame del Excel aplicando todas las transformaciones
    'estado' NO se busca en Excel, se asigna "N/A" automáticamente
    """
    # Buscar columnas por coincidencia (sin 'estado')
    mapeo_columnas = buscar_columnas_por_coincidencia(df)
    
    # Verificar columnas encontradas (NO incluye 'estado')
    columnas_requeridas = [
        'distrito', 'sector', 'manzana', 'tipo', 
        'numero_lote', 'partida', 'aprobados', 'rechazados', 'horas', 'observaciones', 'tipo_errores'
    ]
    
    columnas_faltantes = [col for col in columnas_requeridas if col not in mapeo_columnas]
    
    if columnas_faltantes:
        return None, columnas_faltantes, mapeo_columnas
    
    # Crear nuevo DataFrame con nombres estandarizados
    df_procesado = pd.DataFrame()
    
    for nombre_requerido, nombre_real in mapeo_columnas.items():
        df_procesado[nombre_requerido] = df[nombre_real]
    
    # Asignar 'estado' como "N/A" fijo (NO viene del Excel)
    df_procesado['estado'] = "N/A"
    
    # Aplicar transformaciones
    df_procesado['sector'] = df_procesado['sector'].apply(formatear_sector)
    df_procesado['manzana'] = df_procesado['manzana'].apply(formatear_manzana)
    df_procesado['numero_lote'] = df_procesado['numero_lote'].apply(formatear_lote)
    df_procesado['horas'] = df_procesado['horas'].apply(normalizar_horas)
    
    # Aprobados y rechazados: convertir a entero
    df_procesado['aprobados'] = pd.to_numeric(df_procesado['aprobados'], errors='coerce').fillna(0).astype(int)
    df_procesado['rechazados'] = pd.to_numeric(df_procesado['rechazados'], errors='coerce').fillna(0).astype(int)
    
    # Unidades catastrales = Aprobados + Rechazados (cálculo automático)
    df_procesado['unidades_catastrales'] = df_procesado['aprobados'] + df_procesado['rechazados']
    
    df_procesado['observaciones'] = df_procesado['observaciones'].apply(lambda x: normalizar_texto(x, "N/A"))
    df_procesado['partida'] = df_procesado['partida'].apply(lambda x: normalizar_texto(x, "N/A"))
    df_procesado['numero_lote'] = df_procesado['numero_lote'].apply(lambda x: normalizar_texto(x, "Todos"))
    df_procesado['tipo_errores'] = df_procesado['tipo_errores'].apply(lambda x: normalizar_texto(x, "N/A"))
    
    # Agregar campo operador_cc con valor fijo "IA"
    df_procesado['operador_cc'] = "IA"
    
    return df_procesado, [], mapeo_columnas

def validar_datos_masivos(df, fecha_seleccionada):
    """
    Valida los datos antes de la inserción masiva
    Retorna (es_valido, mensaje_error)
    NOTA: No valida 'estado' porque es "N/A" fijo
    """
    errores = []
    
    if df.empty:
        return False, "La tabla está vacía. No hay datos para procesar."
    
    columnas_requeridas = ['distrito', 'sector', 'manzana', 'tipo']
    for col in columnas_requeridas:
        nulos = df[col].isnull().sum()
        if nulos > 0:
            errores.append(f"La columna '{col}' tiene {nulos} valores nulos")
    
    distritos_validos = ["Chorrillos", "San Juan De Miraflores", "Villa el Salvador"]
    distritos_invalidos = df[~df['distrito'].isin(distritos_validos)]
    if not distritos_invalidos.empty:
        filas_invalidas = distritos_invalidos.index.tolist()
        errores.append(f"Hay {len(distritos_invalidos)} registros con distrito inválido en filas: {filas_invalidas}")
    
    tipos_validos = ["Ordinario", "Reproceso Ordinario", "Corrección de Calidad", 
                     "Corrección de Calidad Extraordinaria", "Producción Horas Extras"]
    tipos_invalidos = df[~df['tipo'].isin(tipos_validos)]
    if not tipos_invalidos.empty:
        filas_invalidas = tipos_invalidos.index.tolist()
        errores.append(f"Hay {len(tipos_invalidos)} registros con tipo inválido en filas: {filas_invalidas}")
    
    horas_invalidas = df[df['horas'] < 0]
    if not horas_invalidas.empty:
        errores.append(f"Hay {len(horas_invalidas)} registros con horas negativas")
    
    aprobados_invalidos = df[df['aprobados'] < 0]
    if not aprobados_invalidos.empty:
        errores.append(f"Hay {len(aprobados_invalidos)} registros con aprobados negativos")
    
    rechazados_invalidos = df[df['rechazados'] < 0]
    if not rechazados_invalidos.empty:
        errores.append(f"Hay {len(rechazados_invalidos)} registros con rechazados negativos")
    
    if errores:
        return False, "\n".join(errores)
    
    return True, "Datos válidos"

def insertar_registros_masivos(df, fecha_seleccionada, usuario, usuario_activo):
    """
    Inserta múltiples registros usando la función execute existente
    """
    try:
        marca = datetime.now(pytz.timezone('America/Guatemala')).strftime("%Y-%m-%d %H:%M:%S")
        nombre = usuario_activo["nombre"]
        supervisor = usuario_activo["supervisor"]
        puesto = usuario_activo.get("puesto", "")
        
        semana = fecha_seleccionada.isocalendar()[1]
        año = fecha_seleccionada.isocalendar()[0]
        
        registros_insertados = 0
        
        for index, row in df.iterrows():
            sector_formateado = row['sector']
            manzana_formateada = row['manzana']
            horas = float(row['horas'])
            horas_bi = horas
            aprobados = int(row.get('aprobados', 0))
            rechazados = int(row.get('rechazados', 0))
            unidades_catastrales = aprobados + rechazados
            partida = str(row['partida'])
            observaciones = str(row['observaciones'])
            numero_lote = str(row['numero_lote'])
            operador_cc = str(row.get('operador_cc', 'IA'))
            tipo_errores = str(row.get('tipo_errores', 'N/A'))
            estado = "N/A"  # FIJO para CC Precampo Jurídico
            
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
                    marca, usuario, nombre, puesto, supervisor, "CC Precampo Jurídico", 
                    fecha_seleccionada, semana, año, row['distrito'], row['tipo'], 0, aprobados, rechazados, horas,
                    manzana_formateada, sector_formateado, numero_lote, estado, 
                    0.0, unidades_catastrales, 0, partida, 0, 0, observaciones, "N/A",
                    "N/A", horas_bi, 0.0, operador_cc, 0, 0, tipo_errores, 0
                ],
            )
            registros_insertados += 1
        
        return True, registros_insertados, f"Se insertaron {registros_insertados} registros exitosamente"
    
    except Exception as e:
        return False, registros_insertados, f"Error al insertar registros: {str(e)}"

def CC_Precampo_Juridico(usuario, puesto):

    # ----- Conexión, Botones y Memoria ---- #
    uri = st.secrets.db_credentials.URI

    # Inicializar TODOS los placeholders como None
    placeholder_fecha_masiva = None
    placeholder_instrucciones_masivo = None
    placeholder_descarga = None
    placeholder_archivo = None
    placeholder_tabla_masiva = None
    placeholder_boton_masivo = None
    placeholder_estadisticas = None

    placeholder1_cc = st.sidebar.empty()
    titulo = placeholder1_cc.title("Menú")

    placeholder2_cc = st.sidebar.empty()
    procesos_cc = placeholder2_cc.button("Procesos", key="procesos_cc")

    placeholder3_cc = st.sidebar.empty()
    historial_cc = placeholder3_cc.button("Historial", key="historial_cc")

    placeholder4_cc = st.sidebar.empty()
    capacitacion_cc = placeholder4_cc.button("Capacitaciones", key="capacitacion_cc")

    placeholder5_cc = st.sidebar.empty()
    otros_registros_cc = placeholder5_cc.button("Otros Registros", key="otros_registros_cc")

    placeholder6_cc = st.sidebar.empty()
    bonos_extras_cc = placeholder6_cc.button("Bonos y Horas Extras", key="bonos_extras_cc")

    placeholder7_cc = st.sidebar.empty()
    salir_cc = placeholder7_cc.button("Salir", key="salir_cc")

    # ----- Selector de modo de carga ----- #
    placeholder_modo = st.empty()
    modo_carga = placeholder_modo.radio(
        "Selecciona el modo de carga:",
        options=["📝 Carga Manual (Formulario)", "📋 Carga Masiva (Subir Excel)"],
        key="modo_carga_cc_precampo"
    )

    placeholder8_cc = st.empty()
    CC_Precampo_Juridico_titulo = placeholder8_cc.title("Control de Calidad Precampo Jurídico")

    # Inicializar variables del formulario manual como None
    placeholder9_cc = None
    placeholder10_cc = None
    placeholder11_cc = None
    placeholder12_cc = None
    placeholder13_cc = None
    placeholder14_cc = None
    placeholder15_cc = None
    placeholder16_cc = None
    placeholderP_cc = None
    placeholder17_cc = None
    placeholder18_cc = None
    placeholder19_cc = None
    placeholder20_cc = None
    
    fecha_cc = None
    distrito_cc = None
    manzana_cc = None
    sector_cc = None
    numero_lote_cc = None
    operador_cc = None
    tipo_cc = None
    tipo_errores_cc = None
    partida_cc = None
    aprobados_cc = None
    rechazados_cc = None
    horas_cc = None
    reporte_cc = None

    # ============================================
    # MODO DE CARGA MANUAL (FORMULARIO SIMPLIFICADO)
    # ============================================
    if modo_carga == "📝 Carga Manual (Formulario)":
        
        default_date_cc = datetime.now(pytz.timezone('America/Guatemala'))

        placeholder9_cc = st.empty()
        fecha_cc = placeholder9_cc.date_input("📅 Fecha", value=default_date_cc, key="fecha_cc")
         
        placeholder10_cc = st.empty()
        distrito_cc = placeholder10_cc.selectbox("📍 Distrito", options=("Chorrillos", "San Juan De Miraflores", "Villa el Salvador"), key="distrito_cc")
        
        placeholder11_cc = st.empty()
        manzana_cc = placeholder11_cc.selectbox("🏠 Manzana", options=("001","002","003","004","005","006","007","008","009","010","011","012","013","014","015","016","017","018","019","020","021","022","023","024","025","026","027","028","029","030","031","032","033","034","035","036","037","038","039","040","041","042","043","044","045","046","047","048","049","050","051","052","053","054","055","056","057","058","058","059","060","061","062","063","064","065","066","067","068","069","070","071","072","073","074","075","076","077","078","079","080","081","082","083","084","085","086","087","088","089","090","091","092","093","094","095","096","097","098","099","100","101","102","103","104","105","106","107","108","109","110","111","112","113","114","115","116","117","118","119","120"), key="manzana_cc")
        
        placeholder12_cc = st.empty()
        sector_cc = placeholder12_cc.selectbox("🏘️ Sector", options=("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100","101","102","103","104","105","106","107","108","109","110","111","112","113","114","115","116","117","118","119","120"), key="sector_cc")

        # =========================
        # Generar lista dinámica de lotes
        # =========================
        lotes = ["Todos"] + [f"{i:03d}" for i in range(1,249)]
        
        placeholder13_cc = st.empty()
        numero_lote_seleccionado = placeholder13_cc.multiselect(
            "🔢 Número de Lote",
            options=lotes,
            key="numero_lote_cc"
        )
        
        # Lógica para "Todos"
        if "Todos" in numero_lote_seleccionado:
            numero_lote_seleccionado = ["Todos"]
        
        numero_lote_cc = ",".join(numero_lote_seleccionado)
        
        # ----- Selector de Operador con datos desde BD ---- #
        operadores_disponibles = fetch_operadores_cc(
            filtro_proceso='Jurídico',
            filtro_subproceso=['Descarga', 'Análisis'],
            filtro_proceso_anterior='Jurídico',
            filtro_subproceso_anterior=['Descarga', 'Análisis']
        )
        
        if operadores_disponibles:
            opciones_operadores = [op['nombre'] for op in operadores_disponibles]
        else:
            opciones_operadores = ["No hay operadores disponibles"]
        
        placeholder14_cc = st.empty()
        operador_cc = placeholder14_cc.selectbox(
            "👤 Operador objeto de CC",
            options=opciones_operadores,
            key="operador_cc"
        )
        
        placeholder15_cc = st.empty()
        tipo_cc = placeholder15_cc.selectbox(
            "📋 Tipo",
            options=("Inspección", "Primera Reinspección", "Inspección Horas Extras", "Control de Calidad Supervisión"),
            key="tipo_cc"
        )
        
        placeholder16_cc = st.empty()
        tipo_errores_seleccionados = placeholder16_cc.multiselect(
            "⚠️ Tipo de Errores",
            options=("Numeración errónea o incompleta",
                     "Errores geométricos y/o de forma",
                     "Polígonos y/o puntos duplicados",
                     "Omisión/Comisión de polígonos",
                     "Polígonos no se ajustan a ortofoto",
                     "Omisión/Comisión de puertas"),
            key="tipo_errores_cc"
        )
        
        placeholderP_cc = st.empty()
        partida_cc = placeholderP_cc.text_input("📄 Número de Partida", value='N/A', max_chars=60, key="partida_cc")
        
        placeholder17_cc = st.empty()
        aprobados_cc = placeholder17_cc.number_input("✅ Cantidad de Registros Aprobados", min_value=0, step=1, key="aprobados_cc")
        
        placeholder18_cc = st.empty()
        rechazados_cc = placeholder18_cc.number_input("❌ Cantidad de Registros Rechazados", min_value=0, step=1, key="rechazados_cc")
        
        placeholder19_cc = st.empty()
        horas_cc = placeholder19_cc.number_input("⏱️ Cantidad de Horas Trabajadas en el Proceso", min_value=0.0, key="horas_cc")
        
        placeholder20_cc = st.empty()
        reporte_cc = placeholder20_cc.button("🚀 Generar Reporte", key="reporte_cc", type="primary")

    # ============================================
    # MODO DE CARGA MASIVA (SUBIR EXCEL) - SIN MODIFICACIONES
    # ============================================
    else:
        
        placeholder_fecha_masiva = st.empty()
        fecha_masiva = placeholder_fecha_masiva.date_input(
            "📅 Fecha para todos los registros",
            value=datetime.now(pytz.timezone('America/Guatemala')),
            key="fecha_masiva_cc_precampo"
        )
        
        placeholder_instrucciones_masivo = st.empty()
        with placeholder_instrucciones_masivo.container():
            st.info("""
        📋 **Instrucciones:**
        1. Descarga la plantilla Excel oficial (abajo)
        2. Llena tus datos en la **Hoja1** del Excel
        3. Los nombres de columna pueden variar ligeramente (se detectan por coincidencia)
        4. Sube el archivo Excel
        5. Revisa la vista previa antes de confirmar
        
        **Columnas requeridas en el Excel:**
        - Distrito, Sector, Manzana, Tipo
        - N° Lote, Partida, Aprobados, Rechazados
        - Horas, Observaciones, Tipo de Errores
        
        **⚠️ NO incluir columna "Estado"** (se asigna "N/A" automáticamente)
        
        **Transformaciones automáticas:**
        - Sector: 1 → 01
        - Manzana: 5 → 005
        - N° Lote: 2,3,112 → 002,003,112
        - Horas: 8,5 → 8.5
        - Campos vacíos → "N/A" o "Todos"
        - Estado → "N/A" (fijo)
        - Operador CC → "IA" (fijo)
        - **Unidades Catastrales = Aprobados + Rechazados** (automático)
            """)
        
        placeholder_descarga = st.empty()
        with placeholder_descarga.container():
            st.markdown("### 📥 Plantilla oficial")
            
            url_plantilla = "https://raw.githubusercontent.com/formtpz/TPZ-Peru-Pruebas/main/docs/ccprecampojuridico.xlsx"
            
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
                st.caption("Descarga el machote oficial `ccprecampojuridico.xlsx`")
                st.caption(f"🔗 [Enlace directo]({url_plantilla})")
        
        placeholder_archivo = st.empty()
        archivo_excel = placeholder_archivo.file_uploader(
            "📁 Subir archivo Excel con datos",
            type=['xlsx', 'xls'],
            key="archivo_excel_cc_precampo",
            help="Selecciona el archivo Excel con los datos a cargar (Hoja1)"
        )
        
        df_editado = None
        placeholder_tabla_masiva = st.empty()
        placeholder_estadisticas = st.empty()
        
        if archivo_excel is not None:
            try:
                df_excel = pd.read_excel(archivo_excel, sheet_name=0)
                
                if df_excel.empty:
                    with placeholder_tabla_masiva.container():
                        st.error("❌ El archivo Excel está vacío")
                else:
                    df_procesado, columnas_faltantes, mapeo = procesar_dataframe_excel(df_excel)
                    
                    if columnas_faltantes:
                        with placeholder_tabla_masiva.container():
                            st.error(f"❌ No se encontraron las siguientes columnas: {', '.join(columnas_faltantes)}")
                            st.info(f"Columnas detectadas en el Excel: {', '.join(df_excel.columns.tolist())}")
                            st.info("💡 Puedes usar nombres similares. Revisa la plantilla oficial para ver los nombres exactos.")
                            st.info("📋 Columnas requeridas: Distrito, Sector, Manzana, Tipo, N° Lote, Partida, Aprobados, Rechazados, Horas, Observaciones, Tipo de Errores")
                            st.info("⚠️ La columna 'Estado' NO debe incluirse (se asigna 'N/A' automáticamente)")
                    else:
                        with placeholder_tabla_masiva.container():
                            with st.expander("🔍 Ver mapeo de columnas detectadas"):
                                st.write("Columnas encontradas en el Excel y su correspondencia:")
                                for nombre_requerido, nombre_real in mapeo.items():
                                    st.write(f"  • '{nombre_real}' → **{nombre_requerido}**")
                        
                        with placeholder_tabla_masiva.container():
                            st.subheader("📊 Vista previa de datos procesados")
                            st.caption("✏️ Los datos ya fueron transformados. Puedes editarlos antes de subir.")
                            
                            df_editado = st.data_editor(
                                df_procesado,
                                num_rows="dynamic",
                                use_container_width=True,
                                hide_index=True,
                                column_config={
                                    "distrito": st.column_config.SelectboxColumn(
                                        "📍 Distrito",
                                        options=["Chorrillos", "San Juan De Miraflores", "Villa el Salvador"],
                                        required=True
                                    ),
                                    "sector": st.column_config.TextColumn(
                                        "🏘️ Sector",
                                        help="Formateado a 2 dígitos",
                                        required=True
                                    ),
                                    "manzana": st.column_config.TextColumn(
                                        "🏠 Manzana",
                                        help="Formateado a 3 dígitos",
                                        required=True
                                    ),
                                    "tipo": st.column_config.SelectboxColumn(
                                        "📋 Tipo",
                                        options=["Ordinario", "Reproceso Ordinario", "Corrección de Calidad", 
                                                "Corrección de Calidad Extraordinaria", "Producción Horas Extras"],
                                        required=True
                                    ),
                                    "estado": st.column_config.TextColumn(
                                        "📌 Estado",
                                        disabled=True,
                                        help="Valor fijo: N/A (no aplica para CC Precampo Jurídico)"
                                    ),
                                    "numero_lote": st.column_config.TextColumn(
                                        "🔢 N° Lote",
                                        help="Para múltiples lotes, separar por comas. Ej: 2,3,112 → 002,003,112"
                                    ),
                                    "partida": st.column_config.TextColumn("📄 Partida"),
                                    "aprobados": st.column_config.NumberColumn(
                                        "✅ Aprobados",
                                        min_value=0,
                                        required=True
                                    ),
                                    "rechazados": st.column_config.NumberColumn(
                                        "❌ Rechazados",
                                        min_value=0,
                                        required=True
                                    ),
                                    "unidades_catastrales": st.column_config.NumberColumn(
                                        "📊 Total U.C.",
                                        disabled=True,
                                        help="Aprobados + Rechazados (automático)"
                                    ),
                                    "horas": st.column_config.NumberColumn(
                                        "⏱️ Horas Trab.",
                                        min_value=0.0,
                                        required=True
                                    ),
                                    "observaciones": st.column_config.TextColumn("📝 Observaciones"),
                                    "tipo_errores": st.column_config.TextColumn("⚠️ Tipo de Errores"),
                                    "operador_cc": st.column_config.TextColumn(
                                        "🤖 Operador CC",
                                        disabled=True,
                                        help="Valor fijo: IA"
                                    )
                                },
                                key="editor_masivo_cc_precampo"
                            )
                            
                            # Recalcular después de edición
                            df_editado['observaciones'] = df_editado['observaciones'].fillna('N/A').replace('', 'N/A')
                            df_editado['partida'] = df_editado['partida'].fillna('N/A').replace('', 'N/A')
                            df_editado['numero_lote'] = df_editado['numero_lote'].fillna('Todos').replace('', 'Todos')
                            df_editado['tipo_errores'] = df_editado['tipo_errores'].fillna('N/A').replace('', 'N/A')
                            df_editado['estado'] = 'N/A'  # Asegurar que estado siempre sea N/A
                            df_editado['aprobados'] = pd.to_numeric(df_editado['aprobados'], errors='coerce').fillna(0).astype(int)
                            df_editado['rechazados'] = pd.to_numeric(df_editado['rechazados'], errors='coerce').fillna(0).astype(int)
                            df_editado['unidades_catastrales'] = df_editado['aprobados'] + df_editado['rechazados']
                            df_editado['sector'] = df_editado['sector'].apply(formatear_sector)
                            df_editado['manzana'] = df_editado['manzana'].apply(formatear_manzana)
                            df_editado['numero_lote'] = df_editado['numero_lote'].apply(formatear_lote)
                            df_editado['operador_cc'] = 'IA'
                        
                        if not df_editado.empty:
                            with placeholder_estadisticas.container():
                                col1, col2, col3, col4 = st.columns(4)
                                with col1:
                                    st.metric("📊 Registros", len(df_editado))
                                with col2:
                                    sectores_unicos = df_editado['sector'].unique()
                                    st.metric("🏘️ Sectores", len(sectores_unicos))
                                with col3:
                                    total_aprobados = df_editado['aprobados'].sum()
                                    st.metric("✅ Total Aprobados", total_aprobados)
                                with col4:
                                    total_rechazados = df_editado['rechazados'].sum()
                                    st.metric("❌ Total Rechazados", total_rechazados)
            
            except Exception as e:
                with placeholder_tabla_masiva.container():
                    st.error(f"❌ Error al leer el archivo Excel: {str(e)}")
                    st.info("💡 Asegúrate de que el archivo sea un Excel válido (.xlsx o .xls) y que los datos estén en la Hoja1")
        
        placeholder_boton_masivo = st.empty()
        subir_masivo = placeholder_boton_masivo.button(
            "🚀 Subir Registros Masivos", 
            type="primary", 
            use_container_width=True,
            key="subir_masivo_cc_precampo",
            disabled=(df_editado is None or df_editado.empty)
        )
        
        if subir_masivo and df_editado is not None:
            with st.spinner("⏳ Validando datos..."):
                es_valido, mensaje_validacion = validar_datos_masivos(df_editado, fecha_masiva)
                
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
                        exito, insertados, mensaje = insertar_registros_masivos(
                            df_editado, fecha_masiva, usuario, usuario_activo
                        )
                        
                        if exito:
                            st.success(f"✅ {mensaje}")
                            st.balloons()
                        else:
                            st.error(f"❌ {mensaje}")
                            st.error(f"Se insertaron {insertados} registros antes del error.")

    # ============================================
    # FUNCIÓN PARA LIMPIAR PLACEHOLDERS
    # ============================================
    def limpiar_placeholders():
        """Limpia todos los placeholders posibles"""
        placeholder1_cc.empty()
        placeholder2_cc.empty()
        placeholder3_cc.empty()
        placeholder4_cc.empty()
        placeholder5_cc.empty()
        placeholder6_cc.empty()
        placeholder7_cc.empty()
        placeholder8_cc.empty()
        placeholder_modo.empty()
        
        if placeholder9_cc: placeholder9_cc.empty()
        if placeholder10_cc: placeholder10_cc.empty()
        if placeholder11_cc: placeholder11_cc.empty()
        if placeholder12_cc: placeholder12_cc.empty()
        if placeholder13_cc: placeholder13_cc.empty()
        if placeholder14_cc: placeholder14_cc.empty()
        if placeholder15_cc: placeholder15_cc.empty()
        if placeholder16_cc: placeholder16_cc.empty()
        if placeholderP_cc: placeholderP_cc.empty()
        if placeholder17_cc: placeholder17_cc.empty()
        if placeholder18_cc: placeholder18_cc.empty()
        if placeholder19_cc: placeholder19_cc.empty()
        if placeholder20_cc: placeholder20_cc.empty()
        
        if placeholder_fecha_masiva: placeholder_fecha_masiva.empty()
        if placeholder_instrucciones_masivo: placeholder_instrucciones_masivo.empty()
        if placeholder_descarga: placeholder_descarga.empty()
        if placeholder_archivo: placeholder_archivo.empty()
        if placeholder_tabla_masiva: placeholder_tabla_masiva.empty()
        if placeholder_estadisticas: placeholder_estadisticas.empty()
        if placeholder_boton_masivo: placeholder_boton_masivo.empty()

    # ============================================
    # NAVEGACIÓN ENTRE MÓDULOS
    # ============================================
    
    # ----- Procesos ---- #
    if procesos_cc:
        limpiar_placeholders()
        st.session_state.Procesos = False
        st.session_state.Postcampo = False
        usuario_activo = obtener_usuario_activo(usuario)
        perfil = str(usuario_activo["perfil"]) if usuario_activo else ""
        if perfil == "1":        
            Procesos.Procesos1(usuario, puesto)
        elif perfil == "2":        
            Procesos.Procesos2(usuario, puesto)   
        elif perfil == "3":  
            Procesos.Procesos3(usuario, puesto)       

    # ----- Historial ---- #
    elif historial_cc:
        limpiar_placeholders()
        st.session_state.Postcampo = False
        st.session_state.Historial = True
        Historial.Historial(usuario, puesto)   

    # ----- Capacitación ---- #
    elif capacitacion_cc:
        limpiar_placeholders()
        st.session_state.Postcampo = False
        st.session_state.Capacitacion = True
        Capacitacion.Capacitacion(usuario, puesto)

    # ----- Otros Registros ---- #
    elif otros_registros_cc:
        limpiar_placeholders()
        st.session_state.Postcampo = False
        st.session_state.Otros_Registros = True
        Otros_Registros.Otros_Registros(usuario, puesto)

    # ----- Bonos y Horas Extras ---- #
    elif bonos_extras_cc:
        limpiar_placeholders()
        st.session_state.Postcampo = False
        st.session_state.Bonos_Extras = True
        Bonos_Extras.Bonos_Extras(usuario, puesto)    

    # ----- Salir ---- #
    elif salir_cc:
        limpiar_placeholders()
        st.session_state.Ingreso = False
        st.session_state.Postcampo = False
        st.session_state.Salir = True
        Salir.Salir()

    # ============================================
    # ENVÍO DE FORMULARIO MANUAL (SIMPLIFICADO)
    # ============================================
    elif modo_carga == "📝 Carga Manual (Formulario)" and reporte_cc:

        marca_cc = datetime.now(pytz.timezone('America/Guatemala')).strftime("%Y-%m-%d %H:%M:%S")
        
        usuario_activo = obtener_usuario_activo(usuario)
        if not usuario_activo:
            st.error("No se encontró un usuario activo para generar el reporte.")
            return

        nombre_cc = usuario_activo["nombre"]
        supervisor_cc = usuario_activo["supervisor"]
        semana_cc = fecha_cc.isocalendar()[1]
        año_cc = fecha_cc.isocalendar()[0]
        horas_bi = float(horas_cc)
        unidades_catastrales_cc = aprobados_cc + rechazados_cc
        tipos_de_errores_cc = ','.join(tipo_errores_seleccionados)
        conteo_errores_cc = len(tipo_errores_seleccionados)
        
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
                marca_cc, usuario, nombre_cc, puesto, supervisor_cc, "Control de Calidad Precampo Jurídico", 
                fecha_cc, semana_cc, año_cc, distrito_cc, tipo_cc, 0, aprobados_cc, rechazados_cc, horas_cc,
                manzana_cc, sector_cc, numero_lote_cc, "N/A", 0.0, unidades_catastrales_cc, 0, partida_cc, 0, 0, "N/A", "N/A",
                "N/A", horas_bi, 0.0, operador_cc, 0, 0, tipos_de_errores_cc, conteo_errores_cc
            ],
        )
        st.success('✅ Reporte enviado correctamente')
        st.balloons()
