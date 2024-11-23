from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame


def load_table_from_duckdb(spark: SparkSession, table: str) -> DataFrame:
    """Load a table from duckdb (used for dimension tables)

    Args:
        spark (SparkSession): the spark session object
        table (str): Name of the table

    Returns:
        DataFrame: the desired duckdb table as a spark dataframe
    """
    duckdb_url = "jdbc:duckdb:data/dw/datawarehouse.db"
    connection = (
        spark.read.format("jdbc")
        .option("driver", "org.duckdb.DuckDBDriver")
        .option("url", duckdb_url)
    )
    if table == "type_dim":
        return connection.option(
            "query", "SELECT id, CAST(type AS STRING) AS type FROM type_dim"
        ).load()
    return connection.option("dbtable", table).load()


def create_type_dim(df: DataFrame, type_dim_existing: DataFrame) -> DataFrame:
    """Create the dimension table for the type column

    Args:
        df (DataFrame): the input dataframe
        type_dim_existing (DataFrame): type_dim from duckdb

    Returns:
        DataFrame: the resulting type dimension table
    """
    types = df.select("type").distinct()
    new_types = types.join(type_dim_existing, on="type", how="left_anti")
    new_types = new_types.withColumn(
        "id", F.monotonically_increasing_id() + F.lit(type_dim_existing.count() + 1)
    )
    return type_dim_existing.select("id", "type").union(new_types.select("id", "type"))


def create_date_dim(df: DataFrame, date_dim_existing: DataFrame) -> DataFrame:
    """Create the dimension table for the year and month columns

    Args:
        df (DataFrame): the input dataframe
        date_dim_existing (DataFrame): date_dim from duckdb

    Returns:
        DataFrame: the resulting date dimension table
    """
    dates = df.select("year", "month").distinct()
    new_dates = dates.join(date_dim_existing, on=["year", "month"], how="left_anti")
    new_dates = new_dates.withColumn(
        "id",
        F.concat(F.col("year"), F.format_string("%02d", F.col("month"))).cast("int"),
    )
    return date_dim_existing.select("id", "year", "month").union(
        new_dates.select("id", "year", "month")
    )


def create_location_dim(df: DataFrame, location_dim_existing: DataFrame) -> DataFrame:
    """Create the dimension table for the city and neighborhood columns

    Args:
        df (DataFrame): the input dataframe
        location_dim_existing (DataFrame): location_dim from duckdb

    Returns:
        DataFrame: the resulting location dimension table
    """
    locations = df.select("city", "neighborhood").distinct()
    new_locations = locations.join(
        location_dim_existing, on=["city", "neighborhood"], how="left_anti"
    )
    new_locations = new_locations.withColumn(
        "id", F.monotonically_increasing_id() + 1 + F.lit(location_dim_existing.count())
    )
    return location_dim_existing.select("id", "city", "neighborhood").union(
        new_locations.select("id", "city", "neighborhood")
    )


def create_source_dim(df: DataFrame, source_dim_existing: DataFrame) -> DataFrame:
    """Create the dimension table for the source column

    Args:
        df (DataFrame): the input dataframe
        source_dim_existing (DataFrame): source_dim from duckdb

    Returns:
        DataFrame: the resulting source dimension table
    """
    sources = df.select("source").distinct()
    new_sources = sources.join(source_dim_existing, on="source", how="left_anti")
    new_sources = new_sources.withColumn(
        "id", F.monotonically_increasing_id() + 1 + F.lit(source_dim_existing.count())
    )
    return source_dim_existing.select("id", "source").union(
        new_sources.select("id", "source")
    )


def create_property_facts(
    df: DataFrame,
    property_facts_existing: DataFrame,
    source_dim: DataFrame,
    type_dim: DataFrame,
    location_dim: DataFrame,
    date_dim: DataFrame,
) -> DataFrame:
    """Create the fact table

    Args:
        df (DataFrame): the input dataframe
        property_facts_existing (DataFrame): property_facts from duckdb
        source_dim (DataFrame): updated source dimension table
        type_dim (DataFrame): updated type demension table
        location_dim (DataFrame): updated location dimension table
        date_dim (DataFrame): updated date dimension table

    Returns:
        DataFrame: the resulting fact table
    """
    # replace dimension values with their coresponding ids
    df = (
        df.join(source_dim, on="source", how="inner")
        .withColumnRenamed("id", "source_id")
        .drop("source")
    )
    df = (
        df.join(type_dim, on="type", how="inner")
        .withColumnRenamed("id", "type_id")
        .drop("type")
    )
    df = (
        df.join(location_dim, on=["city", "neighborhood"], how="inner")
        .withColumnRenamed("id", "location_id")
        .drop("city", "neighborhood")
    )
    df = (
        df.join(date_dim, on=["year", "month"], how="inner")
        .withColumnRenamed("id", "date_id")
        .drop("year", "month")
    )
    return df.withColumn(
        "id",
        F.monotonically_increasing_id() + 1 + F.lit(property_facts_existing.count()),
    )


def load_dim_table(dim_df: DataFrame):
    pass


def load_fact_table(fact_df: DataFrame):
    pass


if __name__ == "__main__":

    file_path = (
        ".data/clean/avito/avito_2024-11-14/"
        "part-00000-31df9b63-1454-48d6-8bf4-20cb34de3625-c000.csv"
    )

    duckdb_jdbc_jar = "./libs/duckdb_jdbc-1.1.3.jar"

    spark = (
        SparkSession.builder.appName("Avito Cleaning ETL")
        .config("spark.jars", duckdb_jdbc_jar)
        .getOrCreate()
    )

    # load clean csv file
    df = spark.read.csv(file_path, header=True)

    # load existing dim and fact tables from duckdb
    source_dim_existing = load_table_from_duckdb(spark, "source_dim")
    type_dim_existing = load_table_from_duckdb(spark, "type_dim")
    location_dim_existing = load_table_from_duckdb(spark, "location_dim")
    date_dim_existing = load_table_from_duckdb(spark, "date_dim")
    property_facts_existing = load_table_from_duckdb(spark, "property_facts")

    # update dim tables with new dim values from the clean data
    source_dim = create_source_dim(df, source_dim_existing)
    location_dim = create_location_dim(df, location_dim_existing)
    type_dim = create_type_dim(df, type_dim_existing)
    date_dim = create_date_dim(df, date_dim_existing)

    # transform clean data into a fact table
    df = df.transform(
        create_property_facts,
        property_facts_existing=property_facts_existing,
        source_dim=source_dim,
        type_dim=type_dim,
        location_dim=location_dim,
        date_dim=date_dim,
    )

    # TODO: load dim tables into duckdb (overwrite)
    load_dim_table(source_dim)
    load_dim_table(type_dim)
    load_dim_table(location_dim)
    load_dim_table(date_dim)

    # TODO: load fact table into duckdb (append)
    load_fact_table(df)
