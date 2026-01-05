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

**Clonación del Github**
Primeramente se debe de clonar el repositorio del siguiente [Github](https://github.com/PHDRENIS/Steam-Data-Lab/tree/main) que es el que se va a utilizar para poder inciar el proyecto.

**Descarga de los datos**
Despues de tener ya el repositorio clonado se tiene que entrar al link de Kaggle ya que estos son los que se utilizaran para el entrenammiento del programa específicamente tomaremos los archivos de:

1. **steam_games.json**
2. **australian_user_reviews.json**
3. **australian_users_items.json**

Debes tener estos datos cargados dentro de la carpeta **data/raw/** se ponden dentro los archivos que se indican para le correcto funcionamiento del proyecto

**Iniciar el Docker**
Una vez que se haya clonado el repositorio y se tengan los datos agregados en las carpetas correctas es necesario inicializar el proyecto en Docker utilizando los siguientes comando para iniciar el Docker.

1. **Linux** sudo docker run -it -p 8888:8888 -p 8501:8501 -v "$(pwd)":/home/jovyan/work jupyter/pyspark-notebook

2. **Windows** docker run -it -p 8888:8888 -p 8501:8501 -v ${PWD}:/home/jovyan/work jupyter/pyspark-notebook

Para iniciar el proyecto debes de ingrear al siguiente link del Jupyter notebook que se acaba de iniciar en el link: http://localhost:8888/lab

**Confuración del entrono**
Primeramente se debe de instalar las librerias que se tienen que utilizar para el funcionamiento del proyecto los cuales se encuentran en el archivo de requeriments.txt por lo que es necesario que se utilice el comando que instale las librerias del documento las cuales se instalan con el comando:

**pip install -r requirements.txt**

Al instalar la libraria anterior el entorno para que el proyecto funcione de manera correcta estara completo

**Implementación del pipeline del proyecto**

1. **Limpieza de los datos** 
Primeramente se deben de limpiar los datos que se van a utilizar para el proyecto lo que se hace con el programa que creamos previamente por lo que es necesario que ejecutemos este codigo para que los datos se preprocesen de manera correcta por lo que ejecutamos el comando:

**python src/ingestion.py**

Una vez que se haya implementado el codigo los datos se habran procesado correctamente

2. **Entrenamiento del modelo**
Posteriormente se debe de utilizar el código que creamos para entrenar el modelo de predicción del proyecto lo que pemitira que el sistema funcione correctamente utilizando este comando para ejecutar el codigo:

|   **python src/train_model.py**

3. **Lanzamiento de la app**

Finalmente se debe de inicializar la aplicación que nos enseñara la interfaz gráfica de la aplicación la cual utiliza streamlit para la visualización de la misma además de que utiliza un truco de CSS para que esta interfaz se parezca visualmente a la interfaz de Steam, para iniciarlo es necesario ejecutar el siguiente comando:

**streamlit run src/dashboard.py --server.port 8501 --server.address 0.0.0.0 --browser.serverAddress localhost**

Finalmente con la inicialización de estas se puede visualizar esta aplicación en la entrada del servidor

http://localhost:8501/

Listo se puede visualizar el proyecto montado correctamente