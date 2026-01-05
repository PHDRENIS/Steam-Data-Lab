# 🎮 Steam Data Lab

**Steam Data Lab** es un sistema de recomendación de videojuegos "Big Data" que utiliza **Apache Spark (PySpark)** para procesar masivamente datos y **Streamlit** para la visualización.

El sistema implementa un motor de recomendación híbrido que analiza:
1.  **Similitud de Contenido:** Géneros, desarrolladores y etiquetas.
2.  **Procesamiento de Lenguaje Natural (NLP):** Análisis de reseñas de usuarios.
3.  **Comportamiento de Usuario:** Tiempos de juego promedio.

---

## 🚀 Requisitos Previos

* [Docker](https://www.docker.com/) instalado.
* Datasets de Kaggle (Steam Reviews).

## 📂 Estructura de Carpetas

Asegúrate de colocar los archivos de datos en la carpeta correcta antes de iniciar:

```text
proyecto-bigdata-steam/
├── src/
│   ├── data/
│   │   ├── raw/          <-- AQUÍ van tus JSONs de Kaggle
│   │   ├── processed/    <-- Aquí se guardan los parquets limpios
│   │   └── models/       <-- Aquí se guardan los vectores entrenados
│   ├── ingestion.py      # Script de limpieza (ETL)
│   ├── train_model.py    # Script de entrenamiento (Machine Learning)
│   └── dashboard.py      # Aplicación Web (Streamlit)
└── README.md