# ----- Librerías ---- #

import streamlit as st
from PIL import Image

img = Image.open("logoicon.png")

st.set_page_config(
    page_title="Formularios TPZ",
    page_icon=img,
    layout="wide"
)


import pandas as pd
import Autenticacion, Procesos
import importlib

# ----- Configuración inicial ----- #

importlib.reload(Procesos)

# ----- CSS GLOBAL (Ocultar menú + Wallpaper dinámico) ----- #
custom_style = """
<style>

/* ===== OCULTAR ELEMENTOS STREAMLIT ===== */
div[data-testid="stToolbar"] {visibility: hidden; height: 0%; position: fixed;}
div[data-testid="stDecoration"] {visibility: hidden; height: 0%; position: fixed;}
div[data-testid="stStatusWidget"] {visibility: visible; height: 0%; position: fixed;}
#MainMenu {visibility: hidden; height: 0%;}
header {visibility: hidden; height: 0%;}
footer {visibility: hidden; height: 0%;}

/* ===== WALLPAPER DINÁMICO CORPORATIVO ===== */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    overflow: hidden;
}

.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 200%;
    height: 200%;
    background-repeat: repeat;
    background-image: radial-gradient(rgba(255,255,255,0.8) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.12;
    animation: moveParticles 80s linear infinite;
    z-index: -1;
}

.stApp::after {
    background-size: 60px 60px;
    animation-duration: 140s;
    opacity: 0.06;
}

@keyframes moveParticles {
    from { transform: translate(0, 0); }
    to { transform: translate(-600px, -600px); }
}

</style>
"""

st.markdown("""
<style>

/* Fondo base */
div[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    overflow: hidden;
}

/* Hacer contenedores transparentes */
div[data-testid="stHeader"],
div[data-testid="stToolbar"],
section[data-testid="stSidebar"],
.main {
    background: transparent !important;
}

/* Partículas */
div[data-testid="stAppViewContainer"]::before,
div[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 200%;
    height: 200%;
    background-repeat: repeat;
    background-image: radial-gradient(rgba(255,255,255,0.8) 1px, transparent 1px);
    background-size: 40px 40px;
    opacity: 0.15;
    animation: moveParticles 80s linear infinite;
    z-index: 0;
}

div[data-testid="stAppViewContainer"]::after {
    background-size: 60px 60px;
    animation-duration: 140s;
    opacity: 0.08;
}

@keyframes moveParticles {
    from { transform: translate(0, 0); }
    to { transform: translate(-600px, -600px); }
}

</style>
""", unsafe_allow_html=True)

# ----- Conexión, Botones y Memoria ---- #
uri = st.secrets.db_credentials.URI
pivot = 0

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

# ----- Usuario ya autenticado ----- #
if st.session_state.Ingreso:

    st.session_state.Ingreso = True
    placeholder1_1.empty()
    placeholder2_1.empty()
    placeholder3_1.empty()
    placeholder4_1.empty()
    
    puesto = pd.read_sql(f"select puesto from usuarios where usuario ='{usuario}'", uri).loc[0,'puesto']
    perfil = pd.read_sql(f"select perfil from usuarios where usuario ='{usuario}'", uri).loc[0,'perfil']

    if perfil == "1":        
        Procesos.Procesos1(usuario, puesto)
    elif perfil == "2":        
        Procesos.Procesos2(usuario, puesto)   
    elif perfil == "3":        
        Procesos.Procesos3(usuario, puesto)   

    pivot += 1

# ----- Validación Login ----- #
if iniciar_sesion_1:

    if usuario == '' or contraseña_1 == '':
        st.error('Favor ingresar sus credenciales')
    else:
        contraseña = Autenticacion.contraseña(usuario)

        if contraseña.empty:
            st.error('El usuario no existe, intente de nuevo')
        else:
            contraseña = contraseña.loc[0,'contraseña']

            if contraseña == contraseña_1:

                nombre_1 = pd.read_sql(f"select nombre from usuarios where usuario ='{usuario}'", uri).loc[0,'nombre']
                st.success(f'¡Saludos {nombre_1}!')

                placeholder1_1.empty()
                placeholder2_1.empty()
                placeholder3_1.empty()
                placeholder4_1.empty()

                # Reset de módulos
                for key in [
                    "Procesos","Historial","Capacitacion","Otros_Registros","Bonos_Extras",
                    "Correcciones","Salir","FMI","CC_FMI","Postcampo_FMI",
                    "Postcampo_CC_FMI","Consulta_Campo","Restitucion_Tierras",
                    "Revision_Segregados","Calidad_externa_XTF","Precampo",
                    "Precampo_Juridico","Descarga_Partidas_Juridico","CC_Precampo",
                    "Vinculacion_Precampo","Preparacion_Insumos","Entregas_Postcampo",
                    "Revision_Campo","Postcampo","CC_Postcampo",
                    "CC_Precampo_Juridico","CC_Vinculacion_precampo","Estado_UIT_Hito"
                ]:
                    st.session_state[key] = False

                st.session_state.Ingreso = True

                puesto = pd.read_sql(f"select puesto from usuarios where usuario ='{usuario}'", uri).loc[0,'puesto']
                perfil = pd.read_sql(f"select perfil from usuarios where usuario ='{usuario}'", uri).loc[0,'perfil']

                if perfil == "1":        
                    Procesos.Procesos1(usuario, puesto)
                elif perfil == "2":        
                    Procesos.Procesos2(usuario, puesto)   
                elif perfil == "3":  
                    Procesos.Procesos3(usuario, puesto)       

                pivot += 1
            else:
                st.error('Contraseña incorrecta, intente de nuevo')

# ----- Mensajes Generales ----- #
if pivot != 1:
    st.image(Image.open("logo.png"))
    st.title("Telespazio Argentina S.A.")
    st.header("Aplicación de uso exclusivo para el personal de Telespazio Argentina S.A.")
    st.subheader("Proyecto Perú")
    st.subheader("Para soporte técnico favor escribir a brayan.rojas@tpzcr.com")

# ----- Pie de Página ----- #
footer = """
<style>
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: rgba(0,0,0,0.4);
    text-align: center;
    padding: 4px;
    font-size: 12px;
    color: #ddd;
}
.footer a {
    color: #00c6ff;
    text-decoration: none;
    font-weight: bold;
}
</style>
<div class="footer">
    <p>V.1.6 © 2025 Telespazio Argentina S.A. | <a href="https://www.telespazio.com/en" target="_blank">Visit our website</a></p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
