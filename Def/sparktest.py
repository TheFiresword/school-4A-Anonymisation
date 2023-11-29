from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, DoubleType
from pyspark.sql import functions as F
from functions import *
import numpy as np
import names

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, StructType, StructField

LyonGps = (45.75, 4.85)
BordeauxGps = (44.837789, -0.57918)
ParisGps = (48.866667, 2.333333)
ToulouseGps = (43.6, 1.43)
Nbdiv = 100
echelle = 0.001
diametre = Nbdiv * echelle / 2
Lyon = CreationCarte(LyonGps[0], LyonGps[1], echelle, Nbdiv)
Bordeaux = CreationCarte(BordeauxGps[0], BordeauxGps[1], echelle, Nbdiv)
Paris = CreationCarte(ParisGps[0], ParisGps[1], echelle, Nbdiv)
Toulouse = CreationCarte(ToulouseGps[0], ToulouseGps[1], echelle, Nbdiv)

cartes = {
    (LyonGps, diametre): Lyon,
    (BordeauxGps, diametre): Bordeaux,
    (ParisGps, diametre): Paris,
    (ToulouseGps, diametre): Toulouse
}


# Création d'une session Spark
spark = SparkSession.builder.appName("Anonymisation").getOrCreate()

def anonymiser_donnees(lat, lont, cartes):
    for (gps, diametre), carte in cartes.items():
        if gps[0] - diametre / 2 <= lat <= gps[0] + diametre / 2 and gps[1] - diametre / 2 <= lont <= gps[1] + diametre / 2:
            for case, (min_lat, max_lat, min_lon, max_lon) in carte.items():
                if min_lat <= lat <= max_lat and min_lon <= lont <= max_lon:
                    milieu_lat = (min_lat + max_lat) / 2
                    milieu_lont = (min_lon + max_lon) / 2
                    return milieu_lat, milieu_lont
    return lat, lont

# Enregistrement de la fonction UDF pour une utilisation dans PySpark
anonymiser_udf = F.udf(anonymiser_donnees, StructType([
    StructField("lat", DoubleType(), True),
    StructField("lont", DoubleType(), True)
]))

# Lecture du DataFrame à partir d'un fichier CSV
df = spark.read.csv("../../User/sous_ensemble_98.csv", header=True, inferSchema=True)

# Application de la fonction anonymiser_donnees à chaque ligne du DataFrame
df_anonymise = df.withColumn("lat_lont", anonymiser_udf(col("lat"), col("lont"), F.lit(cartes)))

# Séparation de la structure en deux colonnes distinctes
df_anonymise = df_anonymise.withColumn("lat", col("lat_lont.lat")).withColumn("lont", col("lat_lont.lont")).drop("lat_lont")

# Gestion du bruit
noise_udf = F.udf(lambda x: x + np.random.uniform(-0.0001, 0.0001), DoubleType())
df_anonymise = df_anonymise.withColumn("lat", noise_udf("lat")).withColumn("lont", noise_udf("lont"))

# Gestion de la semaine
df_anonymise = df_anonymise.withColumn("week", F.weekofyear("date"))
df_anonymise = df_anonymise.drop("date")

# Gestion de l'id_x
df_anonymise = df_anonymise.withColumn("id_x", F.when(F.col("lat") != "DEL", names.get_first_name()))

# Continuer avec le reste du traitement...

# Affichage du DataFrame résultant
df_anonymise.show()

# Arrêt de la session Spark
spark.stop()
