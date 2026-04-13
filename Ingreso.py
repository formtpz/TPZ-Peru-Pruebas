# ----- Librerías ---- #
import streamlit as st
from PIL import Image

import Autenticacion
import Procesos
import importlib

img = Image.open('logoicon.png')
st.set_page_config(page_title="Formularios TPZ", page_icon=img, layout="wide")

importlib.reload(Procesos)

hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: Visible;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ----- Conexión, Botones y Memoria ---- #

pivot = 0  # Se requiere para mantener las indicaciones generales en caso de errores de ingreso

placeholder1_1 = st.sidebar.empty()
titulo_1 = placeholder1_1.title("Ingreso")

placeholder2_1 = st.sidebar.empty()
usuario = placeholder2_1.text_input("Usuario", key="usuario")

placeholder3_1 = st.sidebar.empty()
contraseña_1 = placeholder3_1.text_input("Contraseña", type='password', key="contraseña_1")

placeholder4_1 = st.sidebar.empty()
iniciar_sesion_1 = placeholder4_1.button("Iniciar sesión", key="iniciar_sesion_1")

if "Ingreso" not in st.session_state:
    st.session_state.Ingreso = False


def _inicializar_banderas():
    flags = [
        "Procesos", "Historial", "Capacitacion", "Otros_Registros", "Bonos_Extras", "Correcciones", "Salir",
        "FMI", "CC_FMI", "Postcampo_FMI", "Postcampo_CC_FMI", "Consulta_Campo", "Restitucion_Tierras",
        "Revision_Segregados", "Calidad_externa_XTF", "Precampo", "Precampo_Juridico", "Descarga_Partidas_Juridico",
        "Asignacion_Partidas", "CC_Precampo", "Vinculacion_Precampo", "Preparacion_Insumos", "Entregas_Postcampo",
        "Revision_Campo", "Postcampo", "CC_Postcampo", "CC_Precampo_Juridico", "CC_Vinculacion_precampo",
        "Estado_UIT_Hito"
    ]
    for key in flags:
        st.session_state[key] = False


def _redirigir_procesos(usuario_login, puesto_login, perfil_login):
    if perfil_login == "1":
        Procesos.Procesos1(usuario_login, puesto_login)
    elif perfil_login == "2":
        Procesos.Procesos2(usuario_login, puesto_login)
    elif perfil_login == "3":
        Procesos.Procesos3(usuario_login, puesto_login)


if st.session_state.Ingreso:
    st.session_state.Ingreso = True
    placeholder1_1.empty()
    placeholder2_1.empty()
    placeholder3_1.empty()
    placeholder4_1.empty()

    usuario_activo = Autenticacion.obtener_usuario_activo(usuario)
    if usuario_activo:
        _redirigir_procesos(usuario, usuario_activo['puesto'], str(usuario_activo['perfil']))
        pivot = pivot + 1

# ----- Validación ---- #

if iniciar_sesion_1:

    if usuario == '' or contraseña_1 == '':
        st.error('Favor ingresar sus credenciales')

    else:
        usuario_activo = Autenticacion.obtener_usuario_activo(usuario)

        if not usuario_activo:
            st.error('El usuario no existe, intente de nuevo')

        else:
            if usuario_activo['contraseña'] == contraseña_1:
                st.success(f"¡Saludos {usuario_activo['nombre']}!")

                placeholder1_1.empty()
                placeholder2_1.empty()
                placeholder3_1.empty()
                placeholder4_1.empty()

                _inicializar_banderas()

                _redirigir_procesos(usuario, usuario_activo['puesto'], str(usuario_activo['perfil']))
                pivot = pivot + 1

            else:
                st.error('Contraseña incorrecta, intente de nuevo')

# ----- Mensajes Generales ---- #

if pivot != 1:
    st.image(Image.open("logo.png"))

    st.title("Telespazio Argentina S.A.")

    st.header("Aplicación de uso exclusivo para el personal de Telespazio Argentina S.A.")

    st.subheader("Proyecto Perú")

    st.subheader("Para soporte técnico favor escribir a brayan.rojas@tpzcr.com")

# ----- Pie de Página ---- #

footer = """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 2px;
        font-size: 12px;
        color: #555;
     }
     .footer a {
        color: tomato;
        text-decoration: none;
        font-weight: bold;
     }

    </style>
    <div class="footer">
        <p>V.1.6 © 2025 Telespazio Argentina S.A. | <a href="https://www.telespazio.com/en" target="_blank">Visit our website</a></p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)
