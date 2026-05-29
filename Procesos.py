# ----- Librerías ---- #
import streamlit as st
import time

# Importaciones de módulos
import Historial, Capacitacion, Otros_Registros, Correcciones, Bonos_Extras, Salir
import Precampo_Juridico, Descarga_Partidas_Juridico, Asignacion_Partidas, CC_Precampo_Juridico
import Consulta_Campo, Restitucion_Tierras, Revision_Segregados, Estado_UIT_Hito
import Precampo, CC_Precampo, Preparacion_Insumos, Entregas_Postcampo, Postcampo, CC_Postcampo
import CC_Vinculacion_Precampo, Vinculacion_Precampo

# ------------------- CONTADOR PARA REFRESCAR PÁGINA ------------------- #
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if time.time() - st.session_state.start_time > 29 * 60:
    st.session_state.clear()
    st.rerun()

def auto_refresh(seconds=30600):
    st.markdown(
        f'<meta http-equiv="refresh" content="{seconds}">',
        unsafe_allow_html=True
    )

auto_refresh(30600)
# --------------------------------------------------------------------- #

def limpiar_sidebar_y_contenido(placeholder_list):
    """Vacía todos los placeholders proporcionados."""
    for ph in placeholder_list:
        if ph is not None:
            ph.empty()

def navegar_a(modulo_func, usuario, puesto, flag_name):
    """Establece flags de estado y llama al módulo correspondiente."""
    st.session_state.Procesos = True
    # Activar solo la bandera del módulo destino
    for key in ["Historial", "Capacitacion", "Otros_Registros", "Bonos_Extras",
                "Correcciones", "Precampo_Juridico", "Descarga_Partidas_Juridico",
                "CC_Precampo_Juridico", "Asignacion_Partidas", "Precampo", "CC_Precampo",
                "Vinculacion_Precampo", "Preparacion_Insumos", "Entregas_Postcampo",
                "Postcampo", "CC_Postcampo", "CC_Vinculacion_Precampo",
                "Restitucion_Tierras", "Revision_Segregados", "Estado_UIT_Hito"]:
        st.session_state[key] = (key == flag_name)
    modulo_func(usuario, puesto)

