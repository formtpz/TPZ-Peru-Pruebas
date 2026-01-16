# ----- Librerías ---- #

import streamlit as st
import Historial, Capacitacion, Otros_Registros, Bonos_Extras, Salir, Precampo_Juridico, CC_Precampo_Juridico, Consulta_Campo,Restitucion_Tierras,Revision_Segregados,Estado_UIT_Hito,Precampo, CC_Precampo, Preparacion_Insumos, Entregas_Postcampo, Postcampo, CC_Postcampo, CC_Vinculacion_Precampo, Vinculacion_Precampo

import time

#-------------------CONTADOR PARA REFRESCAR PAGINA---------------#
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if time.time() - st.session_state.start_time >  29*60:
    st.session_state.clear()
    st.rerun()

def auto_refresh(seconds=1741):
    st.markdown(   f"""  <meta http-equiv="refresh" content="{seconds}" >   """,  unsafe_allow_html=True )

auto_refresh(1741)

#-----------------FINCONTADOR-----------------#

def Procesos1(usuario,puesto):

    st.session_state.Ingreso=True

    if st.session_state.Procesos==False: 

        placeholder1_2= st.sidebar.empty()
        titulo= placeholder1_2.title("Menú")

        placeholder2_2= st.sidebar.empty()
        historial_2 = placeholder2_2.button("Historial",key="historial_2")

        placeholder3_2 = st.sidebar.empty()
        capacitacion_2 = placeholder3_2.button("Capacitaciones",key="capacitacion_2")

        placeholder4_2 = st.sidebar.empty()
        otros_registros_2 = placeholder4_2.button("Otros Registros",key="otros_registros_2")

        placeholder5_2 = st.sidebar.empty()
        bonos_extras_2 = placeholder5_2.button("Bonos y Horas Extras",key="bonos_extras_2")

        placeholder6_2 = st.sidebar.empty()
        salir_2 = placeholder6_2.button("Salir",key="salir_2")

        placeholder7_2 = st.empty()
        procesos_2 = placeholder7_2.title("Procesos")

        placeholder8_2 = st.empty()
        precampo_juridico_2 = placeholder8_2.button(":orange[Precampo Jurídico]", key="precampo_juridico_2")

        placeholder9_2 = st.empty()
        cc_precampo_juridico_2 = placeholder9_2.button(":orange[Control de Calidad Precampo Jurídico]",key="cc_precampo_juridico_2")

        placeholder10_2 = st.empty()
        precampo_2 = placeholder10_2.button(":green[Precampo]",key="precampo_2")

        placeholder11_2 = st.empty()
        cc_precampo_2 = placeholder11_2.button(":green[Control de Calidad Precampo]",key="cc_precampo_2")

        placeholder12_2 = st.empty()
        vinculacion_precampo_2 = placeholder12_2.button(":blue[Vinculación Precampo]",key="vinculacion_precampo_2")
                      
        placeholder13_2 = st.empty()
        preparacion_insumos_2 = placeholder13_2.button(":gray[Preparación de Insumos]",key="preparacion_insumos_2") 
        
        placeholder14_2 = st.empty()
        entregas_2 = placeholder14_2.button(":gray[Entregas Postcampo]",key="entregas_2")

        placeholder15_2 = st.empty()
        postcampo_2 = placeholder15_2.button(":blue[Postcampo]",key="postcampo_2")

        placeholder16_2 = st.empty()
        cc_postcampo_2 = placeholder16_2.button(":blue[Control de Calidad Postcampo]",key="cc_postcampo_2")

        placeholder17_2 = st.empty()
        cc_vinculacion_precampo_2 = placeholder17_2.button(":green[Control de Calidad Vinculación Precampo]",key="cc_vinculacion_precampo_2")

        #placeholder18_2 = st.empty()
        #restitucion_tierras_2 = placeholder18_2.button("Restitución de Tierras",key="restitucion_tierras_2")

        #placeholder19_2 = st.empty()
        #revision_segregados_2 = placeholder19_2.button("Revisión de Predios Segregados",key="revision_segregados_2")

        placeholder20_2 = st.empty()
        estado_uit_hito_2 = placeholder20_2.button("Calidad Interna XTF",key="estado_uit_hito_2")

        # ----- Historial ---- #

        if historial_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Historial=True
            Historial.Historial(usuario,puesto)

        # ----- Capacitación ---- #

        elif capacitacion_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Capacitacion=True
            Capacitacion.Capacitacion(usuario,puesto)

        # ----- Otros Registros ---- #

        elif otros_registros_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Otros_Registros=True
            Otros_Registros.Otros_Registros(usuario,puesto)

        # ----- Bonos y Horas Extras ---- #

        elif bonos_extras_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Bonos_Extras=True
            Bonos_Extras.Bonos_Extras(usuario,puesto)

        # ----- Salir ---- #

        elif salir_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Ingreso= False
            st.session_state.Procesos=True
            st.session_state.Salir=True
            Salir.Salir()
            
             # -----  Precampo_Juridico ---- #

        elif precampo_juridico_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Precampo_Juridico=True
            Precampo_Juridico.Precampo_Juridico(usuario,puesto) 
                
                  
               
        # ----- Control Calidad Precampo Juridico ---- #

        elif cc_precampo_juridico_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.CC_Precampo_Juridico=True
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario,puesto)

        # ----- Precampo ---- #

        elif precampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Precampo=True
            Precampo.Precampo(usuario,puesto)

        # ----- CC_Precampo ---- #

        elif cc_precampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.CC_Precampo=True
            CC_Precampo.CC_Precampo(usuario,puesto)

     # -----vinculacion_precampo_---- #

        elif vinculacion_precampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Vinculacion_Precampo=True
            Vinculacion_Precampo.Vinculacion_Precampo(usuario,puesto)
            
        # ----- Preparación de Insumos ---- #

        elif preparacion_insumos_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Preparacion_Insumos=True
            Preparacion_Insumos.Preparacion_Insumos(usuario,puesto)

          # ----- Revisión de Campo ---- #

        elif entregas_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Entregas_Postcampo=True
            Entregas_Postcampo.Entregas_Postcampo(usuario,puesto)

        # ----- Postcampo ---- #

        elif postcampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Postcampo=True
            Postcampo.Postcampo(usuario,puesto)

         # ----- CC Postcampo---- #

        elif cc_postcampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.CC_Postcampo=True
            CC_Postcampo.CC_Postcampo(usuario,puesto)
         
        # ----- CC Validacion Precampo---- #

        elif cc_vinculacion_precampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.CC_Vinculacion_Precampo=True
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario,puesto)

        # ----- Restitución de Tierras ---- #

        #elif restitucion_tierras_2:

            #placeholder1_2.empty()
            #placeholder2_2.empty()
            #placeholder3_2.empty()
            #placeholder4_2.empty()
            #placeholder5_2.empty()
            #placeholder6_2.empty()
            #placeholder7_2.empty()
            #placeholder8_2.empty()
            #placeholder9_2.empty()
            #placeholder10_2.empty()
            #placeholder11_2.empty()
            #placeholder12_2.empty()
            #placeholder13_2.empty()
            #placeholder14_2.empty()
            #placeholder15_2.empty()
            #placeholder16_2.empty()
            #placeholder17_2.empty()
            #placeholder18_2.empty()
            #st.session_state.Procesos=True
            #st.session_state.Restitucion_Tierras=True
            #Restitucion_Tierras.Restitucion_Tierras(usuario,puesto)

        # ----- Revisión de Predios Segredados ---- #

        #elif revision_segregados_2:

            #placeholder1_2.empty()
            #placeholder2_2.empty()
            #placeholder3_2.empty()
            #placeholder4_2.empty()
            #placeholder5_2.empty()
            #placeholder6_2.empty()
            #placeholder7_2.empty()
            #placeholder8_2.empty()
            #placeholder9_2.empty()
            #placeholder10_2.empty()
            #placeholder11_2.empty()
            #placeholder12_2.empty()
            #placeholder13_2.empty()
            #placeholder14_2.empty()
            #placeholder15_2.empty()
            #placeholder16_2.empty()
            #placeholder17_2.empty()
            #placeholder18_2.empty()
            #st.session_state.Procesos=True
            #st.session_state.Revision_Segregados=True
            #Revision_Segregados.Revision_Segregados(usuario,puesto)
                   
        # ----- Estado UIT Hito ---- #

        elif estado_uit_hito_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            placeholder16_2.empty()
            placeholder17_2.empty()
            #placeholder18_2.empty()
            #placeholder19_2.empty()
            placeholder20_2.empty()
            st.session_state.Procesos=True
            st.session_state.Estado_UIT_Hito=True
            Estado_UIT_Hito.Estado_UIT_Hito(usuario,puesto)

    elif st.session_state.Procesos==True:

        if st.session_state.Historial==True:
            Historial.Historial(usuario,puesto)

        elif st.session_state.Capacitacion==True:
            Capacitacion.Capacitacion(usuario,puesto)

        elif st.session_state.Otros_Registros==True:
            Otros_Registros.Otros_Registros(usuario,puesto)

        elif st.session_state.Bonos_Extras==True:
            Bonos_Extras.Bonos_Extras(usuario,puesto)

        elif st.session_state.Precampo_Juridico==True:
            Precampo_Juridico.Precampo_Juridico(usuario,puesto)
           
        elif st.session_state.CC_Precampo_Juridico==True:
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario,puesto)

        #elif st.session_state.Consulta_Campo==True:
            #Consulta_Campo.Consulta_Campo(usuario,puesto)

        elif st.session_state.Precampo==True:
            Precampo.Precampo(usuario,puesto)

        elif st.session_state.CC_Precampo==True:
            CC_Precampo.CC_Precampo(usuario,puesto)

        elif st.session_state.Vinculacion_Precampo==True:
            Vinculacion_Precampo.Vinculacion_Precampo(usuario,puesto)

        elif st.session_state.Preparacion_Insumos==True:
            Preparacion_Insumos.Preparacion_Insumos(usuario,puesto)
            
        elif st.session_state.Entregas_Postcampo==True:
            Entregas_Postcampo.Entregas_Postcampo(usuario,puesto)

        elif st.session_state.Postcampo==True:
            Postcampo.Postcampo(usuario,puesto)

        elif st.session_state.CC_Postcampo==True:
            CC_Postcampo.CC_Postcampo(usuario,puesto)

        elif st.session_state.CC_Vinculacion_Precampo==True:
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario,puesto)

        #elif st.session_state.Restitucion_Tierras==True:
            #Restitucion_Tierras.Restitucion_Tierras(usuario,puesto)

        #elif st.session_state.Revision_Segregados==True:
            #Revision_Segregados.Revision_Segregados(usuario,puesto)
            
        elif st.session_state.Estado_UIT_Hito==True:
            Estado_UIT_Hito.Estado_UIT_Hito(usuario,puesto)
            
