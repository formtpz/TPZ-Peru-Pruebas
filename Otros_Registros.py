# ----- Librerías ---- #
import streamlit as st
import pandas as pd
from datetime import datetime

import pytz

import Procesos,Historial,Capacitacion,Bonos_Extras,Salir
from Autenticacion import obtener_usuario_activo
from db_core import execute, fetch_one

def Otros_Registros(usuario,puesto):

  # ----- Conexión, Botones y Memoria ---- #
  uri=st.secrets.db_credentials.URI



  placeholder1_13= st.sidebar.empty()
  titulo= placeholder1_13.title("Menú")

  placeholder2_13 = st.sidebar.empty()
  procesos_13 = placeholder2_13.button("Procesos",key="procesos_13")

  placeholder3_13 = st.sidebar.empty()
  historial_13 = placeholder3_13.button("Historial",key="historial_13")

  placeholder4_13 = st.sidebar.empty()
  capacitacion_13 = placeholder4_13.button("Capacitaciones",key="capacitacion_13")

  placeholder5_13 = st.sidebar.empty()
  bonos_extras_13 = placeholder5_13.button("Bonos y Horas Extra",key="bonos-extras_13")

  placeholder6_13 = st.sidebar.empty()
  salir_13 = placeholder6_13.button("Salir",key="salir_13")

  placeholder7_13 = st.empty()
  otros_registros_13 = placeholder7_13.title("Otros Registros")

  if puesto== "Coordinador":

    nombre_13= pd.read_sql(f"select nombre from usuarios where usuario='{usuario}'",uri)
    nombre_13 = nombre_13.loc[0,'nombre']

    placeholder8_13 = st.empty()
    otros_registros_registro_13 = placeholder8_13.subheader("Registro")

    data_personal_13 = pd.read_sql(f"select nombre from usuarios where estado='Activo'", con)
    placeholder9_13 = st.empty()
    personal_13= placeholder9_13.multiselect("Personal",data_personal_13,key="personal_13")

    default_date_13=datetime.now(pytz.timezone('America/Guatemala'))

    placeholder10_13= st.empty()
    fecha_13= placeholder10_13.date_input("Fecha",value=default_date_13,key="fecha_13")
    
    placeholder11_13= st.empty()
    motivo_13= placeholder11_13.selectbox("Motivo", options=("Reposición de tiempo","Cita CCSS","Entregas","Incapacidad","Control de Calidad Masivos","Fallos en Aplicativo o Conexión","Horas Extras","Licencia por Fallecimiento de Familiar","Licencia por Maternidad, Paternidad o Lactancia", "Reunión", "Supervisión","Vacaciones","Horas Extra Apoyo Otros Proyectos", "Horas Ordinarias Apoyo a Otros Proyectos","Otros"),key="motivo_13")
        
    placeholder12_13= st.empty()
    horas_13= placeholder12_13.number_input("Cantidad de Horas Individuales",min_value=0.0,key="horas_13")

    placeholder13_13 = st.empty()
    observaciones_13 = placeholder13_13.text_input("Observaciones",max_chars=60,key="observaciones_13")

    placeholder14_13 = st.empty()
    reporte_13 = placeholder14_13.button("Generar Reporte",key="reporte_13")

    placeholder15_13= st.empty()
    separador_13 = placeholder15_13.markdown("_____")

    placeholder16_13 = st.empty()
    otros_registros_historial_13 = placeholder16_13.subheader("Historial")

    placeholder17_13 = st.empty()
    fecha_de__inicio_13 = placeholder17_13.date_input("Fecha de Inicio",value=default_date_13,key="fecha_de_inicio_13")

    placeholder18_13 = st.empty()
    fecha_de__finalizacion_13 = placeholder18_13.date_input("Fecha de Finalización",value=default_date_13,key="fecha_de_finalizacion_13")
      
    placeholder19_13 = st.empty()
    filtro_13 = placeholder19_13.selectbox("Filtro", options=("Todos","Operarios","Profesional Jurídico","Propio","Personal Asignado","Reportados"), key="filtro_13")

    if filtro_13=="Todos":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)

    elif filtro_13=="Operarios":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where puesto='Operario Catastral' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)
    
    elif filtro_13=="Profesional Jurídico":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where puesto='Profesional Jurídico' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)
  
    elif filtro_13=="Propio" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)

    elif filtro_13=="Personal Asignado" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where supervisor='{nombre_13}' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)

    elif filtro_13=="Reportados" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where reporte='{nombre_13}' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)

  elif puesto=="Supervisor":   
    
    nombre_13= pd.read_sql(f"select nombre from usuarios where usuario ='{usuario}'",uri)
    nombre_13 = nombre_13.loc[0,'nombre']   

    placeholder8_13 = st.empty()
    otros_registros_registro_13 = placeholder8_13.subheader("Registro")

    data_personal_13 = pd.read_sql(f"select nombre from usuarios where estado='Activo' and supervisor='{nombre_13}' or usuario='{usuario}'", con)
    placeholder9_13 = st.empty()
    personal_13= placeholder9_13.multiselect("Personal",data_personal_13,key="personal_13")

    default_date_13=datetime.now(pytz.timezone('America/Guatemala'))

    placeholder10_13= st.empty()
    fecha_13= placeholder10_13.date_input("Fecha",value=default_date_13,key="fecha_13")

    placeholder11_13= st.empty()
    motivo_13= placeholder11_13.selectbox("Motivo", options=("Reposición de tiempo","Cita CCSS","Entregas","Incapacidad","Control de Calidad Masivos","Fallos en Aplicativo o Conexión","Horas Extras","Licencia por Fallecimiento de Familiar","Licencia por Maternidad, Paternidad o Lactancia", "Reunión", "Supervisión","Vacaciones","Horas Extra Apoyo Otros Proyectos", "Horas Ordinarias Apoyo a Otros Proyectos","Otros"),key="motivo_13")
        
    placeholder12_13= st.empty()
    horas_13= placeholder12_13.number_input("Cantidad de Horas Individuales",min_value=0.0,key="horas_13")

    placeholder13_13 = st.empty()
    observaciones_13 = placeholder13_13.text_input("Observaciones",max_chars=60,key="observaciones_13")

    placeholder14_13 = st.empty()
    reporte_13 = placeholder14_13.button("Generar Reporte",key="reporte_13")

    placeholder15_13= st.empty()
    separador_13 = placeholder15_13.markdown("_____")

    placeholder16_13 = st.empty()
    otros_registros_historial_13 = placeholder16_13.subheader("Historial")

    placeholder17_13 = st.empty()
    fecha_de__inicio_13 = placeholder17_13.date_input("Fecha de Inicio",value=default_date_13,key="fecha_de_inicio_13")

    placeholder18_13 = st.empty()
    fecha_de__finalizacion_13 = placeholder18_13.date_input("Fecha de Finalización",value=default_date_13,key="fecha_de_finalizacion_13")
      
    placeholder19_13 = st.empty()
    filtro_13 = placeholder19_13.selectbox("Filtro", options=("Todos","Operarios","Profesional Jurídico","Propio","Personal Asignado","Reportados"), key="filtro_13")

    if filtro_13=="Todos":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)

    elif filtro_13=="Operarios":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where puesto='Operario Catastral' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)
    
    elif filtro_13=="Profesional Jurídico":
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where puesto='Profesional Jurídico' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)
      
    elif filtro_13=="Propio" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)

    elif filtro_13=="Personal Asignado" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where supervisor='{nombre_13}' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)

    elif filtro_13=="Reportados" :
      data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where reporte='{nombre_13}' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)

  elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico"or puesto=="QC":
 
    placeholder20_13 = st.empty()
    otros_registros_historial_13 = placeholder20_13.subheader("Historial")

    default_date_13 = datetime.now(pytz.timezone('America/Guatemala'))

    placeholder21_13 = st.empty()
    fecha_de__inicio_13 = placeholder21_13.date_input("Fecha de Inicio",value=default_date_13,key="fecha_de_inicio_13")

    placeholder22_13 = st.empty()
    fecha_de__finalizacion_13 = placeholder22_13.date_input("Fecha de Finalización",value=default_date_13,key="fecha_de_finalizacion_13")
      
    data = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_13}' and fecha<='{fecha_de__finalizacion_13}'", con)

  placeholder23_13 = st.empty()
  histo_13= placeholder23_13.dataframe(data=data)

  # ----- Registro ---- #
    
  if procesos_13:
    placeholder1_13.empty()
    placeholder2_13.empty()
    placeholder3_13.empty()
    placeholder4_13.empty()
    placeholder5_13.empty()   
    placeholder6_13.empty()
    placeholder7_13.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_13.empty()
      placeholder9_13.empty()
      placeholder10_13.empty()
      placeholder11_13.empty()
      placeholder12_13.empty()
      placeholder13_13.empty()
      placeholder14_13.empty()
      placeholder15_13.empty()
      placeholder16_13.empty()
      placeholder17_13.empty()  
      placeholder18_13.empty()
      placeholder19_13.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder20_13.empty()
      placeholder21_13.empty()
      placeholder22_13.empty()
    placeholder23_13.empty()
    st.session_state.Procesos=False
    st.session_state.Otros_Registros=False

    usuario_activo = obtener_usuario_activo(usuario)
    perfil = str(usuario_activo["perfil"]) if usuario_activo else ""

    if perfil=="1":        
                    
      Procesos.Procesos1(usuario,puesto)
                
    elif perfil=="2":        
                    
      Procesos.Procesos2(usuario,puesto)   

    elif perfil=="3":  

      Procesos.Procesos3(usuario,puesto)       

  # ----- Historial ---- #
    
  elif historial_13:
    placeholder1_13.empty()
    placeholder2_13.empty()
    placeholder3_13.empty()
    placeholder4_13.empty()
    placeholder5_13.empty()   
    placeholder6_13.empty()
    placeholder7_13.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_13.empty()
      placeholder9_13.empty()
      placeholder10_13.empty()
      placeholder11_13.empty()
      placeholder12_13.empty()
      placeholder13_13.empty()
      placeholder14_13.empty()
      placeholder15_13.empty()
      placeholder16_13.empty()
      placeholder17_13.empty()  
      placeholder18_13.empty()
      placeholder19_13.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder20_13.empty()
      placeholder21_13.empty()
      placeholder22_13.empty()
    placeholder23_13.empty()
    st.session_state.Otros_Registros=False
    st.session_state.Historial=True
    Historial.Historial(usuario,puesto)

  # ----- Capacitación ---- #
    
  elif capacitacion_13:
    placeholder1_13.empty()
    placeholder2_13.empty()
    placeholder3_13.empty()
    placeholder4_13.empty()
    placeholder5_13.empty()   
    placeholder6_13.empty()
    placeholder7_13.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_13.empty()
      placeholder9_13.empty()
      placeholder10_13.empty()
      placeholder11_13.empty()
      placeholder12_13.empty()
      placeholder13_13.empty()
      placeholder14_13.empty()
      placeholder15_13.empty()
      placeholder16_13.empty()
      placeholder17_13.empty()  
      placeholder18_13.empty()
      placeholder19_13.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder20_13.empty()
      placeholder21_13.empty()
      placeholder22_13.empty()
    placeholder23_13.empty()
    st.session_state.Otros_Registros=False
    st.session_state.Capacitacion=True
    Capacitacion.Capacitacion(usuario,puesto)

  # ----- Bonos y Horas Extras ---- #

  elif bonos_extras_13:
    placeholder1_13.empty()
    placeholder2_13.empty()
    placeholder3_13.empty()
    placeholder4_13.empty()
    placeholder5_13.empty()   
    placeholder6_13.empty()
    placeholder7_13.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_13.empty()
      placeholder9_13.empty()
      placeholder10_13.empty()
      placeholder11_13.empty()
      placeholder12_13.empty()
      placeholder13_13.empty()
      placeholder14_13.empty()
      placeholder15_13.empty()
      placeholder16_13.empty()
      placeholder17_13.empty()  
      placeholder18_13.empty()
      placeholder19_13.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder20_13.empty()
      placeholder21_13.empty()
      placeholder22_13.empty()
    placeholder23_13.empty()
    st.session_state.Otros_Registros=False
    st.session_state.Bonos_Extras=True
    Bonos_Extras.Bonos_Extras(usuario,puesto)
    
  # ----- Salir ---- #
    
  elif salir_13:
    placeholder1_13.empty()
    placeholder2_13.empty()
    placeholder3_13.empty()
    placeholder4_13.empty()
    placeholder5_13.empty()   
    placeholder6_13.empty()
    placeholder7_13.empty()
    if puesto=="Supervisor" or puesto=="Coordinador":
      placeholder8_13.empty()
      placeholder9_13.empty()
      placeholder10_13.empty()
      placeholder11_13.empty()
      placeholder12_13.empty()
      placeholder13_13.empty()
      placeholder14_13.empty()
      placeholder15_13.empty()
      placeholder16_13.empty()
      placeholder17_13.empty()  
      placeholder18_13.empty()
      placeholder19_13.empty()
    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico" or puesto=="QC":
      placeholder20_13.empty()
      placeholder21_13.empty()
      placeholder22_13.empty()
    placeholder23_13.empty()
    st.session_state.Ingreso = False
    st.session_state.Otros_Registros=False
    st.session_state.Salir=True
    Salir.Salir()

  # ----- Reporte ---- #

  if puesto=="Supervisor" or puesto=="Coordinador":

    if reporte_13:

      if personal_13 =='':
        
        st.error('Favor ingresar el nombre de alguna persona')

      else:
        for nombre in personal_13:
          marca_13= datetime.now(pytz.timezone('America/Guatemala')).strftime("%Y-%m-%d %H:%M:%S")
          persona = fetch_one(
            """
            SELECT usuario, puesto, supervisor
            FROM usuarios
            WHERE nombre = %s
            LIMIT 1
            """,
            params=[nombre],
          )
          if not persona:
            continue

          horas_bi = float(horas_13)
          execute(
            """
            INSERT INTO otros_registros (marca,usuario,nombre,puesto,supervisor,fecha,motivo,horas,observaciones,reporte,horas_bi)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            params=[
              marca_13, persona["usuario"], nombre, persona["puesto"], persona["supervisor"],
              fecha_13, motivo_13, horas_13, observaciones_13, nombre_13, horas_bi
            ],
          )
        st.success('Registro enviado correctamente')