def menu_principal_por_perfil(usuario, puesto, perfil):
    """
    Muestra el menú de procesos usando selectboxes por categoría.
    Todos los elementos usan placeholders para limpieza completa.
    """
    # Inicializar estado si no existe
    if "Procesos" not in st.session_state:
        st.session_state.Procesos = False

    # Si ya estamos dentro de un submódulo
    if st.session_state.Procesos:
        return True

    # --- Placeholders del Sidebar ---
    placeholders_sidebar = []
    
    ph_titulo = st.sidebar.empty()
    ph_titulo.title("Menú")
    placeholders_sidebar.append(ph_titulo)

    btn_historial = st.sidebar.empty()
    btn_capacitacion = st.sidebar.empty()
    btn_otros = st.sidebar.empty()
    btn_bonos = st.sidebar.empty()
    btn_correcciones = st.sidebar.empty()
    btn_salir = st.sidebar.empty()
    
    placeholders_sidebar.extend([btn_historial, btn_capacitacion, btn_otros, 
                                  btn_bonos, btn_correcciones, btn_salir])

    # --- Placeholders del contenido principal ---
    ph_main = []
    titulo_procesos = st.empty()
    ph_main.append(titulo_procesos)
    titulo_procesos.title("Procesos")

    # --- Configuración de módulos por perfil ---
    modulos_config = {
        "1": {  # Perfil completo
            "⚖️ Área Jurídica": {
                "Precampo Jurídico": ("Precampo_Juridico", ":orange[Precampo Jurídico]", Precampo_Juridico.Precampo_Juridico),
                "Descarga Partidas Jurídico": ("Descarga_Partidas_Juridico", ":orange[Descarga Partidas Jurídico]", Descarga_Partidas_Juridico.Descarga_Partidas_Juridico),
                "Control de Calidad Precampo Jurídico": ("CC_Precampo_Juridico", ":orange[Control de Calidad Precampo Jurídico]", CC_Precampo_Juridico.CC_Precampo_Juridico),
                "Asignación de Partidas": ("Asignacion_Partidas", ":orange[Asignación de Partidas]", Asignacion_Partidas.Asignacion_Partidas),
            },
            "🌱 Precampo": {
                "Precampo": ("Precampo", ":green[Precampo]", Precampo.Precampo),
                "Control de Calidad Precampo": ("CC_Precampo", ":green[Control de Calidad Precampo]", CC_Precampo.CC_Precampo),
                "Vinculación Precampo": ("Vinculacion_Precampo", ":green[Vinculación Precampo]", Vinculacion_Precampo.Vinculacion_Precampo),
                "Control de Calidad Vinculación": ("CC_Vinculacion_Precampo", ":green[Control de Calidad Vinculación Precampo]", CC_Vinculacion_Precampo.CC_Vinculacion_Precampo),
            },
            "📦 Postcampo": {
                "Entregas Postcampo": ("Entregas_Postcampo", ":blue[Entregas Postcampo]", Entregas_Postcampo.Entregas_Postcampo),
                "Postcampo": ("Postcampo", ":blue[Postcampo]", Postcampo.Postcampo),
                "Control de Calidad Postcampo": ("CC_Postcampo", ":blue[Control de Calidad Postcampo]", CC_Postcampo.CC_Postcampo),
            }
        },
        "2": {  # Gabinete
            "🌱 Precampo": {
                "Precampo": ("Precampo", "Precampo", Precampo.Precampo),
                "Control de Calidad Precampo": ("CC_Precampo", "Control de Calidad Precampo", CC_Precampo.CC_Precampo),
                "Vinculación Precampo": ("Vinculacion_Precampo", "Vinculación Precampo", Vinculacion_Precampo.Vinculacion_Precampo),
                "Control de Calidad Vinculación": ("CC_Vinculacion_Precampo", "Control de Calidad Vinculación Precampo", CC_Vinculacion_Precampo.CC_Vinculacion_Precampo),
            },
            "📦 Postcampo": {
                "Entregas Postcampo": ("Entregas_Postcampo", "Entregas Postcampo", Entregas_Postcampo.Entregas_Postcampo),
                "Postcampo": ("Postcampo", "Postcampo", Postcampo.Postcampo),
                "Control de Calidad Postcampo": ("CC_Postcampo", "Control de Calidad Postcampo", CC_Postcampo.CC_Postcampo),
            }
        },
        "3": {  # Jurídicos
            "⚖️ Área Jurídica": {
                "Precampo Jurídico": ("Precampo_Juridico", "Precampo Jurídico", Precampo_Juridico.Precampo_Juridico),
                "Descarga Partidas Jurídico": ("Descarga_Partidas_Juridico", "Descarga Partidas Jurídico", Descarga_Partidas_Juridico.Descarga_Partidas_Juridico),
                "Control de Calidad Precampo Jurídico": ("CC_Precampo_Juridico", "Control de Calidad Precampo Jurídico", CC_Precampo_Juridico.CC_Precampo_Juridico),
                "Asignación de Partidas": ("Asignacion_Partidas", "Asignación de Partidas", Asignacion_Partidas.Asignacion_Partidas),
            }
        }
    }

    # --- Lista para almacenar todos los placeholders creados ---
    placeholders_contenido = []

    # --- Mostrar selectboxes por categoría ---
    categorias = modulos_config.get(perfil, {})
    
    for categoria, modulos in categorias.items():
        # Título de categoría
        ph_categoria = st.empty()
        ph_categoria.markdown(f"### {categoria}")
        placeholders_contenido.append(ph_categoria)
        
        # Selectbox para la categoría
        ph_select = st.empty()
        opciones = list(modulos.keys())
        seleccion = ph_select.selectbox(f"Seleccionar módulo", [""] + opciones, key=f"select_{categoria}")
        placeholders_contenido.append(ph_select)
        
        # Botón para ejecutar
        ph_boton = st.empty()
        if seleccion and seleccion != "":
            if ph_boton.button(f"▶️ Ir a {seleccion}", key=f"btn_{categoria}_{seleccion}", use_container_width=True):
                flag_name, texto, modulo_func = modulos[seleccion]
                if modulo_func:
                    limpiar_sidebar_y_contenido(placeholders_sidebar + ph_main + placeholders_contenido)
                    navegar_a(modulo_func, usuario, puesto, flag_name)
                    return True
        placeholders_contenido.append(ph_boton)
        
        # Separador entre categorías
        ph_sep = st.empty()
        ph_sep.markdown("---")
        placeholders_contenido.append(ph_sep)

    # --- Botones comunes del sidebar ---
    if btn_historial.button("Historial", key="historial_2"):
        limpiar_sidebar_y_contenido(placeholders_sidebar + ph_main + placeholders_contenido)
        navegar_a(Historial.Historial, usuario, puesto, "Historial")
        return True
    
    if btn_capacitacion.button("Capacitaciones", key="capacitacion_2"):
        limpiar_sidebar_y_contenido(placeholders_sidebar + ph_main + placeholders_contenido)
        navegar_a(Capacitacion.Capacitacion, usuario, puesto, "Capacitacion")
        return True
    
    if btn_otros.button("Otros Registros", key="otros_registros_2"):
        limpiar_sidebar_y_contenido(placeholders_sidebar + ph_main + placeholders_contenido)
        navegar_a(Otros_Registros.Otros_Registros, usuario, puesto, "Otros_Registros")
        return True
    
    if btn_bonos.button("Bonos y Horas Extras", key="bonos_extras_2"):
        limpiar_sidebar_y_contenido(placeholders_sidebar + ph_main + placeholders_contenido)
        navegar_a(Bonos_Extras.Bonos_Extras, usuario, puesto, "Bonos_Extras")
        return True
    
    if btn_correcciones.button("Solicitud Correcciones", key="correcciones"):
        limpiar_sidebar_y_contenido(placeholders_sidebar + ph_main + placeholders_contenido)
        navegar_a(Correcciones.Correcciones, usuario, puesto, "Correcciones")
        return True
    
    if btn_salir.button("Salir", key="salir_2"):
        limpiar_sidebar_y_contenido(placeholders_sidebar + ph_main + placeholders_contenido)
        st.session_state.Ingreso = False
        st.session_state.Procesos = True
        st.session_state.Salir = True
        Salir.Salir()
        return True

    return False

