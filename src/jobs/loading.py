import os
import sys

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.dataframe import DataFrame

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.jobs.utils import DF_SCHEMA, spark_setup


def load_table_from_duckdb(spark: SparkSession, table: str) -> DataFrame:
    """Load a table from duckdb (used for dimension tables)

    Args:
        spark (SparkSession): the spark session object
        table (str): Name of the table

    Returns:
        DataFrame: the desired duckdb table as a spark dataframe
    """
    duckdb_url = "jdbc:duckdb:data/dw/datawarehouse.db"
    return (
        spark.read.format("jdbc")
        .option("driver", "org.duckdb.DuckDBDriver")
        .option("url", duckdb_url)
        .option("dbtable", table)
        .load()
    )


def create_type_dim_new(df: DataFrame, type_dim_existing: DataFrame) -> DataFrame:
    """Create the new dimension table data for the type column

    Args:
        df (DataFrame): the input dataframe
        type_dim_existing (DataFrame): type_dim from duckdb

    Returns:
        DataFrame: new values for the type dimension table
    """
    types = df.select("type").distinct()
    new_types = types.join(type_dim_existing, on="type", how="left_anti")
    new_types = new_types.withColumn(
        "id", F.monotonically_increasing_id() + F.lit(type_dim_existing.count() + 1)
    )
    return new_types.select("id", "type")


def create_date_dim_new(df: DataFrame, date_dim_existing: DataFrame) -> DataFrame:
    """Create the new dimension table data for the year and month columns

    Args:
        df (DataFrame): the input dataframe
        date_dim_existing (DataFrame): date_dim from duckdb

    Returns:
        DataFrame: new values for the date dimension table
    """
    dates = df.select("year", "month").distinct()
    new_dates = dates.join(date_dim_existing, on=["year", "month"], how="left_anti")
    new_dates = new_dates.withColumn(
        "id",
        F.concat(F.col("year"), F.format_string("%02d", F.col("month"))).cast("int"),
    )
    return new_dates.select("id", "year", "month")


def create_location_dim_new(
    df: DataFrame, location_dim_existing: DataFrame
) -> DataFrame:
    """Create the new dimension table data for the city and neighborhood columns

    Args:
        df (DataFrame): the input dataframe
        location_dim_existing (DataFrame): location_dim from duckdb

    Returns:
        DataFrame: new values for the location dimension table
    """
    locations = df.select("city", "neighborhood").distinct()
    new_locations = locations.join(
        location_dim_existing, on=["city", "neighborhood"], how="left_anti"
    )
    new_locations = new_locations.withColumn(
        "id", F.monotonically_increasing_id() + 1 + F.lit(location_dim_existing.count())
    )
    return new_locations.select("id", "city", "neighborhood")


def create_source_dim_new(df: DataFrame, source_dim_existing: DataFrame) -> DataFrame:
    """Create the new dimension table data for the source column

    Args:
        df (DataFrame): the input dataframe
        source_dim_existing (DataFrame): source_dim from duckdb

    Returns:
        DataFrame: new values for the source dimension table
    """
    sources = df.select("source").distinct()
    new_sources = sources.join(source_dim_existing, on="source", how="left_anti")
    new_sources = new_sources.withColumn(
        "id", F.monotonically_increasing_id() + 1 + F.lit(source_dim_existing.count())
    )
    return new_sources.select("id", "source")


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


def load_source_dim_to_duckdb(source_dim: DataFrame, duckdb_path: str):
    """Load source dimension data into duckdb table

    Args:
        source_dim (DataFrame): source dimension dataframe
        duckdb_path (str): path to the duckdb data warehouse
    """
    duckdb_url = "jdbc:duckdb:" + duckdb_path
    (
        source_dim.write.format("jdbc")
        .option("driver", "org.duckdb.DuckDBDriver")
        .option("url", duckdb_url)
        .option("dbtable", "source_dim")
        .mode("append")
        .save()
    )


def load_location_dim_to_duckdb(location_dim: DataFrame, duckdb_path: str):
    """Load location dimension data into duckdb table

    Args:
        location_dim (DataFrame): location dimension dataframe
        duckdb_path (str): path to the duckdb data warehouse
    """
    duckdb_url = "jdbc:duckdb:" + duckdb_path
    (
        location_dim.write.format("jdbc")
        .option("driver", "org.duckdb.DuckDBDriver")
        .option("url", duckdb_url)
        .option("dbtable", "location_dim")
        .mode("append")
        .save()
    )


