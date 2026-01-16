# ----- Librerías ---- #
import streamlit as st
from PIL import Image
img=Image.open('logoicon.png')
st.set_page_config(page_title="Formularios TPZ",page_icon=img,layout="wide")
import pandas as pd
import Autenticacion, Procesos
import importlib

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

uri=st.secrets.db_credentials.URI

pivot=0 # Se requiere para mantener las indicaciones generales en caso de errores de ingreso

placeholder1_1= st.sidebar.empty()
titulo_1= placeholder1_1.title("Ingreso")

placeholder2_1= st.sidebar.empty()
usuario=placeholder2_1.text_input("Usuario",key="usuario")

placeholder3_1= st.sidebar.empty()
contraseña_1 = placeholder3_1.text_input("Contraseña", type = 'password', key="contraseña_1")

placeholder4_1 = st.sidebar.empty()
iniciar_sesion_1 = placeholder4_1.button("Iniciar sesión",key="iniciar_sesion_1")

if "Ingreso" not in st.session_state:
     st.session_state.Ingreso = False

if st.session_state.Ingreso:

    st.session_state.Ingreso=True
    placeholder1_1.empty()
    placeholder2_1.empty()
    placeholder3_1.empty()
    placeholder4_1.empty()
    
    puesto=pd.read_sql(f"select puesto from usuarios where usuario ='{usuario}'",uri)
    puesto= puesto.loc[0,'puesto']

    perfil=pd.read_sql(f"select perfil from usuarios where usuario ='{usuario}'",uri)
    perfil= perfil.loc[0,'perfil']

    if perfil=="1":        
        
        Procesos.Procesos1(usuario,puesto)
    
    elif perfil=="2":        
        
        Procesos.Procesos2(usuario,puesto)   

    elif perfil=="3":        
        
        Procesos.Procesos3(usuario,puesto)   

    pivot=pivot + 1

# ----- Validación ---- #

if iniciar_sesion_1:

    if usuario == '' or contraseña_1 == '':
        st.error('Favor ingresar sus credenciales')

    else:
        
        contraseña= Autenticacion.contraseña(usuario)

        if contraseña.empty:
            st.error('El usuario no existe, intente de nuevo')

        else:

            contraseña = contraseña.loc[0,'contraseña']

            if contraseña == contraseña_1:

                nombre_1=pd.read_sql(f"select nombre from usuarios where usuario ='{usuario}'",uri)
                nombre_1 = nombre_1.loc[0,'nombre']
                st.success(f'¡Saludos {nombre_1}!')

                placeholder1_1.empty()
                placeholder2_1.empty()
                placeholder3_1.empty()
                placeholder4_1.empty()

                st.session_state.Procesos=False
                st.session_state.Historial=False
                st.session_state.Capacitacion=False
                st.session_state.Otros_Registros=False
                st.session_state.Bonos_Extras=False
                st.session_state.Salir=False
                st.session_state.FMI=False
                st.session_state.CC_FMI=False
                st.session_state.Postcampo_FMI=False
                st.session_state.Postcampo_CC_FMI=False
                st.session_state.Consulta_Campo=False
                st.session_state.Restitucion_Tierras=False
                st.session_state.Revision_Segregados=False
                st.session_state.Calidad_externa_XTF=False
                st.session_state.Precampo=False
                st.session_state.Precampo_Juridico=False
                st.session_state.CC_Precampo=False
                st.session_state.Vinculacion_Precampo=False 
                st.session_state.Preparacion_Insumos=False
                st.session_state.Entregas_Postcampo=False
                st.session_state.Revision_Campo=False
                st.session_state.Postcampo=False
                st.session_state.CC_Postcampo=False
                st.session_state.CC_Precampo_Juridico=False
                st.session_state.CC_Vinculacion_precampo=False
                st.session_state.Estado_UIT_Hito=False
                                    
                puesto=pd.read_sql(f"select puesto from usuarios where usuario ='{usuario}'",uri)
                puesto= puesto.loc[0,'puesto']
                   
                perfil=pd.read_sql(f"select perfil from usuarios where usuario ='{usuario}'",uri)
                perfil= perfil.loc[0,'perfil']

                if perfil=="1":        
                    
                    Procesos.Procesos1(usuario,puesto)
                
                elif perfil=="2":        
                    
                    Procesos.Procesos2(usuario,puesto)   

                elif perfil=="3":  

                    Procesos.Procesos3(usuario,puesto)       

                pivot= pivot + 1
                                
            else:
                st.error('Contraseña incorrecta, intente de nuevo')

# ----- Mensajes Generales ---- #
     
if pivot!=1:
    
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