# ------------------- FUNCIONES PÚBLICAS ------------------- #

def Procesos1(usuario, puesto):
    st.session_state.Ingreso = True
    if st.session_state.get("Procesos"):
        if st.session_state.get("Historial"):
            Historial.Historial(usuario, puesto)
        elif st.session_state.get("Capacitacion"):
            Capacitacion.Capacitacion(usuario, puesto)
        elif st.session_state.get("Otros_Registros"):
            Otros_Registros.Otros_Registros(usuario, puesto)
        elif st.session_state.get("Bonos_Extras"):
            Bonos_Extras.Bonos_Extras(usuario, puesto)
        elif st.session_state.get("Correcciones"):
            Correcciones.Correcciones(usuario, puesto)
        elif st.session_state.get("Precampo_Juridico"):
            Precampo_Juridico.Precampo_Juridico(usuario, puesto)
        elif st.session_state.get("Descarga_Partidas_Juridico"):
            Descarga_Partidas_Juridico.Descarga_Partidas_Juridico(usuario, puesto)
        elif st.session_state.get("CC_Precampo_Juridico"):
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario, puesto)
        elif st.session_state.get("Asignacion_Partidas"):
            Asignacion_Partidas.Asignacion_Partidas(usuario, puesto)
        elif st.session_state.get("Precampo"):
            Precampo.Precampo(usuario, puesto)
        elif st.session_state.get("CC_Precampo"):
            CC_Precampo.CC_Precampo(usuario, puesto)
        elif st.session_state.get("Vinculacion_Precampo"):
            Vinculacion_Precampo.Vinculacion_Precampo(usuario, puesto)
        elif st.session_state.get("Preparacion_Insumos"):
            Preparacion_Insumos.Preparacion_Insumos(usuario, puesto)
        elif st.session_state.get("Entregas_Postcampo"):
            Entregas_Postcampo.Entregas_Postcampo(usuario, puesto)
        elif st.session_state.get("Postcampo"):
            Postcampo.Postcampo(usuario, puesto)
        elif st.session_state.get("CC_Postcampo"):
            CC_Postcampo.CC_Postcampo(usuario, puesto)
        elif st.session_state.get("CC_Vinculacion_Precampo"):
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario, puesto)
        elif st.session_state.get("Estado_UIT_Hito"):
            Estado_UIT_Hito.Estado_UIT_Hito(usuario, puesto)
        else:
            st.session_state.Procesos = False
            menu_principal_por_perfil(usuario, puesto, "1")
    else:
        menu_principal_por_perfil(usuario, puesto, "1")

