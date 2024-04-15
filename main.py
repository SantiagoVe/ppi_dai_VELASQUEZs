import streamlit as st
from streamlit_option_menu import option_menu

import about, account, home, post

# Configuración de la página
st.set_page_config(
    page_title="Busca tu casa",
)

class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, function):
        """
        Agrega una aplicación a la lista de aplicaciones disponibles.

        Args:
            title (str): Título de la aplicación.
            function (function): Función que ejecuta la aplicación.
        """
        self.apps.append({
        "title": title,
        "function":  function
    })

    def run():
        """
        Ejecuta la aplicación multiaplicación.
        """

        with st.sidebar:
            # Menú de opciones para seleccionar la aplicación
            app = option_menu(
                menu_title='Busca tu casa ',
                options=['Inicio','Cuenta','Tus publicaciones','Acerca de'],
                icons=['house-fill','person-circle','trophy-fill','chat-fill','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab22"},}
                
                )

        # Ejecutar la aplicación correspondiente seleccionada en el menú
        if app == "Inicio":
            home.app()
        if app == "Cuenta":
            account.app()    
        if app == "Tus publicaciones":
            post.app()        
        if app == 'Acerca de':
            about.app()    
             
          
     # Crear una instancia de la clase MultiApp y ejecutar la aplicación        
    run()
