# ----- Librerías -----
import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import pytz
from urllib.parse import urlparse
import Procesos


def Correcciones(usuario, puesto):

    # =============================
    # Conexión a la BD
    # =============================
    uri = st.secrets.db_credentials.URI
    result = urlparse(uri)

    con = psycopg2.connect(
        host=result.hostname,
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        port=result.port
    )
    cursor = con.cursor()

    # =============================
    # Utilidad: convertir numpy → python
    # =============================
    def to_python(v):
        return v.item() if hasattr(v, "item") else v

    # =============================
    # Menú lateral (placeholders)
    # =============================
    placeholder1_3 = st.sidebar.empty()
    titulo = placeholder1_3.title("Menú")

    placeholder2_3 = st.sidebar.empty()
    procesos_3 = placeholder2_3.button("Regresar", key="procesos_3")

    # =========================================================
    # USUARIO NORMAL (NO COORDINADOR)
    # =========================================================
    if puesto != "Coordinador":

        page = st.empty()
        with page.container():

            st.title("Corrección de Reportes")

            st.write(
                "Aquí puedes visualizar tus reportes y solicitar correcciones "
                "o eliminaciones en caso de errores."
            )

            # -----------------------------
            # Filtro de fechas
            # -----------------------------
            st.subheader("Filtrar por fecha")

            col1, col2 = st.columns(2)
            with col1:
                fecha_inicio = st.date_input("Fecha inicio")
            with col2:
                fecha_fin = st.date_input("Fecha fin")

            if fecha_inicio > fecha_fin:
                st.error("La fecha de inicio no puede ser mayor que la fecha final.")
                st.stop()

            # -----------------------------
            # Obtener nombre del usuario
            # -----------------------------
            df_nombre = pd.read_sql(
                f"SELECT nombre FROM usuarios WHERE usuario = '{usuario}'",
                con
            )
            nombre = df_nombre.loc[0, "nombre"]

            # -----------------------------
            # Consultar reportes
            # -----------------------------
            query_registro = f"""
                SELECT *
                FROM registro
                WHERE usuario = '{usuario}'
                  AND fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
                ORDER BY fecha DESC
            """

            query_otros = f"""
                SELECT *
                FROM otros_registros
                WHERE usuario = '{usuario}'
                  AND fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
                ORDER BY fecha DESC
            """

            query_capacitacion = f"""
                SELECT *
                FROM capacitaciones
                WHERE usuario = '{usuario}'
                  AND fecha BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
                ORDER BY fecha DESC
            """

            df = pd.read_sql(query_registro, con)
            dfo = pd.read_sql(query_otros, con)
            dfc = pd.read_sql(query_capacitacion, con)

            # ----- Evitar formato 2,000 en IDs -----
            if "id" in df.columns:
                df["id"] = df["id"].astype(str)

            if "id" in dfo.columns:
                dfo["id"] = dfo["id"].astype(str)

            if "id" in dfc.columns:
                dfc["id"] = dfc["id"].astype(str)

            st.subheader("Registro")
            st.dataframe(df, use_container_width=True)

            st.subheader("Otros Registros")
            st.dataframe(dfo, use_container_width=True)

            st.subheader("Capacitaciones")
            st.dataframe(dfc, use_container_width=True)

            # -----------------------------
            # Solicitud de corrección
            # -----------------------------
            st.subheader("Solicitar corrección o eliminación")

            id_reporte = st.text_input("ID del reporte")

            tipo_correccion = st.radio(
                "Tipo de solicitud",
                ("Modificar valor", "Eliminar reporte")
            )

            tabla = st.radio(
                "Tabla",
                ("registro", "otros_registros", "capacitaciones")
            )

            columna = None
            nuevo_valor = None

            if tipo_correccion == "Modificar valor":

                descripcion1 = st.radio(
                    "Motivo",
                    (
                        "Estado Incorrecto",
                        "Fecha Incorrecta",
                        "Distrito Incorrecto",
                        "Tipo Incorrecto",
                        "Horas Incorrectas",
                        "Manzana Incorrecta",
                        "Sector Incorrecto",
                        "Lote Incorrecto",
                        "Aprobados-Rechazados Incorrectos",
                        "Área Incorrecta",
                        "Edificas Incorrectos",
                        "Unidades Catastrales Incorrectas",
                        "Partida Incorrecta",
                        "Zona Incorrecta",
                        "Otro"
                    )
                )

                columna = st.text_input(
                    "Columna a corregir (según se visualiza en las tablas anteriores)"
                )

                nuevo_valor = st.text_input(
                    "Nuevo valor (Ej: Aprobados-Rechazados = 3-2)"
                )

            else:
                descripcion1 = st.radio(
                    "Motivo",
                    (
                        "Reporte Duplicado",
                        "Reporte Incorrecto",
                        "Reporte de Prueba",
                        "Proceso Incorrecto"
                    )
                )
                columna = "N/A"
                nuevo_valor = "0"

            # -----------------------------
            # Enviar solicitud
            # -----------------------------
            if st.button("Enviar solicitud"):

                if not id_reporte:
                    st.error("Debe indicar el ID del reporte.")
                    st.stop()

                if tipo_correccion == "Modificar valor":
                    if not columna.strip() or not nuevo_valor.strip():
                        st.error("Debe indicar columna y nuevo valor.")
                        st.stop()

                marca = datetime.now(
                    pytz.timezone("America/Guatemala")
                ).strftime("%Y-%m-%d %H:%M:%S")

                solicitud = "Modificar" if tipo_correccion == "Modificar valor" else "Eliminar"

                cursor.execute("""
                    INSERT INTO correcciones (
                        usuario, nombre, tipo_error, id_asociado,
                        fecha, solucion, tabla, columna, nuevo_valor, estado
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    usuario,
                    nombre,
                    descripcion1,
                    id_reporte,
                    marca,
                    solicitud,
                    tabla,
                    columna,
                    nuevo_valor,
                    "Pendiente"
                ))

                con.commit()
                st.success("Solicitud registrada correctamente")

        pass  # fin page usuario

    # =========================================================
    # COORDINADOR
    # =========================================================
    else:

        page = st.empty()
        with page.container():

            st.title("Gestión de Correcciones")

            filtro = st.selectbox(
                "Mostrar",
                ("Todos", "Pendiente")
            )

            query_corr = "SELECT * FROM correcciones"
            if filtro == "Pendiente":
                query_corr += " WHERE estado = 'Pendiente'"

            df_corr_original = pd.read_sql(query_corr, con)

            df_corr_editado = st.data_editor(
                df_corr_original,
                use_container_width=True,
                num_rows="fixed"
            )

            if st.button("Guardar cambios"):

                cambios = df_corr_editado.compare(df_corr_original)

                if cambios.empty:
                    st.info("No hay cambios para guardar.")
                    st.stop()

                for idx in cambios.index.get_level_values(0).unique():

                    fila_nueva = df_corr_editado.loc[idx]
                    fila_original = df_corr_original.loc[idx]

                    columnas_cambiadas = [
                        col for col in df_corr_original.columns
                        if fila_nueva[col] != fila_original[col]
                    ]

                    set_clause = ", ".join(f"{col} = %s" for col in columnas_cambiadas)
                    valores = [to_python(fila_nueva[col]) for col in columnas_cambiadas]
                    id_python = to_python(fila_nueva["id"])

                    sql = f"""
                        UPDATE correcciones
                        SET {set_clause}
                        WHERE id = %s
                    """

                    cursor.execute(sql, valores + [id_python])

                con.commit()
                st.success("Cambios guardados correctamente")

        pass  # fin page coordinador

    # =========================================================
    # Regresar a Procesos
    # =========================================================
    if procesos_3:

        placeholder1_3.empty()
        placeholder2_3.empty()

        try:
            page.empty()
        except:
            pass

        st.session_state.Procesos = False
        st.session_state.Correcciones = False

        perfil = pd.read_sql(
            f"SELECT perfil FROM usuarios WHERE usuario = '{usuario}'",
            uri
        ).loc[0, "perfil"]

        if perfil == "1":
            Procesos.Procesos1(usuario, puesto)
        elif perfil == "2":
            Procesos.Procesos2(usuario, puesto)
        elif perfil == "3":
            Procesos.Procesos3(usuario, puesto)