def Procesos2(usuario, puesto):
    st.session_state.Ingreso = True
    if st.session_state.get("Procesos"):
        if st.session_state.get("Historial"):
            Historial.Historial(usuario, puesto)
        elif st.session_state.get("Capacitacion"):
            Capacitacion.Capacitacion(usuario, puesto)
        elif st.session_state.get("Otros_Registros"):
            Otros_Registros.Otros_Registros(usuario, puesto)
        elif st.session_state.get("Bonos_Extras"):
            Bonos_Extras.Bonos_Extras(usuario, puesto)
        elif st.session_state.get("Correcciones"):
            Correcciones.Correcciones(usuario, puesto)
        elif st.session_state.get("Precampo"):
            Precampo.Precampo(usuario, puesto)
        elif st.session_state.get("CC_Precampo"):
            CC_Precampo.CC_Precampo(usuario, puesto)
        elif st.session_state.get("Vinculacion_Precampo"):
            Vinculacion_Precampo.Vinculacion_Precampo(usuario, puesto)
        elif st.session_state.get("Entregas_Postcampo"):
            Entregas_Postcampo.Entregas_Postcampo(usuario, puesto)
        elif st.session_state.get("Postcampo"):
            Postcampo.Postcampo(usuario, puesto)
        elif st.session_state.get("CC_Postcampo"):
            CC_Postcampo.CC_Postcampo(usuario, puesto)
        elif st.session_state.get("CC_Vinculacion_Precampo"):
            CC_Vinculacion_Precampo.CC_Vinculacion_Precampo(usuario, puesto)
        else:
            st.session_state.Procesos = False
            menu_principal_por_perfil(usuario, puesto, "2")
    else:
        menu_principal_por_perfil(usuario, puesto, "2")

def Procesos3(usuario, puesto):
    st.session_state.Ingreso = True
    if st.session_state.get("Procesos"):
        if st.session_state.get("Historial"):
            Historial.Historial(usuario, puesto)
        elif st.session_state.get("Capacitacion"):
            Capacitacion.Capacitacion(usuario, puesto)
        elif st.session_state.get("Otros_Registros"):
            Otros_Registros.Otros_Registros(usuario, puesto)
        elif st.session_state.get("Bonos_Extras"):
            Bonos_Extras.Bonos_Extras(usuario, puesto)
        elif st.session_state.get("Correcciones"):
            Correcciones.Correcciones(usuario, puesto)
        elif st.session_state.get("Precampo_Juridico"):
            Precampo_Juridico.Precampo_Juridico(usuario, puesto)
        elif st.session_state.get("Descarga_Partidas_Juridico"):
            Descarga_Partidas_Juridico.Descarga_Partidas_Juridico(usuario, puesto)
        elif st.session_state.get("CC_Precampo_Juridico"):
            CC_Precampo_Juridico.CC_Precampo_Juridico(usuario, puesto)
        elif st.session_state.get("Asignacion_Partidas"):
            Asignacion_Partidas.Asignacion_Partidas(usuario, puesto)
        else:
            st.session_state.Procesos = False
            menu_principal_por_perfil(usuario, puesto, "3")
    else:
        menu_principal_por_perfil(usuario, puesto, "3")
