import streamlit as st
from streamlit_option_menu import option_menu

import about, account, home, houses

st.set_page_config(
    page_title="Busca tu casa",
)

class MultiApp:
    def __init__(self):
        self.apps = []
    def add_app(self, title, function):
        self.apps.append({
        "title": title,
        "function":  function
    })

    def run():

        with st.sidebar:
            app = option_menu(
                menu_title='Busca tu casa ',
                options=['Home','Account','Houses','about'],
                icons=['house-fill','person-circle','trophy-fill','chat-fill','info-circle-fill'],
                menu_icon='chat-text-fill',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'black'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        
        if app == "Home":
            home.app()
        if app == "Account":
            account.app()    
        if app == "Houses":
            houses.app()        
        if app == 'about':
            about.app()    
             
          
             
    run()