# ----- Procesos 2 (Gabinete) ---- #

def Procesos2(usuario,puesto):

    st.session_state.Ingreso=True

    if st.session_state.Procesos==False:

        placeholder1_2= st.sidebar.empty()
        titulo= placeholder1_2.title("Menú")

        placeholder2_2= st.sidebar.empty()
        historial_2 = placeholder2_2.button("Historial",key="historial_2")

        placeholder3_2 = st.sidebar.empty()
        capacitacion_2 = placeholder3_2.button("Capacitaciones",key="capacitacion_2")

        placeholder4_2 = st.sidebar.empty()
        otros_registros_2 = placeholder4_2.button("Otros Registros",key="otros_registros_2")

        placeholder5_2 = st.sidebar.empty()
        bonos_extras_2 = placeholder5_2.button("Bonos y Horas Extras",key="bonos_extras_2")

        placeholder6_2 = st.sidebar.empty()
        salir_2 = placeholder6_2.button("Salir",key="salir_2")

        placeholder7_2 = st.empty()
        registro_2 = placeholder7_2.title("Procesos")

        placeholder8_2 = st.empty()
        precampo_2 = placeholder8_2.button("Precampo",key="precampo_2")

        placeholder9_2 = st.empty()
        cc_precampo_2 = placeholder9_2.button("Control de Calidad Precampo",key="cc_precampo_2")

        #placeholder10_2 = st.empty()
        #preparacion_insumos_2 = placeholder10_2.button("Preparación de Insumos",key="preparacion_insumos_2")

        placeholder11_2 = st.empty()
        entregas_2 = placeholder11_2.button("Entregas Postcampo",key="entregas_2")

        placeholder12_2 = st.empty()
        postcampo_2 = placeholder12_2.button("Postcampo",key="postcampo_2")

        placeholder13_2 = st.empty()
        vinculacion_precampo_2 = placeholder13_2.button("Vinculacion Precampo",key="vinculacion_precampo_2")

        placeholder14_2 = st.empty()
        cc_postcampo_2 = placeholder14_2.button("Control de Calidad Postcampo",key="cc_postcampo_2")

        placeholder15_2 = st.empty()
        cc_vinculacion_precampo_2 = placeholder15_2.button("Control de Calidad Vinculacion Precampo",key="cc_vinculacion_precampo_2")
       
        # ----- Historial ---- #

        if historial_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.Historial=True
            Historial.Historial(usuario,puesto)

        # ----- Capacitación ---- #

        elif capacitacion_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.Capacitacion=True
            Capacitacion.Capacitacion(usuario,puesto)

        # ----- Otros Registros ---- #

        elif otros_registros_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.Otros_Registros=True
            Otros_Registros.Otros_Registros(usuario,puesto)

        # ----- Bonos y Horas Extras ---- #

        elif bonos_extras_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.Bonos_Extras=True
            Bonos_Extras.Bonos_Extras(usuario,puesto)

        # ----- Salir ---- #

        elif salir_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Ingreso = False
            st.session_state.Procesos=True
            st.session_state.Salir=True
            Salir.Salir()

        # ----- Precampo ---- #

        elif precampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.Precampo=True
            Precampo.Precampo(usuario,puesto)

        # ----- CC Precampo ---- #

        elif cc_precampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.CC_Precampo=True
            CC_Precampo.CC_Precampo(usuario,puesto)

        # ----- Preparación de Insumos ---- #

        #elif preparacion_insumos_2:

            #placeholder1_2.empty()
            #placeholder2_2.empty()
            #placeholder3_2.empty()
            #placeholder4_2.empty()
            #placeholder5_2.empty()
            #placeholder6_2.empty()
            #placeholder7_2.empty()
            placeholder8_2.empty()
            #placeholder9_2.empty()
            #placeholder10_2.empty()
            #placeholder11_2.empty()
            #placeholder12_2.empty()
            #placeholder13_2.empty()
            #st.session_state.Procesos=True
            #st.session_state.Preparacion_Insumos=True
            #Preparacion_Insumos.Preparacion_Insumos(usuario,puesto)

         # ----- Entregas ---- #

        elif entregas_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.Entregas_Postcampo=True
            Entregas_Postcampo.Entregas_Postcampo(usuario,puesto)

        # ----- Postcampo ---- #

        elif postcampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.Postcampo=True
            Postcampo.Postcampo(usuario,puesto)

        # ----- Validación Precampo ---- #

        elif vinculacion_precampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.Vinculacion_Precampo=True
            Vinculacion_Precampo.Vinculacion_Precampo(usuario,puesto)
            
        # ----- CC_Postcampo ---- #

        elif cc_postcampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.CC_Postcampo=True
            CC_Postcampo.CC_Postcampo(usuario,puesto)

    # ----- CC_Postcampo ---- #

        elif cc_vinculacion_precampo_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()
            #placeholder10_2.empty()
            placeholder11_2.empty()
            placeholder12_2.empty()
            placeholder13_2.empty()
            placeholder14_2.empty()
            placeholder15_2.empty()
            st.session_state.Procesos=True
            st.session_state.CC_Vinculacion_Precampo=True
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario,puesto)
            
    elif st.session_state.Procesos==True:

        if st.session_state.Historial==True:
            Historial.Historial(usuario,puesto)

        elif st.session_state.Capacitacion==True:
            Capacitacion.Capacitacion(usuario,puesto)

        elif st.session_state.Otros_Registros==True:
            Otros_Registros.Otros_Registros(usuario,puesto)

        elif st.session_state.Bonos_Extras==True:
            Bonos_Extras.Bonos_Extras(usuario,puesto)

        elif st.session_state.Precampo==True:
            Precampo.Precampo(usuario,puesto)

        elif st.session_state.CC_Precampo==True:
            CC_Precampo.CC_Precampo(usuario,puesto)

        elif st.session_state.Preparacion_Insumos==True:
            Preparacion_Insumos.Preparacion_Insumos(usuario,puesto)
        
        elif st.session_state.Entregas_Postcampo==True:
            Entregas_Postcampo.Entregas_Postcampo(usuario,puesto)

        elif st.session_state.Postcampo==True:
            Postcampo.Postcampo(usuario,puesto)

        elif st.session_state.Vinculacion_Precampo==True:
            Vinculacion_Precampo.Vinculacion_Precampo(usuario,puesto)

        elif st.session_state.CC_Postcampo==True:
            CC_Postcampo.CC_Postcampo(usuario,puesto)

        elif st.session_state.CC_Vinculacion_Precampo==True:
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario,puesto)

