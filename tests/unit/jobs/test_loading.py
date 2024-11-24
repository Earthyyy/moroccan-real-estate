import os
from typing import List, Set, Tuple

import duckdb
import pytest
from pyspark.sql import Row
from pyspark.sql import types as T
from pyspark.sql.dataframe import DataFrame

from src.db.dw_schema import main
from src.jobs.loading import (
    create_date_dim_new,
    create_location_dim_new,
    create_property_facts,
    create_source_dim_new,
    create_type_dim_new,
    load_date_dim_to_duckdb,
    load_fact_table_to_duckdb,
    load_location_dim_to_duckdb,
    load_source_dim_to_duckdb,
    load_table_from_duckdb,
    load_type_dim_to_duckdb,
)


def _test_datawarehouse(duckdb_path):
    main(duckdb_path)


@pytest.mark.parametrize(
    "table_name",
    ["location_dim", "source_dim", "type_dim", "date_dim", "property_facts"],
)
def test_load_table_from_duckdb(spark, table_name: str):
    df = load_table_from_duckdb(spark, table_name)
    assert df is not None
    assert isinstance(df, DataFrame)


@pytest.mark.parametrize(
    ("type_dim_data", "expected_types", "expected_ids"),
    [
        ([], {"apartment", "duplex/triplex", "studio"}, [1, 2, 3]),
        ([(1, "apartment"), (2, "studio")], {"duplex/triplex"}, [3]),
        ([(1, "apartment"), (2, "studio"), (3, "duplex/triplex")], set(), []),
    ],
)
def test_create_type_dim_new(
    spark,
    type_dim_data: List[Tuple[int, str]],
    expected_types: Set[str],
    expected_ids: List[int],
):
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
    result_df = create_type_dim_new(df=property_df, type_dim_existing=type_dim_existing)
    rows = [row.asDict() for row in result_df.collect()]
    types = {row["type"] for row in rows}
    ids = sorted([row["id"] for row in rows])
    assert types == expected_types
    assert ids == expected_ids


@pytest.mark.parametrize(
    ("date_dim_data", "expected_ids"),
    [
        ([], {202312, 202401, 202412}),
        ([(202312, 2023, 12), (202401, 2024, 1)], {202412}),
        ([(202312, 2023, 12), (202401, 2024, 1), (202412, 2024, 12)], set()),
    ],
)
def test_create_date_dim_new(
    spark, date_dim_data: List[Tuple[int, int, int]], expected_ids: Set[int]
):
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
    result_df = create_date_dim_new(df=property_df, date_dim_existing=date_dim_existing)
    rows = [row.asDict() for row in result_df.collect()]
    assert {row["id"] for row in rows} == expected_ids


