# 🎮 Steam Data Lab

**Steam Data Lab** es un sistema de recoemdación de juegos que utiliza fundamentos de Big data asi como elementos de Inteligencia Artificial para recomendar videojuegos bbasados en la similitud para obtener entonces 10 juegos que se parezcan de manera significativa al juego que hayas seleccionado previamente en el sidebar previamente instalado utilizando la herramienta de **Apache Spark (PySpark)** para procesar masivamente datos y además cuenta con una interfaz grafica creada con **Streamlit** para la visualización de la aplicación web además de utilizar un truco de CSS para hacer que tenga similitud visual con Steam.

El sistema implementa un motor de recomendación híbrido que analiza:
1.  **Similitud de Contenido:** Géneros, desarrolladores y etiquetas de todos los juegos con el juego seleccionado.
2.  **Procesamiento de Lenguaje Natural (NLP):** Análisis de reseñas de usuarios para buscar similitud en las palabras utilizadas.
3.  **Comportamiento de Usuario:** Tiempos de juego promedio para asumir la similitud de los juegos en base al tiempo que los juegan los usuarios.

---

## Requisitos Previos

* [Docker](https://www.docker.com/) instalado debido a que el proyecto esta creado en Docker y esto es necesario para iniciar el proyecto
* Datasets de [Kaggle](https://www.kaggle.com/datasets/inogai/steam-data/data) Steam Bundle Recommendation Dataset que cuenta con los datos que se van a utilizar en este proyecto.

## Estructura de Carpetas

Esta es la estrucutra con la que cuentan las carpetas de este proyecto teniendo todo estructurado correctamente.

```text
proyecto-bigdata-steam/
├── data/
│   ├── raw/         
│   ├── processed/   
│   └── models/
├── src/
│   ├── ingestion.py    
│   ├── train_model.py   
│   └── dashboard.py     
├── docker-compose.yml
├── .gitignore
└── README.md

```
---

# Implementación del proyecto en tu propia computadora