def load_type_dim_to_duckdb(type_dim: DataFrame, duckdb_path: str):
    """Load type dimension data into duckdb table

    Args:
        type_dim (DataFrame): type dimension dataframe
        duckdb_path (str): path to the duckdb data warehouse
    """
    duckdb_url = "jdbc:duckdb:" + duckdb_path
    (
        type_dim.write.format("jdbc")
        .option("driver", "org.duckdb.DuckDBDriver")
        .option("url", duckdb_url)
        .option("dbtable", "type_dim")
        .mode("append")
        .save()
    )


def load_date_dim_to_duckdb(date_dim: DataFrame, duckdb_path: str):
    """Load date dimension data into duckdb table

    Args:
        date_dim (DataFrame): date dimension dataframe
        duckdb_path (str): path to the duckdb data warehouse
    """
    duckdb_url = "jdbc:duckdb:" + duckdb_path
    # insert all of the dimension values
    (
        date_dim.write.format("jdbc")
        .option("driver", "org.duckdb.DuckDBDriver")
        .option("url", duckdb_url)
        .option("dbtable", "date_dim")
        .mode("append")
        .save()
    )


def load_fact_table_to_duckdb(property_facts: DataFrame, duckdb_path: str):
    """Load facts data into duckdb table

    Args:
        property_facts (DataFrame): facts dataframe
        duckdb_path (str): path to the duckdb data warehouse
    """
    duckdb_url = "jdbc:duckdb:" + duckdb_path
    (
        property_facts.write.format("jdbc")
        .option("driver", "org.duckdb.DuckDBDriver")
        .option("url", duckdb_url)
        .option("dbtable", "property_facts")
        .mode("append")
        .save()
    )


if __name__ == "__main__":

    paths = [
        "./data/clean/avito/2024-11-30T19-40-08+00-00/part-00000-39b01b3c-97a4-4bb6-ab7f-126d272f899c-c000.csv",
        "./data/clean/yakeey/2024-11-30T19-39-41+00-00/part-00000-b9cf4e76-8f31-45d0-a47d-b6a59fdd750e-c000.csv",
    ]

    spark = spark_setup("Loading ETL")

    for path in paths:
        # load clean csv file

        df = spark.read.csv(path, header=True, schema=DF_SCHEMA)

        # load existing dim and fact tables from duckdb
        source_dim_existing = load_table_from_duckdb(spark, "source_dim")
        type_dim_existing = load_table_from_duckdb(spark, "type_dim")
        location_dim_existing = load_table_from_duckdb(spark, "location_dim")
        date_dim_existing = load_table_from_duckdb(spark, "date_dim")
        property_facts_existing = load_table_from_duckdb(spark, "property_facts")

        # update dim tables with new dim values from the clean data
        source_dim_new = create_source_dim_new(df, source_dim_existing)
        location_dim_new = create_location_dim_new(df, location_dim_existing)
        type_dim_new = create_type_dim_new(df, type_dim_existing)
        date_dim_new = create_date_dim_new(df, date_dim_existing)

        # transform clean data into a fact table
        property_facts = df.transform(
            create_property_facts,
            property_facts_existing=property_facts_existing,
            source_dim=source_dim_existing.select("id", "source").union(source_dim_new),
            type_dim=type_dim_existing.select("id", "type").union(type_dim_new),
            location_dim=location_dim_existing.select(
                "id", "city", "neighborhood"
            ).union(location_dim_new),
            date_dim=date_dim_existing.select("id", "year", "month").union(
                date_dim_new
            ),
        )

        # load to dev dw
        dev_dw_path = "data/dw/datawarehouse.db"
        load_source_dim_to_duckdb(source_dim_new, dev_dw_path)
        load_location_dim_to_duckdb(location_dim_new, dev_dw_path)
        load_type_dim_to_duckdb(type_dim_new, dev_dw_path)
        load_date_dim_to_duckdb(date_dim_new, dev_dw_path)
        load_fact_table_to_duckdb(property_facts, dev_dw_path)

    spark.stop()
