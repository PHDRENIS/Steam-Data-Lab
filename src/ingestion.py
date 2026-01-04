#Librerias utilizadas
import ast
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, concat_ws, avg, lit, when
from pyspark.sql.types import StringType, DoubleType
import os
import shutil

#Files
FILE_GAMES = "steam_games.json"
FILE_REVIEWS = "australian_user_reviews.json"
FILE_ITEMS = "australian_users_items.json"

def parse_python_lines(line):
    try:
        return ast.literal_eval(line)
    except:
        return None

def ingest_robust_final():
    print("Entrenando modelo")
    spark = SparkSession.builder \
        .appName("SteamRobustETL") \
        .config("spark.driver.memory", "8g") \
        .master("local[*]") \
        .getOrCreate()

    base_raw = "/home/jovyan/work/data/raw"
    base_processed = "/home/jovyan/work/data/processed"
    
    sc = spark.sparkContext

    #Procesamiento del catalogo de juegos
    print(f"\n🎮 1. Procesando Catálogo (Modo Robusto)...")
    path_games_raw = f"{base_raw}/{FILE_GAMES}"
    path_games_out = f"{base_processed}/store_clean"

    # Verificación de nombres
    if not os.path.exists(path_games_raw):
        if os.path.exists(f"{base_raw}/output_steam_games.json"):
            path_games_raw = f"{base_raw}/output_steam_games.json"
            print(f"Dataset cargado con exito ")
        else:
            print(f"No se encuentra el archivo{base_raw}")
            return

    try:
        #Busqueda de archivos
        rdd_games = sc.textFile(path_games_raw).map(parse_python_lines).filter(lambda x: x is not None)
        df_games_raw = spark.createDataFrame(rdd_games)

        #Selección de columnas que se van a utilizar en el entrenamiento
        df_games = df_games_raw.select(
            col("id"),
            col("app_name"),
            col("developer"),
            col("genres"),
            col("price")
        )
        
        #Conversión de generos a String y limpieza de datos nulos
        df_games = df_games.withColumn("genres_str", concat_ws(" ", col("genres"))) \
                           .drop("genres") \
                           .withColumnRenamed("genres_str", "genres") \
                           .fillna({"developer": "Unknown Studio", "app_name": "Unknown Game"}) \
                           .dropna(subset=["id"])

        # Guardamos
        df_games.write.mode("overwrite").parquet(path_games_out)
        print(f"Juegos cargados correctamente")

    except Exception as e:
        print(f"Error al procesar los juegos{e}")

    #Procesamiento de las reseñas 
    print(f"\nCargando reseñas")
    path_reviews_raw = f"{base_raw}/{FILE_REVIEWS}"
    path_reviews_out = f"{base_processed}/user_reviews_clean"

    if os.path.exists(path_reviews_out):
        print("Se omiten las celdar con redundancia")
    else:
        try:
            rdd_reviews = sc.textFile(path_reviews_raw).map(parse_python_lines).filter(lambda x: x is not None)
            df_reviews_raw = spark.createDataFrame(rdd_reviews)
            df_exploded = df_reviews_raw.select(col("user_id"), explode("reviews").alias("review_data"))
            df_reviews_clean = df_exploded.select(
                col("review_data.item_id").alias("item_id"),
                col("review_data.review").alias("review")
            )
            df_reviews_clean.write.mode("overwrite").parquet(path_reviews_out)
            print(f"Procesamiento de las reseñas completado")
        except Exception as e: print(f"Error al procesar las reseñas{e}")

    #Preprocesamiento tiempo jugado
    print(f"\nProcesando el tiempo jugado")
    path_items_raw = f"{base_raw}/{FILE_ITEMS}"
    path_items_out = f"{base_processed}/users_items_clean"

    if os.path.exists(path_items_out):
        print("Omitiendo celdas redundantes")
    else:
        try:
            rdd_items = sc.textFile(path_items_raw).map(parse_python_lines).filter(lambda x: x is not None)
            df_items_raw = spark.createDataFrame(rdd_items)
            df_items_exploded = df_items_raw.select(explode("items").alias("item_data"))
            df_items_clean = df_items_exploded.select(
                col("item_data.item_id").alias("item_id"),
                col("item_data.playtime_forever").alias("playtime_forever")
            )
            df_items_clean = df_items_clean.withColumn("playtime_forever", col("playtime_forever").cast(DoubleType()))
            df_items_agg = df_items_clean.groupBy("item_id").agg(avg("playtime_forever").alias("playtime_forever"))
            df_items_agg.write.mode("overwrite").parquet(path_items_out)
            print(f"Tiempo procesado")
        except Exception as e: print(f"Error al procesar el tiempo{e}")

    print("\nProcesamiento terminado con exito")
    spark.stop()

if __name__ == "__main__":
    ingest_robust_final()