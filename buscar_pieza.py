"""Este codigo buscara por cancion, album, genero, año, u artista."""

#librerias de python
import json
# Mis modulos
import memoria_rom
# librerias de terceros
import pandas as pd
import streamlit as st

def buscar_cancion(user:str, df):
    """Interfaz y logica de busqueda"""
    with open(memoria_rom.FILE_PATH, 'r',encoding='utf-8') as r_file:
        
        gross_data = json.load(r_file)
        user_data = gross_data[user]
        
        cancion_cache = []
        for song in user_data['cancion']:
            if not song in cancion_cache:
                cancion_cache.append(song)
            else:
                continue
        selecciones = st.multiselect(
            key='cancion_search',
            accept_new_options=False,
            options=cancion_cache,
            label='TITLES'
        )

        df_selections = df[df['cancion'].isin(selecciones)]
        return df_selections

def buscar_autor(user:str, df):
    """Interfaz y logica de busqueda"""
    with open(memoria_rom.FILE_PATH, 'r',encoding='utf-8') as r_file:
        
        gross_data = json.load(r_file)
        user_data = gross_data[user]
        
        autor_cache = []
        for autor in user_data['autor']:
            if not autor in autor_cache:
                autor_cache.append(autor)
            else:
                continue
        selecciones = st.multiselect(
            key='autor_search',
            accept_new_options=False,
            options=autor_cache,
            label='AUTHORS'
        )

        df_selections = df[df['autor'].isin(selecciones)]
        return df_selections

def buscar_genero(user:str, df):
    """Interfaz y logica de busqueda"""
    with open(memoria_rom.FILE_PATH, 'r',encoding='utf-8') as r_file:
        
        gross_data = json.load(r_file)
        user_data = gross_data[user]
        
        genero_cache = []
        for ind in user_data['genero']:
            for gen in ind:
                if not gen in genero_cache:
                    genero_cache.append(gen)
                else:
                    continue
        selecciones = st.multiselect(
            key='genero_search',
            accept_new_options=False,
            options=genero_cache,
            label='GENRES'
        )

        mascara = df['genero'].apply(lambda x: any(g in selecciones for g in x))
        df_selections = df[mascara]
        return df_selections
    
def buscar_cancion_eliminar(user:str):
    with open(memoria_rom.FILE_PATH, 'r',encoding='utf-8') as r_file:
        
        gross_data = json.load(r_file)
        user_data = gross_data[user]
        
        cancion_cache = []
        for song in user_data['cancion']:
            if not song in cancion_cache:
                cancion_cache.append(song)
            else:
                continue
        return cancion_cache
    
def buscar_autor_eliminar(user:str):
    with open(memoria_rom.FILE_PATH, 'r',encoding='utf-8') as r_file:
        
        gross_data = json.load(r_file)
        user_data = gross_data[user]
        
        autor_cache = []
        for autor in user_data['autor']:
            if not autor in autor_cache:
                autor_cache.append(autor)
            else:
                continue
        return autor_cache