from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame

# cleaning functions


def clean_n_bedrooms(df: DataFrame) -> DataFrame:
    return df.withColumn("n_bedrooms", F.col("n_bedrooms").cast("int"))


def clean_n_bathrooms(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "n_bathrooms",
        F.when(F.col("n_bathrooms") == "7+", "7")
        .otherwise(F.col("n_bathrooms"))
        .cast("int"),
    )


def clean_total_area(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "total_area",
        F.regexp_replace(
            F.when(F.col("total_area") == "m²", None).otherwise(F.col("total_area")),
            " m²",
            "",
        ).cast("int"),
    )


def clean_price(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "price",
        F.when(F.col("price") == "Prix non spécifié", None).otherwise(
            F.regexp_replace(F.col("price"), "(\u202f| |DH$)", "").cast("int")
        ),
    )


def clean_attributes_n_living_rooms(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "n_living_room",
        F.when(F.col("attributes.Salons") == "+7", "7")
        .otherwise(F.col("attributes.Salons"))
        .cast("int"),
    )


def clean_attributes_floor_number(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "floor_number",
        F.when(F.col("attributes.Étage") == "Rez de chaussée", "0")
        .when(F.col("attributes.Étage") == "+7", "7")
        .otherwise(F.col("attributes.Étage"))
        .cast("int"),
    )


def clean_attributes_living_area(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "living_area", F.col("attributes.Surface habitable").cast("int")
    )


def clean_attributes_syndicate_price(df: DataFrame) -> DataFrame:
    return df.withColumn(
        "syndicate_price_per_month",
        F.col("attributes.Frais de syndic / mois").cast("int"),
    )


if __name__ == "__main__":
    # dummy Avito data json file
    # TODO: replace dummy file with runtime args
    file_path = "./data/avito/2024-10-12_avito.json"

    spark = SparkSession.builder.appName("Avito Cleaning ETL").getOrCreate()

    df = spark.read.json(file_path, multiLine=True)

    df_cleaned = (
        df.transform(clean_n_bedrooms)
        .transform(clean_n_bathrooms)
        .transform(clean_total_area)
        .transform(clean_price)
        .transform(clean_attributes_n_living_rooms)
        .transform(clean_attributes_floor_number)
        .transform(clean_attributes_living_area)
        .transform(clean_attributes_syndicate_price)
    )

    output_path = file_path.replace("data/avito", "data/clean/avito").replace(
        ".json", ""
    )
    df_cleaned.coalesce(1).write.json(output_path, mode="overwrite")

    spark.stop()
