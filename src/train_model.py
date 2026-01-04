from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, collect_list, avg, lower, regexp_replace, lit
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, Normalizer, VectorAssembler, MinMaxScaler
from pyspark.ml import Pipeline
import os
import shutil

def train_final_model():
  
    # Iniciamos Spark
    spark = SparkSession.builder \
        .appName("SteamHybridEngine") \
        .config("spark.driver.memory", "6g") \
        .master("local[*]") \
        .getOrCreate()

    # Rutas de entrada y salida
    base_processed = "/home/jovyan/work/data/processed"
    model_path = "/home/jovyan/work/data/models/content_engine"

    #Limpiar modelos por si se cambia el entrenamiento
    if os.path.exists(model_path):
        shutil.rmtree(model_path)

    #Cargar dataset
    df_games = spark.read.parquet(f"{base_processed}/store_clean")
    
    #Cargar las reseñas procesadas
    if os.path.exists(f"{base_processed}/user_reviews_clean"):
        df_reviews = spark.read.parquet(f"{base_processed}/user_reviews_clean")
        #Aqui concatenamos las reseñas del mismo juego
        reviews_grouped = df_reviews.groupBy("item_id") \
            .agg(concat_ws(" ", collect_list("review")).alias("merged_reviews"))
    else:
        #Por si no se encuentran reseñas
        reviews_grouped = df_games.select(col("id").alias("item_id"), lit("").alias("merged_reviews"))

    #Cargando el tiempo
    if os.path.exists(f"{base_processed}/users_items_clean"):
        df_items = spark.read.parquet(f"{base_processed}/users_items_clean")
        playtime_grouped = df_items.groupBy("item_id") \
            .agg(avg("playtime_forever").alias("avg_playtime"))
    else:
        playtime_grouped = df_games.select(col("id").alias("item_id"), lit(0.0).alias("avg_playtime"))

    #Unimos las secciones utilizando el ID del juego
    df_master = df_games.join(reviews_grouped, df_games.id == reviews_grouped.item_id, "left") \
                        .join(playtime_grouped, df_games.id == playtime_grouped.item_id, "left") \
                        .fillna({"merged_reviews": "", "avg_playtime": 0, "developer": "Unknown"})

    #Juntar todo bao el ID
    df_master = df_master.withColumn("text_context", 
                                     concat_ws(" ", 
                                               col("app_name"), 
                                               col("genres"), 
                                               col("developer"),
                                               col("merged_reviews")))
    
    # Limpieza de texto
    df_master = df_master.withColumn("text_clean", lower(regexp_replace("text_context", "[^a-zA-Z\\s]", "")))

    print(f"Juegos a procesar: {df_master.count()}")

    # Procesamiento del texto
    tokenizer = Tokenizer(inputCol="text_clean", outputCol="words")
    remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
    hashingTF = HashingTF(inputCol="filtered_words", outputCol="raw_tf", numFeatures=3000)
    idf = IDF(inputCol="raw_tf", outputCol="text_vector")
    normalizer_text = Normalizer(inputCol="text_vector", outputCol="text_vec_norm", p=2.0)

    #Procesamiento numerico para el tiempo
    assembler_num = VectorAssembler(inputCols=["avg_playtime"], outputCol="playtime_vec")
    scaler = MinMaxScaler(inputCol="playtime_vec", outputCol="playtime_scaled")

    #Ensamblar todo finalmente
    final_assembler = VectorAssembler(
        inputCols=["text_vec_norm", "playtime_scaled"], 
        outputCol="features"
    )

    pipeline = Pipeline(stages=[
        tokenizer, remover, hashingTF, idf, normalizer_text, 
        assembler_num, scaler, final_assembler
    ])

    #Entrenar y guardar el modelo
    model = pipeline.fit(df_master)
    df_vectorized = model.transform(df_master)

    #Columnas a utilizar en el dashboar
    df_final = df_vectorized.select("id", "app_name", "genres", "price", "avg_playtime", "features")

    print("Guardando vectores generados")
    df_final.write.mode("overwrite").parquet(f"{model_path}/vectors")
    
    print("Modelo entrenado con exito")
    spark.stop()

if __name__ == "__main__":
    train_final_model()