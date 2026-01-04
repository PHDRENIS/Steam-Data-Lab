import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

#Info de la pestaña
st.set_page_config(page_title="Steam Data Lab", layout="wide", page_icon="🎮")


#Utilización del CSS para que se asemeje a la página de Steam
st.markdown("""
    <style>
    .stApp { background-color: #171a21; color: #c7d5e0; }
    [data-testid="stSidebar"] { background-color: #171a21; border-right: 1px solid #2a475e; }
    h1, h2, h3 { color: #ffffff !important; font-family: "Motiva Sans", Sans-serif; }
    p, label { color: #c7d5e0 !important; }
    .steam-card {
        background-color: #16202d;
        border: 1px solid #2a475e;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .steam-card:hover {
        transform: scale(1.02);
        background-color: #2a475e;
        border: 1px solid #66c0f4;
    }
    .price-tag {
        background-color: black;
        color: #c7d5e0;
        padding: 5px 10px;
        border-radius: 3px;
        font-weight: bold;
        float: right;
    }
    .stButton>button {
        background: linear-gradient(to bottom, #47bfff 5%, #1a44c2 100%);
        color: white;
        border: none;
        border-radius: 2px;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(to bottom, #66c0f4 5%, #47bfff 100%);
        color: white;
    }
    .stAlert { background-color: #1b2838; color: white; border: 1px solid #66c0f4; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

#Titulos de la página
st.markdown("# <span style='color:#66c0f4'>STEAM</span> DATA LAB", unsafe_allow_html=True)
st.markdown("Sistema recomendador de juegos de Steam utilizando IA y Big Data")

#Spark con memoria asignada
@st.cache_resource
def get_spark():
    return SparkSession.builder \
        .appName("SteamDataLab") \
        .config("spark.driver.memory", "4g") \
        .master("local[*]") \
        .getOrCreate()

spark = get_spark()

#Vectores para la similitud
@st.cache_resource
def load_vectors():
    path = "/home/jovyan/work/data/models/content_engine/vectors"
    if not os.path.exists(path):
        return None
    return spark.read.parquet(path).cache()

df_vectors = load_vectors()

#Iniciar sidebar de busqueda
st.sidebar.markdown("Recomiendame un juego")
st.sidebar.markdown("---")

#Optimización evitar repetir juegos y no saturar la RAM
@st.cache_data
def get_game_list():
    return df_vectors.select("app_name").distinct().sort("app_name").toPandas()["app_name"].tolist()

all_games = get_game_list()
total_juegos = len(all_games)

# diseño sidebar
st.markdown(f"""
<div style="background-color: #1b2838; padding: 10px; border-radius: 5px; border: 1px solid #000; display: inline-block;">
    <span style="color: #8f98a0;">Juegos disponibles:</span> 
    <span style="color: #66c0f4; font-weight: bold; font-size: 20px;">{total_juegos}</span>
</div>
<br><br>
""", unsafe_allow_html=True)

selected_game = st.sidebar.selectbox(
    "Selecciona un título:",
    all_games,
    index=None,
    placeholder="Escribe para buscar..."
)

#Lógica 
if st.sidebar.button("Encontrar juegos para ti UwU"):
    
    if not selected_game:
        st.sidebar.warning("Selecciona un juego para inciar la busqueda")
    else:
        with st.spinner(f"Buscando juegos para ti'{selected_game}'..."):
            
            #Encontrar el vector más cercano
            target_row = df_vectors.filter(df_vectors.app_name == selected_game).collect()
            
            if not target_row:
                st.error("Error encontrando el juego correcto")
            else:
                target_vector = target_row[0]['features']
                
                # Función de similitud
                def calculate_similarity(row):
                    # Producto punto de la similitud coseno
                    score = float(row.features.dot(target_vector))
                    return (row.app_name, row.genres, row.price, score)

                #10 Vectores mas cercanos
                similar_games = df_vectors.rdd \
                    .map(calculate_similarity) \
                    .takeOrdered(11, key=lambda x: -x[3]) 
                
                #Resultados
                st.markdown(f"Veo que te gusta: <span style='color:#66c0f4'>{selected_game}</span>, deberias de probar:", unsafe_allow_html=True)
                st.markdown("---")
                
                cols = st.columns(2)
                
                for i, (name, genres, price, score) in enumerate(similar_games):
                    if name == selected_game: continue
                    
                    match_percent = int(score * 100)
                    
                    #Colores
                    match_color = "#4c6b22" 
                    if match_percent > 85: match_color = "#a4d007" 
                    elif match_percent < 50: match_color = "#6c3c3c" 
                    
                    #Incluir precio cuidando formato
                    price_display = f"${price}" if price is not None else "N/A"
                    if price == 0: price_display = "Free"

                    card_html = f"""
                    <div class="steam-card">
                        <div style="display:flex; justify-content:space-between;">
                            <h4 style="color: #66c0f4; margin: 0; width: 75%;">{name}</h4>
                            <div class="price-tag">{price_display}</div>
                        </div>
                        <p style="font-size: 12px; color: #8f98a0; margin: 5px 0;">{genres}</p>
                        <div style="margin-top: 10px; font-size: 13px;">
                            Similitud: <span style="color:{match_color}; font-weight:bold;">{match_percent}%</span>
                        </div>
                    </div>
                    """
                    
                    with cols[i % 2]:
                        st.markdown(card_html, unsafe_allow_html=True)