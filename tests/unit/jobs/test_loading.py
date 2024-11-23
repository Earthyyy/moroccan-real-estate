from typing import List, Tuple

import pytest
from pyspark.sql import Row, SparkSession
from pyspark.sql import types as T
from pyspark.sql.dataframe import DataFrame

from src.jobs.loading import (
    create_date_dim,
    create_location_dim,
    create_property_facts,
    create_source_dim,
    create_type_dim,
    load_table_from_duckdb,
)


@pytest.fixture(scope="session")
def spark():
    duckdb_jdbc_jar = "./libs/duckdb_jdbc-1.1.3.jar"
    spark = (
        SparkSession.builder.master("local[1]")
        .appName("pytest loading")
        .config("spark.jars", duckdb_jdbc_jar)
        .getOrCreate()
    )
    yield spark
    spark.stop()


@pytest.mark.parametrize(
    "table_name",
    ["location_dim", "source_dim", "type_dim", "date_dim", "property_facts"],
)
def test_load_table_from_duckdb(spark, table_name: str):
    df = load_table_from_duckdb(spark, table_name)
    assert df is not None
    assert isinstance(df, DataFrame)


@pytest.mark.parametrize(
    "type_dim_data",
    [
        [],
        [(1, "apartment"), (2, "studio")],
        [(1, "apartment"), (2, "studio"), (3, "duplex/triplex")],
    ],
)
def test_create_type_dim(spark, type_dim_data: List[Tuple[int, str]]):
    property_df = spark.createDataFrame(
        [("apartment",), ("studio",), ("studio",), ("duplex/triplex",)],
        ["type"],
    )
    type_dim_schema = T.StructType(
        [
            T.StructField("id", T.IntegerType()),
            T.StructField("type", T.StringType()),
        ]
    )
    type_dim_existing = spark.createDataFrame(type_dim_data, type_dim_schema)
    result_df = create_type_dim(df=property_df, type_dim_existing=type_dim_existing)
    rows = [row.asDict() for row in result_df.collect()]
    types = {row["type"] for row in rows}
    ids = sorted([row["id"] for row in rows])
    assert types == {"apartment", "duplex/triplex", "studio"}
    assert ids == [1, 2, 3]


@pytest.mark.parametrize(
    "date_dim_data",
    [
        [],
        [(202312, 2023, 12), (202401, 2024, 1)],
        [(202312, 2023, 12), (202401, 2024, 1), (202412, 2024, 12)],
    ],
)
def test_create_date_dim(spark, date_dim_data: List[Tuple[int, int, int]]):
    property_df = spark.createDataFrame(
        [(2023, 12), (2024, 1), (2024, 1), (2024, 12)],
        ["year", "month"],
    )
    date_dim_schema = T.StructType(
        [
            T.StructField("id", T.IntegerType()),
            T.StructField("year", T.IntegerType()),
            T.StructField("month", T.IntegerType()),
        ]
    )
    date_dim_existing = spark.createDataFrame(date_dim_data, date_dim_schema)
    result_df = create_date_dim(df=property_df, date_dim_existing=date_dim_existing)
    rows = [row.asDict() for row in result_df.collect()]
    assert {row["id"] for row in rows} == {202312, 202401, 202412}


@pytest.mark.parametrize(
    "location_dim_data",
    [
        [],
        [
            (1, "casablanca", "oulfa"),
            (2, "casablanca", "hay hassani"),
            (3, "rabat", "alirfane"),
            (4, "agadir", "hay hassani"),
        ],
        [
            (1, "casablanca", "oulfa"),
            (2, "casablanca", "hay hassani"),
            (3, "rabat", "alirfane"),
            (4, "agadir", "hay hassani"),
            (5, "agadir", "alquds"),
            (6, "fes", "zouagha"),
        ],
    ],
)
def test_create_location_dim(spark, location_dim_data: List[Tuple[int, str, str]]):
    property_df = spark.createDataFrame(
        [
            ("casablanca", "oulfa"),
            ("casablanca", "oulfa"),
            ("agadir", "alquds"),
            ("rabat", "alirfane"),
            ("fes", "zouagha"),
            ("rabat", "alirfane"),
            ("casablanca", "hay hassani"),
            ("agadir", "hay hassani"),
        ],
        ["city", "neighborhood"],
    )
    location_dim_schema = T.StructType(
        [
            T.StructField("id", T.IntegerType()),
            T.StructField("city", T.StringType()),
            T.StructField("neighborhood", T.StringType()),
        ]
    )
    location_dim_existing = spark.createDataFrame(
        location_dim_data, location_dim_schema
    )
    result_df = create_location_dim(
        df=property_df, location_dim_existing=location_dim_existing
    )
    rows = [row.asDict() for row in result_df.collect()]
    assert sorted([row["city"] + " " + row["neighborhood"] for row in rows]) == [
        "agadir alquds",
        "agadir hay hassani",
        "casablanca hay hassani",
        "casablanca oulfa",
        "fes zouagha",
        "rabat alirfane",
    ]


