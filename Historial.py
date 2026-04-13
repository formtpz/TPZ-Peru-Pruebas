# ----- Librerías ---- #
import numpy as np
import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime
import pytz
import plotly.graph_objects as go
import plotly.express as px
from urllib.parse import urlparse
uri=st.secrets.db_credentials.URI
import Procesos,Capacitacion,Otros_Registros,Bonos_Extras,Salir
from Autenticacion import hostname, database, username, pwd, port_id, con

def Historial(usuario,puesto):

  # ----- Conexión, Botones y Memoria ---- #


  uri=st.secrets.db_credentials.URI

  placeholder1_7= st.sidebar.empty()
  titulo= placeholder1_7.title("Menú")

  placeholder2_7 = st.sidebar.empty()
  procesos_7 = placeholder2_7.button("Procesos",key="procesos_7")

  placeholder3_7 = st.sidebar.empty()
  capacitacion_7 = placeholder3_7.button("Capacitaciones",key="capacitacion_7")

  placeholder4_7 = st.sidebar.empty()
  otros_registros_7 = placeholder4_7.button("Otros Registros",key="otros_registros_7")

  placeholder5_7 = st.sidebar.empty()
  bonos_extras_7 = placeholder5_7.button("Bonos y Horas Extras",key="bonos_extras_7")

  placeholder6_7 = st.sidebar.empty()
  salir_7 = placeholder6_7.button("Salir",key="salir_7")

  placeholder7_7 = st.empty()
  historial_7 = placeholder7_7.title("Historial")

  default_date_7 = datetime.now(pytz.timezone('America/Guatemala'))

  placeholder8_7 = st.empty()
  fecha_de__inicio_7 = placeholder8_7.date_input("Fecha de Inicio",value=default_date_7,key="fecha_de_inicio_7")

  placeholder9_7 = st.empty()
  fecha_de__finalizacion_7 = placeholder9_7.date_input("Fecha de Finalización",value=default_date_7,key="fecha_de_finalizacion_7")
  
  nombre_7= pd.read_sql(f"select nombre from usuarios where usuario ='{usuario}'",uri)
  nombre_7 = nombre_7.loc[0,'nombre']

  # ----- Supervisor y Coordinador ---- #



  if puesto=="Supervisor" or puesto=="Técnico SIG" or puesto=="Coordinador": 

    placeholder10_7 = st.empty()
    personal_7 = placeholder10_7.selectbox("Personal", options=("Todos","Operarios","Profesional Jurídico","Propio","Personal Asignado"), key="filtro_7")

    placeholder11_7 = st.empty()
    proceso_7_s = placeholder11_7.selectbox("Proceso", options=("Todos","Postcampo Folios de Matricula Inmobiliaria","Postcampo Control de Calidad FMI","Control de Calidad Folios de Matricula Inmobiliaria","Calidad Externa XTF","Consultas de Campo","Folios de Matricula Inmobiliaria","Precampo","Control de Calidad Precampo","Preparación de Insumos","Entregas Postcampo","Postcampo","Control de Calidad Postcampo","Restitución de Tierras","Revisión de Predios Segregados","Vinculación Precampo","Control de Calidad Vinculación Precampo"), key="proceso_7_s")
    
    placeholder12_7 = st.empty()
    tipo_7_s = placeholder12_7.selectbox("Tipo", options=("Todos","Ordinario","Corrección","Corrección Inspección","Corrección Primera Reinspección","Reproceso Ordinario","Reproceso Corrección Inspección","Reproceso Corrección Primera Reinspección","Inspección","Reinspección","Primera Reinspección","Segunda Reinspección","Reproceso Inspección","Reproceso Primera Reinspección","Reproceso Segunda Reinspección"), key="tipo_7_s")

    
    base_1_reportes =pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float)from registro where fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
    base_1_capacitaciones = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,cast(horas as float),observaciones,reporte from capacitaciones where fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
    base_1_otros = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)

    base_r = base_1_reportes.copy()
    base_c = base_1_capacitaciones.copy()
    base_o = base_1_otros.copy()

    # ------------------------------------------------------------------------------------------------------------------------------------
    # FILTRO PERSONAL
    # ----------------------------
    
    if personal_7 == "Operarios":
    
        base_r = base_r[base_r["puesto"] == "Operario Catastral"]
        base_c = base_c[base_c["puesto"] == "Operario Catastral"]
        base_o = base_o[base_o["puesto"] == "Operario Catastral"]
    
    
    elif personal_7 == "Profesional Jurídico":
    
        base_r = base_r[base_r["puesto"] == "Profesional Jurídico"]
        base_c = base_c[base_c["puesto"] == "Profesional Jurídico"]
        base_o = base_o[base_o["puesto"] == "Profesional Jurídico"]
    
    
    elif personal_7 == "Propio":
    
        base_r = base_r[base_r["nombre"] == nombre_7]
        base_c = base_c[base_c["nombre"] == nombre_7]
        base_o = base_o[base_o["nombre"] == nombre_7]
    
    
    elif personal_7 == "Personal Asignado":
    
        base_r = base_r[base_r["supervisor"] == nombre_7]
        base_c = base_c[base_c["supervisor"] == nombre_7]
        base_o = base_o[base_o["supervisor"] == nombre_7]
    
    
    # ----------------------------
    # FILTRO PROCESO
    # ----------------------------
    
    if proceso_7_s != "Todos":
    
        base_r = base_r[base_r["proceso"] == proceso_7_s]
    
    
    # ----------------------------
    # FILTRO TIPO
    # ----------------------------
    
    if tipo_7_s != "Todos":
    
        base_r = base_r[base_r["tipo"] == tipo_7_s]
    
    
    # ----------------------------
    # DATASETS FINALES (equivalentes a los SQL)
    # ----------------------------
    
    data_1_r = base_r.copy()
    data_1_c = base_c.copy()
    data_1_o = base_o.copy()
    #--------------------------------------------------------------Fin Filtros----------------------------------------------------------------------------
    # ----- Reportes ---- #
    # ----------------------------
    # DATASETS PARA RESUMEN HORAS (igual operador)
    # ----------------------------
    
    data_8_r = base_r[
        ~base_r["tipo"].isin([
            "Producción Horas Extras",
            "Inspección Horas Extras",
            "Reproceso Horas Extras"
        ])
    ].copy()
    
    
    data_6_r = base_r[
        base_r["tipo"].isin([
            "Producción Horas Extras",
            "Inspección Horas Extras",
            "Reproceso Horas Extras"
        ])
    ].copy()
    
    
    data_6_o = base_o[
        base_o["motivo"].isin([
            "Horas Extra",
            "Horas Extra Apoyo Otros Proyectos",
            "Horas Extras"
        ])
    ].copy()
    
    
    data_7_o = base_o[
        base_o["motivo"] == "Reposición de tiempo"
    ].copy()
    
    
    data_9_o = base_o[
        ~base_o["motivo"].isin([
            "Reposición de tiempo",
            "Horas Extra",
            "Horas Extra Apoyo Otros Proyectos",
            "Horas Extras"
        ])
    ].copy()
    
    
    # --------------------------------------------------
    # REPORTES
    # --------------------------------------------------
    
    placeholder13_7 = st.empty()
    reportes_7 = placeholder13_7.subheader("Reportes")
    
    pivot_reportes = len(data_1_r.iloc[:,0])
    pivot_reportes_o = len(data_1_o.iloc[:,0])
    
    if pivot_reportes == 0 and pivot_reportes_o == 0:
    
        placeholder14_7 = st.empty()
        placeholder14_7.error("No existen reportes para mostrar")
    
    else:
    
        placeholder15_7 = st.empty()
        placeholder15_7.dataframe(data=data_1_r)
    
    
    # --------------------------------------------------
    # RESUMEN DE HORAS (VERSION SEGURA)
    # --------------------------------------------------
    pivot_r=len(base_r.iloc[:,0])
    pivot_c=len(base_c.iloc[:,0])
    pivot_o=len(base_o.iloc[:,0])
    placeholder17_7 = st.empty()
    placeholder17_7.subheader("Resumen de Horas")
    
    
    # PRODUCCION NORMAL
    
    if len(data_8_r) > 0:
    
        data_10_r = data_8_r.groupby(
            ["nombre","fecha"],
            as_index=False
        )[["horas"]].agg(np.sum)
    
        data_10_r.rename(
            columns={"horas":"horas_produccion"},
            inplace=True
        )
    
    else:
    
        data_10_r = pd.DataFrame(
            columns=["nombre","fecha","horas_produccion"]
        )
    
    
    # HORAS EXTRA PRODUCCION
    
    if len(data_6_r) > 0:
    
        data_12_r = data_6_r.groupby(
            ["nombre","fecha"],
            as_index=False
        )[["horas"]].agg(np.sum)
    
        data_12_r.rename(
            columns={"horas":"horas_extra_produccion"},
            inplace=True
        )
    
    else:
    
        data_12_r = pd.DataFrame(
            columns=["nombre","fecha","horas_extra_produccion"]
        )
    
    
    # CAPACITACIONES
    
    if len(data_1_c) > 0:
    
        data_2_c = data_1_c.groupby(
            ["nombre","fecha"],
            as_index=False
        )[["horas"]].agg(np.sum)
    
        data_2_c.rename(
            columns={"horas":"horas_capacitacion"},
            inplace=True
        )
    
    else:
    
        data_2_c = pd.DataFrame(
            columns=["nombre","fecha","horas_capacitacion"]
        )
    
    
    # OTROS REGISTROS
    
    if len(data_9_o) > 0:
    
        data_11_o = data_9_o.groupby(
            ["nombre","fecha"],
            as_index=False
        )[["horas"]].agg(np.sum)
    
        data_11_o.rename(
            columns={"horas":"horas_otros_registros"},
            inplace=True
        )
    
    else:
    
        data_11_o = pd.DataFrame(
            columns=["nombre","fecha","horas_otros_registros"]
        )
    
    
    # HORAS EXTRA OTROS
    
    if len(data_6_o) > 0:
    
        data_13_o = data_6_o.groupby(
            ["nombre","fecha"],
            as_index=False
        )[["horas"]].agg(np.sum)
    
        data_13_o.rename(
            columns={"horas":"horas_extra_otros_registros"},
            inplace=True
        )
    
    else:
    
        data_13_o = pd.DataFrame(
            columns=["nombre","fecha","horas_extra_otros_registros"]
        )
    
    
    # REPOSICION
    
    if len(data_7_o) > 0:
    
        data_14_o = data_7_o.groupby(
            ["nombre","fecha"],
            as_index=False
        )[["horas"]].agg(np.sum)
    
        data_14_o.rename(
            columns={"horas":"reposicion"},
            inplace=True
        )
    
    else:
    
        data_14_o = pd.DataFrame(
            columns=["nombre","fecha","reposicion"]
        )
    
    
    # --------------------------------------------------
    # COMBINAR RESULTADOS
    # --------------------------------------------------
    
    datos_horas = pd.concat(
        [data_10_r,data_12_r,data_2_c,data_11_o,data_13_o],
        axis=0
    )
    
    if len(datos_horas) == 0:
    
        placeholder18_7 = st.empty()
        placeholder18_7.error("No existen horas para mostrar")
    
    else:
    
        datos_horas = pd.DataFrame(datos_horas).groupby(
            ["nombre","fecha"],
            as_index=False
        ).size()
    
    
        datos_horas = pd.merge(datos_horas,data_10_r,on=["nombre","fecha"],how="left")
        datos_horas = pd.merge(datos_horas,data_12_r,on=["nombre","fecha"],how="left")
        datos_horas = pd.merge(datos_horas,data_2_c,on=["nombre","fecha"],how="left")
        datos_horas = pd.merge(datos_horas,data_11_o,on=["nombre","fecha"],how="left")
        datos_horas = pd.merge(datos_horas,data_13_o,on=["nombre","fecha"],how="left")
        datos_horas = pd.merge(datos_horas,data_14_o,on=["nombre","fecha"],how="left")
    
    
        datos_horas = datos_horas.fillna(0)
    
    
        datos_horas["Total"] = (
            datos_horas["horas_produccion"]
            + datos_horas["horas_capacitacion"]
            + datos_horas["horas_otros_registros"]
        )
    
    
        placeholder19_7 = st.empty()
        placeholder19_7.dataframe(data=datos_horas)



    # ----- Resumen de Producción ---- #

    placeholder21_7 = st.empty()
    producción_7=placeholder21_7.subheader("Resumen de Producción")  

    data_2_r = data_1_r.groupby(["nombre", "fecha"], as_index=False)[["lotes","edificas","horas"]].agg(np.sum)

    data_4_r = data_1_r.groupby(["nombre", "semana","proceso"], as_index=False)[["edificas","unidades_catastrales","horas"]].agg(np.sum)

    if pivot_r==0:  

      placeholder22_7 = st.empty()
      error_producción= placeholder22_7.error('No existe producción para mostrar')

    else:

      data_2_r ["rendimiento"] = data_2_r["edificas"]/data_2_r["horas"]
      data_2_r['rendimiento'] *= 8.5 
      
      placeholder23_7 = st.empty()
      historial_7_producción= placeholder23_7.dataframe(data=data_2_r)

      data_4_r ["valor esperado"] = [340 if x == 'Precampo' else 510 if x == 'Control de Calidad Precampo' else 340 if x == 'Postcampo' else 765 if x == 'Control de Calidad Postcampo' else 0 for x in data_4_r['proceso']]    
      data_4_r ["diferencia"] = data_4_r["edificas"] - data_4_r["valor esperado"]

      placeholder23_2_7 = st.empty()
      historial_7_diferencia= placeholder23_2_7.subheader("Resumen Semanal")  
    
      placeholder24_2_7 = st.empty()
      descarga_7_diferencia= placeholder24_2_7.dataframe(data=data_4_r)


      #------Creando el dataframe de Resumen Calidad--------
      
      # Filtramos los datos antes del groupby
      data_filtrada = data_1_r[(data_1_r["tipo"] == "Inspección") & (data_1_r["operador_cc"].notna()) & (data_1_r["operador_cc"] != "N/A")]
      # Agrupamos los datos filtrados
      data_5_r = (data_filtrada.groupby(["operador_cc", "semana"], as_index=False)[["edificas", "aprobados", "rechazados"]].agg(np.sum))

      # Calculamos el porcentaje de aprobación
      data_5_r["porcentaje_aprobacion"] = ((data_5_r["aprobados"] / data_5_r["edificas"]) * 100).round(2).astype(str) + "%" 
                  
      placeholder25_2_7 = st.empty()
      titulo_resumen_calidad= placeholder25_2_7.subheader("Resumen Calidad")

      # Renombrar la columna 'edificas' por 'muestra' solo para visualización
      data_5_r_vista = data_5_r.rename(columns={"edificas": "muestra"})

      # Mostrar el DataFrame renombrado en Streamlit
      placeholder26_2_7 = st.empty()
      tabla_resumen_calidad = placeholder26_2_7.dataframe(data=data_5_r_vista)
    
      #-----Fin data frame Resumen Calidad-------
      
      
      nombre_producción=data_2_r.iloc[:,0]
      fecha_producción=data_2_r.iloc[:,1]
      rendimiento_producción=data_2_r.iloc[:,4]
      datos_producción = pd.DataFrame(data={'Nombre':nombre_producción, 'Fecha':fecha_producción,'Rendimiento':rendimiento_producción})
      lista_nombres = datos_producción["Nombre"].unique().tolist()

      placeholder25_7 = st.empty()
      nombres= placeholder25_7.multiselect("Seleccionar",lista_nombres)

      datos_producción_pivot = {nombre: datos_producción[datos_producción["Nombre"] == nombre] for nombre in nombres}
      fig_producción = go.Figure()
      for nombre, datos_producción in datos_producción_pivot.items():
        fig_producción = fig_producción.add_trace(go.Scatter(x=datos_producción["Fecha"], y=datos_producción["Rendimiento"], name=nombre))

      placeholder26_7 = st.empty()
      grafico_producción= placeholder26_7.plotly_chart(fig_producción)
      
    # ----- Total ---- #

    data_3_r= data_1_r.groupby(["fecha","proceso"], as_index=False)["edificas"].agg(np.sum)

    placeholder27_7 = st.empty()
    total_7=placeholder27_7.subheader("Totales")

    if pivot_r==0:
         
      placeholder28_7 = st.empty()
      error_total_producción= placeholder28_7.error('No existe producción para mostrar')

    else:
         
      fig_producción_total = px.bar(data_3_r, x="fecha", y="edificas", text="edificas", color="proceso", barmode="group")
      fig_producción_total.update_traces(textposition="outside")
      placeholder29_7 = st.empty()
      grafico_producción_total= placeholder29_7.plotly_chart(fig_producción_total)

    if pivot_r==0 or pivot_c==0 or pivot_o==0:
       
      placeholder30_7 = st.empty()
      error_horas_total = placeholder30_7.error('No existen horas para mostrar')

    else:
         
      fig_horas_total_1=px.bar(datos_horas,x="fecha", y=["horas_produccion","horas_capacitacion","horas_otros_registros"],barmode="group")
      placeholder31_7 = st.empty()
      grafico_horas_total_1= placeholder31_7.plotly_chart(fig_horas_total_1)
      
      fig_horas_total_2=px.bar(datos_horas,x="fecha", y=["horas_produccion","horas_capacitacion","horas_otros_registros"])

      placeholder32_7 = st.empty()
      grafico_horas_total_2 = placeholder32_7.plotly_chart(fig_horas_total_2)







  
  # ----- Operario Catastral y Profesional Jurídico ---- #

  elif puesto=="Operario Catastral" or puesto=="Entregas" or puesto=="QC" or puesto=="Profesional Jurídico":

    placeholder33_7 = st.empty()
    proceso_7_o = placeholder33_7.selectbox("Proceso", options=("Todos","Control de Calidad Folios de Matricula Inmobiliaria","Postcampo Control de Calidad FMI","Consultas de Campo","Postcampo Folios de Matricula Inmobiliaria","Folios de Matricula Inmobiliaria","Precampo", "Control de Calidad Precampo","Preparación de Insumos","Entregas Postcampo","Postcampo","Control de Calidad Postcampo","Restitución de Tierras","Revisión de Predios Segregados","Vinculación Precampo","Control de Calidad Vinculación Precampo"), key="proceso_7_s")
    
    placeholder34_7 = st.empty()
    tipo_7_o = placeholder34_7.selectbox("Tipo", options=("Todos","Ordinario","Corrección","Corrección Inspección","Correccion Primera Reinspección","Inspección","Reinspección","Primera Reinspección","Segunda Reinspección","Reproceso Inspección","Reproceso Primera Reinspección"), key="tipo_7_s")

    if proceso_7_o =="Todos" and tipo_7_o=="Todos":
        
      data_1_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      data_8_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and tipo not in ('Producción Horas Extras', 'Inspección Horas Extras','Reproceso Horas Extras')", con)
      data_6_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and tipo in ('Producción Horas Extras', 'Inspección Horas Extras','Reproceso Horas Extras')", con)


      #-----Para Resumen Calidad: importar la base completa sin filtro de usuario para jalar operador cc en la vista resumen
      data_5_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where operador_cc='{nombre_7}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      
      data_1_c = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,cast(horas as float),observaciones,reporte from capacitaciones where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)

      data_6_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo in ('Reposición de tiempo','Horas Extra','Horas Extra Apoyo Otros Proyectos','Horas Extras')", con)
      data_9_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo not in ('Reposición de tiempo','Horas Extra','Horas Extra Apoyo Otros Proyectos','Horas Extras')", con)
      data_7_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo = 'Reposición de tiempo' ", con)
      data_1_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)

    elif proceso_7_o =="Todos" and tipo_7_o!="Todos":
      
      data_1_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float)from registro where usuario='{usuario}' and tipo='{tipo_7_o}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      data_8_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and tipo not in ('Producción Horas Extras', 'Inspección Horas Extras','Reproceso Horas Extras')", con)
      data_6_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and tipo in ('Producción Horas Extras', 'Inspección Horas Extras','Reproceso Horas Extras')", con)

      #-----Para Resumen Calidad: importar la base completa sin filtro de usuario para jalar operador cc en la vista resumen
      data_5_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where operador_cc='{nombre_7}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      
      data_1_c = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,cast(horas as float),observaciones,reporte from capacitaciones where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)

      data_1_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      data_9_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo not in ('Reposición de tiempo','Horas Extra','Horas Extra Apoyo Otros Proyectos','Horas Extras')", con)
      data_7_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo = 'Reposición de tiempo' ", con)
      data_6_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo in ('Reposición de tiempo','Horas Extra','Horas Extra Apoyo Otros Proyectos','Horas Extras')", con)
      
    elif proceso_7_o !="Todos" and tipo_7_o=="Todos":
      
      data_1_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float)from registro where usuario='{usuario}' and proceso='{proceso_7_o}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      data_8_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and tipo not in ('Producción Horas Extras', 'Inspección Horas Extras','Reproceso Horas Extras')", con)
      data_6_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and tipo in ('Producción Horas Extras', 'Inspección Horas Extras','Reproceso Horas Extras')", con)

      #-----Para Resumen Calidad: importar la base completa sin filtro de usuario para jalar operador cc en la vista resumen
      data_5_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where operador_cc='{nombre_7}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      
      data_1_c = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,cast(horas as float),observaciones,reporte from capacitaciones where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)

      data_7_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo = 'Reposición de tiempo' ", con)
      data_9_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo not in ('Reposición de tiempo','Horas Extra','Horas Extra Apoyo Otros Proyectos','Horas Extras')", con)
      data_6_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo in ('Reposición de tiempo','Horas Extra','Horas Extra Apoyo Otros Proyectos','Horas Extras')", con)
      data_1_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)

    elif proceso_7_o !="Todos" and tipo_7_o!="Todos":
      
      data_1_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float)from registro where usuario='{usuario}' and proceso='{proceso_7_o}' and tipo='{tipo_7_o}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      data_8_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and tipo not in ('Producción Horas Extras', 'Inspección Horas Extras','Reproceso Horas Extras')", con)
      data_6_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and tipo in ('Producción Horas Extras', 'Inspección Horas Extras','Reproceso Horas Extras')", con)

      #-----Para Resumen Calidad: importar la base completa sin filtro de usuario para jalar operador cc en la vista resumen
      data_5_r=pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,proceso,fecha,semana,año,distrito, manzana, sector, cast(edificas as float), cast(unidades_catastrales as float), tipo,cast(lotes as float),cast(aprobados as float),cast(rechazados as float),operador_cc,tipo_de_errores,conteo_de_errores,numero_lote,observaciones,cast(horas as float) from registro where operador_cc='{nombre_7}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      
      data_1_c = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,tema,cast(horas as float),observaciones,reporte from capacitaciones where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)

      data_6_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo in ('Horas Extra','Horas Extra Apoyo Otros Proyectos','Horas Extras')", con)
      data_1_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}'", con)
      data_9_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo not in ('Reposición de tiempo','Horas Extra','Horas Extra Apoyo Otros Proyectos','Horas Extras')", con)
      data_7_o = pd.read_sql(f"select cast(id as integer),marca,usuario,nombre,puesto,supervisor,fecha,motivo,cast(horas as float),observaciones,reporte from otros_registros where usuario='{usuario}' and fecha>='{fecha_de__inicio_7}' and fecha<='{fecha_de__finalizacion_7}' and motivo = 'Reposición de tiempo' ", con)
    # ----- Reportes ---- #

    placeholder35_7 = st.empty()
    reportes_7=placeholder35_7.subheader("Reportes")   

    pivot_reportes=len(data_1_r.iloc[:,0])

    if pivot_reportes==0:
       
      placeholder36_7 = st.empty()
      error_reportes= placeholder36_7.error('No existen reportes para mostrar')

    else:

      placeholder37_7 = st.empty()
      historial_7_reportes=placeholder37_7.dataframe(data=data_1_r)

    #------Creando el dataframe de Resumen calidad 
    placeholder25_2_7 = st.empty()
    titulo_resumen_calidad= placeholder25_2_7.subheader("Resumen Calidad")  
    
    # Filtramos los datos antes del groupby
    data_filtrada_1 = data_5_r[(data_5_r["tipo"] == "Inspección")]
    # Agrupamos los datos filtrados
    data_5=(data_filtrada_1.groupby(["operador_cc", "semana"], as_index=False)[["edificas","unidades_catastrales", "aprobados", "rechazados"]].agg(np.sum))
       
    pivot_calidad=len(data_5.iloc[:,0])
    
    if pivot_calidad==0:
      placeholder55_7 = st.empty()
      error_reportes= placeholder55_7.error('No existen reportes para mostrar')
      
    else:
      data_5["porcentaje_aprobacion"] = ((data_5["aprobados"] / (data_5["edificas"]+data_5["unidades_catastrales"])) * 100).round(2).astype(str) + "%"         
   
      # Renombrar la columna 'edificas' por 'muestra' solo para visualización
      
      data_5_r_vista= data_5.rename(columns={"unidades_catastrales": "muestra unidades catastrales","edificas": "muestra edificas"})


      # Mostrar el DataFrame renombrado en Streamlit
      placeholder26_2_7 = st.empty()
      tabla_resumen_calidad = placeholder26_2_7.dataframe(data=data_5_r_vista)
      
    #-------fin del dataframe para resumen calidad-------
    
    
    # ----- Resumen de Horas ---- #

    placeholder39_7 = st.empty()
    horas_7=placeholder39_7.subheader("Resumen de Horas")  

    data_10_r = data_8_r.groupby(["nombre", "fecha"], as_index=False)[["horas"]].agg(np.sum)
    data_10_r.rename(columns={"horas":"horas_produccion"}, inplace=True)

    data_12_r = data_6_r.groupby(["nombre", "fecha"], as_index=False)[["horas"]].agg(np.sum)
    data_12_r.rename(columns={"horas":"horas_extra_produccion"}, inplace=True)
    
    data_2_c = data_1_c.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum)
    data_2_c.rename(columns={"horas":"horas_capacitacion"}, inplace=True)
    
    data_11_o = data_9_o.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum)
    data_11_o.rename(columns={"horas":"horas_otros_registros"}, inplace=True)

    data_13_o = data_6_o.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum)
    data_13_o.rename(columns={"horas":"horas_extra_otros_registros"}, inplace=True)

    data_14_o = data_7_o.groupby(["nombre", "fecha"], as_index=False)["horas"].agg(np.sum)
    data_14_o.rename(columns={"horas":"reposicion"}, inplace=True)
  
    pivot_r=len(data_10_r.iloc[:,0])
    pivot_re=len(data_12_r.iloc[:,0])
    pivot_c=len(data_2_c.iloc[:,0])
    pivot_o=len(data_11_o.iloc[:,0])
    
    if pivot_r==0 and pivot_c==0 and pivot_o==0 and pivot_re==0:
       
      placeholder40_7 = st.empty()
      error_horas= placeholder40_7.error('No existen horas para mostrar')

    else:
      
      datos_horas= pd.concat([data_10_r,data_12_r,data_2_c,data_11_o, data_13_o], axis=0)
    
      datos_horas = pd.DataFrame(data=datos_horas).groupby(["nombre","fecha"],as_index=False).size()

      datos_horas = pd.merge(datos_horas,data_10_r, on=['nombre','fecha'], how="left") 
      datos_horas = pd.merge(datos_horas,data_12_r, on=['nombre','fecha'], how="left") 
      datos_horas = pd.merge(datos_horas,data_2_c, on=['nombre','fecha'], how="left") 
      datos_horas = pd.merge(datos_horas,data_11_o, on=['nombre','fecha'], how="left") 
      datos_horas = pd.merge(datos_horas,data_13_o, on=['nombre','fecha'], how="left") 
      datos_horas = pd.merge(datos_horas,data_14_o, on=['nombre','fecha'], how="left")
      datos_horas= datos_horas.fillna(0)
      columnas = [
        "horas_produccion",
        "horas_capacitacion",
        "horas_otros_registros"
      ]
      for col in columnas:
        if col not in datos_horas.columns:
          datos_horas[col] = 0
      for col in columnas:
        datos_horas[col] = pd.to_numeric(datos_horas[col], errors="coerce")
        
      datos_horas["horas_produccion"] = pd.to_numeric(datos_horas["horas_produccion"], errors="coerce")
      datos_horas["horas_capacitacion"] = pd.to_numeric(datos_horas["horas_capacitacion"], errors="coerce")
      datos_horas["horas_otros_registros"] = pd.to_numeric(datos_horas["horas_otros_registros"], errors="coerce")
         
      datos_horas["Total"]= datos_horas["horas_produccion"] + datos_horas["horas_capacitacion"] + datos_horas["horas_otros_registros"]

      placeholder41_7 = st.empty()
      historial_7_horas= placeholder41_7.dataframe(data=datos_horas)

    # ----- Resumen de Producción ---- #

    placeholder43_7 = st.empty()
    producción_7=placeholder43_7.subheader(" ")  

    data_2_r = data_1_r.groupby(["nombre", "fecha"], as_index=False)[["lotes","edificas","horas"]].agg(np.sum)

    data_4_r = data_1_r.groupby(["nombre", "semana","proceso"], as_index=False)[["edificas","unidades_catastrales","horas"]].agg(np.sum)

    if pivot_r==0:  

      placeholder44_7 = st.empty()
      error_producción= placeholder44_7.error('No existe producción para mostrar')

    else:

      data_2_r ["rendimiento"] = data_2_r["edificas"]/data_2_r["horas"]
      data_2_r['rendimiento'] *= 8.5 
       
      placeholder45_7 = st.empty()
      producciónb_7=placeholder45_7.subheader(" ") 
      #historial_7_producción= placeholder45_7.dataframe(data=data_2_r)

      placeholder46_7 = st.empty()
      producción_7=placeholder46_7.subheader("Resumen de Producción por Proceso")

      data_4_r ["valor esperado"] = [8 if x == 'Precampo' else 10 if x == 'Control de Calidad Precampo' else 7 if x == 'Postcampo' else 10 if x == 'Control de Calidad Postcampo' else 8 if x == 'Vinculación Precampo' else 10  if x == 'Control de Calidad Vinculación Precampo' else 0 for x in data_4_r['proceso']]   
      data_4_r ["valor esperado"] = data_4_r ["valor esperado"]*data_4_r["horas"]
        
      data_4_r ["diferencia"] = data_4_r["edificas"]+data_4_r["unidades_catastrales"] - data_4_r["valor esperado"]

      data_4_r["ratio bruto"]= data_4_r["edificas"]+data_4_r["unidades_catastrales"]
      data_4_r["ratio bruto"]= data_4_r["ratio bruto"]/data_4_r["horas"]
      placeholder45_2_7 = st.empty()
      historial_7_diferencia= placeholder45_2_7.dataframe(data=data_4_r)
      
      placeholder46_2_7 = st.empty()
      descarga_7_diferencia = placeholder46_2_7.download_button("Decargar CSV",data=data_4_r.to_csv(),mime="text/csv",key="descarga_7_diferencia")
      
      nombre_producción=data_2_r.iloc[:,0]
      fecha_producción=data_2_r.iloc[:,1]
      rendimiento_producción=data_2_r.iloc[:,4]
      datos_producción = pd.DataFrame(data={'Nombre':nombre_producción, 'Fecha':fecha_producción,'Rendimiento':rendimiento_producción})
      lista_nombres = datos_producción["Nombre"].unique().tolist()

      placeholder47_7 = st.empty()
      nombres= placeholder47_7.multiselect("Seleccionar",lista_nombres)

      datos_producción_pivot = {nombre: datos_producción[datos_producción["Nombre"] == nombre] for nombre in nombres}
      fig_producción = go.Figure()
      for nombre, datos_producción in datos_producción_pivot.items():
        fig_producción = fig_producción.add_trace(go.Scatter(x=datos_producción["Fecha"], y=datos_producción["Rendimiento"], name=nombre))

      placeholder48_7 = st.empty()
      grafico_producción= placeholder48_7.plotly_chart(fig_producción)


    # ----- Total ---- #

    data_3_r= data_1_r.groupby(["fecha","proceso"], as_index=False)["edificas"].agg(np.sum)

    placeholder49_7 = st.empty()
    total_7=placeholder49_7.subheader("Totales")

    if pivot_r==0:
         
      placeholder50_7 = st.empty()
      error_total_producción= placeholder50_7.error('No existe producción para mostrar')

    else:
         
      fig_producción_total = px.bar(data_3_r, x="fecha", y="edificas", text="edificas", color="proceso", barmode="group")
      fig_producción_total.update_traces(textposition="outside")
      placeholder51_7 = st.empty()
      grafico_producción_total= placeholder51_7.plotly_chart(fig_producción_total)

    if pivot_r==0 or pivot_c==0 or pivot_o==0:
       
      placeholder52_7 = st.empty()
      error_horas_total = placeholder52_7.error('No existen horas para mostrar')

    else:
         
      fig_horas_total_1=px.bar(datos_horas,x="fecha", y=["horas_produccion","horas_capacitacion","horas_otros_registros"],barmode="group")
      placeholder53_7 = st.empty()
      grafico_horas_total_1= placeholder53_7.plotly_chart(fig_horas_total_1)
      
      fig_horas_total_2=px.bar(datos_horas,x="fecha", y=["horas_produccion","horas_capacitacion","horas_otros_registros"])

      placeholder54_7 = st.empty()
      grafico_horas_total_2 = placeholder54_7.plotly_chart(fig_horas_total_2)

  # ----- Proceso ---- #
  
  if procesos_7:
    placeholder1_7.empty()
    placeholder2_7.empty()
    placeholder3_7.empty()
    placeholder4_7.empty()
    placeholder5_7.empty()   
    placeholder6_7.empty()
    placeholder7_7.empty()
    placeholder8_7.empty()
    placeholder9_7.empty()
    
    if puesto=="Supervisor" or puesto=="Coordinador":  
      placeholder10_7.empty()
      placeholder11_7.empty()
      placeholder12_7.empty()
      placeholder13_7.empty()
      placeholder17_7.empty()
      placeholder21_7.empty()
      placeholder27_7.empty()
    
      if pivot_reportes==0:
        placeholder14_7.empty()
      
      else:
        placeholder15_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder18_7.empty()
        
      else:
        placeholder19_7.empty()

      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder30_7.empty()
        
      else: 
        placeholder31_7.empty()
        placeholder32_7.empty()
      
      if pivot_r==0:
        placeholder22_7.empty()
        placeholder28_7.empty()

      else:
        placeholder23_7.empty()
        placeholder23_2_7.empty()
        placeholder24_2_7.empty()
        placeholder25_2_7.empty()
        placeholder26_2_7.empty()
        placeholder25_7.empty()
        placeholder26_7.empty()
        placeholder29_7.empty()

    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico":
      placeholder33_7.empty()
      placeholder34_7.empty()
      placeholder35_7.empty()
      placeholder39_7.empty()
      placeholder43_7.empty()
      placeholder49_7.empty()
      placeholder25_2_7.empty()

      if pivot_calidad==0:
        placeholder55_7.empty()

      else:
        placeholder26_2_7.empty()

      if pivot_reportes==0:
        placeholder36_7.empty()
      
      else:
        placeholder37_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder40_7.empty()
        
      else:
        placeholder41_7.empty()

      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder52_7.empty()
        
      else: 
        placeholder53_7.empty()
        placeholder54_7.empty()
        
      if pivot_r==0:
        placeholder44_7.empty()
        placeholder50_7.empty()

      else:
        placeholder45_7.empty()
        placeholder46_7.empty()
        placeholder45_2_7.empty()
        placeholder46_2_7.empty()
        placeholder47_7.empty()
        placeholder48_7.empty()
        placeholder51_7.empty()

    st.session_state.Procesos=False
    st.session_state.Historial=False

    perfil=pd.read_sql(f"select perfil from usuarios where usuario ='{usuario}'",uri)
    perfil= perfil.loc[0,'perfil']

    if perfil=="1":        
                    
      Procesos.Procesos1(usuario,puesto)
                
    elif perfil=="2":        
                    
      Procesos.Procesos2(usuario,puesto)   

    elif perfil=="3":  

      Procesos.Procesos3(usuario,puesto)

  # ----- Capacitación ---- #
    
  elif capacitacion_7:
    placeholder1_7.empty()
    placeholder2_7.empty()
    placeholder3_7.empty()
    placeholder4_7.empty()
    placeholder5_7.empty()   
    placeholder6_7.empty()
    placeholder7_7.empty()
    placeholder8_7.empty()
    placeholder9_7.empty()
    
    if puesto=="Supervisor" or puesto=="Coordinador":  
      placeholder10_7.empty()
      placeholder11_7.empty()
      placeholder12_7.empty()
      placeholder13_7.empty()
      placeholder17_7.empty()
      placeholder21_7.empty()
      placeholder27_7.empty()
    
      if pivot_reportes==0:
        placeholder14_7.empty()
      
      else:
        placeholder15_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder18_7.empty()
        
      else:
        placeholder19_7.empty()

      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder30_7.empty()
        
      else: 
        placeholder31_7.empty()
        placeholder32_7.empty()
      
      if pivot_r==0:
        placeholder22_7.empty()
        placeholder28_7.empty()

      else:
        placeholder23_7.empty()
        placeholder23_2_7.empty()
        placeholder24_2_7.empty()
        placeholder25_2_7.empty()
        placeholder26_2_7.empty()
        placeholder25_7.empty()
        placeholder26_7.empty()
        placeholder29_7.empty()

    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico":
      placeholder33_7.empty()
      placeholder34_7.empty()
      placeholder35_7.empty()
      placeholder39_7.empty()
      placeholder43_7.empty()
      placeholder49_7.empty()
      placeholder25_2_7.empty()

      if pivot_calidad==0:
        placeholder55_7.empty()

      else:
        placeholder26_2_7.empty()


      if pivot_reportes==0:
        placeholder36_7.empty()
      
      else:
        placeholder37_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder40_7.empty()
        
      else:
        placeholder41_7.empty()
        
      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder52_7.empty()
        
      else: 
        placeholder53_7.empty()
        placeholder54_7.empty()
        
      if pivot_r==0:
        placeholder44_7.empty()
        placeholder50_7.empty()

      else:
        placeholder45_7.empty()
        placeholder46_7.empty()
        placeholder45_2_7.empty()
        placeholder46_2_7.empty()
        placeholder47_7.empty()
        placeholder48_7.empty()
        placeholder51_7.empty()
        
    st.session_state.Historial=False
    st.session_state.Capacitacion=True
    Capacitacion.Capacitacion(usuario,puesto)

  # ----- Otros Registros ---- #
    
  elif otros_registros_7:
    placeholder1_7.empty()
    placeholder2_7.empty()
    placeholder3_7.empty()
    placeholder4_7.empty()
    placeholder5_7.empty()   
    placeholder6_7.empty()
    placeholder7_7.empty()
    placeholder8_7.empty()
    placeholder9_7.empty()
    
    if puesto=="Supervisor" or puesto=="Coordinador":  
      placeholder10_7.empty()
      placeholder11_7.empty()
      placeholder12_7.empty()
      placeholder13_7.empty()
      placeholder17_7.empty()
      placeholder21_7.empty()
      placeholder27_7.empty()
    
      if pivot_reportes==0:
        placeholder14_7.empty()
      
      else:
        placeholder15_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder18_7.empty()
        
      else:
        placeholder19_7.empty()

      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder30_7.empty()
        
      else: 
        placeholder31_7.empty()
        placeholder32_7.empty()
      
      if pivot_r==0:
        placeholder22_7.empty()
        placeholder28_7.empty()

      else:
        placeholder23_7.empty()
        placeholder23_2_7.empty()
        placeholder24_2_7.empty()
        placeholder25_2_7.empty()
        placeholder26_2_7.empty()
        placeholder25_7.empty()
        placeholder26_7.empty()
        placeholder29_7.empty()

    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico":
      placeholder33_7.empty()
      placeholder34_7.empty()
      placeholder35_7.empty()
      placeholder39_7.empty()
      placeholder43_7.empty()
      placeholder49_7.empty()
      placeholder25_2_7.empty()

      if pivot_calidad==0:
        placeholder55_7.empty()

      else:
        placeholder26_2_7.empty()


      if pivot_reportes==0:
        placeholder36_7.empty()
      
      else:
        placeholder37_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder40_7.empty()
        
      else:
        placeholder41_7.empty()
    
      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder52_7.empty()
        
      else: 
        placeholder53_7.empty()
        placeholder54_7.empty()
        
      if pivot_r==0:
        placeholder44_7.empty()
        placeholder50_7.empty()

      else:
        placeholder45_7.empty()
        placeholder46_7.empty()
        placeholder45_2_7.empty()
        placeholder46_2_7.empty()
        placeholder47_7.empty()
        placeholder48_7.empty()
        placeholder51_7.empty()

    st.session_state.Historial=False
    st.session_state.Otros_Registros=True
    Otros_Registros.Otros_Registros(usuario,puesto)

  # ----- Bonos y Horas Extras ---- #
    
  elif bonos_extras_7:
    placeholder1_7.empty()
    placeholder2_7.empty()
    placeholder3_7.empty()
    placeholder4_7.empty()
    placeholder5_7.empty()   
    placeholder6_7.empty()
    placeholder7_7.empty()
    placeholder8_7.empty()
    placeholder9_7.empty()
    
    if puesto=="Supervisor" or puesto=="Coordinador":  
      placeholder10_7.empty()
      placeholder11_7.empty()
      placeholder12_7.empty()
      placeholder13_7.empty()
      placeholder17_7.empty()
      placeholder21_7.empty()
      placeholder27_7.empty()
    
      if pivot_reportes==0:
        placeholder14_7.empty()
      
      else:
        placeholder15_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder18_7.empty()
        
      else:
        placeholder19_7.empty()

      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder30_7.empty()
        
      else: 
        placeholder31_7.empty()
        placeholder32_7.empty()
      
      if pivot_r==0:
        placeholder22_7.empty()
        placeholder28_7.empty()

      else:
        placeholder23_7.empty()
        placeholder23_2_7.empty()
        placeholder24_2_7.empty()
        placeholder25_2_7.empty()
        placeholder26_2_7.empty()
        placeholder25_7.empty()
        placeholder26_7.empty()
        placeholder29_7.empty()

    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico":
      placeholder33_7.empty()
      placeholder34_7.empty()
      placeholder35_7.empty()
      placeholder39_7.empty()
      placeholder43_7.empty()
      placeholder49_7.empty()
      placeholder25_2_7.empty()

      if pivot_calidad==0:
        placeholder55_7.empty()

      else:
        placeholder26_2_7.empty()


      if pivot_reportes==0:
        placeholder36_7.empty()
      
      else:
        placeholder37_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder40_7.empty()
        
      else:
        placeholder41_7.empty()

      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder52_7.empty()
        
      else: 
        placeholder53_7.empty()
        placeholder54_7.empty()
        
      if pivot_r==0:
        placeholder44_7.empty()
        placeholder50_7.empty()

      else:
        placeholder45_7.empty()
        placeholder46_7.empty()
        placeholder45_2_7.empty()
        placeholder46_2_7.empty()
        placeholder47_7.empty()
        placeholder48_7.empty()
        placeholder51_7.empty()

    st.session_state.Historial=False
    st.session_state.Bonos_Extras=True
    Bonos_Extras.Bonos_Extras(usuario,puesto)
   
  # ----- Salir ---- #
    
  elif salir_7:
    placeholder1_7.empty()
    placeholder2_7.empty()
    placeholder3_7.empty()
    placeholder4_7.empty()
    placeholder5_7.empty()   
    placeholder6_7.empty()
    placeholder7_7.empty()
    placeholder8_7.empty()
    placeholder9_7.empty()
    
    if puesto=="Supervisor" or puesto=="Coordinador":  
      placeholder10_7.empty()
      placeholder11_7.empty()
      placeholder12_7.empty()
      placeholder13_7.empty()
      placeholder17_7.empty()
      placeholder21_7.empty()
      placeholder27_7.empty()
    
      if pivot_reportes==0:
        placeholder14_7.empty()
      
      else:
        placeholder15_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder18_7.empty()
        
      else:
        placeholder19_7.empty()

      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder30_7.empty()
        
      else: 
        placeholder31_7.empty()
        placeholder32_7.empty()
      
      
      if pivot_r==0:
        placeholder22_7.empty()
        placeholder28_7.empty()

      else:
        placeholder23_7.empty()
        placeholder23_2_7.empty()
        placeholder24_2_7.empty()
        placeholder25_2_7.empty()
        placeholder26_2_7.empty()
        placeholder25_7.empty()
        placeholder26_7.empty()
        placeholder29_7.empty()

    elif puesto=="Operario Catastral" or puesto=="Profesional Jurídico":
      placeholder33_7.empty()
      placeholder34_7.empty()
      placeholder35_7.empty()
      placeholder39_7.empty()
      placeholder43_7.empty()
      placeholder49_7.empty()
      placeholder25_2_7.empty()

      if pivot_calidad==0:
        placeholder55_7.empty()

      else:
        placeholder26_2_7.empty()


      if pivot_reportes==0:
        placeholder36_7.empty()
      
      else:
        placeholder37_7.empty()
         
      if pivot_r==0 and pivot_c==0 and pivot_o==0:
        placeholder40_7.empty()
        
      else:
        placeholder41_7.empty()

      if pivot_r==0 or pivot_c==0 or pivot_o==0:
        placeholder52_7.empty()
        
      else: 
        placeholder53_7.empty()
        placeholder54_7.empty()
        
      if pivot_r==0:
        placeholder44_7.empty()
        placeholder50_7.empty()

      else:
        placeholder45_7.empty()
        placeholder46_7.empty()
        placeholder45_2_7.empty()
        placeholder46_2_7.empty()
        placeholder47_7.empty()
        placeholder48_7.empty()
        placeholder51_7.empty()

    st.session_state.Ingreso = False
    st.session_state.Historial=False
    st.session_state.Salir=True
    Salir.Salir()
