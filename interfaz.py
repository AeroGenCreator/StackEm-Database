"""Este codigo muestra la interfaz de Usuario"""
import streamlit as st

# Modulos propios
import agregar_pieza
import memoria_rom
import buscar_pieza
import validacion
import contrasenha

# Titulos
st.title(':green[STACK\'EM]')

user_name = contrasenha.contrasenha()

if not user_name:
    st.divider()
else:
    validacion.validacion(user_name)

    # Agregar pieza
    ag1, ag2 = st.columns(2)
    with ag1:
        agregar = st.toggle(':green-background[ADD AN ENTRY]', key='agregar_registro')
    with ag2:
        st.image('agg_image.png', width=65)
    if agregar:
        pre_diccionario = agregar_pieza.formulario_agregar_pieza(user_name)
        if not isinstance(pre_diccionario, dict):
            st.info('⌨︎')
            st.stop()
        else:
            memoria_rom.agregar_al_room(pre_diccionario, user_name)
            with st.chat_message(name='assistant'):
                st.write(':green-background[NEW ENTRY SUCCESSFULLY SAVED]')
                st.info('_Please, close the form_')
                st.stop()

    # Buscar pieza
    st.divider()
    busqueda = st.toggle(':blue-background[>> SEARCH AN ENTRY]', key='busqueda_de_registros_menu')
    df = memoria_rom.acceso_a_rom(user_name)

    if busqueda:
        por_cancion = st.checkbox(':orange[-- BY TITLE ⌨︎]')
        if por_cancion:
            coincidencias_1 = buscar_pieza.buscar_cancion(user_name, df)
            st.dataframe(coincidencias_1)

        por_artista = st.checkbox(':orange[-- BY AUTHOR ⌨︎]')
        if por_artista:
            coincidencias_2 = buscar_pieza.buscar_autor(user_name, df)
            st.dataframe(coincidencias_2)

        por_genero = st.checkbox(':orange[-- BY GENRE ⌨︎]')
        if por_genero:
            coincidencias_3 = buscar_pieza.buscar_genero(user_name, df)
            st.dataframe(coincidencias_3)
            

    # Mostrar generos unicos de cada base de datos.
    mostrar_generos_unicos = st.toggle(':blue-background[>> LIST UNIQUE GENRES]', key='outer_menu')
    if mostrar_generos_unicos:
        lista = memoria_rom.generos_unicos(user_name)
        col1, col2 = st.columns(2)
        with col1:
            st.title(':green[GENRES]')
        with col2:
            st.dataframe(lista)

    # Toda la base de datos del usuario
    mostrar_base_completa = st.toggle(':blue-background[>> SEE ALL ENTRIES]', key='database_menu_dislpay')
    if mostrar_base_completa:
        st.title(':green[DATABASE] 🗃️')
        tabla = memoria_rom.acceso_a_rom(user_name)
        st.dataframe(tabla)

    # Eliminar un registro
    st.divider()
    eliminar_registro = st.checkbox('\tDELETE AN ENTRY')
    if eliminar_registro:
        st.subheader(':red[PLEASE FILL IN ALL THE FIELDS IN THE FORM]')
        dat1, dat2 = st.columns(2)
        with dat1:
            opciones_cancion = buscar_pieza.buscar_cancion_eliminar(user_name)
            opcion_formato1 = []
            for c in opciones_cancion:
                try:
                    c.title().strip()
                    opcion_formato1.append(c)
                except AttributeError:
                    opcion_formato1.append(c)
            seleccion_cancion = st.multiselect(
                key='eliminar_cancion',
                max_selections=1,
                options=opcion_formato1,
                label=':orange[TYPE A TITLE]'
            )
        with dat2:
            opciones_autor = buscar_pieza.buscar_autor_eliminar(user_name)
            opcion_formato2 = []
            for a in opciones_autor:
                try:
                    a.title().strip()
                    opcion_formato2.append(a)
                except AttributeError:
                    opcion_formato2.append(a)
            seleccion_autor = st.multiselect(
                key='eliminar_autor',
                max_selections=1,
                options=opcion_formato2,
                label=':orange[TYPE AN AUTHOR]'
            )

        if len(seleccion_cancion) and len(seleccion_autor) > 0:
            
            par1 = seleccion_cancion[0]
            par2 = seleccion_autor[0]

            df = memoria_rom.acceso_a_rom(user_name)
            pieza = df[(df['cancion'] == par1) & (df['autor'] == par2)]
            st.dataframe(pieza)
            eliminar = st.button(':red[DELETE]')
            if eliminar:
                datos_sin_registro = memoria_rom.eliminar_en_dict(user_name, par1, par2)
                with st.chat_message(name='assistant'):
                    st.write(':orange[ENTRY DELETED]')         
        else:
            st.warning('Fill in both fields to see the "cofirmation" button ', icon = 'ℹ️')

    # Formateo, todo este codigo maneja el borrado de disco
    st.divider()
    casilla_formatear = st.checkbox(':red-background[⚠️ Clear Database]')
    if casilla_formatear:
        st.subheader(':orange-badge[⚠️ This action can\'t be undone]')
        formateo = st.button(':red[_CLEAR DATABASE_]')
        if formateo:
            memoria_rom.reset_memoria_rom(user_name)
            st.chat_message("assistant")
            st.write('THE DATABASE WAS SUCCESSFULLY INITIALIZED ⚙️')
            st.write(':orange[Close This Menu]')