# ----- Procesos 3 (Jurídicos) ---- #

def Procesos3(usuario,puesto):

    st.session_state.Ingreso=True

    if st.session_state.Procesos==False:

        placeholder1_2= st.sidebar.empty()
        titulo= placeholder1_2.title("Menú")

        placeholder2_2= st.sidebar.empty()
        historial_2 = placeholder2_2.button("Historial",key="historial_2")

        placeholder3_2 = st.sidebar.empty()
        capacitacion_2 = placeholder3_2.button("Capacitaciones",key="capacitacion_2")

        placeholder4_2 = st.sidebar.empty()
        otros_registros_2 = placeholder4_2.button("Otros Registros",key="otros_registros_2")

        placeholder5_2 = st.sidebar.empty()
        bonos_extras_2 = placeholder5_2.button("Bonos y Horas Extras",key="bonos_extras_2")

        placeholder6_2 = st.sidebar.empty()
        salir_2 = placeholder6_2.button("Salir",key="salir_2")

        placeholder7_2 = st.empty()
        registro_2 = placeholder7_2.title("Procesos")

        placeholder8_2 = st.empty()
        precampo_juridico_2 = placeholder8_2.button("Precampo Jurídico",key="precampo_juridico_2")
      
        placeholder9_2 = st.empty()
        cc_precampo_juridico_2 = placeholder9_2.button("Control de Calidad Precampo Jurídico",key="cc_precampo_juridico_2")

        #placeholder10_2 = st.empty()
        #restitucion_tierras_2 = placeholder10_2.button("Restitución de Tierras",key="restitucion_tierras_2")

        #placeholder11_2 = st.empty()
        #revision_segregados_2 = placeholder11_2.button("Revisión de Predios Segregados",key="revision_segregados_2")
              
       # ----- Historial ---- #

        if historial_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()

            st.session_state.Procesos=True
            st.session_state.Historial=True
            Historial.Historial(usuario,puesto)

        # ----- Capacitación ---- #

        elif capacitacion_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()

            st.session_state.Procesos=True
            st.session_state.Capacitacion=True
            Capacitacion.Capacitacion(usuario,puesto)

        # ----- Otros Registros ---- #

        elif otros_registros_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()

            st.session_state.Procesos=True
            st.session_state.Otros_Registros=True
            Otros_Registros.Otros_Registros(usuario,puesto)

        # ----- Bonos y Horas Extras ---- #

        elif bonos_extras_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()

            st.session_state.Procesos=True
            st.session_state.Bonos_Extras=True
            Bonos_Extras.Bonos_Extras(usuario,puesto)

        # ----- Salir ---- #

        elif salir_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()

            st.session_state.Ingreso = False
            st.session_state.Procesos = True
            st.session_state.Salir=True
            Salir.Salir()

        # ----- Precampo_Juridico ---- #

        elif precampo_juridico_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()

            st.session_state.Procesos=True
            st.session_state.Precampo_Juridico=True
            Precampo_Juridico.Precampo_Juridico(usuario,puesto)

      
        # ----- Control de Calidad Precampo Jurídico ---- #

        elif cc_precampo_juridico_2:

            placeholder1_2.empty()
            placeholder2_2.empty()
            placeholder3_2.empty()
            placeholder4_2.empty()
            placeholder5_2.empty()
            placeholder6_2.empty()
            placeholder7_2.empty()
            placeholder8_2.empty()
            placeholder9_2.empty()

            st.session_state.Procesos=True
            st.session_state.CC_Precampo_Juridico=True
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario,puesto)
        
        # ----- Restitución de Tierras ---- #

        #elif restitucion_tierras_2:

            #placeholder1_2.empty()
            #placeholder2_2.empty()
            #placeholder3_2.empty()
            #placeholder4_2.empty()
            #placeholder5_2.empty()
            #placeholder6_2.empty()
            #placeholder7_2.empty()
            #placeholder8_2.empty()
            #placeholder9_2.empty()
            #placeholder10_2.empty()
            #placeholder11_2.empty()
            #st.session_state.Procesos=True
            #st.session_state.Restitucion_Tierras=True
            #Restitucion_Tierras.Restitucion_Tierras(usuario,puesto)

        # ----- Revisión de Predios Segredados ---- #

        #elif revision_segregados_2:

            #placeholder1_2.empty()
            #placeholder2_2.empty()
            #placeholder3_2.empty()
            #placeholder4_2.empty()
            #placeholder5_2.empty()
            #placeholder6_2.empty()
            #placeholder7_2.empty()
            #placeholder8_2.empty()
            #placeholder9_2.empty()
            #placeholder10_2.empty()
            #placeholder11_2.empty()
            #st.session_state.Procesos=True
            #st.session_state.Revision_Segregados=True
            #Revision_Segregados.Revision_Segregados(usuario,puesto)
    
    elif st.session_state.Procesos==True:

        if st.session_state.Historial==True:
            Historial.Historial(usuario,puesto)       

        elif st.session_state.Capacitacion==True:
            Capacitacion.Capacitacion(usuario,puesto)

        elif st.session_state.Otros_Registros==True:
            Otros_Registros.Otros_Registros(usuario,puesto)

        elif st.session_state.Bonos_Extras==True:
            Bonos_Extras.Bonos_Extras(usuario,puesto)

        elif st.session_state.Precampo_Juridico==True:
            Precampo_Juridico.Precampo_Juridico(usuario,puesto)
        
        elif st.session_state.CC_Precampo_Juridico==True:
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario,puesto)

        #elif st.session_state.Restitucion_Tierras==True:
            #Restitucion_Tierras.Restitucion_Tierras(usuario,puesto)

        #elif st.session_state.Revision_Segregados==True:
            #Revision_Segregados.Revision_Segregados(usuario,puesto)
