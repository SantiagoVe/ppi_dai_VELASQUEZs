import streamlit as st
from firebase_admin import firestore

def app():
    # Verifica si 'db' no está en el estado de la sesión de Streamlit y lo inicializa
    if 'db' not in st.session_state:
        st.session_state.db = ''

    # Inicializa la conexión a Firestore
    db = firestore.client()
    st.session_state.db = db

    # Define el mensaje de placeholder según si el usuario ha iniciado sesión o no
    ph = ''
    if st.session_state.useremail == '':
        ph = '¡Ingresa para publicar tu casa!'
    else:
        ph = 'Publica tu vivienda'
    
    # Crea un área de texto para la nueva publicación
    post = st.text_area(label=':green[+ Nueva publicación]', placeholder=ph, height=None, max_chars=500)
    
    # Botón para publicar la publicación
    if st.button('Publicar', use_container_width=20):
        if post != '':
            # Obtiene la información de la colección 'Casas' para el usuario actual
            info = db.collection('Casas').document(st.session_state.username).get()
            if info.exists:
                info = info.to_dict()
                if 'Content' in info.keys():
                    # Actualiza la publicación existente con la nueva publicación
                    pos = db.collection('Casas').document(st.session_state.username)
                    pos.update({u'Content': firestore.ArrayUnion([u'{}'.format(post)])})
                else:
                    # Crea un nuevo documento con la publicación si no existe
                    data = {"Content": [post], 'Username': st.session_state.username}
                    db.collection('Casas').document(st.session_state.username).set(data)
            else:
                # Crea un nuevo documento con la publicación si no existe
                data = {"Content": [post], 'Username': st.session_state.username}
                db.collection('Casas').document(st.session_state.username).set(data)
                
            st.success('¡Vivienda publicada!')
    
    # Encabezado para mostrar las casas publicadas
    st.header(' :violet[Casas Publicadas]')
    
    # Obtiene todas las publicaciones de la colección 'Casas'
    docs = db.collection('Casas').get()
    
    # Muestra las publicaciones en un área de texto
    for doc in docs:
        d = doc.to_dict()
        try:
            st.text_area(label=':green[Publicada por:] ' + ':orange[{}]'.format(d['Username']), value=d['Content'][-1], height=20)
        except:
            pass
