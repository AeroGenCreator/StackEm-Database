import json
import os
import streamlit as st

PATH = 'base_de_datos.json'
def validacion(user:str):
    """Este codigo valida usuarios en una base de datos"""
    
    if os.path.exists(PATH) and os.path.getsize(PATH) > 0:
        #primero debemos leer:
        with open(PATH, 'r', encoding='utf-8') as leer_file:
            dict_json = json.loads(leer_file.read())
            if user in dict_json.keys():
                st.title(f'Welcome Back :orange[{user}]')                    
                st.image('user.png', width=65, caption=f'{user}')
                st.badge("Your database has been loaded", icon=":material/check:", color="green")
                st.divider()
                return 
            else:
                with open(PATH, 'w', encoding='utf-8') as crear_user_file:
                    dict_json[user] = {
                        'cancion': [''],
                        'autor': [''],
                        'album': [''],
                        'genero': [''],
                        'fecha': [0],
                        'duracion': [0],
                        'calificacion': [0],
                        }
                    json.dump(dict_json, crear_user_file, indent=2, ensure_ascii=False)
                    st.subheader(f'User name :orange[{user}] has been created')
                    st.image('user.png', width=65, caption=f'{user}')
                    st.badge('Please log in', icon=':material/check:', color='orange')
                    st.divider()
                    return st.stop()
    else:
        with open(PATH, 'w', encoding='utf-8') as crear_file:
            clean_data = {
                user:{
                    'cancion': [''],
                    'autor': [''],
                    'album': [''],
                    'genero': [''],
                    'fecha': [0],
                    'duracion': [0],
                    'calificacion': [0],
                    }
                }
            json.dump(clean_data, crear_file, indent=2, ensure_ascii=False)
            st.subheader(f'User name :orange[{user}] has been created')
            st.image('user.png', width=65, caption=f'{user}')
            st.badge('Please log in', icon=':material/check:', color='orange')
            st.divider()
            return st.stop()
