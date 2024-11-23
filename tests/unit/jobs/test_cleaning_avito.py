import pytest
from pyspark.sql import Row

from src.jobs.cleaning_avito import (
    add_equipments_binary,
    add_neighborhood,
    add_source,
    add_type,
    clean_attributes_floor_number,
    clean_attributes_living_area,
    clean_attributes_syndicate_price,
    clean_n_bathrooms,
    clean_n_bedrooms,
    clean_price,
    clean_total_area,
    drop_irrelevant_columns,
    spark_setup,
)


@pytest.fixture(scope="module")
def spark():
    spark = spark_setup()
    yield spark
    spark.stop()


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
    result = [row.monthly_syndicate_price for row in result_df.collect()]
    assert result == [100, 200, None]


def test_add_neighborhood(spark):
    data = [
        Row(attributes={"Secteur": "test_1"}),
        Row(attributes={"Autres": "test_2"}),
        Row(attributes={"Secteur": "test_3"}),
    ]
    df = spark.createDataFrame(data)
    result_df = add_neighborhood(df)
    result = [row.neighborhood for row in result_df.collect()]
    assert result == ["test_1", None, "test_3"]


def test_add_type(spark):
    data = [
        Row(title="Appartement", equipments=[]),
        Row(title="Appartement", equipments=["Duplex"]),
        Row(title="Studio", equipments=[]),
        Row(title="Studio", equipments=["Duplex"]),
    ]
    df = spark.createDataFrame(data)
    result_df = add_type(df)
    result = [row.type for row in result_df.collect()]
    assert result == ["apartment", "duplex/triplex", "studio", "duplex/triplex"]


def test_add_source(spark):
    data = [
        Row(n_bedrooms=2),
        Row(n_bedrooms=3),
        Row(n_bedrooms=4),
    ]
    df = spark.createDataFrame(data)
    result_df = add_source(df)
    result = [row.source for row in result_df.collect()]
    assert result == ["avito", "avito", "avito"]


def test_add_equipments_binary(spark):
    data = [
        Row(equipments=["test_1", "Sécurité"]),
        Row(equipments=["test_2", "Concierge", "Climatisation"]),
        Row(equipments=["Ascenseur", "Cuisine équipée", "Meublé"]),
        Row(equipments=["Parking", "Terrasse"]),
        Row(equipments=["Chauffage", "Balcon"]),
    ]
    df = spark.createDataFrame(data)
    result_df = add_equipments_binary(df)
    bool_columns = [col for col in result_df.columns if col.startswith("bool_")]
    result = [[row[col] for col in bool_columns] for row in result_df.collect()]
    assert result == [
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    ]


def test_drop_irrelevant_columns(spark):
    data = [
        Row(
            a=1,
            b=2,
            title="test",
            user="test",
            time="test",
            date_time="test",
            attributes={"test_1": "test_1", "test_2": "test_2"},
            equipments=["test_1", "test_2"],
        )
    ]
    df = spark.createDataFrame(data)
    result_df = drop_irrelevant_columns(df)
    assert result_df.columns == ["a", "b"]
