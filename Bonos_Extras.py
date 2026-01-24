#---INDEX----
#---Perfil 2 Operador- 1 Supervisor Linea 539
#---Perfil 

# ----- Librerías ---- #

import streamlit as st
import numpy as np
import pandas as pd
import psycopg2
from urllib.parse import urlparse
import Procesos,Historial,Capacitacion,Otros_Registros,Salir
from sqlalchemy import create_engine
from Autenticacion import hostname, database, username, pwd, port_id, con

def Bonos_Extras(usuario,puesto):

  # ----- Conexión, Botones y Memoria ---- #
  uri=st.secrets.db_credentials.URI

    

  placeholder1_9= st.sidebar.empty()
  titulo= placeholder1_9.title("Menú")

  placeholder2_9 = st.sidebar.empty()
  procesos_9 = placeholder2_9.button("Procesos",key="procesos_9")

  placeholder3_9 = st.sidebar.empty()
  historial_9 = placeholder3_9.button("Historial",key="historial_9")

  placeholder4_9 = st.sidebar.empty()
  capacitacion_9= placeholder4_9.button("Capacitaciones",key="capacitacion_9")

  placeholder5_9 = st.sidebar.empty()
  otros_registros_9= placeholder5_9.button("Otros Registros",key="otros_registros_9")

  placeholder6_9 = st.sidebar.empty()
  salir_9 = placeholder6_9.button("Salir",key="salir_9")

  placeholder7_9 = st.empty()
  registro_bonos_extras_9 = placeholder7_9.title("Registros de Bonos y Horas Extra")

  nombre_9= pd.read_sql(f"select nombre from usuarios where usuario='{usuario}'",uri)
  nombre_9 = nombre_9.loc[0,'nombre']

  perfil_9= pd.read_sql(f"select perfil from usuarios where usuario='{usuario}'",uri)
  perfil_9 = perfil_9.loc[0,'perfil']
  
  if nombre_9=="Brayan Rojas Pastrana" or nombre_9=="Brandon Felipe Mata Ortega" or nombre_9=="Evelyn Burgos Chavarria":
    
    placeholder8_9 = st.empty()
    archivos = placeholder8_9.subheader("Archivos")

    placeholder9_9 = st.empty()
    bloques_nuevos_9 = placeholder9_9.file_uploader("Cargar Archivo de Bloques",['csv','xlsx'])

    placeholder10_9 = st.empty()
    bonos_nuevos_9 = placeholder10_9.file_uploader("Cargar Archivo de Bonos",['csv','xlsx'])

    placeholder11_9 = st.empty()
    extras_nuevas_9 = placeholder11_9.file_uploader("Cargar Archivo de Extras",['csv','xlsx'])

    placeholder9_9_J = st.empty()
    unidades_nuevas_9 = placeholder9_9_J.file_uploader("Cargar Archivo de Unidades Jurídicas",['csv','xlsx'])

    placeholder10_9_J = st.empty()
    bonos_nuevos_juridico_9 = placeholder10_9_J.file_uploader("Cargar Archivo de Bonos Jurídicos",['csv','xlsx'])

    placeholder12_9 = st.empty()
    cargar_archivos_9 = placeholder12_9.button("Cargar Archivos",key="cargar_archivos_9")

    #----INICIO CAMBIOS SUBIDA DE EXCEL INDIVIDUAL----#
    if cargar_archivos_9:
      if bloques_nuevos_9 is not None:
        df_bloques = pd.read_excel(bloques_nuevos_9) if bloques_nuevos_9.name.endswith('.xlsx') else pd.read_csv(bloques_nuevos_9)
        engine = create_engine(uri)
        df_bloques.to_sql(name='bloques', con=engine, if_exists='append', index=False)
        st.success('Archivo "bloques" cargado correctamente')


      if bonos_nuevos_9 is not None:
        df_bonos = pd.read_excel(bonos_nuevos_9) if bonos_nuevos_9.name.endswith('.xlsx') else pd.read_csv(bonos_nuevos_9)
        engine = create_engine(uri)
        df_bonos.to_sql(name='bonos', con=engine, if_exists='append', index=False)
        st.success('Archivo "bonos" cargado correctamente')

 
      if extras_nuevas_9 is not None:
        df_extras = pd.read_excel(extras_nuevas_9) if extras_nuevas_9.name.endswith('.xlsx') else pd.read_csv(extras_nuevas_9)
        engine = create_engine(uri)
        df_extras.to_sql(name='extras', con=engine, if_exists='append', index=False)
        st.success('Archivo "extras" cargado correctamente')

   
      if unidades_nuevas_9 is not None:
        df_unidades = pd.read_excel(unidades_nuevas_9) if unidades_nuevas_9.name.endswith('.xlsx') else pd.read_csv(unidades_nuevas_9)
        engine = create_engine(uri)
        df_unidades.to_sql(name='unidades', con=engine, if_exists='append', index=False)
        st.success('Archivo "unidades" cargado correctamente')

   
      if bonos_nuevos_juridico_9 is not None:
        df_bonos_juridico = pd.read_excel(bonos_nuevos_juridico_9) if bonos_nuevos_juridico_9.name.endswith('.xlsx') else pd.read_csv(bonos_nuevos_juridico_9)
        engine = create_engine(uri)
        df_bonos_juridico.to_sql(name='bonos_juridico', con=engine, if_exists='append', index=False)
        st.success('Archivo "bonos_juridico" cargado correctamente')

      if all(file is None for file in [bloques_nuevos_9, bonos_nuevos_9, extras_nuevas_9, unidades_nuevas_9, bonos_nuevos_juridico_9]):
        st.warning("No se cargó ningún archivo.")
