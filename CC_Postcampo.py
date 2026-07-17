# ----- Librerías ---- #

import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import Procesos, Historial, Capacitacion, Otros_Registros, Bonos_Extras, Salir
import historial_peru  # <-- NUEVO
from Autenticacion import obtener_usuario_activo
from db_core import execute
from db_core import fetch_operadores_cc

# Constante para puestos peruanos
PUESTOS_PERUANOS = ("Supervisor Perú", "Operario Perú", "Coordinador Perú")

def obtener_modulo_historial(puesto):
    """Retorna la función del módulo de historial adecuada según el puesto."""
    if puesto in PUESTOS_PERUANOS:
        return historial_peru.Historial_Peru
    else:
        return Historial.Historial


# ------------------------------------------------------------
# Funciones auxiliares para la carga masiva (mismo criterio que
# Descarga_Partidas_Juridico, adaptadas a las columnas de CC Postcampo)
# ------------------------------------------------------------
def formatear_sector_cc(valor):
    try:
        return str(int(float(valor))).zfill(2)
    except Exception:
        v = str(valor).strip()
        return v.zfill(2) if v else "01"

def formatear_manzana_cc(valor):
    try:
        return str(int(float(valor))).zfill(3)
    except Exception:
        v = str(valor).strip()
        return v.zfill(3) if v else "001"

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
                    except Exception:
                        numeros.append(num)
            return ','.join(numeros) if numeros else 'Todos'
        else:
            return str(int(float(valor_str))).zfill(3)
    except Exception:
        return str(valor)

def normalizar_horas_cc(valor):
    try:
        if isinstance(valor, str):
            valor = valor.replace(',', '.')
        return float(valor)
    except Exception:
        return 0.0

def normalizar_texto_cc(valor, default="N/A"):
    if valor is None or pd.isna(valor) or str(valor).strip() == '':
        return default
    return str(valor).strip()


