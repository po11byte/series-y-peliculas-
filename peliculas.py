import streamlit as st
import requests

st.set_page_config(page_title="Movie Explorer", layout="centered")
st.title(" Movie Explorer")
st.write("Busca información sobre películas y actores usando IMDb API")

#
API_KEY = "e398161a3emshc3d47f2cbb3353cp18748djsn927bb5a028be"  
API_HOST = "imdb236.p.rapidapi.com"
BASE_URL = "https://imdb236.p.rapidapi.com/api/imdb"

def buscar_peliculas(tipo, query):
    """Buscar películas en IMDb API"""
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    try:
        if tipo == "actor":
            
            url = f"{BASE_URL}/cast/{query}/titles"
            response = requests.get(url, headers=headers, timeout=10)
        elif tipo == "pelicula":
          
            url = f"{BASE_URL}/search"
            params = {"q": query}
            response = requests.get(url, headers=headers, params=params, timeout=10)
        else:  
            url = f"{BASE_URL}/search"
            params = {"q": query, "type": "director"}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en la API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

def obtener_id_actor(nombre_actor):
    """Obtener el ID de actor basado en el nombre"""
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    try:
        url = f"{BASE_URL}/search"
        params = {"q": nombre_actor, "type": "actor"}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return data[0].get('id', '')
        return None
    except:
        return None

def mostrar_imagen_pelicula(imagen_url, width=150):
    """Muestra imágenes de películas de manera segura"""
    if imagen_url and imagen_url.startswith('http'):
        try:
            st.image(imagen_url, width=width)
        except:
            st.image("https://via.placeholder.com/150x225/333333/FFFFFF?text=", width=width)
    else:
        st.image("https://via.placeholder.com/150x225/333333/FFFFFF?text=", width=width)


with st.sidebar:
    st.header(" Configuración")
    tipo_busqueda = st.selectbox(
        "Tipo de búsqueda:",
        ["Películas", "Actor", "Director"]
    )
    
    if tipo_busqueda == "Películas":
        metodo = "pelicula"
    elif tipo_busqueda == "Actor":
        metodo = "actor"
    else:
        metodo = "director"


busqueda = st.text_input(" Escribe el nombre de la película, actor o director:")

col1, col2 = st.columns([1, 1])
with col1:
    buscar_btn = st.button("🎭 Buscar Películas", use_container_width=True)
with col2:
    if st.button(" Limpiar", use_container_width=True):
        st.rerun()

if buscar_btn:
    if not API_KEY or API_KEY == "e398161a3emshc3d47f2cbb3353cp18748djsn927bb5a028be":
        st.error(" **Configura tu API Key de RapidAPI**")
        st.info("""
        ** Cómo obtener tu API Key:**
        
        1.  **Ve a:** https://rapidapi.com/
        2.  **Regístrate o inicia sesión**
        3.  **Busca:** "IMDb236" en el marketplace
        4.  **Suscríbete** al plan gratuito
        5.  **Copia tu API Key** y pégala en el código
        """)
        
    elif not busqueda:
        st.warning(" Por favor, escribe algo para buscar")
        
    else:
        with st.spinner(f" Buscando {tipo_busqueda.lower()}..."):
            if metodo == "actor":
                
                with st.spinner("Obteniendo ID del actor..."):
                    actor_id = obtener_id_actor(busqueda)
                    if actor_id:
                        resultados = buscar_peliculas(metodo, actor_id)
                    else:
                        st.error("No se pudo encontrar el ID del actor")
                        resultados = None
            else:
                resultados = buscar_peliculas(metodo, busqueda)
            
            if resultados:
                st.success(f" Encontrados resultados para: '{busqueda}'")
                
                if metodo == "actor":
                   
                    if isinstance(resultados, list) and len(resultados) > 0:
                        st.subheader(f" Filmografía de {busqueda}")
                        for pelicula in resultados:
                            with st.container():
                                col1, col2 = st.columns([1, 3])
                                with col1:
                                    mostrar_imagen_pelicula(pelicula.get('image', ''))
                                with col2:
                                    st.subheader(pelicula.get('title', 'Título no disponible'))
                                    if pelicula.get('year'):
                                        st.write(f"**Año:** {pelicula['year']}")
                                    if pelicula.get('role'):
                                        st.write(f"**Rol:** {pelicula['role']}")
                                    if pelicula.get('imdbRating'):
                                        st.write(f"**Rating IMDb:**  {pelicula['imdbRating']}")
                                st.markdown("---")
                    else:
                        st.warning(f"No se encontró filmografía para: '{busqueda}'")
                
                elif metodo == "pelicula":
                  
                    if isinstance(resultados, list) and len(resultados) > 0:
                        st.subheader(f" Resultados para: '{busqueda}'")
                        for pelicula in resultados:
                            with st.container():
                                col1, col2 = st.columns([1, 3])
                                with col1:
                                    mostrar_imagen_pelicula(pelicula.get('image', ''))
                                with col2:
                                    st.subheader(pelicula.get('title', 'Título no disponible'))
                                    if pelicula.get('year'):
                                        st.write(f"**Año:** {pelicula['year']}")
                                    if pelicula.get('director'):
                                        st.write(f"**Director:** {pelicula['director']}")
                                    if pelicula.get('cast'):
                                        st.write(f"**Reparto:** {', '.join(pelicula['cast'][:3])}...")
                                    if pelicula.get('imdbRating'):
                                        st.write(f"**Rating IMDb:**  {pelicula['imdbRating']}")
                                st.markdown("---")
                    else:
                        st.warning(f"No se encontraron películas para: '{busqueda}'")
                
                else:  
                    if isinstance(resultados, list) and len(resultados) > 0:
                        st.subheader(f" Películas dirigidas por: '{busqueda}'")
                        for pelicula in resultados:
                            with st.container():
                                col1, col2 = st.columns([1, 3])
                                with col1:
                                    mostrar_imagen_pelicula(pelicula.get('image', ''))
                                with col2:
                                    st.subheader(pelicula.get('title', 'Título no disponible'))
                                    if pelicula.get('year'):
                                        st.write(f"**Año:** {pelicula['year']}")
                                    if pelicula.get('genre'):
                                        st.write(f"**Género:** {pelicula['genre']}")
                                    if pelicula.get('imdbRating'):
                                        st.write(f"**Rating IMDb:**  {pelicula['imdbRating']}")
                                st.markdown("---")
                    else:
                        st.warning(f"No se encontraron películas del director: '{busqueda}'")
            else:
                st.error(" Error al conectar con IMDb API")


st.markdown("---")