@pytest.mark.parametrize(
    ("location_dim_data", "expected_locations"),
    [
        (
            [],
            [
                "agadir hay hassani",
                "casablanca hay hassani",
                "casablanca oulfa",
                "rabat alirfane",
            ],
        ),
        (
            [
                (1, "casablanca", "oulfa"),
                (2, "casablanca", "hay hassani"),
            ],
            ["agadir hay hassani", "rabat alirfane"],
        ),
        (
            [
                (1, "casablanca", "oulfa"),
                (2, "casablanca", "hay hassani"),
                (3, "rabat", "alirfane"),
                (4, "agadir", "hay hassani"),
            ],
            [],
        ),
    ],
)
def test_create_location_dim_new(
    spark,
    location_dim_data: List[Tuple[int, str, str]],
    expected_locations: List[str],
):
    property_df = spark.createDataFrame(
        [
            ("casablanca", "oulfa"),
            ("casablanca", "oulfa"),
            ("rabat", "alirfane"),
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
    result_df = create_location_dim_new(
        df=property_df, location_dim_existing=location_dim_existing
    )
    rows = [row.asDict() for row in result_df.collect()]
    assert (
        sorted([row["city"] + " " + row["neighborhood"] for row in rows])
        == expected_locations
    )


@pytest.mark.parametrize(
    ("source_dim_data", "expected_sources"),
    [
        ([], ["avito", "yakeey"]),
        ([(1, "avito")], ["yakeey"]),
        ([(1, "avito"), (2, "yakeey")], []),
    ],
)
def test_create_source_dim_new(
    spark, source_dim_data: List[Tuple[int, str]], expected_sources: List[str]
):
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
    result_df = create_source_dim_new(
        df=property_df, source_dim_existing=source_dim_existing
    )
    rows = [row.asDict()["source"] for row in result_df.collect()]
    assert sorted(rows) == expected_sources


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
    spark,
    property_facts_data: List[Tuple[int, int, int, int, int]],
    start_id: int,
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


def test_load_source_dim_to_duckdb(spark):
    duckdb_path = "./data/dw/temp.db"
    try:
        # build temporary datawarehouse
        _test_datawarehouse(duckdb_path)
        # add data to source_dim
        with duckdb.connect(duckdb_path) as conn:
            conn.execute(
                """
                INSERT INTO source_dim VALUES
                    (1, 'avito');
                """
            )
        # create source_dim dataframe
        source_dim_df = spark.createDataFrame([(2, "yakeey")], ["id", "source"])
        # load source_dim dataframe to duckdb
        load_source_dim_to_duckdb(source_dim_df, duckdb_path)
        # check if the data is loaded correctly
        with duckdb.connect(duckdb_path) as conn:
            results = conn.sql("SELECT * FROM source_dim").fetchall()
            assert results == [(1, "avito"), (2, "yakeey")]
    except Exception as e:
        raise AssertionError(f"Test failed: {e}") from None
    finally:
        os.remove(duckdb_path)


def test_load_type_dim_to_duckdb(spark):
    duckdb_path = "./data/dw/temp.db"
    try:
        # build temporary datawarehouse
        _test_datawarehouse(duckdb_path)
        # add data to type_dim
        with duckdb.connect(duckdb_path) as conn:
            conn.execute(
                """
                INSERT INTO type_dim VALUES
                    (1, 'apartment');
                """
            )
        # create type_dim dataframe
        type_dim_df = spark.createDataFrame(
            [
                (2, "studio"),
            ],
            ["id", "type"],
        )
        # load type_dim dataframe to duckdb
        load_type_dim_to_duckdb(type_dim_df, duckdb_path)
        # check if the data is loaded correctly
        with duckdb.connect(duckdb_path) as conn:
            results = conn.sql("SELECT * FROM type_dim").fetchall()
            assert results == [(1, "apartment"), (2, "studio")]
    except Exception as e:
        raise AssertionError(f"Test failed: {e}") from None
    finally:
        os.remove(duckdb_path)


def test_load_location_dim_to_duckdb(spark):
    duckdb_path = "./data/dw/temp.db"
    try:
        # build temporary datawarehouse
        _test_datawarehouse(duckdb_path)
        # add data to location_dim
        with duckdb.connect(duckdb_path) as conn:
            conn.execute(
                """
                INSERT INTO location_dim VALUES
                    (1, 'casablanca', 'oulfa');
                """
            )
        # create location_dim dataframe
        location_dim_df = spark.createDataFrame(
            [
                (2, "casablanca", "maarif"),
            ],
            ["id", "city", "neighborhood"],
        )
        # load location_dim dataframe to duckdb
        load_location_dim_to_duckdb(location_dim_df, duckdb_path)
        # check if the data is loaded correctly
        with duckdb.connect(duckdb_path) as conn:
            results = conn.sql("SELECT * FROM location_dim").fetchall()
            assert results == [(1, "casablanca", "oulfa"), (2, "casablanca", "maarif")]
    except Exception as e:
        raise AssertionError(f"Test failed: {e}") from None
    finally:
        os.remove(duckdb_path)


def test_load_date_dim_to_duckdb(spark):
    duckdb_path = "./data/dw/temp.db"
    try:
        # build temporary datawarehouse
        _test_datawarehouse(duckdb_path)
        # add data to date_dim
        with duckdb.connect(duckdb_path) as conn:
            conn.execute(
                """
                INSERT INTO date_dim VALUES
                    (202301, 2023, 1);
                """
            )
        # create date_dim dataframe
        date_dim_df = spark.createDataFrame(
            [
                (202310, 2023, 10),
            ],
            ["id", "year", "month"],
        )
        # load date_dim dataframe to duckdb
        load_date_dim_to_duckdb(date_dim_df, duckdb_path)
        # check if the data is loaded correctly
        with duckdb.connect(duckdb_path) as conn:
            results = conn.sql("SELECT * FROM date_dim").fetchall()
            assert results == [(202301, 2023, 1), (202310, 2023, 10)]
    except Exception as e:
        raise AssertionError(f"Test failed: {e}") from None
    finally:
        os.remove(duckdb_path)


def test_load_fact_table_to_duckdb(spark):
    try:
        # create test dw table
        duckdb_path = "./data/dw/temp.db"
        _test_datawarehouse(duckdb_path)
        row1 = (
            1,
            "test1",
            1,
            1,
            50,
            50,
            2,
            250000,
            50,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            2,
            202301,
            1,
        )
        row2 = (
            2,
            "test2",
            2,
            1,
            60,
            60,
            2,
            300000,
            100,
            1,
            0,
            0,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
            3,
            2,
            202301,
            1,
        )
        row3 = (
            3,
            "test3",
            2,
            2,
            70,
            75,
            3,
            500000,
            150,
            1,
            0,
            0,
            1,
            1,
            1,
            0,
            1,
            0,
            0,
            2,
            1,
            202310,
            2,
        )
        with duckdb.connect(duckdb_path) as con:
            con.execute(
                f"""
                INSERT INTO source_dim VALUES
                    (1, 'avito'),
                    (2, 'yakeey');
                INSERT INTO type_dim VALUES
                    (1, 'apartment'),
                    (2, 'studio'),
                    (3, 'duplex/triplex');
                INSERT INTO location_dim VALUES
                    (1, 'casablanca', 'oulfa'),
                    (2, 'casablanca', 'maarif'),
                    (3, 'rabat', 'alirfane');
                INSERT INTO date_dim VALUES
                    (202301, 2023, 1),
                    (202310, 2023, 10);
                INSERT INTO property_facts VALUES {row1}
                """
            )
        property_facts = spark.createDataFrame(
            [row2, row3],
            [
                "id",
                "url",
                "n_bedrooms",
                "n_bathrooms",
                "total_area",
                "living_area",
                "floor",
                "price",
                "monthly_syndicate_price",
                "bool_security",
                "bool_elevator",
                "bool_balcony",
                "bool_heating",
                "bool_air_conditioning",
                "bool_concierge",
                "bool_equipped_kitchen",
                "bool_furniture",
                "bool_parking",
                "bool_terrace",
                "location_id",
                "type_id",
                "date_id",
                "source_id",
            ],
        )
        load_fact_table_to_duckdb(property_facts, duckdb_path)
        with duckdb.connect(duckdb_path) as con:
            results = con.sql("SELECT * FROM property_facts").fetchall()
            for row in [row1, row2, row3]:
                assert row in results
    except Exception as e:
        raise AssertionError(f"Test failed! {e}") from None
    finally:
        # delete the test dw
        os.remove(duckdb_path)
