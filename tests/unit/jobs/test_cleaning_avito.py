import pytest
from pyspark.sql import Row, SparkSession

from src.jobs.cleaning_avito import (
    clean_attributes_floor_number,
    clean_attributes_living_area,
    clean_attributes_n_living_rooms,
    clean_attributes_syndicate_price,
    clean_n_bathrooms,
    clean_n_bedrooms,
    clean_price,
    clean_total_area,
)


@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.master("local[1]").appName("pytest").getOrCreate()


def test_clean_n_bedrooms(spark):
    data = [Row(n_bedrooms="3"), Row(n_bedrooms="2"), Row(n_bedrooms=None)]
    df = spark.createDataFrame(data)
    result_df = clean_n_bedrooms(df)
    result = [row.n_bedrooms for row in result_df.collect()]
    assert result == [3, 2, None]


def test_clean_n_bathrooms(spark):
    data = [Row(n_bathrooms="7"), Row(n_bathrooms="7+"), Row(n_bathrooms=None)]
    df = spark.createDataFrame(data)
    result_df = clean_n_bathrooms(df)
    result = [row.n_bathrooms for row in result_df.collect()]
    assert result == [7, 7, None]


def test_clean_total_area(spark):
    data = [
        Row(total_area="100 m²"),
        Row(total_area="200 m²"),
        Row(total_area="m²"),
        Row(total_area=None),
    ]
    df = spark.createDataFrame(data)
    result_df = clean_total_area(df)
    result = [row.total_area for row in result_df.collect()]
    assert result == [100, 200, None, None]


def test_clean_price(spark):
    data = [
        Row(price="830 000 DH"),  # noqa: RUF001
        Row(price="Prix non spécifié"),
        Row(price="1 480 000 DH"),  # noqa: RUF001
        Row(price=None),
    ]
    df = spark.createDataFrame(data)
    result_df = clean_price(df)
    result = [row.price for row in result_df.collect()]
    assert result == [830000, None, 1480000, None]


def test_clean_attributes_n_living_rooms(spark):
    data = [
        Row(attributes={"Salons": "2"}),
        Row(attributes={"Salons": "3"}),
        Row(attributes={"Salons": "+7"}),
        Row(attributes={"Salons": None}),
    ]
    df = spark.createDataFrame(data)
    result_df = clean_attributes_n_living_rooms(df)
    result = [row.n_living_room for row in result_df.collect()]
    assert result == [2, 3, 7, None]


def test_clean_attributes_floor_number(spark):
    data = [
        Row(attributes={"Étage": "1"}),
        Row(attributes={"Étage": "Rez de chaussée"}),
        Row(attributes={"Étage": "+7"}),
        Row(attributes={"Étage": None}),
    ]
    df = spark.createDataFrame(data)
    result_df = clean_attributes_floor_number(df)
    result = [row.floor_number for row in result_df.collect()]
    assert result == [1, 0, 7, None]


def test_clean_attributes_living_area(spark):
    data = [
        Row(attributes={"Surface habitable": "100"}),
        Row(attributes={"Surface habitable": "200"}),
        Row(attributes={"Surface habitable": None}),
    ]
    df = spark.createDataFrame(data)
    result_df = clean_attributes_living_area(df)
    result = [row.living_area for row in result_df.collect()]
    assert result == [100, 200, None]


def test_clean_attributes_syndicate_price(spark):
    data = [
        Row(attributes={"Frais de syndic / mois": "100"}),
        Row(attributes={"Frais de syndic / mois": "200"}),
        Row(attributes={"Frais de syndic / mois": None}),
    ]
    df = spark.createDataFrame(data)
    result_df = clean_attributes_syndicate_price(df)
    result = [row.syndicate_price_per_month for row in result_df.collect()]
    assert result == [100, 200, None]