#----FIN CAMBIOS SUBIDA DE EXCEL INDIVIDUAL----#

      

  elif nombre_9=="Gabriel Martin Prieto" or nombre_9=="Madeline Hernandez Gamboa":

    data_personal_9 = pd.read_sql(f"select nombre from usuarios where estado='Activo'", con)
    Todo = pd.DataFrame({"nombre": ["Todos"]})
    data_personal_9 = pd.concat([data_personal_9,Todo],ignore_index=True)

    placeholder13_9 = st.empty()
    personal_9= placeholder13_9.selectbox("Personal",data_personal_9,key="personal_9")

    placeholder14_9 = st.empty()
    periodo_9 = placeholder14_9.selectbox("Periodo de Bono", options=("Agosto-2025","Septiembre-2025","Octubre-2025","Noviembre-2025","Diciembre-2025","Enero-2026","Febrero-2026","Marzo-2026","Abril-2026","Mayo-2026","Junio-2026","Julio-2026","Agosto-2026","Septiembre-2026","Octubre-2026","Noviembre-2026","Diciembre-2026"), key="periodo_9")    

    if personal_9 == "Todos" :

      placeholder15_9 = st.empty()
      titulo_bonos_9 = placeholder15_9.subheader("Bonos")
      
      bonos_9= pd.read_sql(f"select a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23 from bonos where a23='{periodo_9}'", con)
      bonos_9=  pd.DataFrame(data=bonos_9)


      pivot1= len(bonos_9.iloc[:,0])

      if pivot1==0:

        placeholder16_9 = st.empty()
        error_9 = placeholder16_9.error('No existen datos para mostrar')

      else:

        bono_productividad_9=0
        bono_calidad_9=0
        bono_supervision_9=0
        bono_calidad_externa_9=0
        bonos_entregas_9=0
        bonos_fijos_9=0
        bono_total_9=0
        
        for a in range(0,pivot1):
          bono_productividad_9 = bono_productividad_9 + sum([float(bonos_9.iloc[a,8])])
          bono_calidad_9 = bono_calidad_9 + sum([float(bonos_9.iloc[a,15])])
          bono_supervision_9 = bono_supervision_9 + sum([float(bonos_9.iloc[a,17])])
          bono_calidad_externa_9 = bono_calidad_externa_9 + sum([float(bonos_9.iloc[a,18])])
          bonos_entregas_9 = bonos_entregas_9 + sum([float(bonos_9.iloc[a,21])])
          bonos_fijos_9 = bonos_fijos_9 + sum([float(bonos_9.iloc[a,16])])
          #bonos_fijos_9 = bonos_fijos_9 + sum([float(bonos_9.iloc[a,75]),float(bonos_9.iloc[a,76]),float(bonos_9.iloc[a,77]),float(bonos_9.iloc[a,78]),float(bonos_9.iloc[a,79]),float(bonos_9.iloc[a,80]),float(bonos_9.iloc[a,81]),float(bonos_9.iloc[a,82]),float(bonos_9.iloc[a,83])])
          bono_total_9= bono_total_9 + sum([float(bonos_9.iloc[a,22])])
          #a8-bono productividad a15-bono calidad a16-bono fijo a17-bono por supervision a18-bono calidad externa igac a21 bono variable a22 bono total
        
        placeholder17_9 = st.empty()
        col1, col2, col3, col4, col5, col6, col7 = placeholder17_9.columns(7)
        col1.metric("Bono Productividad", bono_productividad_9)
        col2.metric("Bono Calidad", bono_calidad_9)
        col3.metric("Bono Supervisión", bono_supervision_9)
        col4.metric("Bono Calidad Externa IGAC", bono_calidad_externa_9)
        col5.metric("Bono Variable", bonos_entregas_9)
        col6.metric("Bono Fijo", bonos_fijos_9)
        col7.metric("Bono Total", bono_total_9)

      placeholder18_9 = st.empty()
      titulo_extras_9 = placeholder18_9.subheader("Horas Extra")
      
      extras_9= pd.read_sql(f"select marca,usuario,nombre,puesto,supervisor,tipo_reporte,justificacion,fecha,horas,semana,dia,fecha_corte,fecha_bono from extras where (tipo_reporte='Extra' or tipo_reporte='Horas Extra' or tipo_reporte='Horas Extra Apoyo Otros Proyectos') and fecha_bono='{periodo_9}'", con)
      extras_9=  pd.DataFrame(data=extras_9)

      pivot2= len(extras_9.iloc[:,0])

      if pivot2==0:

        placeholder19_9 = st.empty()
        error_9 = placeholder19_9.error('No existen datos para mostrar')
      
      else:

        total_extras_9=0
        
        for b in range(0,pivot2):

            total_extras_9 = total_extras_9 + float(extras_9.iloc[b,8])

        placeholder20_9 = st.empty()
        total = placeholder20_9.metric("Total de Horas Extra",total_extras_9)

    else:

      placeholder21_9 = st.empty()
      titulo_bonos_9 = placeholder21_9.subheader("Bonos")
      
      bonos_9= pd.read_sql(f"select a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23 from bonos where a1='{personal_9}' and a23='{periodo_9}'", con)
      bonos_9=  pd.DataFrame(data=bonos_9)
    

      pivot3= len(bonos_9.iloc[:,0])

      if pivot3==0:

        placeholder22_9 = st.empty()
        error_9 = placeholder22_9.error('No existen datos para mostrar')

      else:

        # Resumen #
        bono_productividad_9=sum([float(bonos_9.iloc[0,8])])
        bono_calidad_9=sum([float(bonos_9.iloc[0,15])])
        bono_supervision_9=sum([float(bonos_9.iloc[0,17])])
        bono_calidad_externa_9=sum([float(bonos_9.iloc[0,18])])
        bonos_entregas_9=sum([float(bonos_9.iloc[0,21])])
        bonos_fijos_9=sum([float(bonos_9.iloc[0,16])])
        bono_total_9=sum([float(bonos_9.iloc[0,22])])
        
        placeholder23_9 = st.empty()
        col1, col2, col3, col4, col5, col6, col7 = placeholder23_9.columns(7)
        col1.metric("Bono Productividad", bono_productividad_9)
        col2.metric("Bono Calidad", bono_calidad_9)
        col3.metric("Bono Supervisión", bono_supervision_9)
        col4.metric("Bono Calidad Externa IGAC", bono_calidad_externa_9)
        col5.metric("Bono Variable", bonos_entregas_9)
        col6.metric("Bono Fijo", bonos_fijos_9)
        col7.metric("Bono Total", bono_total_9)

        # Procesos #
          
        #variables_9=["Ratio Promedio por Bloque (Predio/Día)","Duración (Día)","Producción (Según Reportes)","Producción Limpia","Producción (Según Ratio)","Producción (Estándar)","Bono Variable","Bono Fijo","Cantidad de Personal"]								

        #conciliacion_9=[0]*9
        #ubicacion_9=[0]*9
        #conformacion_9=[0]*9
        #cc_conformacion_9=[0]*9 	
        #validacion_9=[0]*9	
        #if_i_9=[0]*9
        #cc_if_i_9=[0]*9
        #if_ii_9=[0]*9
        #if_iii_9=[0]*9

        #bonos_procesos_9= pd.DataFrame(data={"Variables":variables_9,"Conciliación":conciliacion_9,"Ubicación":ubicacion_9,"Conformación":conformacion_9,"CC Conformación":cc_conformacion_9,"Validación":validacion_9,"Información Final I":if_i_9,"CC Información Final I":cc_if_i_9,"Información Final II":if_ii_9,"Información Final III":if_iii_9})

        # Conciliación #
          
        #bonos_procesos_9.iloc[0,1] = bonos_9.iloc[0,5]
        #bonos_procesos_9.iloc[1,1] = bonos_9.iloc[0,15]
        #bonos_procesos_9.iloc[2,1] = bonos_9.iloc[0,25]
        #bonos_procesos_9.iloc[3,1] = bonos_9.iloc[0,35]
        #bonos_procesos_9.iloc[4,1] = bonos_9.iloc[0,45]
        #bonos_procesos_9.iloc[5,1] = bonos_9.iloc[0,55]
        #bonos_procesos_9.iloc[6,1] = bonos_9.iloc[0,65]
        #bonos_procesos_9.iloc[7,1] = bonos_9.iloc[0,75]
        #bonos_procesos_9.iloc[8,1] = bonos_9.iloc[0,85]

        # Ubicación #
          
        #bonos_procesos_9.iloc[0,2] = bonos_9.iloc[0,6]
        #bonos_procesos_9.iloc[1,2] = bonos_9.iloc[0,16]
        #bonos_procesos_9.iloc[2,2] = bonos_9.iloc[0,26]
        #bonos_procesos_9.iloc[3,2] = bonos_9.iloc[0,36]
        #bonos_procesos_9.iloc[4,2] = bonos_9.iloc[0,46]
        #bonos_procesos_9.iloc[5,2] = bonos_9.iloc[0,56]
        #bonos_procesos_9.iloc[6,2] = bonos_9.iloc[0,66]
        #bonos_procesos_9.iloc[7,2] = bonos_9.iloc[0,76]
        #bonos_procesos_9.iloc[8,2] = bonos_9.iloc[0,86]

        # Conformación #
          
        #bonos_procesos_9.iloc[0,3] = bonos_9.iloc[0,7]
        #bonos_procesos_9.iloc[1,3] = bonos_9.iloc[0,17]
        #bonos_procesos_9.iloc[2,3] = bonos_9.iloc[0,27]
        #bonos_procesos_9.iloc[3,3] = bonos_9.iloc[0,37]
        #bonos_procesos_9.iloc[4,3] = bonos_9.iloc[0,47]
        #bonos_procesos_9.iloc[5,3] = bonos_9.iloc[0,57]
        #bonos_procesos_9.iloc[6,3] = bonos_9.iloc[0,67]
        #bonos_procesos_9.iloc[7,3] = bonos_9.iloc[0,77]
        #bonos_procesos_9.iloc[8,3] = bonos_9.iloc[0,87]

        #  Control de Calidad Conformación #
          
        #bonos_procesos_9.iloc[0,4] = bonos_9.iloc[0,8]
        #bonos_procesos_9.iloc[1,4] = bonos_9.iloc[0,18]
        #bonos_procesos_9.iloc[2,4] = bonos_9.iloc[0,28]
        #bonos_procesos_9.iloc[3,4] = bonos_9.iloc[0,38]
        #bonos_procesos_9.iloc[4,4] = bonos_9.iloc[0,48]
        #bonos_procesos_9.iloc[5,4] = bonos_9.iloc[0,58]
        #bonos_procesos_9.iloc[6,4] = bonos_9.iloc[0,68]
        #bonos_procesos_9.iloc[7,4] = bonos_9.iloc[0,78]
        #bonos_procesos_9.iloc[8,4] = bonos_9.iloc[0,88]

        # Validación #
          
        #bonos_procesos_9.iloc[0,5] = bonos_9.iloc[0,9]
        #bonos_procesos_9.iloc[1,5] = bonos_9.iloc[0,19]
        #bonos_procesos_9.iloc[2,5] = bonos_9.iloc[0,29]
        #bonos_procesos_9.iloc[3,5] = bonos_9.iloc[0,39]
        #bonos_procesos_9.iloc[4,5] = bonos_9.iloc[0,49]
        #bonos_procesos_9.iloc[5,5] = bonos_9.iloc[0,59]
        #bonos_procesos_9.iloc[6,5] = bonos_9.iloc[0,69]
        #bonos_procesos_9.iloc[7,5] = bonos_9.iloc[0,79]
        #bonos_procesos_9.iloc[8,5] = bonos_9.iloc[0,89]

        # Información Final I #

        #bonos_procesos_9.iloc[0,6] = bonos_9.iloc[0,10]
        #bonos_procesos_9.iloc[1,6] = bonos_9.iloc[0,20]
        #bonos_procesos_9.iloc[2,6] = bonos_9.iloc[0,30]
        #bonos_procesos_9.iloc[3,6] = bonos_9.iloc[0,40]
        #bonos_procesos_9.iloc[4,6] = bonos_9.iloc[0,50]
        #bonos_procesos_9.iloc[5,6] = bonos_9.iloc[0,60]
        #bonos_procesos_9.iloc[6,6] = bonos_9.iloc[0,70]
        #bonos_procesos_9.iloc[7,6] = bonos_9.iloc[0,80]
        #bonos_procesos_9.iloc[8,6] = bonos_9.iloc[0,90]

        # Control de Calidad Información Final I #

        #bonos_procesos_9.iloc[0,7] = bonos_9.iloc[0,11]
        #bonos_procesos_9.iloc[1,7] = bonos_9.iloc[0,21]
        #bonos_procesos_9.iloc[2,7] = bonos_9.iloc[0,31]
        #bonos_procesos_9.iloc[3,7] = bonos_9.iloc[0,41]
        #bonos_procesos_9.iloc[4,7] = bonos_9.iloc[0,51]
        #bonos_procesos_9.iloc[5,7] = bonos_9.iloc[0,61]
        #bonos_procesos_9.iloc[6,7] = bonos_9.iloc[0,71]
        #bonos_procesos_9.iloc[7,7] = bonos_9.iloc[0,81]
        #bonos_procesos_9.iloc[8,7] = bonos_9.iloc[0,91]

        # Información Final II #

        #bonos_procesos_9.iloc[0,8] = bonos_9.iloc[0,12]
        #bonos_procesos_9.iloc[1,8] = bonos_9.iloc[0,22]
        #bonos_procesos_9.iloc[2,8] = bonos_9.iloc[0,32]
        #bonos_procesos_9.iloc[3,8] = bonos_9.iloc[0,42]
        #bonos_procesos_9.iloc[4,8] = bonos_9.iloc[0,52]
        #bonos_procesos_9.iloc[5,8] = bonos_9.iloc[0,62]
        #bonos_procesos_9.iloc[6,8] = bonos_9.iloc[0,72]
        #bonos_procesos_9.iloc[7,8] = bonos_9.iloc[0,82]
        #bonos_procesos_9.iloc[8,8] = bonos_9.iloc[0,92]

        # Información Final III #

        #bonos_procesos_9.iloc[0,9] = bonos_9.iloc[0,13]
        #bonos_procesos_9.iloc[1,9] = bonos_9.iloc[0,23]
        #bonos_procesos_9.iloc[2,9] = bonos_9.iloc[0,33]
        #bonos_procesos_9.iloc[3,9] = bonos_9.iloc[0,43]
        #bonos_procesos_9.iloc[4,9] = bonos_9.iloc[0,53]
        #bonos_procesos_9.iloc[5,9] = bonos_9.iloc[0,63]
        #bonos_procesos_9.iloc[6,9] = bonos_9.iloc[0,73]
        #bonos_procesos_9.iloc[7,9] = bonos_9.iloc[0,83]
        #bonos_procesos_9.iloc[8,9] = bonos_9.iloc[0,93]

        #placeholder24_9 = st.empty()
        #dataframe_bonos_procesos_9=placeholder24_9.dataframe(data=bonos_procesos_9)

        # Otros Bonos #

        #variables_9=["Bonos Variables","Bonos Fijos","Bonificación por Entregas","Bonificación Cumplimiento RN","Bonificación Supervisión","Bonificación Exposiciones Públicas","Bonificación Otras Funciones","Observaciones","Bonificación Total"]								
        #valor_9=[0]*9

        #otros_bonos_9= pd.DataFrame(data={"Variables":variables_9,"Valor":valor_9})
          
        #otros_bonos_9.iloc[0,1] = bonos_entregas_9
        #otros_bonos_9.iloc[1,1] = bonos_fijos_9
        #otros_bonos_9.iloc[2,1] = bonos_9.iloc[0,95]
        #otros_bonos_9.iloc[3,1] = bonos_9.iloc[0,96]
        #otros_bonos_9.iloc[4,1] = bonos_9.iloc[0,97]
        #otros_bonos_9.iloc[5,1] = bonos_9.iloc[0,98]
        #otros_bonos_9.iloc[6,1] = bonos_9.iloc[0,99]
        #otros_bonos_9.iloc[7,1] = bonos_9.iloc[0,101]
        #otros_bonos_9.iloc[8,1] = bonos_9.iloc[0,102]

        #placeholder25_9 = st.empty()
        #dataframe_otros_bonos_9=placeholder25_9.dataframe(data=otros_bonos_9)

      placeholder26_9 = st.empty()
      titulo_extras_9 = placeholder26_9.subheader("Horas Extra")
      
      extras_9= pd.read_sql(f"select marca,usuario,nombre,puesto,supervisor,tipo_reporte,justificacion,fecha,horas,semana,dia,fecha_corte,fecha_bono from extras where nombre='{personal_9}' and (tipo_reporte='Extra' or tipo_reporte='Horas Extra' or tipo_reporte='Horas Extra Apoyo Otros Proyectos') and fecha_bono='{periodo_9}'", con)
      extras_9= pd.DataFrame(data=extras_9)

      pivot4= len(extras_9.iloc[:,0])

      if pivot4==0:

        placeholder27_9 = st.empty()
        error_9 = placeholder27_9.error('No existen datos para mostrar')
      
      else:

        total_extras_9=0
        
        for b in range(0,pivot4):

            total_extras_9 = total_extras_9 + float(extras_9.iloc[b,8])

        placeholder28_9 = st.empty()
        total = placeholder28_9.metric("Total de Horas Extra",total_extras_9)
        
        data_extras=pd.read_sql(f"select marca,usuario,nombre,puesto,supervisor,tipo_reporte,justificacion,fecha,horas,semana,dia,fecha_corte,fecha_bono from extras where (tipo_reporte='Extra' or tipo_reporte='Horas Extra' or tipo_reporte='Horas Extra Apoyo Otros Proyectos') and fecha_bono='{periodo_9}' and nombre='{personal_9}'",con)

        placeholder29_9 = st.empty()
        historial_9_extras=placeholder29_9.dataframe(data=data_extras)
  
  elif nombre_9=="Ignacio Aguglino":
    data_personal_9 = pd.read_sql(f"select nombre from usuarios where puesto='Profesional Jurídico' and estado='Activo'", con)
    Todo = pd.DataFrame({"nombre": ["Todos"]})
    data_personal_9 = pd.concat([data_personal_9,Todo],ignore_index=True)

    placeholder101_9 = st.empty()
    personal_9= placeholder101_9.selectbox("Personal",data_personal_9,key="personal_9")

    placeholder102_9 = st.empty()
    periodo_9 = placeholder102_9.selectbox("Periodo de Bono", options=("Agosto-2025","Septiembre-2025","Octubre-2025","Noviembre-2025","Diciembre-2025","Enero-2026","Febrero-2026","Marzo-2026","Abril-2026","Mayo-2026","Junio-2026","Julio-2026","Agosto-2026","Septiembre-2026","Octubre-2026","Noviembre-2026","Diciembre-2026"), key="periodo_9")    

    if personal_9 == "Todos" :

      placeholder103_9 = st.empty()
      titulo_bonos_9 = placeholder103_9.subheader("Bonos")
      
      bonos_juridico_9= pd.read_sql(f"select a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24 from bonos_juridico where a24='{periodo_9}'", con)
      bonos_juridico_9=  pd.DataFrame(data=bonos_juridico_9)
   
      
      pivot101= len(bonos_juridico_9.iloc[:,0])

      if pivot101==0:

        placeholder104_9 = st.empty()
        error_9 = placeholder104_9.error('No existen datos para mostrar')

      else:
        
        placeholder105_9 = st.empty()
        total = placeholder105_9.metric(label="Total Bonos Jurídicos (COP)", value= pd.to_numeric(bonos_juridico_9['a23']).sum())   

    else:
    
      placeholder106_9 = st.empty()
      titulo_bonos_9 = placeholder106_9.subheader("Bonos")
      
      bonos_juridico_9= pd.read_sql(f"select a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24 from bonos_juridico where a0='{nombre_9}' and a24='{periodo_9}'", con)
      bonos_juridico_9=  pd.DataFrame(data=bonos_juridico_9)
   
  
      pivot102= len(bonos_juridico_9.iloc[:,0])
  
      if pivot102==0:
        
        placeholder107_9 = st.empty()
        error_9 = placeholder107_9.error('No existen datos para mostrar')
  
      else:
  
        # Procesos #
        
        variables_1_9=["Producción (Según Reportes)","Producción (Limpia)","Producción (Estándar)","Bono (COP)","Bonificación Otras Funciones (COP)","Observaciones","Bonificación Total (COP)"]								
  
        fmi_9=[0]*7
        cc_fmi_9=[0]*7
        consultas_campo_9=[0]*7
  
        bonos_procesos_9= pd.DataFrame(data={"Variables":variables_1_9,"Folios de Matricula Inmobiliaria":fmi_9,"CC Folios de Matricula Inmobiliaria":cc_fmi_9,"Consultas de Campo":consultas_campo_9})
  
        # Folios de Matricula Inmobiliaria #
        
        bonos_procesos_9.iloc[0,1] = bonos_juridico_9.iloc[0,4]
        bonos_procesos_9.iloc[1,1] = bonos_juridico_9.iloc[0,8]
        bonos_procesos_9.iloc[2,1] = bonos_juridico_9.iloc[0,12]
        bonos_procesos_9.iloc[3,1] = bonos_juridico_9.iloc[0,16]
        bonos_procesos_9.iloc[4,1] = bonos_juridico_9.iloc[0,20]
        bonos_procesos_9.iloc[5,1] = bonos_juridico_9.iloc[0,22]
        bonos_procesos_9.iloc[6,1] = bonos_juridico_9.iloc[0,23]
  
        # CC_Folios de Matricula Inmobiliaria #
        
        bonos_procesos_9.iloc[0,2] = bonos_juridico_9.iloc[0,5]
        bonos_procesos_9.iloc[1,2] = bonos_juridico_9.iloc[0,9]
        bonos_procesos_9.iloc[2,2] = bonos_juridico_9.iloc[0,13]
        bonos_procesos_9.iloc[3,2] = bonos_juridico_9.iloc[0,17]
        bonos_procesos_9.iloc[4,2] = " "
        bonos_procesos_9.iloc[5,2] = " "
        bonos_procesos_9.iloc[6,2] = " "
  
        # Consultas de Campo #
        
        bonos_procesos_9.iloc[0,3] = bonos_juridico_9.iloc[0,6]
        bonos_procesos_9.iloc[1,3] = bonos_juridico_9.iloc[0,10]
        bonos_procesos_9.iloc[2,3] = bonos_juridico_9.iloc[0,14]
        bonos_procesos_9.iloc[3,3] = bonos_juridico_9.iloc[0,18]
        bonos_procesos_9.iloc[4,3] = " "
        bonos_procesos_9.iloc[5,3] = " "
        bonos_procesos_9.iloc[6,3] = " "
  
        placeholder108_9 = st.empty()
        dataframe_bonos_procesos_9=placeholder108_9.dataframe(data=bonos_procesos_9)
  
      # Unidades #
  
      placeholder109_9 = st.empty()
      titulo_bloques_9 = placeholder109_9.subheader("Unidades de Asignación")
  
      placeholder110_9 = st.empty()
      periodo_bloques_9 = placeholder110_9.selectbox("Fecha de Producción", options=("Todos","Agosto-2025","Septiembre-2025","Octubre-2025","Noviembre-2025","Diciembre-2025","Enero-2026","Febrero-2026","Marzo-2026","Abril-2026","Mayo-2026","Junio-2026","Julio-2026","Agosto-2026","Septiembre-2026","Octubre-2026","Noviembre-2026","Diciembre-2026"), key="periodo_bloques_9")    
  
      if periodo_bloques_9=="Todos":
  
        bloques_9= pd.read_sql(f"select nombre,supervisor,proceso,unidad_asignacion,tipo_revision,produccion_segun_reporte,produccion_rechazada_primera_revision,produccion_aprobada_primera_revision,porcentage_error,produccion_penalizada,produccion_limpia,fecha_produccion,fecha_bono from unidades where nombre='{personal_9}'", con)
        bloques_9=  pd.DataFrame(data=bloques_9)
      
      else:
  
        bloques_9= pd.read_sql(f"select nombre,supervisor,proceso,unidad_asignacion,tipo_revision,produccion_segun_reporte,produccion_rechazada_primera_revision,produccion_aprobada_primera_revision,porcentage_error,produccion_penalizada,produccion_limpia,fecha_produccion,fecha_bono from unidades where nombre='{personal_9}' and fecha_produccion='{periodo_bloques_9}'", con)
        bloques_9=  pd.DataFrame(data=bloques_9)
      
  
      pivot103= len(bloques_9.iloc[:,1])
  
      if pivot103 ==0:
  
        placeholder111_9 = st.empty()
        error_9 = placeholder111_9.error('No existen datos para mostrar')
  
      else:
  
        placeholder112_9 = st.empty()
        dataframe_bloques_9=placeholder112_9.dataframe(data=bloques_9)
        
  #------PERFIL OPERADOR y SUPERVISOR-------------------------------------------------------------------------------------------------------------------------------#

  elif perfil_9 == "2" or perfil_9 == "1":
    
    placeholder30_9 = st.empty()
    periodo_9 = placeholder30_9.selectbox("Periodo", options=("Agosto-2025","Septiembre-2025","Octubre-2025","Noviembre-2025","Diciembre-2025","Enero-2026","Febrero-2026","Marzo-2026","Abril-2026","Mayo-2026","Junio-2026","Julio-2026","Agosto-2026","Septiembre-2026","Octubre-2026","Noviembre-2026","Diciembre-2026"), key="periodo_bonos_9")    

    bonos_9 = pd.read_sql(f"select a0, a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22, a23 FROM bonos WHERE a0='{usuario}' AND a23='{periodo_9}'", con)
    bonos_9= pd.DataFrame(data=bonos_9)
    
    pivot5= len(bonos_9.iloc[:,0])

    if pivot5==0:

      placeholder32_9 = st.empty()
      error_9 = placeholder32_9.error('No existen datos para mostrar')
    else:
      # Reemplaza nulos por 0 y suma solo las columnas necesarias

      bono_productividad_precampo_9= float(bonos_9.iloc[0, 5]) 
      bono_calidad_precampo_9= float(bonos_9.iloc[0, 6]) 
      bono_productividad_postcampo_9= float(bonos_9.iloc[0, 7]) 
      bono_calidad_postcampo_9= float(bonos_9.iloc[0, 8]) 
      bono_productividad_vinculacion_9=float(bonos_9.iloc[0, 9]) 
      bono_calidad_vinculacion_9=float(bonos_9.iloc[0, 10])       
      bono_supervision_9= float(bonos_9.iloc[0, 17])
      bono_calidad_externa_9= float(bonos_9.iloc[0, 19]) 
      bonos_entregas_9 = float(bonos_9.iloc[0, 18]) 
      bonos_fijos_9 = float(bonos_9.iloc[0, 20]) 
      bonos_otro_proyecto_9 = float(bonos_9.iloc[0, 21]) 
      bono_total_9 = float(bonos_9.iloc[0, 22])

     
      
      placeholder33_9 = st.empty()

      df_bonos = pd.DataFrame({
        "Concepto": [
          "Bono Productividad (Precampo)",
          "Bono Calidad (Precampo)",
          "Bono Productividad (Postcampo)",
          "Bono Calidad (Postcampo)",
          "Bono Productividad (Vinculación)",
          "Bono Calidad (Vinculación)",
          "Bono Supervisión",
          "Bono Calidad Externa",
          "Bono Entregas",
          "Bono Fijo",
          "Bono Otro Proyecto",
          "TOTAL"
        ],
        "Monto de bonificación": [
          bono_productividad_precampo_9,
          bono_calidad_precampo_9,
          bono_productividad_postcampo_9,
          bono_calidad_postcampo_9,
          bono_productividad_vinculacion_9,
          bono_calidad_vinculacion_9,
          bono_supervision_9,
          bono_calidad_externa_9,
          bonos_entregas_9,
          bonos_fijos_9,
          bonos_otro_proyecto_9,
          bono_total_9
        ]
      })

      placeholder33_9.dataframe(
        df_bonos,
        hide_index=True,
        height=460  # ajusta si quieres más o menos alto
      )
      
   
      #col1, col2, col3, col4, col5, col6, col7 = placeholder33_9.columns(7)
      #col1.metric("Bono Productividad", bono_productividad_9)
      #col2.metric("Bono Calidad", bono_calidad_9)
      #col3.metric("Bono Supervisión", bono_supervision_9)
      #col4.metric("Bono Calidad Externa", bono_calidad_externa_9)
      #col5.metric("Bono Entregas", bonos_entregas_9)
      #col6.metric("Bono Fijo", bonos_fijos_9)
      #col7.metric("Bono Total", bono_total_9)

     

    
      # Procesos #
      
      #variables_1_9=["Ratio Promedio por Bloque (Predio/Día)","Duración (Día)","Producción (Según Reportes)","Producción Limpia","Producción (Según Ratio)","Producción (Estándar)","Bono Variable","Bono Fijo","Cantidad de Personal"]								

      #conciliacion_9=[0]*9
      #ubicacion_9=[0]*9
      #conformacion_9=[0]*9
      #cc_conformacion_9=[0]*9 	
      #validacion_9=[0]*9	
      #if_i_9=[0]*9
      #cc_if_i_9=[0]*9
      #if_ii_9=[0]*9
      #if_iii_9=[0]*9

      #bonos_procesos_9= pd.DataFrame(data={"Variables":variables_1_9,"Conciliación":conciliacion_9,"Ubicación":ubicacion_9,"Conformación":conformacion_9,"CC Conformación":cc_conformacion_9,"Validación":validacion_9,"Información Final I":if_i_9,"CC Información Final I":cc_if_i_9,"Información Final II":if_ii_9,"Información Final III":if_iii_9})

      # Conciliación #
      
      #bonos_procesos_9.iloc[0,1] = bonos_9.iloc[0,5]
      #bonos_procesos_9.iloc[1,1] = bonos_9.iloc[0,15]
      #bonos_procesos_9.iloc[2,1] = bonos_9.iloc[0,25]
      #bonos_procesos_9.iloc[3,1] = bonos_9.iloc[0,35]
      #bonos_procesos_9.iloc[4,1] = bonos_9.iloc[0,45]
      #bonos_procesos_9.iloc[5,1] = bonos_9.iloc[0,55]
      #bonos_procesos_9.iloc[6,1] = bonos_9.iloc[0,65]
      #bonos_procesos_9.iloc[7,1] = bonos_9.iloc[0,75]
      #bonos_procesos_9.iloc[8,1] = bonos_9.iloc[0,85]

      # Ubicación #
      
      #bonos_procesos_9.iloc[0,2] = bonos_9.iloc[0,6]
      #bonos_procesos_9.iloc[1,2] = bonos_9.iloc[0,16]
      #bonos_procesos_9.iloc[2,2] = bonos_9.iloc[0,26]
      #bonos_procesos_9.iloc[3,2] = bonos_9.iloc[0,36]
      #bonos_procesos_9.iloc[4,2] = bonos_9.iloc[0,46]
      #bonos_procesos_9.iloc[5,2] = bonos_9.iloc[0,56]
      #bonos_procesos_9.iloc[6,2] = bonos_9.iloc[0,66]
      #bonos_procesos_9.iloc[7,2] = bonos_9.iloc[0,76]
      #bonos_procesos_9.iloc[8,2] = bonos_9.iloc[0,86]

      # Conformación #
      
      #bonos_procesos_9.iloc[0,3] = bonos_9.iloc[0,7]
      #bonos_procesos_9.iloc[1,3] = bonos_9.iloc[0,17]
      #bonos_procesos_9.iloc[2,3] = bonos_9.iloc[0,27]
      #bonos_procesos_9.iloc[3,3] = bonos_9.iloc[0,37]
      #bonos_procesos_9.iloc[4,3] = bonos_9.iloc[0,47]
      #bonos_procesos_9.iloc[5,3] = bonos_9.iloc[0,57]
      #bonos_procesos_9.iloc[6,3] = bonos_9.iloc[0,67]
      #bonos_procesos_9.iloc[7,3] = bonos_9.iloc[0,77]
      #bonos_procesos_9.iloc[8,3] = bonos_9.iloc[0,87]

      #  Control de Calidad Conformación #
      
      #bonos_procesos_9.iloc[0,4] = bonos_9.iloc[0,8]
      #bonos_procesos_9.iloc[1,4] = bonos_9.iloc[0,18]
      #bonos_procesos_9.iloc[2,4] = bonos_9.iloc[0,28]
      #bonos_procesos_9.iloc[3,4] = bonos_9.iloc[0,38]
      #bonos_procesos_9.iloc[4,4] = bonos_9.iloc[0,48]
      #bonos_procesos_9.iloc[5,4] = bonos_9.iloc[0,58]
      #bonos_procesos_9.iloc[6,4] = bonos_9.iloc[0,68]
      #bonos_procesos_9.iloc[7,4] = bonos_9.iloc[0,78]
      #bonos_procesos_9.iloc[8,4] = bonos_9.iloc[0,88]

      # Validación #
      
      #bonos_procesos_9.iloc[0,5] = bonos_9.iloc[0,9]
      #bonos_procesos_9.iloc[1,5] = bonos_9.iloc[0,19]
      #bonos_procesos_9.iloc[2,5] = bonos_9.iloc[0,29]
      #bonos_procesos_9.iloc[3,5] = bonos_9.iloc[0,39]
      #bonos_procesos_9.iloc[4,5] = bonos_9.iloc[0,49]
      #bonos_procesos_9.iloc[5,5] = bonos_9.iloc[0,59]
      #bonos_procesos_9.iloc[6,5] = bonos_9.iloc[0,69]
      #bonos_procesos_9.iloc[7,5] = bonos_9.iloc[0,79]
      #bonos_procesos_9.iloc[8,5] = bonos_9.iloc[0,89]

      # Información Final I #

      #bonos_procesos_9.iloc[0,6] = bonos_9.iloc[0,10]
      #bonos_procesos_9.iloc[1,6] = bonos_9.iloc[0,20]
      #bonos_procesos_9.iloc[2,6] = bonos_9.iloc[0,30]
      #bonos_procesos_9.iloc[3,6] = bonos_9.iloc[0,40]
      #bonos_procesos_9.iloc[4,6] = bonos_9.iloc[0,50]
      #bonos_procesos_9.iloc[5,6] = bonos_9.iloc[0,60]
      #bonos_procesos_9.iloc[6,6] = bonos_9.iloc[0,70]
      #bonos_procesos_9.iloc[7,6] = bonos_9.iloc[0,80]
      #bonos_procesos_9.iloc[8,6] = bonos_9.iloc[0,90]

      # Control de Calidad Información Final I #

      #bonos_procesos_9.iloc[0,7] = bonos_9.iloc[0,11]
      #bonos_procesos_9.iloc[1,7] = bonos_9.iloc[0,21]
      #bonos_procesos_9.iloc[2,7] = bonos_9.iloc[0,31]
      #bonos_procesos_9.iloc[3,7] = bonos_9.iloc[0,41]
      #bonos_procesos_9.iloc[4,7] = bonos_9.iloc[0,51]
      #bonos_procesos_9.iloc[5,7] = bonos_9.iloc[0,61]
      #bonos_procesos_9.iloc[6,7] = bonos_9.iloc[0,71]
      #bonos_procesos_9.iloc[7,7] = bonos_9.iloc[0,81]
      #bonos_procesos_9.iloc[8,7] = bonos_9.iloc[0,91]

      # Información Final II #

      #bonos_procesos_9.iloc[0,8] = bonos_9.iloc[0,12]
      #bonos_procesos_9.iloc[1,8] = bonos_9.iloc[0,22]
      #bonos_procesos_9.iloc[2,8] = bonos_9.iloc[0,32]
      #bonos_procesos_9.iloc[3,8] = bonos_9.iloc[0,42]
      #bonos_procesos_9.iloc[4,8] = bonos_9.iloc[0,52]
      #bonos_procesos_9.iloc[5,8] = bonos_9.iloc[0,62]
      #bonos_procesos_9.iloc[6,8] = bonos_9.iloc[0,72]
      #bonos_procesos_9.iloc[7,8] = bonos_9.iloc[0,82]
      #bonos_procesos_9.iloc[8,8] = bonos_9.iloc[0,92]

      # Información Final III #

      #bonos_procesos_9.iloc[0,9] = bonos_9.iloc[0,13]
      #bonos_procesos_9.iloc[1,9] = bonos_9.iloc[0,23]
      #bonos_procesos_9.iloc[2,9] = bonos_9.iloc[0,33]
      #bonos_procesos_9.iloc[3,9] = bonos_9.iloc[0,43]
      #bonos_procesos_9.iloc[4,9] = bonos_9.iloc[0,53]
      #bonos_procesos_9.iloc[5,9] = bonos_9.iloc[0,63]
      #bonos_procesos_9.iloc[6,9] = bonos_9.iloc[0,73]
      #bonos_procesos_9.iloc[7,9] = bonos_9.iloc[0,83]
      #bonos_procesos_9.iloc[8,9] = bonos_9.iloc[0,93]

      #placeholder34_9 = st.empty()
      #dataframe_bonos_procesos_9=placeholder34_9.dataframe(data=bonos_procesos_9)

      # Otros Bonos #

      #variables_2_9=["Bonos Variables","Bonos Fijos","Bonificación por Entregas","Bonificación Cumplimiento RN","Bonificación Supervisión","Bonificación Exposiciones Públicas","Bonificación Otras Funciones","Observaciones","Bonificación Total"]								
      #valor_9=[0]*9

      #otros_bonos_9= pd.DataFrame(data={"Variables":variables_2_9,"Valor":valor_9})
      
      #otros_bonos_9.iloc[0,1] = bonos_entregas_9
      #otros_bonos_9.iloc[1,1] = bonos_fijos_9
      #otros_bonos_9.iloc[2,1] = bonos_9.iloc[0,95]
      #otros_bonos_9.iloc[3,1] = bonos_9.iloc[0,96]
      #otros_bonos_9.iloc[4,1] = bonos_9.iloc[0,97]
      #otros_bonos_9.iloc[5,1] = bonos_9.iloc[0,98]
      #otros_bonos_9.iloc[6,1] = bonos_9.iloc[0,99]
      #otros_bonos_9.iloc[7,1] = bonos_9.iloc[0,101]
      #otros_bonos_9.iloc[8,1] = bonos_9.iloc[0,102]

      #placeholder35_9 = st.empty()
      #dataframe_otros_bonos_9=placeholder35_9.dataframe(data=otros_bonos_9)

    # Bloques #

    #placeholder36_9 = st.empty()
    #titulo_bloques_9 = placeholder36_9.subheader("Bloques")

    #placeholder37_9 = st.empty()
    #periodo_bloques_9 = placeholder37_9.selectbox("Fecha de Producción", options=("Todos","Agosto-2025","Septiembre-2025","Octubre-2025","Noviembre-2025","Diciembre-2025","Enero-2026","Febrero-2026","Marzo-2026","Abril-2026","Mayo-2026","Junio-2026","Julio-2026","Agosto-2026","Septiembre-2026","Octubre-2026","Noviembre-2026","Diciembre-2026"), key="periodo_bloques_9")    

    #if periodo_bloques_9=="Todos":

      #bloques_9= pd.read_sql(f"select usuario,nombre,supervisor,proceso,tipo_revision,bloque_distrito,produccion_segun_reporte,horas,produccion_estandar,produccion_rechazada_primera_revision,produccion_aprobada_primera_revision,porcentage_error,produccion_penalizada,produccion_limpia,ratio_limpio_predio_por_dia,primera_reinspeccion,segunda_reinspeccion,porcentage_penalizacion_ratio,ratio_penalizado_predio_por_dia,fecha_produccion,fecha_corte,fecha_bono from bloques where usuario='{usuario}'", con)
      #bloques_9=  pd.DataFrame(data=bloques_9)
    
    #else:

      #bloques_9= pd.read_sql(f"select usuario,nombre,supervisor,proceso,tipo_revision,bloque_distrito,produccion_segun_reporte,horas,produccion_estandar,produccion_rechazada_primera_revision,produccion_aprobada_primera_revision,porcentage_error,produccion_penalizada,produccion_limpia,ratio_limpio_predio_por_dia,primera_reinspeccion,segunda_reinspeccion,porcentage_penalizacion_ratio,ratio_penalizado_predio_por_dia,fecha_produccion,fecha_corte,fecha_bono from bloques where usuario='{usuario}' and fecha_produccion='{periodo_bloques_9}'", con)
      #bloques_9=  pd.DataFrame(data=bloques_9)

    #pivot6= len(bloques_9.iloc[:,1])

    #if pivot6 ==0:

      #placeholder38_9 = st.empty()
      #error_9 = placeholder38_9.error('No existen datos para mostrar')

    #else:

      #placeholder39_9 = st.empty()
      #dataframe_bloques_9=placeholder39_9.dataframe(data=bloques_9)

    placeholder40_9 = st.empty()
    titulo_extras_9 = placeholder40_9.subheader("Horas Extras")

    extras_9= pd.read_sql(f"select marca,usuario,nombre,puesto,supervisor,tipo_reporte,justificacion,fecha,horas,semana,dia,fecha_corte,fecha_bono from extras where (tipo_reporte='Extra' or tipo_reporte='Horas Extra' or tipo_reporte='Horas Extra Apoyo Otros Proyectos') and nombre='{nombre_9}' and fecha_bono='{periodo_9}'", con)
    extras_9= pd.DataFrame(data=extras_9)

    pivot7= len(extras_9.iloc[:,0])

    if pivot7==0:

      placeholder41_9 = st.empty()
      error_9 = placeholder41_9.error('No existen datos para mostrar')
      
    else:

      total_extras_9=0
        
      for b in range(0,pivot7):

        total_extras_9 = total_extras_9 + float(extras_9.iloc[b,8])

      placeholder42_9 = st.empty()
      total = placeholder42_9.metric("Total de Horas Extra",total_extras_9)
        
      data_extras=pd.read_sql(f"select marca,usuario,nombre,puesto,supervisor,tipo_reporte,justificacion,fecha,horas,semana,dia,fecha_corte,fecha_bono from extras where (tipo_reporte='Extra' or tipo_reporte='Horas Extra' or tipo_reporte='Horas Extra Apoyo Otros Proyectos') and fecha_bono='{periodo_9}' and nombre='{nombre_9}'",con)

      placeholder43_9 = st.empty()
      historial_9_extras=placeholder43_9.dataframe(data=data_extras)

  elif perfil_9 == "3":
    
    placeholder44_9 = st.empty()
    periodo_9 = placeholder44_9.selectbox("Periodo",options=("Agosto-2025","Septiembre-2025","Octubre-2025","Noviembre-2025","Diciembre-2025","Enero-2026","Febrero-2026","Marzo-2026","Abril-2026","Mayo-2026","Junio-2026","Julio-2026","Agosto-2026","Septiembre-2026","Octubre-2026","Noviembre-2026","Diciembre-2026"), key="periodo_bonos_9")    

   # placeholder45_9 = st.empty()
   # titulo_bonos_9 = placeholder45_9.subheader("Bonos")
    
   # bonos_juridico_9= pd.read_sql(f"select a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24 from bonos_juridico where a0='{usuario}' and a24='{periodo_9}'", con)
   # bonos_juridico_9=  pd.DataFrame(data=bonos_juridico_9)


    #pivot8= len(bonos_juridico_9.iloc[:,0])

   # if pivot8==0:

     # placeholder46_9 = st.empty()
     # error_9 = placeholder46_9.error('No existen datos para mostrar')

    placeholder46_9 = st.empty()
    titulo_extras_9 = placeholder46_9.subheader("Horas Extras")

    extras_9= pd.read_sql(f"select marca,usuario,nombre,puesto,supervisor,tipo_reporte,justificacion,fecha,horas,semana,dia,fecha_corte,fecha_bono from extras where (tipo_reporte='Extra' or tipo_reporte='Horas Extra' or tipo_reporte='Horas Extra Apoyo Otros Proyectos') and nombre='{nombre_9}' and fecha_bono='{periodo_9}'", con)
    extras_9= pd.DataFrame(data=extras_9)

    pivot8= len(extras_9.iloc[:,0])

    if pivot8==0:

      placeholder47_9 = st.empty()
      error_9 = placeholder47_9.error('No existen datos para mostrar')
      
    else:

      total_extras_9=0
        
      for b in range(0,pivot8):

        total_extras_9 = total_extras_9 + float(extras_9.iloc[b,8])

      placeholder48_9 = st.empty()
      total = placeholder48_9.metric("Total de Horas Extra",total_extras_9)
        
      data_extras=pd.read_sql(f"select marca,usuario,nombre,puesto,supervisor,tipo_reporte,justificacion,fecha,horas,semana,dia,fecha_corte,fecha_bono from extras where (tipo_reporte='Extra' or tipo_reporte='Horas Extra' or tipo_reporte='Horas Extra Apoyo Otros Proyectos') and fecha_bono='{periodo_9}' and nombre='{nombre_9}'",con)

      placeholder49_9 = st.empty()
      historial_9_extras=placeholder49_9.dataframe(data=data_extras)
  
  # ----- Procesos ---- #
    
  if procesos_9:

    placeholder1_9.empty()
    placeholder2_9.empty()
    placeholder3_9.empty()
    placeholder4_9.empty()
    placeholder5_9.empty()   
    placeholder6_9.empty()
    placeholder7_9.empty()

    if nombre_9=="Brayan Rojas Pastrana" or nombre_9=="Brandon Felipe Mata Ortega" or nombre_9=="Evelyn Burgos Chavarria":

      placeholder8_9.empty()
      placeholder9_9.empty()
      placeholder10_9.empty()
      placeholder9_9_J.empty()
      placeholder10_9_J.empty()
      placeholder11_9.empty()
      placeholder12_9.empty()
        
    elif nombre_9== "Gabriel Martin Prieto" or nombre_9=="Madeline Hernandez Gamboa":

      placeholder13_9.empty()
      placeholder14_9.empty()

      if personal_9=="Todos":
        
        placeholder15_9.empty()
        placeholder18_9.empty()       
        
        if pivot1==0:
        
          placeholder16_9.empty()
      
        else:

          placeholder17_9.empty()

        if pivot2==0:
        
          placeholder19_9.empty()
      
        else:

          placeholder20_9.empty()

      else:

        placeholder21_9.empty()
        placeholder26_9.empty()       
        
        if pivot3==0:

          placeholder22_9.empty()

        else:

          placeholder23_9.empty()
          placeholder24_9.empty()
          placeholder25_9.empty()

        if pivot4==0:

          placeholder27_9.empty()

        else:

          placeholder28_9.empty()
          placeholder29_9.empty()

    elif nombre_9== "Ignacio Aguglino":

      placeholder101_9.empty()
      placeholder102_9.empty()

      if personal_9=="Todos":
        
        placeholder103_9.empty()
    
        if pivot101==0:
        
          placeholder104_9.empty()
      
        else:

          placeholder105_9.empty()

      else:

        placeholder106_9.empty()
        placeholder109_9.empty()
        placeholder110_9.empty()
        
        if pivot102==0:

          placeholder107_9.empty()

        else:

          placeholder108_9.empty()

        if pivot103==0:

          placeholder111_9.empty()

        else:

          placeholder112_9.empty()

    elif perfil_9== "2" or perfil_9== "1": 
      
      placeholder30_9.empty()
      #placeholder31_9.empty()
      placeholder40_9.empty()
      #placeholder36_9.empty()
      #placeholder37_9.empty()

      if pivot5==0:

        placeholder32_9.empty()

      else:

        placeholder33_9.empty()
        #placeholder34_9.empty()
        #placeholder35_9.empty()

      #if pivot6==0:

        #placeholder38_9.empty()

      #else:

        #placeholder39_9.empty()

      if pivot7==0:

        placeholder41_9.empty()

      else:

        placeholder42_9.empty()
        placeholder43_9.empty()

    elif perfil_9== "3": 
      
      placeholder44_9.empty()
      #placeholder45_9.empty()
      placeholder46_9.empty()
      if pivot8==0:
        placeholder47_9.empty()
      else:
        placeholder48_9.empty()
        placeholder49_9.empty()
              

    
    st.session_state.Procesos=False
    st.session_state.Bonos_Extras=False

    perfil=pd.read_sql(f"select perfil from usuarios where usuario ='{usuario}'",uri)
    perfil= perfil.loc[0,'perfil']

    if perfil=="1":        
                    
      Procesos.Procesos1(usuario,puesto)
                
    elif perfil=="2":        
                    
      Procesos.Procesos2(usuario,puesto)   

    elif perfil=="3":  

      Procesos.Procesos3(usuario,puesto)

  # ----- Historial ---- #

  if historial_9:
    
    placeholder1_9.empty()
    placeholder2_9.empty()
    placeholder3_9.empty()
    placeholder4_9.empty()
    placeholder5_9.empty()   
    placeholder6_9.empty()
    placeholder7_9.empty()

    if nombre_9=="Brayan Rojas Pastrana" or nombre_9=="Brandon Felipe Mata Ortega" or nombre_9=="Evelyn Burgos Chavarria":

      placeholder8_9.empty()
      placeholder9_9.empty()
      placeholder10_9.empty()
      placeholder9_9_J.empty()
      placeholder10_9_J.empty()
      placeholder11_9.empty()
      placeholder12_9.empty()
        
    elif nombre_9== "Gabriel Martin Prieto" or nombre_9=="Madeline Hernandez Gamboa":

      placeholder13_9.empty()
      placeholder14_9.empty()

      if personal_9=="Todos":
        
        placeholder15_9.empty()
        placeholder18_9.empty()       
        
        if pivot1==0:
        
          placeholder16_9.empty()
      
        else:

          placeholder17_9.empty()

        if pivot2==0:
        
          placeholder19_9.empty()
      
        else:

          placeholder20_9.empty()

      else:

        placeholder21_9.empty()
        placeholder26_9.empty()       
        
        if pivot3==0:

          placeholder22_9.empty()

        else:

          placeholder23_9.empty()
          placeholder24_9.empty()
          placeholder25_9.empty()

        if pivot4==0:

          placeholder27_9.empty()

        else:

          placeholder28_9.empty()
          placeholder29_9.empty()

    elif nombre_9== "Ignacio Aguglino":

      placeholder101_9.empty()
      placeholder102_9.empty()

      if personal_9=="Todos":
        
        placeholder103_9.empty()
    
        if pivot101==0:
        
          placeholder104_9.empty()
      
        else:

          placeholder105_9.empty()

      else:

        placeholder106_9.empty()
        placeholder109_9.empty()
        placeholder110_9.empty()
        
        if pivot102==0:

          placeholder107_9.empty()

        else:

          placeholder108_9.empty()

        if pivot103==0:

          placeholder111_9.empty()

        else:

          placeholder112_9.empty()

    elif perfil_9== "2": 
      
      placeholder30_9.empty()
      #placeholder31_9.empty()
      placeholder40_9.empty()
      #placeholder36_9.empty()
      #placeholder37_9.empty()

      if pivot5==0:

        placeholder32_9.empty()

      else:

        placeholder33_9.empty()
        #placeholder34_9.empty()
        #placeholder35_9.empty()

      #if pivot6==0:

        #placeholder38_9.empty()

      #else:

        #placeholder39_9.empty()

      if pivot7==0:

        placeholder41_9.empty()

      else:

        placeholder42_9.empty()
        placeholder43_9.empty()

    elif perfil_9== "3": 
      
      placeholder44_9.empty()
      #placeholder45_9.empty()
      placeholder46_9.empty()
      if pivot8==0:
        placeholder47_9.empty()
      else:
        placeholder48_9.empty()
        placeholder49_9.empty()


        
    st.session_state.Bonos_Extras=False
    st.session_state.Historial=True
    Historial.Historial(usuario,puesto)

  # ----- Capacitación ---- #
    
  elif capacitacion_9:

    placeholder1_9.empty()
    placeholder2_9.empty()
    placeholder3_9.empty()
    placeholder4_9.empty()
    placeholder5_9.empty()   
    placeholder6_9.empty()
    placeholder7_9.empty()

    if nombre_9=="Brayan Rojas Pastrana" or nombre_9=="Brandon Felipe Mata Ortega" or nombre_9=="Evelyn Burgos Chavarria":

      placeholder8_9.empty()
      placeholder9_9.empty()
      placeholder10_9.empty()
      placeholder9_9_J.empty()
      placeholder10_9_J.empty()
      placeholder11_9.empty()
      placeholder12_9.empty()
        
    elif nombre_9== "Gabriel Martin Prieto" or nombre_9=="Madeline Hernandez Gamboa":

      placeholder13_9.empty()
      placeholder14_9.empty()

      if personal_9=="Todos":
        
        placeholder15_9.empty()
        placeholder18_9.empty()       
        
        if pivot1==0:
        
          placeholder16_9.empty()
      
        else:

          placeholder17_9.empty()

        if pivot2==0:
        
          placeholder19_9.empty()
      
        else:

          placeholder20_9.empty()

      else:

        placeholder21_9.empty()
        placeholder26_9.empty()       
        
        if pivot3==0:

          placeholder22_9.empty()

        else:

          placeholder23_9.empty()
          placeholder24_9.empty()
          placeholder25_9.empty()

        if pivot4==0:

          placeholder27_9.empty()

        else:

          placeholder28_9.empty()
          placeholder29_9.empty()

    elif nombre_9== "Ignacio Aguglino":

      placeholder101_9.empty()
      placeholder102_9.empty()

      if personal_9=="Todos":
        
        placeholder103_9.empty()
    
        if pivot101==0:
        
          placeholder104_9.empty()
      
        else:

          placeholder105_9.empty()

      else:

        placeholder106_9.empty()
        placeholder109_9.empty()
        placeholder110_9.empty()
        
        if pivot102==0:

          placeholder107_9.empty()

        else:

          placeholder108_9.empty()

        if pivot103==0:

          placeholder111_9.empty()

        else:

          placeholder112_9.empty()

    elif perfil_9== "2": 
      
      placeholder30_9.empty()
      #placeholder31_9.empty()
      placeholder40_9.empty()
      #placeholder36_9.empty()
      #placeholder37_9.empty()

      if pivot5==0:

        placeholder32_9.empty()

      else:

        placeholder33_9.empty()
        #placeholder34_9.empty()
        #placeholder35_9.empty()

      #if pivot6==0:

        #placeholder38_9.empty()

      #else:

        #placeholder39_9.empty()

      if pivot7==0:

        placeholder41_9.empty()

      else:

        placeholder42_9.empty()
        placeholder43_9.empty()

    elif perfil_9== "3": 
      
      placeholder44_9.empty()
      #placeholder45_9.empty()
      placeholder46_9.empty()
      if pivot8==0:
        placeholder47_9.empty()
      else:
        placeholder48_9.empty()
        placeholder49_9.empty()


        
    st.session_state.Bonos_Extras=False
    st.session_state.Capacitacion=True
    Capacitacion.Capacitacion(usuario,puesto)

  # ----- Otros Registros ---- #
    
  elif otros_registros_9:
 
    placeholder1_9.empty()
    placeholder2_9.empty()
    placeholder3_9.empty()
    placeholder4_9.empty()
    placeholder5_9.empty()   
    placeholder6_9.empty()
    placeholder7_9.empty()

    if nombre_9=="Brayan Rojas Pastrana" or nombre_9=="Brandon Felipe Mata Ortega" or nombre_9=="Evelyn Burgos Chavarria":

      placeholder8_9.empty()
      placeholder9_9.empty()
      placeholder10_9.empty()
      placeholder9_9_J.empty()
      placeholder10_9_J.empty()
      placeholder11_9.empty()
      placeholder12_9.empty()
        
    elif nombre_9== "Gabriel Martin Prieto" or nombre_9=="Madeline Hernandez Gamboa":

      placeholder13_9.empty()
      placeholder14_9.empty()

      if personal_9=="Todos":
        
        placeholder15_9.empty()
        placeholder18_9.empty()       
        
        if pivot1==0:
        
          placeholder16_9.empty()
      
        else:

          placeholder17_9.empty()

        if pivot2==0:
        
          placeholder19_9.empty()
      
        else:

          placeholder20_9.empty()

      else:

        placeholder21_9.empty()
        placeholder26_9.empty()       
        
        if pivot3==0:

          placeholder22_9.empty()

        else:

          placeholder23_9.empty()
          placeholder24_9.empty()
          placeholder25_9.empty()

        if pivot4==0:

          placeholder27_9.empty()

        else:

          placeholder28_9.empty()
          placeholder29_9.empty()

    elif nombre_9== "Ignacio Aguglino":

      placeholder101_9.empty()
      placeholder102_9.empty()

      if personal_9=="Todos":
        
        placeholder103_9.empty()
    
        if pivot101==0:
        
          placeholder104_9.empty()
      
        else:

          placeholder105_9.empty()

      else:

        placeholder106_9.empty()
        placeholder109_9.empty()
        placeholder110_9.empty()
        
        if pivot102==0:

          placeholder107_9.empty()

        else:

          placeholder108_9.empty()

        if pivot103==0:

          placeholder111_9.empty()

        else:

          placeholder112_9.empty()

    elif perfil_9== "2": 
      
      placeholder30_9.empty()
      #placeholder31_9.empty()
      placeholder40_9.empty()
      #placeholder36_9.empty()
      #placeholder37_9.empty()

      if pivot5==0:

        placeholder32_9.empty()

      else:

        placeholder33_9.empty()
        #placeholder34_9.empty()
        #placeholder35_9.empty()

      #if pivot6==0:

        #placeholder38_9.empty()

      #else:

        #placeholder39_9.empty()

      if pivot7==0:

        placeholder41_9.empty()

      else:

        placeholder42_9.empty()
        placeholder43_9.empty()

    elif perfil_9== "3": 
      
      placeholder44_9.empty()
      #placeholder45_9.empty()
      placeholder46_9.empty()
      if pivot8==0:
        placeholder47_9.empty()
      else:
        placeholder48_9.empty()
        placeholder49_9.empty()
   


    
    st.session_state.Bonos_Extras=False
    st.session_state.Otros_Registros=True
    Otros_Registros.Otros_Registros(usuario,puesto)

  # ----- Salir ---- #
    
  elif salir_9:

    placeholder1_9.empty()
    placeholder2_9.empty()
    placeholder3_9.empty()
    placeholder4_9.empty()
    placeholder5_9.empty()   
    placeholder6_9.empty()
    placeholder7_9.empty()

    if nombre_9=="Brayan Rojas Pastrana" or nombre_9=="Brandon Felipe Mata Ortega" or nombre_9=="Evelyn Burgos Chavarria":

      placeholder8_9.empty()
      placeholder9_9.empty()
      placeholder10_9.empty()
      placeholder9_9_J.empty()
      placeholder10_9_J.empty()
      placeholder11_9.empty()
      placeholder12_9.empty()
        
    elif nombre_9== "Gabriel Martin Prieto" or nombre_9=="Madeline Hernandez Gamboa":

      placeholder13_9.empty()
      placeholder14_9.empty()

      if personal_9=="Todos":
        
        placeholder15_9.empty()
        placeholder18_9.empty()       
        
        if pivot1==0:
        
          placeholder16_9.empty()
      
        else:

          placeholder17_9.empty()

        if pivot2==0:
        
          placeholder19_9.empty()
      
        else:

          placeholder20_9.empty()

      else:

        placeholder21_9.empty()
        placeholder26_9.empty()       
        
        if pivot3==0:

          placeholder22_9.empty()

        else:

          placeholder23_9.empty()
          placeholder24_9.empty()
          placeholder25_9.empty()

        if pivot4==0:

          placeholder27_9.empty()

        else:

          placeholder28_9.empty()
          placeholder29_9.empty()

    elif nombre_9== "Ignacio Aguglino":

      placeholder101_9.empty()
      placeholder102_9.empty()

      if personal_9=="Todos":
        
        placeholder103_9.empty()
    
        if pivot101==0:
        
          placeholder104_9.empty()
      
        else:

          placeholder105_9.empty()

      else:

        placeholder106_9.empty()
        placeholder109_9.empty()
        placeholder110_9.empty()
        
        if pivot102==0:

          placeholder107_9.empty()

        else:

          placeholder108_9.empty()

        if pivot103==0:

          placeholder111_9.empty()

        else:

          placeholder112_9.empty()

    elif perfil_9== "2": 
      
      placeholder30_9.empty()
      #placeholder31_9.empty()
      placeholder40_9.empty()
      #placeholder36_9.empty()
      #placeholder37_9.empty()

      if pivot5==0:

        placeholder32_9.empty()

      else:

        placeholder33_9.empty()
        #placeholder34_9.empty()
        #placeholder35_9.empty()

      #if pivot6==0:

        #placeholder38_9.empty()

      #else:

        #placeholder39_9.empty()

      if pivot7==0:

        placeholder41_9.empty()

      else:

        placeholder42_9.empty()
        placeholder43_9.empty()

    elif perfil_9== "3": 
      
      placeholder44_9.empty()
      #placeholder45_9.empty()
      placeholder46_9.empty()
      if pivot8==0:
        placeholder47_9.empty()
      else:
        placeholder48_9.empty()
        placeholder49_9.empty()

    
    
    st.session_state.Ingreso = False
    st.session_state.Bonos_Extras=False
    st.session_state.Salir=True
    Salir.Salir()
