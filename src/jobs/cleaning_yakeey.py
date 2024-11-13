import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession


def start_spark_session(app_name: str = "cleaning_yakeey") -> SparkSession:
    """Start the spark application
    Args:
        app_name (str, optional): The name of the application.
        Defaults to "cleaning_yakeey".

    Returns:
        SparkSession: The spark session
    """
    return SparkSession.builder.appName(app_name).getOrCreate()


def load_data(spark: SparkSession, file_path: str) -> DataFrame:
    """Load data with spark from a specific file path

    Args:
        spark (SparkSession): The spark session
        file_path (str): The file path
    Returns:
        DataFrame: The loaded dataframe
    """
    return spark.read.option("multiLine", True).json(file_path)


def drop_irrelevant_columns(dataframe: DataFrame, list_columns) -> DataFrame:
    """Drop the specified columns from the dataframe

    Args:
        dataframe (DataFrame): The dataframe
        list_columns (list): The list of columns

    Returns:
        DataFrame: The modified dataframe
    """
    return dataframe.drop(*list_columns)


def drop_na_records(dataframe: DataFrame, list_columns: list[str]) -> DataFrame:
    """Drop the records that have null values in the provided columns

    Args:
        dataframe (DataFrame): The dataframe
        list_columns (list[str]): The list of columns

    Returns:
        DataFrame: The modified dataframe
    """
    return dataframe.na.drop(subset=list_columns)


def add_year_month_columns(dataframe: DataFrame, file_path: str) -> DataFrame:
    """Add a year and month column

    Args:
        dataframe (DataFrame): The dataframe
        file_path (str): The file path

    Returns:
        DataFrame: The modified dataframe
    """
    year, month, _ = map(int, file_path.split("/")[-1].split("_")[0].split("-"))

    return dataframe.withColumn("year", F.lit(year)).withColumn("month", F.lit(month))


def clean_price_column(dataframe: DataFrame) -> DataFrame:
    """Transform the price column to numeric value and remove the currency

    Args:
        dataframe (DataFrame): The dataframe

    Returns:
        DataFrame: The modified dataframe
    """
    dataframe = dataframe.withColumn(
        "price", F.regexp_replace(F.regexp_replace("price", " ", ""), "DH", "")
    )
    return dataframe.withColumn("price", dataframe["price"].cast("integer"))


def standardize_property_type(dataframe: DataFrame) -> DataFrame:
    """Standardize the naming of the types

    Args:
        dataframe (DataFrame): The dataframe
    Returns:
        DataFrame: The modified dataframe
    """
    type_mappings = {
        "Triplex": "duplex/triplex",
        "Appartement": "apartment",
        "Studio": "studio",
        "Duplex": "duplex/triplex",
    }
    for key, value in type_mappings.items():
        dataframe = dataframe.withColumn("type", F.regexp_replace("type", key, value))
    return dataframe


def rename_and_drop_attributes(dataframe: DataFrame) -> DataFrame:
    """Rename the nested fields in the `attributes` column and drop irrelevant
    attributes

    Args:
        dataframe (DataFrame): The dataframe

    Returns:
        DataFrame: The modified dataframe
    """
    return (
        dataframe.withColumn("n_bedrooms", F.col("attributes.`Nb. de chambres`"))
        .withColumn("n_bedrooms", F.col("attributes.`Nb. de chambres`"))
        .withColumn("n_bathrooms", F.col("attributes.`Nb. de salles de bains`"))
        .withColumn("living_area", F.col("attributes.`Surface habitable`"))
        .withColumn("total_area", F.col("attributes.`Surface totale`"))
        .withColumn("living_area", F.col("attributes.`Surface habitable`"))
        .withColumn("floor", F.col("attributes.`Étage du bien`"))
        .withColumn(
            "syndicate_price_per_year", F.col("attributes.Frais de syndic (DH/an)")
        )
        .drop("attributes")
    )


