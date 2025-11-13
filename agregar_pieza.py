"""Agregar una cancion, memoria RAM"""
# Mis modulos
import memoria_rom
# Librerias integradas
import datetime as dt
# Libreria de terceros
import streamlit as st
import streamlit_tags as tg

def formulario_agregar_pieza(user:str):
    """Esta funcion muestra la interfaz de formulario
    y opera con los inputs para almacenarlos en un diccionario
    en RAM"""
    diccionario_cache = {
        'cancion': '',
        'autor': '',
        'album': '',
        'genero': '',
        'fecha': 0,
        'duracion': 0,
        'calificacion': 0,
    }

    # Codigo de la interfaz
    st.title(':green[FORM:]')

    # Elementos de texto:
    cancion_de_usuario = st.text_input(':blue-background[TYPE A TITLE]').title().strip()
    autor_de_usuario = st.text_input(':blue-background[TYPE AN AUTHOR]').title().strip()
    album_de_usuario = st.text_input(':blue-background[TYPE AN ALBUM]').title().strip()

    # Ingreso de generos por medio de Tags, los cuales se almacenan como una lista simple.
    opcion_genero = memoria_rom.generos_unicos(user=user)
    genero_de_usuario = tg.st_tags(
        key='generos_tags',
        suggestions=opcion_genero,
        label=':blue-background[TYPE GENRES]',
        text='Enter Para Agregar'
        )
    genero_de_usuario_con_formato = []
    for genre in genero_de_usuario:
        try:
            genre = genre.title().strip()
            genero_de_usuario_con_formato.append(genre)
        except AttributeError:
            genero_de_usuario_con_formato.append(genre)

    # Mostrar generos unicos de cada base de datos.
    mostrar_generos_unicos = st.toggle(':gray-background[LIST UNIQUE GENRES]', key='inner_menu')
    if mostrar_generos_unicos:
        lista = memoria_rom.generos_unicos(user)
        col1, col2 = st.columns(2)
        with col1:
            st.header(':orange[GENRES]')
        with col2:
            st.dataframe(lista)

    # Elementos numericos:
    fecha_de_usuario = st.number_input(
        ':blue-background[TYPE THE YEAR OF RELEASE (EXAMPLE: 2003)]',
        min_value=0000,
        step=1,
        format='%d')
    col1, col2 = st.columns(2)
    with col1:
        minutos_de_usuario = st.number_input(
            ':blue-background[TYPE THE MINUTES]',
            min_value=0,
            max_value=59,
            step=1,
            format='%d',
            key='registro_de_minutos'
        )
    with col2:
        segundos_de_usuario = st.number_input(
            ':blue-background[TYPE THE SECONDS]',
            min_value=0,
            max_value=59,
            step=1,
            format='%d',
            key='registro_de_segundos'
        )
    duracion_timedelta = dt.timedelta(
        minutes=minutos_de_usuario, seconds=segundos_de_usuario)
    calificacion_de_usuario = st.number_input(
        ':blue-background[TYPE A RATING (EXAMPLE: 8.7)]',
        min_value=0.0,
        max_value=10.0,
        step=0.1,
        format='%.1f')

    # Aqui mando la data a un diccionario limpio.
    diccionario_cache['cancion'] = cancion_de_usuario
    diccionario_cache['autor'] = autor_de_usuario
    diccionario_cache['album'] = album_de_usuario
    diccionario_cache['genero'] = []
    diccionario_cache['genero'].append(genero_de_usuario_con_formato)
    diccionario_cache['fecha'] = fecha_de_usuario
    diccionario_cache['duracion'] = str(duracion_timedelta)[2:]
    diccionario_cache['calificacion'] = calificacion_de_usuario

    st.dataframe(diccionario_cache)

    if len(cancion_de_usuario) and len(autor_de_usuario) and len(album_de_usuario) and len(genero_de_usuario)  > 0 and minutos_de_usuario and fecha_de_usuario and calificacion_de_usuario > 0:
        aceptar_nueva_pieza = st.button(':green[CONFIRM NEW ENTRY]')
        if aceptar_nueva_pieza:
            return diccionario_cache
    else:
        st.info('FILL IN ALL THE FIELDS IN THE FORM', icon='ℹ️')
