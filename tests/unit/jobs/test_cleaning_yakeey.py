import pyspark.sql.functions as F
import pytest
from pyspark.sql.types import (
    ArrayType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

from src.jobs.cleaning_yakeey import (
    add_year_month_columns,
    calculate_monthly_syndicate_fee,
    clean_nested_attributes,
    clean_price_column,
    drop_irrelevant_columns,
    drop_na_records,
    one_hot_encode_equipements,
    rename_and_drop_attributes,
    standardize_property_type,
    start_spark_session,
)


@pytest.fixture(scope="module")
def spark():
    """Create a Spark session for testing."""
    spark = start_spark_session("test_cleaning_yakeey")
    yield spark
    spark.stop()


def test_drop_irrelevant_columns(spark):
    data = [(1, "title1", "reference1"), (2, "title2", "reference2")]
    schema = StructType(
        [
            StructField("id", IntegerType()),
            StructField("title", StringType()),
            StructField("reference", StringType()),
        ]
    )
    df = spark.createDataFrame(data, schema)
    cleaned_df = drop_irrelevant_columns(df, ["title", "reference"])
    assert cleaned_df.columns == ["id"]


def test_drop_na_records(spark):
    data = [("CityA", None, 200000), (None, "NeighborhoodB", 300000)]
    schema = StructType(
        [
            StructField("city", StringType()),
            StructField("neighborhood", StringType()),
            StructField("price", IntegerType()),
        ]
    )
    df = spark.createDataFrame(data, schema)
    cleaned_df = drop_na_records(df, ["city", "neighborhood", "price"])
    assert cleaned_df.count() == 0


def test_add_year_month_columns(spark):
    sample_data = [(1, "sample data"), (2, "more data")]
    dataframe = spark.createDataFrame(sample_data, ["id", "value"])
    file_path = "data/raw/yakeey/2024-11-11_yakeey.json"

    result_df = add_year_month_columns(dataframe, file_path)

    # Expected year and month
    expected_year = 2024
    expected_month = 11

    result = result_df.select("year", "month").distinct().collect()

    assert len(result) == 1  # Only one distinct year-month pair
    assert result[0]["year"] == expected_year
    assert result[0]["month"] == expected_month


def test_clean_price_column(spark):
    data = [("200 000 DH",), ("150000 DH",)]
    schema = StructType([StructField("price", StringType())])
    df = spark.createDataFrame(data, schema)
    cleaned_df = clean_price_column(df)
    assert cleaned_df.select("price").dtypes == [("price", "int")]


def test_standardize_property_type(spark):
    data = [("Triplex",), ("Appartement",), ("Studio",), ("Duplex",)]
    schema = StructType([StructField("type", StringType())])
    df = spark.createDataFrame(data, schema)
    cleaned_df = standardize_property_type(df)
    types = [row["type"] for row in cleaned_df.collect()]
    assert types == ["duplex/triplex", "apartment", "studio", "duplex/triplex"]


def test_rename_and_drop_attributes(spark):
    data = [
        (
            {
                "Nb. de chambres": "3",
                "Surface habitable": "80 m²",
                "Nb. de salles de bains": "2",
                "Surface totale": "100 m²",
                "Étage du bien": "Rez-de-chaussée",
                "Frais de syndic (DH/an)": "1200",
            },
        )
    ]
    schema = StructType(
        [
            StructField(
                "attributes",
                StructType(
                    [
                        StructField("Nb. de chambres", StringType()),
                        StructField("Nb. de salles de bains", StringType()),
                        StructField("Surface habitable", StringType()),
                        StructField("Surface totale", StringType()),
                        StructField("Étage du bien", StringType()),
                        StructField("Frais de syndic (DH/an)", StringType()),
                    ]
                ),
            )
        ]
    )
    df = spark.createDataFrame(data, schema)
    cleaned_df = rename_and_drop_attributes(df)
    # Ensure renamed fields are present
    assert "n_bedrooms" in cleaned_df.columns
    assert "n_bathrooms" in cleaned_df.columns
    assert "living_area" in cleaned_df.columns
    assert "total_area" in cleaned_df.columns
    assert "floor" in cleaned_df.columns
    assert "syndicate_price_per_year" in cleaned_df.columns
    assert "attributes" not in cleaned_df.columns


def test_clean_nested_attributes(spark):
    data = [(3, 2, "80 m²", "Rez-de-chaussée", "100 m²", 1200)]
    schema = StructType(
        [
            StructField("n_bedrooms", StringType()),
            StructField("n_bathrooms", StringType()),
            StructField("living_area", StringType()),
            StructField("floor", StringType()),
            StructField("total_area", StringType()),
            StructField("syndicate_price_per_year", StringType()),
        ]
    )
    df = spark.createDataFrame(data, schema)
    cleaned_df = clean_nested_attributes(df)
    assert cleaned_df.select("living_area").dtypes == [("living_area", "int")]
    assert cleaned_df.filter(F.col("floor") == 0).count() == 1
    assert cleaned_df.select("total_area").dtypes == [("total_area", "int")]
    assert cleaned_df.select("syndicate_price_per_year").dtypes == [
        ("syndicate_price_per_year", "int")
    ]


def test_calculate_monthly_syndicate_fee(spark):
    data = [(1200,)]
    schema = StructType([StructField("syndicate_price_per_year", IntegerType())])
    df = spark.createDataFrame(data, schema)
    cleaned_df = calculate_monthly_syndicate_fee(df)
    assert "syndicate_price_per_month" in cleaned_df.columns
    assert cleaned_df.collect()[0]["syndicate_price_per_month"] == 100.0


def test_one_hot_encode_equipements(spark):
    data = [(["Agent de sécurité", "Ascenseur"],), (["Balcon"],)]
    schema = StructType([StructField("equipements", ArrayType(StringType()))])
    df = spark.createDataFrame(data, schema)
    mappings = {
        "Agent de sécurité": "bool_security",
        "Ascenseur": "bool_elevator",
        "Balcon": "bool_balcony",
    }
    cleaned_df = one_hot_encode_equipements(df, mappings)
    for col in mappings.values():
        assert col in cleaned_df.columns
    assert cleaned_df.filter(F.col("bool_security") == 1).count() == 1
