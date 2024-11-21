import pytest
from pyspark.sql import SparkSession
from pyspark.sql import Row

from src.jobs.loading import (
    load_table_from_duckdb,
    create_type_dim,
    create_date_dim,
    create_location_dim,
    create_source_dim,
    create_property_facts,
)


@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[1]").appName("pytest").getOrCreate()


def test_load_table_from_duckdb(spark):
    table_name = "test_table"
    df = load_table_from_duckdb(spark, table_name)
    assert df is not None
    assert isinstance(df, DataFrame)


def test_create_type_dim(spark):
    df = spark.createDataFrame([Row(type="apartment"), Row(type="house")])
    result_df = create_type_dim(spark, df)
    assert result_df is not None
    assert isinstance(result_df, DataFrame)
    assert "id" in result_df.columns


def test_create_date_dim(spark):
    df = spark.createDataFrame([Row(year=2023, month=1), Row(year=2023, month=2)])
    result_df = create_date_dim(spark, df)
    assert result_df is not None
    assert isinstance(result_df, DataFrame)
    assert "id" in result_df.columns


def test_create_location_dim(spark):
    df = spark.createDataFrame(
        [Row(city="Casablanca", neighborhood="Maarif"), Row(city="Rabat", neighborhood="Agdal")]
    )
    result_df = create_location_dim(spark, df)
    assert result_df is not None
    assert isinstance(result_df, DataFrame)
    assert "id" in result_df.columns


def test_create_source_dim(spark):
    df = spark.createDataFrame([Row(source="avito"), Row(source="mubawab")])
    result_df = create_source_dim(spark, df)
    assert result_df is not None
    assert isinstance(result_df, DataFrame)
    assert "id" in result_df.columns


def test_create_property_facts(spark):
    df = spark.createDataFrame(
        [
            Row(source="avito", type="apartment", city="Casablanca", neighborhood="Maarif", year=2023, month=1),
            Row(source="mubawab", type="house", city="Rabat", neighborhood="Agdal", year=2023, month=2),
        ]
    )
    source_dim_df = spark.createDataFrame([Row(source="avito", id=1), Row(source="mubawab", id=2)])
    type_dim_df = spark.createDataFrame([Row(type="apartment", id=1), Row(type="house", id=2)])
    location_dim_df = spark.createDataFrame(
        [Row(city="Casablanca", neighborhood="Maarif", id=1), Row(city="Rabat", neighborhood="Agdal", id=2)]
    )
    date_dim_df = spark.createDataFrame([Row(year=2023, month=1, id="202301"), Row(year=2023, month=2, id="202302")])

    result_df = create_property_facts(
        spark, df, source_dim_df, type_dim_df, location_dim_df, date_dim_df
    )
    assert result_df is not None
    assert isinstance(result_df, DataFrame)
    assert "id" in result_df.columns