@pytest.mark.parametrize(
    "source_dim_data", [[], [(1, "avito")], [(1, "avito"), (2, "yakeey")]]
)
def test_create_source_dim(spark, source_dim_data: List[Tuple[int, str]]):
    property_df = spark.createDataFrame(
        [
            ("avito",),
            ("avito",),
            ("yakeey",),
            ("avito",),
            ("yakeey",),
        ],
        ["source"],
    )
    source_dim_schema = T.StructType(
        [T.StructField("id", T.IntegerType()), T.StructField("source", T.StringType())]
    )
    source_dim_existing = spark.createDataFrame(source_dim_data, source_dim_schema)
    result_df = create_source_dim(
        df=property_df, source_dim_existing=source_dim_existing
    )
    rows = [row.asDict()["source"] for row in result_df.collect()]
    assert sorted(rows) == ["avito", "yakeey"]


@pytest.mark.parametrize(
    ("property_facts_data", "start_id"),
    [
        ([], 1),
        (
            [
                (1, 1, 202301, 2, 2),
                (2, 1, 202310, 1, 1),
                (3, 3, 202301, 3, 1),
            ],
            4,
        ),
    ],
)
def test_create_property_facts(
    spark, property_facts_data: List[Tuple[int, int, int, int, int]], start_id: int
):
    property_df = spark.createDataFrame(
        [
            Row(
                source="avito",
                type="apartment",
                city="casablanca",
                neighborhood="maarif",
                year=2023,
                month=1,
            ),
            Row(
                source="yakeey",
                type="studio",
                city="rabat",
                neighborhood="agdal",
                year=2023,
                month=2,
            ),
            Row(
                source="avito",
                type="duplex/triplex",
                city="casablanca",
                neighborhood="hay hassani",
                year=2023,
                month=10,
            ),
        ]
    )
    source_dim = spark.createDataFrame(
        [Row(source="avito", id=1), Row(source="yakeey", id=2)]
    )
    type_dim = spark.createDataFrame(
        [
            Row(id=1, type="apartment"),
            Row(id=2, type="studio"),
            Row(id=3, type="duplex/triplex"),
        ]
    )
    location_dim = spark.createDataFrame(
        [
            Row(id=1, city="casablanca", neighborhood="maarif"),
            Row(id=2, city="casablanca", neighborhood="hay hassani"),
            Row(id=3, city="rabat", neighborhood="agdal"),
        ]
    )
    date_dim = spark.createDataFrame(
        [
            Row(id=202301, year=2023, month=1),
            Row(id=202302, year=2023, month=2),
            Row(id=202310, year=2023, month=10),
        ]
    )
    property_facts_schema = T.StructType(
        [
            T.StructField("id", T.IntegerType()),
            T.StructField("type_id", T.IntegerType()),
            T.StructField("date_id", T.IntegerType()),
            T.StructField("location_id", T.IntegerType()),
            T.StructField("source_id", T.IntegerType()),
        ]
    )
    property_facts_existing = spark.createDataFrame(
        property_facts_data, property_facts_schema
    )
    result_df = create_property_facts(
        df=property_df,
        property_facts_existing=property_facts_existing,
        source_dim=source_dim,
        type_dim=type_dim,
        location_dim=location_dim,
        date_dim=date_dim,
    )
    assert [row.asDict() for row in result_df.collect()] == [
        {
            "id": start_id,
            "type_id": 1,
            "date_id": 202301,
            "location_id": 1,
            "source_id": 1,
        },
        {
            "id": start_id + 1,
            "type_id": 2,
            "date_id": 202302,
            "location_id": 3,
            "source_id": 2,
        },
        {
            "id": start_id + 2,
            "type_id": 3,
            "date_id": 202310,
            "location_id": 2,
            "source_id": 1,
        },
    ]
