# ----- Librerías ---- #
import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
from urllib.parse import urlparse
import pytz
import Procesos,Historial,Otros_Registros,Bonos_Extras,Salir
import numpy as np
from Autenticacion import hostname, database, username, pwd, port_id, con

def Capacitacion(usuario,puesto):

  # ----- Conexión, Botones y Memoria ---- #
  uri=st.secrets.db_credentials.URI

  
  placeholder1_8= st.sidebar.empty()
  titulo= placeholder1_8.title("Menú")

  placeholder2_8 = st.sidebar.empty()
  procesos_8 = placeholder2_8.button("Procesos",key="procesos_8")

  placeholder3_8 = st.sidebar.empty()
  historial_8 = placeholder3_8.button("Historial",key="historial_8")

  placeholder4_8 = st.sidebar.empty()
  otros_registros_8 = placeholder4_8.button("Otros Registros",key="otros_registros_8")

  placeholder5_8 = st.sidebar.empty()
  bonos_extras_8 = placeholder5_8.button("Bonos y Horas Extras",key="bonos_extra_8")

  placeholder6_8 = st.sidebar.empty()
  salir_8 = placeholder6_8.button("Salir",key="salir_8")

  placeholder7_8 = st.empty()
  capacitacion_8 = placeholder7_8.title("Capacitaciones")

  if puesto== "Coordinador":

    nombre_8= pd.read_sql(f"select nombre from usuarios where usuario='{usuario}'",uri)
    nombre_8 = nombre_8.loc[0,'nombre']

    placeholder8_8 = st.empty()
    capacitacion_registro_8 = placeholder8_8.subheader("Registro")

    data_personal_8 = pd.read_sql(f"select nombre from usuarios where estado='Activo'", con)
    placeholder9_8 = st.empty()
    personal_8= placeholder9_8.multiselect("Personal",data_personal_8,key="personal_8")

    default_date_8 = datetime.now(pytz.timezone('America/Guatemala'))
      
    placeholder10_8= st.empty()
    fecha_8= placeholder10_8.date_input("Fecha",value=default_date_8,key="fecha_8")

    placeholder11_8= st.empty()
    tema_8=placeholder11_8.selectbox("Tema", options=("Bonos","Información General","Precampo","QC Precampo","Postcampo","QC Postcampo","QGIS","Reportes y Registros","Sistema de Gestión Empresarial","Otros",), key="tema_8")

    placeholder12_8= st.empty()
    observaciones_8= placeholder12_8.text_input("Observaciones",max_chars=60,key="observaciones_8")
    
    placeholder13_8= st.empty()
    horas_8= placeholder13_8.number_input("Cantidad de Horas de Capacitación Individuales",min_value=0.0,key="horas_8")

    placeholder14_8 = st.empty()
    reporte_8 = placeholder14_8.button("Generar Reporte",key="reporte_8")

    placeholder15_8= st.empty()
    separador_8 = placeholder15_8.markdown("_____")

    placeholder16_8 = st.empty()
    capacitacion_historial_8 = placeholder16_8.subheader("Historial Capacitaciones")

    placeholder17_8 = st.empty()
    fecha_de__inicio_8 = placeholder17_8.date_input("Fecha de Inicio",value=default_date_8,key="fecha_de_inicio_8")

    placeholder18_8 = st.empty()
    fecha_de__finalizacion_8 = placeholder18_8.date_input("Fecha de Finalización",value=default_date_8,key="fecha_de_finalizacion_8")
      
    placeholder19_8 = st.empty()
    filtro_8 = placeholder19_8.selectbox("Filtro", options=("Todos","Operarios","Profesional Jurídico","Propio","Personal Asignado","Reportados"), key="filtro_8")

    if filtro_8=="Todos":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

    elif filtro_8=="Operarios":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where puesto='Operario Catastral' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

    elif filtro_8=="Profesional Jurídico":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where puesto='Profesiona Jurídico' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)
    
    elif filtro_8=="Propio" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where usuario='{usuario}' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

    elif filtro_8=="Personal Asignado" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,observaciones,horas,reporte from capacitaciones where supervisor='{nombre_8}' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

    elif filtro_8=="Reportados" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,observaciones,horas,reporte from capacitaciones where reporte='{nombre_8}' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)
      
  elif puesto=="Supervisor":   

    nombre_8= pd.read_sql(f"select nombre from usuarios where usuario ='{usuario}'",uri)
    nombre_8 = nombre_8.loc[0,'nombre']   

    placeholder8_8 = st.empty()
    capacitacion_registro_8 = placeholder8_8.subheader("Registro")

    data_personal_8 = pd.read_sql(f"select nombre from usuarios where estado='Activo' and supervisor='{nombre_8}' or usuario='{usuario}'", con)
    placeholder9_8 = st.empty()
    personal_8= placeholder9_8.multiselect("Personal",data_personal_8,key="personal_8")

    default_date_8 = datetime.now(pytz.timezone('America/Guatemala'))

    placeholder10_8= st.empty()
    fecha_8= placeholder10_8.date_input("Fecha",value=default_date_8,key="fecha_8")
      
    placeholder11_8= st.empty()
    tema_8=placeholder11_8.selectbox("Tema", options=("Bonos","Criterios Técnicos","Información General","QGIS","Reportes y Registros","Sistema de Gestión Empresarial","Otros"), key="tema_8")

    placeholder12_8= st.empty()
    observaciones_8= placeholder12_8.text_input("Observaciones",max_chars=60,key="observaciones_8")
    
    placeholder13_8= st.empty()
    horas_8= placeholder13_8.number_input("Cantidad de Horas de Capacitación Individuales",min_value=0.0,key="horas_8")

    placeholder14_8 = st.empty()
    reporte_8 = placeholder14_8.button("Generar Reporte",key="reporte_8")

    placeholder15_8= st.empty()
    separador_8 = placeholder15_8.markdown("_____")

    placeholder16_8 = st.empty()
    capacitacion_historial_8 = placeholder16_8.subheader("Historial")

    placeholder17_8 = st.empty()
    fecha_de__inicio_8 = placeholder17_8.date_input("Fecha de Inicio",value=default_date_8,key="fecha_de_inicio_8")

    placeholder18_8 = st.empty()
    fecha_de__finalizacion_8 = placeholder18_8.date_input("Fecha de Finalización",value=default_date_8,key="fecha_de_finalizacion_8")
      
    placeholder19_8 = st.empty()
    filtro_8 = placeholder19_8.selectbox("Filtro", options=("Todos","Operarios","Personal Jurídico","Propio","Personal Asignado","Reportados"), key="filtro_8")

    if filtro_8=="Todos":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

    elif filtro_8=="Operarios":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where puesto='Operario Catastral' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

    elif filtro_8=="Personal Jurídico":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where puesto='Profesional Jurídico' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)
      
    elif filtro_8=="Propio" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where usuario='{usuario}' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

    elif filtro_8=="Personal Asignado" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where supervisor='{nombre_8}' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

    elif filtro_8=="Reportados" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where reporte='{nombre_8}' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

  elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":

    placeholder19_8 = st.empty()
    capacitacion_historial_8 = placeholder19_8.subheader("Historial")

    default_date_8 = datetime.now(pytz.timezone('America/Guatemala'))

    placeholder20_8 = st.empty()
    fecha_de__inicio_8 = placeholder20_8.date_input("Fecha de Inicio",value=default_date_8,key="fecha_de_inicio_8")

    placeholder21_8 = st.empty()
    fecha_de__finalizacion_8 = placeholder21_8.date_input("Fecha de Finalización",value=default_date_8,key="fecha_de_finalizacion_8")
      
    data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte from capacitaciones where usuario='{usuario}' and fecha>='{fecha_de__inicio_8}' and fecha<='{fecha_de__finalizacion_8}'", con)

  placeholder22_8 = st.empty()
  histo_8= placeholder22_8.dataframe(data=data)

  # ----- Procesos ---- #
    
  if procesos_8:
    placeholder1_8.empty()
    placeholder2_8.empty()
    placeholder3_8.empty()
    placeholder4_8.empty()
    placeholder5_8.empty()   
    placeholder6_8.empty()
    placeholder7_8.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_8.empty()
      placeholder9_8.empty()
      placeholder10_8.empty()
      placeholder11_8.empty()
      placeholder12_8.empty()
      placeholder13_8.empty()
      placeholder14_8.empty()
      placeholder15_8.empty()  
      placeholder16_8.empty()
      placeholder17_8.empty()
      placeholder18_8.empty()
      placeholder19_8.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder19_8.empty()
      placeholder20_8.empty()
      placeholder21_8.empty()
    placeholder22_8.empty()
    st.session_state.Procesos=False
    st.session_state.Capacitacion=False
    
    perfil=pd.read_sql(f"select perfil from usuarios where usuario ='{usuario}'",uri)
    perfil= perfil.loc[0,'perfil']

    if perfil=="1":        
                    
      Procesos.Procesos1(usuario,puesto)
                
    elif perfil=="2":        
                    
      Procesos.Procesos2(usuario,puesto)   

    elif perfil=="3":  

      Procesos.Procesos3(usuario,puesto)       
                
  # ----- Historial ---- #
    
  elif historial_8:
    placeholder1_8.empty()
    placeholder2_8.empty()
    placeholder3_8.empty()
    placeholder4_8.empty()
    placeholder5_8.empty()   
    placeholder6_8.empty()
    placeholder7_8.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_8.empty()
      placeholder9_8.empty()
      placeholder10_8.empty()
      placeholder11_8.empty()
      placeholder12_8.empty()
      placeholder13_8.empty()
      placeholder14_8.empty()
      placeholder15_8.empty()  
      placeholder16_8.empty()
      placeholder17_8.empty()
      placeholder18_8.empty()
      placeholder19_8.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder19_8.empty()
      placeholder20_8.empty()
      placeholder21_8.empty()
    placeholder22_8.empty()
    st.session_state.Capacitacion=False
    st.session_state.Historial=True
    Historial.Historial(usuario,puesto)

  # ----- Otros Registros ---- #
    
  elif otros_registros_8:
    placeholder1_8.empty()
    placeholder2_8.empty()
    placeholder3_8.empty()
    placeholder4_8.empty()
    placeholder5_8.empty()   
    placeholder6_8.empty()
    placeholder7_8.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_8.empty()
      placeholder9_8.empty()
      placeholder10_8.empty()
      placeholder11_8.empty()
      placeholder12_8.empty()
      placeholder13_8.empty()
      placeholder14_8.empty()
      placeholder15_8.empty()  
      placeholder16_8.empty()
      placeholder17_8.empty()
      placeholder18_8.empty()
      placeholder19_8.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder19_8.empty()
      placeholder20_8.empty()
      placeholder21_8.empty()
    placeholder22_8.empty()
    st.session_state.Capacitacion=False
    st.session_state.Otros_Registros=True
    Otros_Registros.Otros_Registros(usuario,puesto)

  # ----- Bonos y Horas Extras ---- #
    
  elif bonos_extras_8:
    placeholder1_8.empty()
    placeholder2_8.empty()
    placeholder3_8.empty()
    placeholder4_8.empty()
    placeholder5_8.empty()   
    placeholder6_8.empty()
    placeholder7_8.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_8.empty()
      placeholder9_8.empty()
      placeholder10_8.empty()
      placeholder11_8.empty()
      placeholder12_8.empty()
      placeholder13_8.empty()
      placeholder14_8.empty()
      placeholder15_8.empty()  
      placeholder16_8.empty()
      placeholder17_8.empty()
      placeholder18_8.empty()
      placeholder19_8.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder19_8.empty()
      placeholder20_8.empty()
      placeholder21_8.empty()
    placeholder22_8.empty()
    st.session_state.Capacitacion=False
    st.session_state.Bonos_Extras=True
    Bonos_Extras.Bonos_Extras(usuario,puesto)
    
  # ----- Salir ---- #
    
  elif salir_8:
    placeholder1_8.empty()
    placeholder2_8.empty()
    placeholder3_8.empty()
    placeholder4_8.empty()
    placeholder5_8.empty()   
    placeholder6_8.empty()
    placeholder7_8.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_8.empty()
      placeholder9_8.empty()
      placeholder10_8.empty()
      placeholder11_8.empty()
      placeholder12_8.empty()
      placeholder13_8.empty()
      placeholder14_8.empty()
      placeholder15_8.empty()  
      placeholder16_8.empty()
      placeholder17_8.empty()
      placeholder18_8.empty()
      placeholder19_8.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder19_8.empty()
      placeholder20_8.empty()
      placeholder21_8.empty()
    placeholder22_8.empty()
    st.session_state.Ingreso=False
    st.session_state.Capacitacion=False
    st.session_state.Salir=True
    Salir.Salir()

  # ----- Reporte ---- #

  if puesto=="Supervisor" or puesto=="Coordinador":

    if reporte_8:

      if personal_8 =='':
        
        st.error('Favor ingresar el nombre de alguna persona')

      else:
        uri=st.secrets.db_credentials.URI
        for nombre in personal_8:
          cursor01=con.cursor()
          
          marca_8= datetime.now(pytz.timezone('America/Guatemala')).strftime("%Y-%m-%d %H:%M:%S")

          usuario_8= pd.read_sql(f"select usuario from usuarios where nombre ='{nombre}'",uri)
          usuario_8 = usuario_8.loc[0,'usuario']
    
          puesto_8= pd.read_sql(f"select puesto from usuarios where nombre ='{nombre}'",uri)
          puesto_8 = puesto_8.loc[0,'puesto']

          supervisor_8= pd.read_sql(f"select supervisor from usuarios where nombre ='{nombre}'",uri)
          supervisor_8 = supervisor_8.loc[0,'supervisor']
          
          cursor01.execute(f"INSERT INTO capacitaciones (marca,usuario,nombre,puesto,supervisor,fecha,tema,horas,observaciones,reporte)VALUES('{marca_8}','{usuario_8}','{nombre}','{puesto_8}','{supervisor_8}','{fecha_8}','{tema_8}','{horas_8}','{observaciones_8}','{nombre_8}')")
          con.commit()                                                                                               
        st.success('Registro enviado correctamente')
