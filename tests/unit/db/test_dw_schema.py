import pytest

from src.db.dw_schema import (
    create_date_dim,
    create_location_dim,
    create_property_facts,
    create_source_dim,
    create_type_dim,
    setup_duckdb,
)


@pytest.fixture(scope="module")
def db_connection():
    con = setup_duckdb(":memory:")
    yield con
    con.close()


def test_create_date_dim(db_connection):
    # create date dim table
    create_date_dim(db_connection)
    result = db_connection.execute("PRAGMA table_info(date_dim)").fetchdf()

    expected_structure = [
        ("id", "INTEGER", True, 1),  # Primary key
        ("year", "INTEGER", True, 0),  # No constraints
        ("month", "INTEGER", False, 0),  # No constraints
    ]
    for i, (col_name, col_type, notnull, pk) in enumerate(expected_structure):
        assert (
            result.iloc[i]["name"] == col_name
        ), f"Column name mismatch for {col_name}"
        assert (
            result.iloc[i]["type"] == col_type
        ), f"Column type mismatch for {col_name}"
        assert result.iloc[i]["notnull"] == (
            1 if notnull else 0
        ), f"Not-null constraint mismatch for {col_name}"
        assert (
            result.iloc[i]["pk"] == pk
        ), f"Primary key constraint mismatch for {col_name}"


def test_create_source_dim(db_connection):
    # create date dim table
    create_source_dim(db_connection)
    result = db_connection.execute("PRAGMA table_info(source_dim)").fetchdf()

    expected_structure = [
        ("id", "INTEGER", True, 1),  # Primary key
        ("source", "VARCHAR", True, 0),  # No constraints
    ]

    for i, (col_name, col_type, notnull, pk) in enumerate(expected_structure):
        assert (
            result.iloc[i]["name"] == col_name
        ), f"Column name mismatch for {col_name}"
        assert (
            result.iloc[i]["type"] == col_type
        ), f"Column type mismatch for {col_name}"
        assert result.iloc[i]["notnull"] == (
            1 if notnull else 0
        ), f"Not-null constraint mismatch for {col_name}"
        assert (
            result.iloc[i]["pk"] == pk
        ), f"Primary key constraint mismatch for {col_name}"


def test_create_type_dim(db_connection):
    # create date dim table
    create_type_dim(db_connection)
    result = db_connection.execute("PRAGMA table_info(type_dim)").fetchdf()

    expected_structure = [
        ("id", "INTEGER", True, 1),  # Primary key
        ("type", "ENUM('apartment', 'studio', 'duplex/triplex')", True, 0),
    ]

    for i, (col_name, col_type, notnull, pk) in enumerate(expected_structure):
        assert (
            result.iloc[i]["name"] == col_name
        ), f"Column name mismatch for {col_name}"
        assert (
            result.iloc[i]["type"] == col_type
        ), f"Column type mismatch for {col_name}"
        assert result.iloc[i]["notnull"] == (
            1 if notnull else 0
        ), f"Not-null constraint mismatch for {col_name}"
        assert (
            result.iloc[i]["pk"] == pk
        ), f"Primary key constraint mismatch for {col_name}"


def test_create_location_dim(db_connection):
    # create date dim table
    create_location_dim(db_connection)
    result = db_connection.execute("PRAGMA table_info(location_dim)").fetchdf()

    expected_structure = [
        ("id", "INTEGER", True, 1),  # Primary key
        ("city", "VARCHAR", True, 0),  # No constraints
        ("neighborhood", "VARCHAR", False, 0),
    ]

    for i, (col_name, col_type, notnull, pk) in enumerate(expected_structure):
        assert (
            result.iloc[i]["name"] == col_name
        ), f"Column name mismatch for {col_name}"
        assert (
            result.iloc[i]["type"] == col_type
        ), f"Column type mismatch for {col_name}"
        assert result.iloc[i]["notnull"] == (
            1 if notnull else 0
        ), f"Not-null constraint mismatch for {col_name}"
        assert (
            result.iloc[i]["pk"] == pk
        ), f"Primary key constraint mismatch for {col_name}"


def test_create_property_facts(db_connection):
    # Create date table
    db_connection.execute(
        """
    CREATE TABLE IF NOT EXISTS date_dim(
                          id INTEGER NOT NULL PRIMARY KEY)
    """
    )

    db_connection.execute(
        """
    CREATE TABLE IF NOT EXISTS source_dim(
                          id INTEGER NOT NULL PRIMARY KEY)
    """
    )

    db_connection.execute(
        """
    CREATE TABLE IF NOT EXISTS location_dim(
                          id INTEGER NOT NULL PRIMARY KEY)
    """
    )

    db_connection.execute(
        """
    CREATE TABLE IF NOT EXISTS type_dim(
                          id INTEGER NOT NULL PRIMARY KEY)
    """
    )

    # Create the fact table
    create_property_facts(db_connection)
    result = db_connection.execute("PRAGMA table_info(property_facts)").fetch_df()

    expected_structure = [
        ("id", "INTEGER", True, 1),
        ("url", "VARCHAR", True, 0),
        ("n_bedrooms", "INTEGER", False, 0),
        ("n_bathrooms", "INTEGER", False, 0),
        ("total_area", "INTEGER", False, 0),
        ("living_area", "INTEGER", False, 0),
        ("floor", "INTEGER", False, 0),
        ("price", "INTEGER", False, 0),
        ("syndicate_price_per_month", "DOUBLE", False, 0),
        ("bool_security", "INTEGER", False, 0),
        ("bool_elevator", "INTEGER", False, 0),
        ("bool_balcony", "INTEGER", False, 0),
        ("bool_heating", "INTEGER", False, 0),
        ("bool_air_conditioning", "INTEGER", False, 0),
        ("bool_concierge", "INTEGER", False, 0),
        ("bool_equipped_kitchen", "INTEGER", False, 0),
        ("bool_furniture", "INTEGER", False, 0),
        ("bool_parking", "INTEGER", False, 0),
        ("bool_terrace", "INTEGER", False, 0),
        ("location_id", "INTEGER", False, 0),
        ("type_id", "INTEGER", False, 0),
        ("date_id", "INTEGER", False, 0),
        ("source_id", "INTEGER", False, 0),
    ]
    for i, (col_name, col_type, notnull, pk) in enumerate(expected_structure):
        assert (
            result.iloc[i]["name"] == col_name
        ), f"Column name mismatch for {col_name}"
        assert (
            result.iloc[i]["type"] == col_type
        ), f"Column type mismatch for {col_name}"
        assert result.iloc[i]["notnull"] == (
            1 if notnull else 0
        ), f"Not-null constraint mismatch for {col_name}"
        assert (
            result.iloc[i]["pk"] == pk
        ), f"Primary key constraint mismatch for {col_name}"
