# ----- Librerías ---- #

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import io
import Procesos,Historial,Capacitacion,Otros_Registros,Bonos_Extras,Salir
from Autenticacion import obtener_usuario_activo
from db_core import execute

def validar_datos_masivos(df):
    """
    Valida los datos antes de la inserción masiva
    Retorna (es_valido, mensaje_error)
    """
    errores = []
    
    # Validar que no esté vacío
    if df.empty:
        return False, "La tabla está vacía. No hay datos para procesar."
    
    # Columnas requeridas según tu estructura
    columnas_requeridas = [
        'fecha', 'distrito', 'sector', 'manzana', 'tipo', 
        'estado', 'numero_lote', 'partida', 'unidades_catastrales', 
        'horas', 'observaciones'
    ]
    
    # Verificar columnas faltantes
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    if columnas_faltantes:
        return False, f"Faltan las siguientes columnas: {', '.join(columnas_faltantes)}"
    
    # Validar valores nulos
    for col in columnas_requeridas:
        nulos = df[col].isnull().sum()
        if nulos > 0:
            errores.append(f"La columna '{col}' tiene {nulos} valores nulos")
    
    # Validar distritos válidos
    distritos_validos = ["Chorrillos", "San Juan De Miraflores", "Villa el Salvador"]
    distritos_invalidos = df[~df['distrito'].isin(distritos_validos)]
    if not distritos_invalidos.empty:
        errores.append(f"Hay {len(distritos_invalidos)} registros con distrito inválido")
    
    # Validar tipos válidos
    tipos_validos = ["Ordinario", "Reproceso Ordinario", "Corrección de Calidad", 
                     "Corrección de Calidad Extraordinaria", "Producción Horas Extras"]
    tipos_invalidos = df[~df['tipo'].isin(tipos_validos)]
    if not tipos_invalidos.empty:
        errores.append(f"Hay {len(tipos_invalidos)} registros con tipo inválido")
    
    # Validar estados válidos
    estados_validos = ["Finalizado", "En Conflicto"]
    estados_invalidos = df[~df['estado'].isin(estados_validos)]
    if not estados_invalidos.empty:
        errores.append(f"Hay {len(estados_invalidos)} registros con estado inválido")
    
    # Validar que horas sea numérico y positivo
    try:
        horas_invalidas = df[~df['horas'].apply(lambda x: float(x) >= 0)]
        if not horas_invalidas.empty:
            errores.append(f"Hay {len(horas_invalidas)} registros con horas negativas")
    except:
        errores.append("La columna 'horas' debe contener valores numéricos")
    
    # Validar que unidades_catastrales sea entero positivo
    try:
        uc_invalidas = df[~df['unidades_catastrales'].apply(lambda x: int(x) >= 0)]
        if not uc_invalidas.empty:
            errores.append(f"Hay {len(uc_invalidas)} registros con unidades catastrales negativas")
    except:
        errores.append("La columna 'unidades_catastrales' debe contener valores enteros")
    
    if errores:
        return False, "\n".join(errores)
    
    return True, "Datos válidos"

def parsear_datos_pegados(texto_pegado):
    """
    Convierte texto pegado desde Excel en un DataFrame
    """
    try:
        # Intentar con tabulación (formato más común al pegar desde Excel)
        df = pd.read_csv(io.StringIO(texto_pegado), sep='\t', encoding='utf-8')
        
        # Si solo tiene una columna, intentar con otros separadores
        if len(df.columns) == 1:
            df = pd.read_csv(io.StringIO(texto_pegado), sep=',', encoding='utf-8')
            if len(df.columns) == 1:
                df = pd.read_csv(io.StringIO(texto_pegado), sep=';', encoding='utf-8')
        
        return df, None
    except Exception as e:
        return None, f"Error al procesar los datos: {str(e)}"

