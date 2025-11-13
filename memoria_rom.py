"""Este codigo interactua en con archivos JSON"""
# Libreria local
import json
import os
# Libreria de terceros
import streamlit as st
import pandas as pd

FILE_PATH = 'base_de_datos.json'

def reset_memoria_rom(user):
    """Este bloque formatea la base de datos y agrega una
    lista vacia en json"""
    if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as new_file:
                full_data = json.load(new_file)
                if user in full_data.keys():
                    full_data.pop(user)
                    with open(FILE_PATH, 'w', encoding='utf-8') as new_file:
                        json.dump(full_data, new_file, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            st.write('Error al formatear la lista')

def agregar_al_room(diccionario: dict, user:str):
    """Aqui agrego a la base de datos permanente"""
    with open(FILE_PATH, 'r', encoding='utf-8') as lectura_1:
        data = json.load(lectura_1)
        if user in data.keys():
            agregacion = data[user]
            if  '' in agregacion['cancion'] and '' in agregacion['album']:
                agregacion['cancion'] = [diccionario['cancion']]
                agregacion['autor'] = [diccionario['autor']]
                agregacion['album'] = [diccionario['album']]
                agregacion['genero'] = diccionario['genero']
                agregacion['fecha'] = [diccionario['fecha']]
                agregacion['duracion'] = [diccionario['duracion']]
                agregacion['calificacion'] = [diccionario['calificacion']]
                with open(FILE_PATH, 'w', encoding='utf-8') as escritura:
                    for k in data.keys():
                        if k == user:
                            data[user] = agregacion
                    json.dump(data, escritura, indent=2, ensure_ascii = False)
                    return st.write('Pieza Agregada con Exito.')
            else:
                agregacion['cancion'].append(diccionario['cancion'])
                agregacion['autor'].append(diccionario['autor'])
                agregacion['album'].append(diccionario['album'])
                
                for genero in diccionario['genero']:
                    try:
                        genero = genero.title().strip()
                        agregacion['genero'].append(genero)
                    except AttributeError:
                        agregacion['genero'].append(genero)
                
                agregacion['fecha'].append(diccionario['fecha'])
                agregacion['duracion'].append(diccionario['duracion'])
                agregacion['calificacion'].append(diccionario['calificacion'])
                with open(FILE_PATH, 'w', encoding='utf-8') as escritura:
                    for k in data.keys():
                        if k == user:
                            data[user] = agregacion
                    json.dump(data, escritura, indent=2, ensure_ascii = False)
                    return
        else:
            st.write('Por alguna razon su usuario cambio, refresque la pagina e ingrese nuevamente.')

def acceso_a_rom(user:str):
    """De aqui se importa json a un DataFrame"""
    with open(FILE_PATH, 'r', encoding='utf-8') as file:
        data_json = json.load(file)
        data_user = data_json[user]
        df = pd.DataFrame(data = data_user)
        return df.sort_values(by='cancion', ascending=True).reset_index(drop=True)

def generos_unicos(user:str):
    with open(FILE_PATH, 'r', encoding='utf-8') as file:
        data_json = json.load(file)
        data_user = data_json[user]

        cache_1 = []
        for ind in data_user['genero']:
            for gen in ind:
                if not gen in cache_1:
                    cache_1.append(gen)
                else:
                    continue
        generos_list = sorted(cache_1)
        return sorted(generos_list)

def eliminar_en_dict(usuario: str, con1: str, con2: str):
    """Este codigo lee el JSON, elimina la entrada dada por el usuario
    y regresa una copia limpia SIN la entrada."""
    with open(FILE_PATH, 'r', encoding='utf-8') as r:
        gross_data = json.load(r)
        user_data = gross_data[usuario]

        index1 = user_data['cancion'].index(con1)
        index2 = user_data['autor'].index(con2)

        if index1 == index2:

            user_data['cancion'].pop(index1)
            user_data['autor'].pop(index1)
            user_data['album'].pop(index1)
            user_data['genero'].pop(index1)
            user_data['fecha'].pop(index1)
            user_data['duracion'].pop(index1)
            user_data['calificacion'].pop(index1)

            gross_data[usuario] = user_data
    
    with open(FILE_PATH, 'w', encoding='utf-8') as e:
        json.dump(gross_data, e, indent=2, ensure_ascii=False)
        return