def validar_datos_masivos_cc(df, distritos_validos, tipos_validos, operadores_validos):
    """Valida el DataFrame pegado/editado antes de insertar en la BD."""
    errores = []

    if df is None or df.empty:
        return False, "La tabla está vacía. No hay datos para procesar."

    # Quitar filas completamente vacías (puede pasar al pegar rangos con blancos)
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
    """Inserta fila por fila en la tabla `registro`, igual que el insert manual."""
    marca = datetime.now(pytz.timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M:%S")
    nombre = usuario_activo["nombre"]
    supervisor = usuario_activo["supervisor"]
    semana = fecha_seleccionada.isocalendar()[1]
    año = fecha_seleccionada.isocalendar()[0]
    registros_insertados = 0

    try:
        for _, row in df.iterrows():
            aprobados = int(row['aprobados']) if not pd.isna(row['aprobados']) else 0
            rechazados = int(row['rechazados']) if not pd.isna(row['rechazados']) else 0
            unidades_catastrales = aprobados + rechazados
            horas = normalizar_horas_cc(row['horas'])

            tipos_de_errores = normalizar_texto_cc(row.get('tipo_de_errores', ''), default="")
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


def CC_Postcampo(usuario, puesto):
    # ----- Conexión, Botones y Memoria ---- #
    uri = st.secrets.db_credentials.URI

    placeholder1_3 = st.sidebar.empty()
    titulo = placeholder1_3.title("Menú")

    placeholder2_3 = st.sidebar.empty()
    procesos_3 = placeholder2_3.button("Procesos", key="procesos_3")

    placeholder3_3 = st.sidebar.empty()
    historial_3 = placeholder3_3.button("Historial", key="historial_3")

    placeholder4_3 = st.sidebar.empty()
    capacitacion_3 = placeholder4_3.button("Capacitaciones", key="capacitacion_3")

    placeholder5_3 = st.sidebar.empty()
    otros_registros_3 = placeholder5_3.button("Otros Registros", key="otros_registros_3")

    # ----- Botón de Bonos solo si NO es peruano -----
    if puesto not in PUESTOS_PERUANOS:
        placeholder6_3 = st.sidebar.empty()
        bonos_extras_3 = placeholder6_3.button("Bonos y Horas Extras", key="bonos_extras_3")
    else:
        placeholder6_3 = None
        bonos_extras_3 = False

    placeholder7_3 = st.sidebar.empty()
    salir_3 = placeholder7_3.button("Salir", key="salir_3")

    placeholder8_3 = st.empty()
    control_calidad_postcampo_3 = placeholder8_3.title(":blue[Control de Calidad Postcampo]")

    # ----- NUEVO: Selector de modo de carga -----
    placeholder_modo_3 = st.empty()
    modo_cc = placeholder_modo_3.radio(
        "Selecciona el modo de carga:",
        options=["📝 Carga Manual (Formulario)", "📋 Carga Masiva (Tabla - pegar desde Excel)"],
        key="modo_cc_postcampo"
    )

    default_date_3 = datetime.now(pytz.timezone('America/Guatemala'))

    # Listas de valores válidos (se usan en ambos modos)
    distritos_opciones = ("Chorrillos", "San Juan De Miraflores", "Villa el Salvador")
    tipo_opciones = ("Inspección", "Inspección Reproceso", "Primera Reinspección",
                      "Inspección Horas Extras", "Control de Calidad Supervisión")
    tipo_errores_opciones = ("Atributos incompletos/erroneos", "Autoensamblado", "Diferencia de áreas",
                               "Errores gráficos", "Puertas no coinciden", "Recapitulación errónea")

    # Obtener operadores desde la base de datos (se usa en ambos modos)
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

    # Contenedor de placeholders dinámicos según el modo (para poder limpiarlos todos)
    placeholders_dinamicos = []

    # Variables usadas más abajo por la rama de "Generar Reporte" manual
    fecha_3 = distrito_3 = manzana_3 = sector_3 = numero_lote_3 = None
    operador_3 = tipo_3 = tipo_de_errores_3 = None
    aprobados_3 = rechazados_3 = horas_3 = None
    reporte_3 = False

    # Variables usadas por la rama masiva
    df_editado_3 = None
    fecha_masiva_3 = None
    subir_masivo_3 = False

    # ================================================================
    # MODO MANUAL (idéntico al original)
    # ================================================================
    if modo_cc == "📝 Carga Manual (Formulario)":
        p = st.empty()
        fecha_3 = p.date_input("Fecha", value=default_date_3, key="fecha_3")
        placeholders_dinamicos.append(p)

        p = st.empty()
        distrito_3 = p.selectbox("Distrito", options=distritos_opciones, key="municipio_3")
        placeholders_dinamicos.append(p)

        p = st.empty()
        manzana_3 = p.selectbox("Manzana", options=tuple(f"{i:03d}" for i in range(1, 121)), key="manzana_3")
        placeholders_dinamicos.append(p)

        p = st.empty()
        sector_3 = p.selectbox("Sector", options=tuple(f"{i:02d}" for i in range(1, 121)), key="sector_3")
        placeholders_dinamicos.append(p)

        # Generar lista dinámica para Número de Lote
        lotes = ["Todos"] + [f"{i:03d}" for i in range(1, 249)]
        p = st.empty()
        numero_lote_sel = p.multiselect("Número de Lote", options=lotes, key="numero_lote_3")
        placeholders_dinamicos.append(p)

        if "Todos" in numero_lote_sel:
            numero_lote_sel = ["Todos"]
        numero_lote_3 = ",".join(numero_lote_sel)

        p = st.empty()
        operador_3 = p.selectbox("Operador objeto de CC", options=opciones_operadores, key="operador_3")
        placeholders_dinamicos.append(p)

        p = st.empty()
        tipo_3 = p.selectbox("Tipo", options=tipo_opciones, key="tipo_3")
        placeholders_dinamicos.append(p)

        p = st.empty()
        tipo_de_errores_3 = p.multiselect("Tipo Errores", options=tipo_errores_opciones, key="tipo_de_errores_3")
        placeholders_dinamicos.append(p)

        p = st.empty()
        aprobados_3 = p.number_input("Cantidad de Unidades Catrastales Aprobados", min_value=0, step=1, key="aprobados_3")
        placeholders_dinamicos.append(p)

        p = st.empty()
        rechazados_3 = p.number_input("Cantidad de Unidades Catrastales Rechazados", min_value=0, step=1, key="rechazados_3")
        placeholders_dinamicos.append(p)

        p = st.empty()
        horas_3 = p.number_input("Cantidad de Horas Trabajadas en el Proceso", min_value=0.0, key="horas_3")
        placeholders_dinamicos.append(p)

        p = st.empty()
        reporte_3 = p.button("Generar Reporte", key="reporte_3")
        placeholders_dinamicos.append(p)

    # ================================================================
    # MODO MASIVO (tabla en caché, pegar desde Excel con Ctrl+V)
    # ================================================================
    else:
        p = st.empty()
        fecha_masiva_3 = p.date_input(
            "📅 Fecha para todos los registros",
            value=default_date_3,
            key="fecha_masiva_3"
        )
        placeholders_dinamicos.append(p)

        p = st.empty()
        with p.container():
            st.info(
                "📋 **Instrucciones:**\n"
                "1. Copia tus datos desde Excel (deben coincidir con las columnas de la tabla de abajo).\n"
                "2. Haz clic en la primera celda de la tabla y pega con **Ctrl+V**; las filas se agregan automáticamente.\n"
                "3. Revisa/corrige lo pegado directamente en la tabla si algo no coincide.\n"
                "4. Presiona **Subir Registros Masivos**.\n\n"
                "**Columnas esperadas (en este orden):** Distrito, Manzana, Sector, N° Lote, Operador, Tipo, "
                "Tipo de Errores (separados por coma), Aprobados, Rechazados, Horas."
            )
        placeholders_dinamicos.append(p)

        # Tabla base con 1 fila vacía, lista para pegar encima
        columnas_cc = ["distrito", "manzana", "sector", "numero_lote", "operador",
                       "tipo", "tipo_de_errores", "aprobados", "rechazados", "horas"]

        if "tabla_masiva_cc" not in st.session_state:
            st.session_state.tabla_masiva_cc = pd.DataFrame(
                [{
                    "distrito": None, "manzana": "", "sector": "", "numero_lote": "Todos",
                    "operador": None, "tipo": None, "tipo_de_errores": "",
                    "aprobados": 0, "rechazados": 0, "horas": 0.0
                }],
                columns=columnas_cc
            )

        p = st.empty()
        with p.container():
            st.subheader("📊 Tabla de carga masiva")
            df_editado_3 = st.data_editor(
                st.session_state.tabla_masiva_cc,
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True,
                key="editor_masivo_cc",
                column_config={
                    "distrito": st.column_config.SelectboxColumn("Distrito", options=list(distritos_opciones), required=True),
                    "manzana": st.column_config.TextColumn("Manzana", help="Ej: 5 → se formatea a 005"),
                    "sector": st.column_config.TextColumn("Sector", help="Ej: 5 → se formatea a 05"),
                    "numero_lote": st.column_config.TextColumn("N° Lote", help="Ej: 1,2,3 o 'Todos'"),
                    "operador": st.column_config.SelectboxColumn("Operador objeto de CC", options=opciones_operadores, required=True),
                    "tipo": st.column_config.SelectboxColumn("Tipo", options=list(tipo_opciones), required=True),
                    "tipo_de_errores": st.column_config.TextColumn("Tipo Errores", help="Separados por coma si son varios"),
                    "aprobados": st.column_config.NumberColumn("Aprobados", min_value=0, step=1, required=True),
                    "rechazados": st.column_config.NumberColumn("Rechazados", min_value=0, step=1, required=True),
                    "horas": st.column_config.NumberColumn("Horas", min_value=0.0, format="%.2f", required=True),
                }
            )
        placeholders_dinamicos.append(p)

        p = st.empty()
        subir_masivo_3 = p.button(
            "🚀 Subir Registros Masivos",
            type="primary",
            use_container_width=True,
            key="subir_masivo_cc",
            disabled=(df_editado_3 is None or df_editado_3.dropna(how="all").empty)
        )
        placeholders_dinamicos.append(p)

    # ------------------------------------------------------------
    # Función para limpiar todos los placeholders (fijos + dinámicos)
    # ------------------------------------------------------------
    def limpiar():
        placeholder1_3.empty()
        placeholder2_3.empty()
        placeholder3_3.empty()
        placeholder4_3.empty()
        placeholder5_3.empty()
        if placeholder6_3 is not None:
            placeholder6_3.empty()
        placeholder7_3.empty()
        placeholder8_3.empty()
        placeholder_modo_3.empty()
        for p in placeholders_dinamicos:
            p.empty()

    # ----- Procesos ---- #
    if procesos_3:
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

    # ----- Historial (con selección de módulo según puesto) ---- #
    elif historial_3:
        limpiar()
        st.session_state.CC_Postcampo = False
        st.session_state.Historial = True
        modulo_hist = obtener_modulo_historial(puesto)
        modulo_hist(usuario, puesto)

    # ----- Capacitación ---- #
    elif capacitacion_3:
        limpiar()
        st.session_state.CC_Postcampo = False
        st.session_state.Capacitacion = True
        Capacitacion.Capacitacion(usuario, puesto)

    # ----- Otros Registros ---- #
    elif otros_registros_3:
        limpiar()
        st.session_state.CC_Postcampo = False
        st.session_state.Otros_Registros = True
        Otros_Registros.Otros_Registros(usuario, puesto)

    # ----- Bonos y Horas Extras (solo si existe el botón) ---- #
    elif bonos_extras_3:
        limpiar()
        st.session_state.CC_Postcampo = False
        st.session_state.Bonos_Extras = True
        Bonos_Extras.Bonos_Extras(usuario, puesto)

    # ----- Salir ---- #
    elif salir_3:
        limpiar()
        st.session_state.Ingreso = False
        st.session_state.CC_Postcampo = False
        st.session_state.Salir = True
        Salir.Salir()

    # ----- Generar Reporte (manual) ---- #
    elif modo_cc == "📝 Carga Manual (Formulario)" and reporte_3:
        marca_3 = datetime.now(pytz.timezone('America/Bogota')).strftime("%Y-%m-%d %H:%M:%S")

        usuario_activo = obtener_usuario_activo(usuario)
        if not usuario_activo:
            st.error("No se encontró un usuario activo para generar el reporte.")
            return

        nombre_3 = usuario_activo["nombre"]
        supervisor_3 = usuario_activo["supervisor"]

        unidades_catastrales_3 = aprobados_3 + rechazados_3
        semana_3 = fecha_3.isocalendar()[1]
        año_3 = fecha_3.isocalendar()[0]
        horas_bi = float(horas_3)
        tipos_de_errores_3 = ','.join(tipo_de_errores_3)
        conteo_3 = len(tipo_de_errores_3)

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
              marca_3, usuario, nombre_3, puesto, supervisor_3, "Control de Calidad Postcampo", fecha_3, semana_3, año_3, distrito_3, tipo_3, 0, aprobados_3, rechazados_3, horas_3,
              manzana_3, sector_3, numero_lote_3, "N/A", 0.0, unidades_catastrales_3, 0, "N/A", 0, 0, "N/A", "N/A",
              "N/A", horas_bi, 0, operador_3, 0, 0, tipos_de_errores_3, conteo_3
            ],
        )
        st.success('Reporte enviado correctamente')

    # ----- Subir Registros Masivos ---- #
    elif modo_cc == "📋 Carga Masiva (Tabla - pegar desde Excel)" and subir_masivo_3:
        with st.spinner("⏳ Validando datos..."):
            es_valido, mensaje_validacion = validar_datos_masivos_cc(
                df_editado_3, list(distritos_opciones), list(tipo_opciones), opciones_operadores
            )

        if not es_valido:
            st.error(f"❌ Error de validación:\n{mensaje_validacion}")
            st.warning("⚠️ No se subió ningún registro. Corrige los errores en la tabla e intenta de nuevo.")
        else:
            st.success("✅ Validación exitosa")
            usuario_activo = obtener_usuario_activo(usuario)
            if not usuario_activo:
                st.error("No se encontró un usuario activo para generar el reporte.")
                return
            with st.spinner("💾 Insertando registros en la base de datos..."):
                exito, insertados, mensaje = insertar_registros_masivos_cc(
                    df_editado_3, fecha_masiva_3, usuario, usuario_activo, puesto
                )
                if exito:
                    st.success(f"✅ {mensaje}")
                    st.balloons()
                    # Reiniciar la tabla en caché para el siguiente lote
                    st.session_state.tabla_masiva_cc = pd.DataFrame(
                        [{
                            "distrito": None, "manzana": "", "sector": "", "numero_lote": "Todos",
                            "operador": None, "tipo": None, "tipo_de_errores": "",
                            "aprobados": 0, "rechazados": 0, "horas": 0.0
                        }],
                        columns=["distrito", "manzana", "sector", "numero_lote", "operador",
                                 "tipo", "tipo_de_errores", "aprobados", "rechazados", "horas"]
                    )
                else:
                    st.error(f"❌ {mensaje}")
                    st.error(f"Se insertaron {insertados} registro(s) antes del error.")
