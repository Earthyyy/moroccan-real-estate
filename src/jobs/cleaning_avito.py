import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.jobs.utils import COLUMNS, spark_setup


def load_data(spark: SparkSession, file_path: str) -> DataFrame:
    """Load data with spark from a specific file path

    Args:
        spark (SparkSession): The spark session
        file_path (str): The file path
    Returns:
        DataFrame: The loaded dataframe
    """
    return spark.read.option("multiLine", True).json(file_path)


def clean_n_bedrooms(df: DataFrame) -> DataFrame:
    """Chaging the data type of the n_bedrooms column to int

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with n_bedrooms column as int
    """
    return df.withColumn("n_bedrooms", F.col("n_bedrooms").cast("int"))


def clean_n_bathrooms(df: DataFrame) -> DataFrame:
    """Formatting the n_bathrooms column and changing its data type to int

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with n_bathrooms column as int
    """
    return df.withColumn(
        "n_bathrooms",
        F.when(F.col("n_bathrooms") == "7+", "7")
        .otherwise(F.col("n_bathrooms"))
        .cast("int"),
    )


def clean_total_area(df: DataFrame) -> DataFrame:
    """Cleaning the total_area column by removing the unit and changing
    the data type to int

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with total_area column as int
    """
    return df.withColumn(
        "total_area",
        F.regexp_replace(
            F.when(F.col("total_area") == "m²", None).otherwise(F.col("total_area")),
            " m²",
            "",
        ).cast("int"),
    )


def clean_price(df: DataFrame) -> DataFrame:
    """Cleaning the price column by removing the unit and changing the data type to int

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with price column as int
    """
    return df.withColumn(
        "price",
        F.when(F.col("price") == "Prix non spécifié", None).otherwise(
            F.regexp_replace(F.col("price"), "(\u202f| |DH$)", "").cast("int")
        ),
    )


def clean_attributes_floor(df: DataFrame) -> DataFrame:
    """Cleaning the attributes.Étage column by changing the data type to int

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with floor_number column as int
    """
    return df.withColumn(
        "floor",
        F.when(F.col("attributes.Étage") == "Rez de chaussée", "0")
        .when(F.col("attributes.Étage") == "+7", "7")
        .otherwise(F.col("attributes.Étage"))
        .cast("int"),
    )


def clean_attributes_living_area(df: DataFrame) -> DataFrame:
    """Changing the data type of the attributes.Surface habitable column to int

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with living_area column as int
    """
    return df.withColumn(
        "living_area", F.col("attributes.Surface habitable").cast("int")
    )


def clean_attributes_syndicate_price(df: DataFrame) -> DataFrame:
    """Changing the data type of the attributes.Frais de syndic / mois column to int

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with syndicate_price_per_month column as int
    """
    return df.withColumn(
        "monthly_syndicate_price",
        F.col("attributes.Frais de syndic / mois").cast("int"),
    )


def add_neighborhood(df: DataFrame) -> DataFrame:
    """Retrieving the neighborhood from attributes

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with neighborhood column
    """
    return df.withColumn("neighborhood", F.col("attributes.Secteur"))


def add_type(df: DataFrame) -> DataFrame:
    """Retrieving the type from attributes

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with type column
    """
    return df.withColumn(
        "type",
        F.when(F.array_contains(F.col("equipments"), "Duplex"), "duplex/triplex")
        .when(F.lower(F.col("title")).contains("studio"), "studio")
        .otherwise("apartment"),
    )


def add_source(df: DataFrame) -> DataFrame:
    """Add source "avito" column to the dataframe

    Args:
        df (DataFrame): dataframe to be cleaned

    Returns:
        DataFrame: resulting dataframe with the source column added
    """
    return df.withColumn("source", F.lit("avito"))


def add_equipments_binary(df: DataFrame) -> DataFrame:
    """Add binary columns for each equipment

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with binary columns for each equipment
    """
    return (
        df.withColumn(
            "bool_elevator",
            F.when(F.array_contains(F.col("equipments"), "Ascenseur"), 1).otherwise(0),
        )
        .withColumn(
            "bool_balcony",
            F.when(F.array_contains(F.col("equipments"), "Balcon"), 1).otherwise(0),
        )
        .withColumn(
            "bool_heating",
            F.when(F.array_contains(F.col("equipments"), "Chauffage"), 1).otherwise(0),
        )
        .withColumn(
            "bool_air_conditioning",
            F.when(F.array_contains(F.col("equipments"), "Climatisation"), 1).otherwise(
                0
            ),
        )
        .withColumn(
            "bool_concierge",
            F.when(F.array_contains(F.col("equipments"), "Concierge"), 1).otherwise(0),
        )
        .withColumn(
            "bool_equipped_kitchen",
            F.when(
                F.array_contains(F.col("equipments"), "Cuisine équipée"), 1
            ).otherwise(0),
        )
        .withColumn(
            "bool_furniture",
            F.when(F.array_contains(F.col("equipments"), "Meublé"), 1).otherwise(0),
        )
        .withColumn(
            "bool_parking",
            F.when(F.array_contains(F.col("equipments"), "Parking"), 1).otherwise(0),
        )
        .withColumn(
            "bool_security",
            F.when(F.array_contains(F.col("equipments"), "Sécurité"), 1).otherwise(0),
        )
        .withColumn(
            "bool_terrace",
            F.when(F.array_contains(F.col("equipments"), "Terrasse"), 1).otherwise(0),
        )
    )


def drop_irrelevant_columns(df: DataFrame) -> DataFrame:
    """Dropping irrelevant columns

    Args:
        df (DataFrame): input DataFrame

    Returns:
        DataFrame: resulting DataFrame with irrelevant columns dropped
    """
    return df.drop("title", "user", "time", "date_time", "attributes", "equipments")


def main(input_path: str, output_path: str):
    spark = spark_setup("Avito Cleaning Job")
    df = load_data(spark, input_path)
    df_cleaned = (
        df.transform(clean_n_bedrooms)
        .transform(clean_n_bathrooms)
        .transform(clean_total_area)
        .transform(clean_price)
        .transform(clean_attributes_floor)
        .transform(clean_attributes_living_area)
        .transform(clean_attributes_syndicate_price)
        .transform(add_neighborhood)
        .transform(add_type)
        .transform(add_source)
        .transform(add_equipments_binary)
        .transform(drop_irrelevant_columns)
    )
    # check with constraints (columns)
    if sorted(df_cleaned.columns) != sorted(COLUMNS):
        raise ValueError("Column mismatch")
    df_cleaned.select(*COLUMNS).coalesce(1).write.csv(
        output_path, header=True, mode="overwrite"
    )
    spark.stop()


if __name__ == "__main__":
    input_path = "./data/raw/avito/2024-11-30T14-44-37+00-00.json"
    output_path = input_path.replace("/raw/", "/clean/").replace(".json", "")
    main(input_path, output_path)