def insertar_registros_masivos(df, usuario, usuario_activo):
    """
    Inserta múltiples registros usando la función execute existente
    Retorna (exito, registros_insertados, mensaje)
    """
    try:
        marca = datetime.now(pytz.timezone('America/Guatemala')).strftime("%Y-%m-%d %H:%M:%S")
        nombre = usuario_activo["nombre"]
        supervisor = usuario_activo["supervisor"]
        puesto = usuario_activo.get("puesto", "")
        
        registros_insertados = 0
        
        for index, row in df.iterrows():
            # Procesar fecha
            fecha = pd.to_datetime(row['fecha']).date()
            semana = fecha.isocalendar()[1]
            año = fecha.isocalendar()[0]
            
            # Convertir horas a float
            horas = float(row['horas'])
            horas_bi = horas
            
            # Convertir unidades catastrales
            unidades_catastrales = int(row['unidades_catastrales'])
            
            # Valores por defecto
            partida = str(row.get('partida', 'N/A'))
            observaciones = str(row.get('observaciones', 'N/A'))
            numero_lote = str(row.get('numero_lote', 'Todos'))
            
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
                    marca, usuario, nombre, puesto, supervisor, "Precampo Jurídico", 
                    fecha, semana, año, row['distrito'], row['tipo'], 0, 0, 0, horas,
                    row['manzana'], row['sector'], numero_lote, row['estado'], 
                    0.0, unidades_catastrales, 0, partida, 0, 0, observaciones, "N/A",
                    "N/A", horas_bi, 0.0, "N/A", 0, 0, "N/A", 0
                ],
            )
            registros_insertados += 1
        
        return True, registros_insertados, f"Se insertaron {registros_insertados} registros exitosamente"
    
    except Exception as e:
        return False, registros_insertados, f"Error al insertar registros: {str(e)}"

