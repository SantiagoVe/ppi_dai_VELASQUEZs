import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests

# Inicialización de la aplicación Firebase si no está ya inicializada
if not firebase_admin._apps:
    cred = credentials.Certificate('buscatucasa-e7c9b-02f9170710da.json')
    firebase_admin.initialize_app(cred)

def app():
    # Verifica si 'username' y 'useremail' no están en el estado de la sesión de Streamlit y los inicializa
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    # Función para registrarse con correo y contraseña
    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyA0DsD_K93jFsctURRIBG6D5mdePqhd8Sc"}, data=payload)
            try:
                return r.json()['email']
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')
    
    # Función para iniciar sesión con correo y contraseña
    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyA0DsD_K93jFsctURRIBG6D5mdePqhd8Sc"}, data=payload)
            try:
                data = r.json()
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName')  # Retrieve username if available
                }
                return user_info
            except:
                st.warning(data)
        except Exception as e:
            st.warning(f'Signin failed: {e}')


    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyA0DsD_K93jFsctURRIBG6D5mdePqhd8Sc"}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                # Handle error response
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)

    # Example usage
    # email = "example@example.com"
    
    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
            "email": email,
            "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyA0DsD_K93jFsctURRIBG6D5mdePqhd8Sc"}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                # Manejar la respuesta de error
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)

    # Función para realizar el inicio de sesión
    def f():
        try:
            # user = auth.get_user_by_email(email)
            # print(user.uid)
            # st.session_state.username = user.uid
            # st.session_state.useremail = user.email

            userinfo = sign_in_with_email_and_password(st.session_state.email_input,st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']

            
            global Usernm
            Usernm=(userinfo['username'])
            
            st.session_state.signedout = True
            st.session_state.signout = True    
  
            
        except: 
            st.warning('Login Failed')
    # Función para cerrar sesión
    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

    # Función para restablecer la contraseña
    def forget():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            print(email)
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {message}") 

    # Verificación del estado de sesión para mostrar el formulario de inicio de sesión o registro
    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    

    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup',['Login','Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password',type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password


        

        
        if choice == 'Sign up':
            username = st.text_input("Enter  your unique username")
            
            if st.button('Create my account'):
                # user = auth.create_user(email = email, password = password,uid=username)
                user = sign_up_with_email_and_password(email=email,password=password,username=username)
                
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
            # st.button('Login', on_click=f)          
            st.button('Login', on_click=f)
            # if st.button('Forget'):
            forget()
            # st.button('Forget',on_click=forget

            # Si se ha iniciado sesión, se muestra el nombre de usuario y correo electrónico con la opción de cerrar sesión
        if st.session_state.signout:
                st.text('Name '+st.session_state.username)
                st.text('Email id: '+st.session_state.useremail)
                st.button('Sign out', on_click=t)

        # Definición de la función 'ap'
        def ap():
            st.write('Casas')