def clean_nested_attributes(dataframe: DataFrame) -> DataFrame:
    """Clean and transform the nested fields in the `attributes` column

    Args:
        dataframe (DataFrame): The dataframe

    Returns:
        DataFrame: The modified dataframe
    """
    return (
        dataframe.withColumn(
            "living_area",
            F.regexp_replace(
                F.regexp_replace(F.col("living_area"), "m²", ""), " ", ""
            ).cast("int"),
        )
        .withColumn(
            "total_area",
            F.regexp_replace(
                F.regexp_replace(F.col("total_area"), "m²", ""), " ", ""
            ).cast("int"),
        )
        .withColumn(
            "floor",
            F.regexp_replace(F.col("floor"), "Rez-de-chaussée", "0").cast("int"),
        )
        .withColumn("n_bedrooms", F.col("n_bedrooms").cast("int"))
        .withColumn("n_bathrooms", F.col("n_bathrooms").cast("int"))
        .withColumn(
            "syndicate_price_per_year",
            F.regexp_replace(
                F.regexp_replace(F.col("syndicate_price_per_year"), "DH", ""), " ", ""
            ).cast("int"),
        )
    )


def calculate_monthly_syndicate_fee(dataframe: DataFrame) -> DataFrame:
    """Transform the annual syndicate fees to monthly fees

    Args:
        dataframe (DataFrame): The dataframe

    Returns:
        DataFrame: The modified dataframe
    """
    return dataframe.withColumn(
        "syndicate_price_per_month",
        (F.col("syndicate_price_per_year") / 12).cast("double"),
    ).drop("syndicate_price_per_year")


def one_hot_encode_equipements(
    dataframe: DataFrame, mappings: dict[str, str]
) -> DataFrame:
    """One-hot encode the equipment based on mappings

    Args:
        dataframe (DataFrame): The dataframe
        mappings (dict[str, str]): The new mapping for each equipment item

    Returns:
        DataFrame: The modified dataframe with one-hot encoded equipment columns
    """
    for equip, col_name in mappings.items():
        dataframe = dataframe.withColumn(
            col_name, F.expr(f"array_contains(equipements, '{equip}')").cast("int")
        )
    return dataframe.drop("equipements")


def main(input_path, output_path):
    spark = start_spark_session()

    # Load data
    dataframe = load_data(spark, input_path)

    # Clean and transform data
    mappings = {
        "Agent de sécurité": "bool_security",
        "Ascenseur": "bool_elevator",
        "Balcon": "bool_balcony",
        "Chauffage centralisé": "bool_heating",
        "Chauffage électrique": "bool_heating",
        "Climatisation centralisée": "bool_air_conditioning",
        "Climatisation split": "bool_air_conditioning",
        "Concierge": "bool_concierge",
        "Cuisine équipée": "bool_equiped_kitchen",
        "Meublé": "bool_furniture",
        "Place de parking en extérieur": "bool_parking",
        "Place de parking en sous-sol": "bool_parking",
        "Terrasse": "bool_terrace",
    }

    dataframe = (
        dataframe.transform(
            lambda df: drop_irrelevant_columns(df, ["title", "reference"])
        )
        .transform(lambda df: drop_na_records(df, ["city", "neighborhood", "price"]))
        .transform(lambda df: add_year_month_columns(df, input_path))
        .transform(clean_price_column)
        .transform(standardize_property_type)
        .transform(rename_and_drop_attributes)
        .transform(clean_nested_attributes)
        .transform(calculate_monthly_syndicate_fee)
        .transform(lambda df: one_hot_encode_equipements(df, mappings))
    )

    dataframe.coalesce(1).write.csv(output_path, header=True, mode="overwrite")

    spark.stop()


if __name__ == "__main__":
    input_path = "data/raw/yakeey/2024-11-11_yakeey.json"
    output_path = input_path.replace("/raw/", "/clean/").replace(".json", "")
    main(input_path, output_path)
