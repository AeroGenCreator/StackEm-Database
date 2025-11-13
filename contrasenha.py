import json
import os

import streamlit as st

PATH = 'user_password.json'

def funcion_registro():
    try:
        user_registro = st.text_input(':orange[User Name]',key='new_user_name')
        user_registro = user_registro.lower().strip()
    except AttributeError:
        user_registro
    user_password = st.text_input(':orange[Password]', key='new_password')
    
    aceptar_registro = st.button('Confirm',key='aceptar_registro')


    if aceptar_registro:
        if user_registro == '' or user_password == '':
            st.info('Fill in both fields')
        else:
            try:
                
                if os.path.exists(PATH) and os.path.getsize(PATH) > 0:
                    
                    with open(PATH, 'r', encoding='utf-8') as r:
                        users = json.load(r)
                        if user_registro in users.keys():
                            st.write(f'The user name :red[{user_registro}] is already taken')
                            st.stop()
                        else:
                            users[user_registro] = user_password
                    
                    with open(PATH, 'w', encoding='utf-8') as rc:
                        json.dump(users, rc, indent=2, ensure_ascii=False)                        
                        bot = st.chat_message(name='assistant')
                        with bot:
                            st.write('You have signed up')
                        try:
                            user_registro = user_registro.title()
                            return user_registro
                        except AttributeError:
                            return user_registro
                
                else:
                    with open(PATH, 'w', encoding='utf-8') as c:
                        new_registro = {user_registro:user_password}
                        json.dump(new_registro, c, indent=2, ensure_ascii=False)
                        chat = st.chat_message(name='assistant')
                        with chat:
                            st.write('You have signed up')
                        try:
                            user_registro = user_registro.title()
                            return user_registro
                        except AttributeError:
                            return user_registro
            
            except FileExistsError:
                st.write('One file is missing, please contact the creator of this app')

def contrasenha():
    
    st.subheader('Access Your Account')
    try:
        user = st.text_input(':orange[Type your user name]')
        user = user.lower().strip()
    except AttributeError:
        user
    password = st.text_input(':orange[Type your password]')


    aceptar = st.toggle('Log in', key='entrar')
    if aceptar:
        if not len(user) and len(password) > 0:
            st.info('Fill in both fields')
        else:
            if os.path.exists(PATH) and os.path.getsize(PATH) > 0:
                with open(PATH, 'r', encoding='utf-8') as l:
                    log_in = json.load(l)
                        
                    try:
                            
                        if log_in[user] == password:
                            try:
                                user = user.title()
                                return user
                            except AttributeError:
                                return user
                            
                        else:
                            st.write(':red[Wrong user name or password]')

                    except KeyError:
                            st.write(':red[Wrong user name or password]')
            else:
                with open(PATH, 'w', encoding='utf-8') as creacion:
                    creacion_limpia_no_log_in = {}
                    json.dump(creacion_limpia_no_log_in, creacion, indent=2, ensure_ascii=False)
                st.write(':red[Wrong user name or password]')

    st.divider()
    st.write(':orange[Need An Account?]')
    registro = st.toggle('Sign Up', key='registro')
    if registro:
        user_en_registro = funcion_registro()        
        return user_en_registro