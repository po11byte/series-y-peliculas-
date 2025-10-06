import streamlit as st
import requests

st.set_page_config(page_title="Movie Ratings Explorer", layout="centered")
st.title(" Movie Ratings Explorer")
st.write("Busca calificaciones de películas usando Movies Ratings API")

API_KEY = "e398161a3emshc3d47f2cbb3353cp18748djsn927bb5a028be"
API_HOST = "movies-ratings2.p.rapidapi.com"
BASE_URL = "https://movies-ratings2.p.rapidapi.com/ratings"

def buscar_calificaciones(movie_id):
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    params = {
        "id": movie_id
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en la API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

with st.sidebar:
    st.header(" Configuración")
    st.info("Ingresa el ID de IMDb de la película (ej: tt0111161 para The Shawshank Redemption)")

busqueda = st.text_input(" Escribe el ID de IMDb de la película:")

col1, col2 = st.columns([1, 1])
with col1:
    buscar_btn = st.button(" Buscar Calificaciones", use_container_width=True)
with col2:
    if st.button(" Limpiar", use_container_width=True):
        st.rerun()

if buscar_btn:
    if not API_KEY or API_KEY == "tu_api_key_aqui":
        st.error(" **Configura tu API Key de RapidAPI**")
        st.info("Cómo obtener tu API Key:\n\n1. Ve a: https://rapidapi.com/\n2. Regístrate o inicia sesión\n3. Busca: 'Movies Ratings' en el marketplace\n4. Suscríbete al plan gratuito\n5. Copia tu API Key y pégala en el código")
        
    elif not busqueda:
        st.warning(" Por favor, escribe un ID de película")
        
    else:
        with st.spinner(" Buscando calificaciones..."):
            resultados = buscar_calificaciones(busqueda)
            
            if resultados:
                st.success(f" Calificaciones encontradas para ID: '{busqueda}'")
                
                if 'title' in resultados:
                    st.subheader(resultados['title'])
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if 'rating' in resultados:
                        st.metric(" Calificación", resultados['rating'])
                
                with col2:
                    if 'votes' in resultados:
                        st.metric(" Votos", resultados['votes'])
                
                with col3:
                    if 'year' in resultados:
                        st.metric(" Año", resultados['year'])
                
                st.markdown("---")
                
                if 'ratings' in resultados and resultados['ratings']:
                    st.subheader("Desglose de Calificaciones")
                    for rating in resultados['ratings']:
                        if 'source' in rating and 'value' in rating:
                            st.write(f"**{rating['source']}:** {rating['value']}")
                
                if 'metacritic' in resultados and resultados['metacritic']:
                    st.subheader("Críticas")
                    st.write(f"**Metacritic:** {resultados['metacritic']}")
                
            else:
                st.error(" No se encontraron calificaciones para este ID")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    " Movie Ratings Explorer - Powered by Movies Ratings API"
    "</div>", 
    unsafe_allow_html=True
)