def Precampo_Juridico(usuario,puesto):

  # ----- Conexión, Botones y Memoria ---- #
  uri=st.secrets.db_credentials.URI

  placeholder1_3= st.sidebar.empty()
  titulo= placeholder1_3.title("Menú")

  placeholder2_3 = st.sidebar.empty()
  procesos_3 = placeholder2_3.button("Procesos",key="procesos_3")

  placeholder3_3 = st.sidebar.empty()
  historial_3 = placeholder3_3.button("Historial",key="historial_3")

  placeholder4_3 = st.sidebar.empty()
  capacitacion_3 = placeholder4_3.button("Capacitaciones",key="capacitacion_3")

  placeholder5_3 = st.sidebar.empty()
  otros_registros_3 = placeholder5_3.button("Otros Registros",key="otros_registros_3")

  placeholder6_3 = st.sidebar.empty()
  bonos_extras_3 = placeholder6_3.button("Bonos y Horas Extras",key="bonos_extras_3")

  placeholder7_3 = st.sidebar.empty()
  salir_3 = placeholder7_3.button("Salir",key="salir_3")

  # ----- NUEVO: Selector de modo de carga ----- #
  placeholder_modo = st.empty()
  modo_carga = placeholder_modo.radio(
      "Selecciona el modo de carga:",
      options=["📝 Carga Manual (Formulario)", "📋 Carga Masiva (Pegar desde Excel)"],
      key="modo_carga_precampo"
  )

  placeholder8_3 = st.empty()
  Precampo_Juridico_3 = placeholder8_3.title("Precampo Jurídico")

  # ============================================
  # MODO DE CARGA MANUAL (TU CÓDIGO ORIGINAL)
  # ============================================
  if modo_carga == "📝 Carga Manual (Formulario)":
    
    default_date_3 = datetime.now(pytz.timezone('America/Guatemala'))

    placeholder9_3= st.empty()
    fecha_3= placeholder9_3.date_input("Fecha",value=default_date_3,key="fecha_3")
     
    placeholder10_3= st.empty()
    distrito_3= placeholder10_3.selectbox("Distrito", options=("Chorrillos","San Juan De Miraflores","Villa el Salvador"), key="distrito_3")
    
    placeholder12_3= st.empty()
    sector_3= placeholder12_3.selectbox("Sector", options=("01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100","101","102","103","104","105","106","107","108","109","110","111","112","113","114","115","116","117","118","119","120"), key="sector_3")

    placeholder13_3= st.empty()
    manzana_3= placeholder13_3.selectbox("Manzana", options=("001","002","003","004","005","006","007","008","009","010","011","012","013","014","015","016","017","018","019","020","021","022","023","024","025","026","027","028","029","030","031","032","033","034","035","036","037","038","039","040","041","042","043","044","045","046","047","048","049","050","051","052","053","054","055","056","057","058","058","059","060","061","062","063","064","065","066","067","068","069","070","071","072","073","074","075","076","077","078","079","080","081","082","083","084","085","086","087","088","089","090","091","092","093","094","095","096","097","098","099","100","101","102","103","104","105","106","107","108","109","110","111","112","113","114","115","116","117","118","119","120"),key="manzana_3")
    
    placeholder15_3= st.empty()
    tipo_3= placeholder15_3.selectbox("Tipo", options=("Ordinario","Reproceso Ordinario","Corrección de Calidad","Corrección de Calidad Extraordinaria","Producción Horas Extras"), key="tipo_3")
    
    placeholder16_3= st.empty()
    estado_3= placeholder16_3.selectbox("Estado" , options=("Finalizado","En Conflicto"),key="estado_3")
    
    lotes = ["Todos"] + [f"{i:03d}" for i in range(1,249)]
    
    placeholder18_3 = st.empty()
    
    numero_lote_3 = placeholder18_3.multiselect(
        "Número de Lote",
        options=lotes,
        key="numero_lote_3"
    )
    
    if "Todos" in numero_lote_3:
        numero_lote_3 = ["Todos"]
    
    numero_lote_3 = ",".join(numero_lote_3) 
    
    placeholder19_3= st.empty()
    partida_3= placeholder19_3.text_input("Número de Partida",value="N/A", max_chars=60,key="partida_3")
         
    placeholder20_3= st.empty()
    unidades_catastrales_3= placeholder20_3.number_input("Cantidad de Registros",min_value=0,step=1,key="unidades_catastrales_3")
    
    placeholder21_3= st.empty()
    horas_3= placeholder21_3.number_input("Cantidad de Horas Trabajadas en el Proceso",min_value=0.0,key="horas_3")

    placeholder22_3= st.empty()
    observaciones_3= placeholder22_3.text_input("Observaciones",value="N/A", max_chars=60, key="observaciones_3")
   
    placeholder23_3 = st.empty()
    reporte_3 = placeholder23_3.button("Generar Reporte",key="reporte_3")

  # ============================================
  # MODO DE CARGA MASIVA (NUEVA FUNCIONALIDAD)
  # ============================================
  else:
    st.info("""
    📋 **Instrucciones para carga masiva:**
    1. Prepara tu archivo Excel con las siguientes columnas:
       - fecha, distrito, sector, manzana, tipo, estado, numero_lote, partida, unidades_catastrales, horas, observaciones
    2. Selecciona todas las celdas en Excel (incluyendo encabezados)
    3. Copia con Ctrl+C
    4. Pega en el área de texto con Ctrl+V
    5. Revisa los datos en la vista previa
    6. Haz clic en 'Subir Registros Masivos'
    """)
    
    placeholder_pegado = st.empty()
    datos_pegados = placeholder_pegado.text_area(
        "📋 Pega aquí los datos desde Excel (Ctrl+V)",
        height=200,
        key="datos_pegados_precampo",
        help="Copia los datos desde Excel incluyendo los encabezados de las columnas"
    )
    
    if datos_pegados:
        df, error = parsear_datos_pegados(datos_pegados)
        
        if error:
            st.error(error)
        elif df is not None:
            st.subheader("📊 Vista previa de datos")
            
            # Permitir edición antes de subir
            df_editado = st.data_editor(
                df,
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True,
                key="editor_datos_precampo"
            )
            
            # Estadísticas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Registros a insertar", len(df_editado))
            with col2:
                st.metric("Columnas detectadas", len(df_editado.columns))
            with col3:
                nulos = df_editado.isnull().sum().sum()
                st.metric("Celdas vacías", nulos)
            
            # Botón de carga masiva
            placeholder_boton_masivo = st.empty()
            subir_masivo = placeholder_boton_masivo.button(
                "🚀 Subir Registros Masivos", 
                type="primary", 
                use_container_width=True,
                key="subir_masivo_precampo"
            )
            
            if subir_masivo:
                with st.spinner("⏳ Validando datos..."):
                    es_valido, mensaje_validacion = validar_datos_masivos(df_editado)
                    
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
                                df_editado, usuario, usuario_activo
                            )
                            
                            if exito:
                                st.success(f"✅ {mensaje}")
                                st.balloons()
                                # Limpiar el área de pegado después de éxito
                                placeholder_pegado.empty()
                                placeholder_boton_masivo.empty()
                            else:
                                st.error(f"❌ {mensaje}")
                                st.error(f"Se insertaron {insertados} registros antes del error. Verifica los datos restantes.")
        else:
            st.warning("No se pudieron procesar los datos pegados. Verifica el formato.")

  # ----- Procesos ---- #
    
  if procesos_3:
    placeholder1_3.empty()
    placeholder2_3.empty()
    placeholder3_3.empty()
    placeholder4_3.empty()
    placeholder5_3.empty()
    placeholder6_3.empty()
    placeholder7_3.empty()
    placeholder8_3.empty()
    placeholder_modo.empty()
    
    if modo_carga == "📝 Carga Manual (Formulario)":
        placeholder9_3.empty()
        placeholder10_3.empty()
        placeholder12_3.empty()
        placeholder13_3.empty()
        placeholder15_3.empty()
        placeholder16_3.empty()
        placeholder18_3.empty()
        placeholder19_3.empty()
        placeholder20_3.empty()
        placeholder21_3.empty()
        placeholder22_3.empty()
        placeholder23_3.empty()
    
    st.session_state.Procesos=False
    st.session_state.Postcampo=False

    usuario_activo = obtener_usuario_activo(usuario)
    perfil = str(usuario_activo["perfil"]) if usuario_activo else ""

    if perfil=="1":        
        Procesos.Procesos1(usuario,puesto)
    elif perfil=="2":        
        Procesos.Procesos2(usuario,puesto)   
    elif perfil=="3":  
        Procesos.Procesos3(usuario,puesto)       

  #----- Historial ---- #
    
  elif historial_3:
    placeholder1_3.empty()
    placeholder2_3.empty()
    placeholder3_3.empty()
    placeholder4_3.empty()
    placeholder5_3.empty()
    placeholder6_3.empty()
    placeholder7_3.empty()
    placeholder8_3.empty()
    placeholder_modo.empty()
    
    if modo_carga == "📝 Carga Manual (Formulario)":
        placeholder9_3.empty()
        placeholder10_3.empty()
        placeholder12_3.empty()
        placeholder13_3.empty()
        placeholder15_3.empty()
        placeholder16_3.empty()
        placeholder18_3.empty()
        placeholder19_3.empty()
        placeholder20_3.empty()
        placeholder21_3.empty()
        placeholder22_3.empty()
        placeholder23_3.empty()
    
    st.session_state.Postcampo=False
    st.session_state.Historial=True
    Historial.Historial(usuario,puesto)   

  # ----- Capacitación ---- #
    
  elif capacitacion_3:
    placeholder1_3.empty()
    placeholder2_3.empty()
    placeholder3_3.empty()
    placeholder4_3.empty()
    placeholder5_3.empty()
    placeholder6_3.empty()
    placeholder7_3.empty()
    placeholder8_3.empty()
    placeholder_modo.empty()
    
    if modo_carga == "📝 Carga Manual (Formulario)":
        placeholder9_3.empty()
        placeholder10_3.empty()
        placeholder12_3.empty()
        placeholder13_3.empty()
        placeholder15_3.empty()
        placeholder16_3.empty()
        placeholder18_3.empty()
        placeholder19_3.empty()
        placeholder20_3.empty()
        placeholder21_3.empty()
        placeholder22_3.empty()
        placeholder23_3.empty()
    
    st.session_state.Postcampo=False
    st.session_state.Capacitacion=True
    Capacitacion.Capacitacion(usuario,puesto)

  # ----- Otros Registros ---- #
    
  elif otros_registros_3:
    placeholder1_3.empty()
    placeholder2_3.empty()
    placeholder3_3.empty()
    placeholder4_3.empty()
    placeholder5_3.empty()
    placeholder6_3.empty()
    placeholder7_3.empty()
    placeholder8_3.empty()
    placeholder_modo.empty()
    
    if modo_carga == "📝 Carga Manual (Formulario)":
        placeholder9_3.empty()
        placeholder10_3.empty()
        placeholder12_3.empty()
        placeholder13_3.empty()
        placeholder15_3.empty()
        placeholder16_3.empty()
        placeholder18_3.empty()
        placeholder19_3.empty()
        placeholder20_3.empty()
        placeholder21_3.empty()
        placeholder22_3.empty()
        placeholder23_3.empty()
    
    st.session_state.Postcampo=False
    st.session_state.Otros_Registros=True
    Otros_Registros.Otros_Registros(usuario,puesto)

  # ----- Bonos y Horas Extras ---- #
    
  elif bonos_extras_3:
    placeholder1_3.empty()
    placeholder2_3.empty()
    placeholder3_3.empty()
    placeholder4_3.empty()
    placeholder5_3.empty()
    placeholder6_3.empty()
    placeholder7_3.empty()
    placeholder8_3.empty()
    placeholder_modo.empty()
    
    if modo_carga == "📝 Carga Manual (Formulario)":
        placeholder9_3.empty()
        placeholder10_3.empty()
        placeholder12_3.empty()
        placeholder13_3.empty()
        placeholder15_3.empty()
        placeholder16_3.empty()
        placeholder18_3.empty()
        placeholder19_3.empty()
        placeholder20_3.empty()
        placeholder21_3.empty()
        placeholder22_3.empty()
        placeholder23_3.empty()
    
    st.session_state.Postcampo=False
    st.session_state.Bonos_Extras=True
    Bonos_Extras.Bonos_Extras(usuario,puesto)    

  # ----- Salir ---- #
    
  elif salir_3:
    placeholder1_3.empty()
    placeholder2_3.empty()
    placeholder3_3.empty()
    placeholder4_3.empty()
    placeholder5_3.empty()
    placeholder6_3.empty()
    placeholder7_3.empty()
    placeholder8_3.empty()
    placeholder_modo.empty()
    
    if modo_carga == "📝 Carga Manual (Formulario)":
        placeholder9_3.empty()
        placeholder10_3.empty()
        placeholder12_3.empty()
        placeholder13_3.empty()
        placeholder15_3.empty()
        placeholder16_3.empty()
        placeholder18_3.empty()
        placeholder19_3.empty()
        placeholder20_3.empty()
        placeholder21_3.empty()
        placeholder22_3.empty()
        placeholder23_3.empty()
    
    st.session_state.Ingreso = False
    st.session_state.Postcampo=False
    st.session_state.Salir=True
    Salir.Salir()

  elif modo_carga == "📝 Carga Manual (Formulario)" and reporte_3:

    marca_3= datetime.now(pytz.timezone('America/Guatemala')).strftime("%Y-%m-%d %H:%M:%S")
    
    usuario_activo = obtener_usuario_activo(usuario)
    if not usuario_activo:
      st.error("No se encontró un usuario activo para generar el reporte.")
      return

    nombre_3 = usuario_activo["nombre"]
    supervisor_3 = usuario_activo["supervisor"]
    semana_3 = fecha_3.isocalendar()[1]
    año_3 = fecha_3.isocalendar()[0]
    horas_bi = float(horas_3)
    
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
        marca_3, usuario, nombre_3, puesto, supervisor_3, "Precampo Jurídico", fecha_3, semana_3, año_3, distrito_3, tipo_3, 0, 0, 0, horas_3,
        manzana_3, sector_3, numero_lote_3, estado_3, 0.0, unidades_catastrales_3, 0, partida_3, 0, 0, observaciones_3, "N/A",
        "N/A", horas_bi, 0.0, "N/A", 0, 0, "N/A", 0
      ],
    )
    st.success('Reporte enviado correctamente')
