import duckdb as db


def setup_duckdb(database: str) -> db.DuckDBPyConnection:
    """Create a connection with a database

    Args:
        database (str): The name of the database

    Returns:
        db.DuckDBPyConnection: The connection
    """
    return db.connect(database=database)


def create_property_facts(con: db.DuckDBPyConnection) -> None:
    """Create the fact table

    Args:
        con (db.DuckDBPyConnection): The connection to the database
    """
    con.execute(
        """CREATE TABLE IF NOT EXISTS property_facts(
        id INTEGER NOT NULL PRIMARY KEY,
        url VARCHAR NOT NULL,
        n_bedrooms INTEGER,
        n_bathrooms INTEGER,
        total_area INTEGER,
        living_area INTEGER,
        floor INTEGER,
        price INTEGER,
        monthly_syndicate_price DOUBLE,
        bool_security INTEGER CHECK (bool_security >= 0 AND bool_security <= 1),
        bool_elevator INTEGER CHECK (bool_elevator >= 0 AND bool_elevator <= 1),
        bool_balcony INTEGER CHECK (bool_balcony >= 0 AND bool_balcony <= 1),
        bool_heating INTEGER CHECK (bool_heating >= 0 AND bool_heating <= 1),
        bool_air_conditioning INTEGER CHECK (bool_air_conditioning >= 0
        AND bool_air_conditioning <= 1),
        bool_concierge INTEGER CHECK (bool_concierge >= 0 AND bool_concierge <= 1),
        bool_equipped_kitchen INTEGER CHECK (bool_equipped_kitchen >= 0
        AND bool_equipped_kitchen <= 1),
        bool_furniture INTEGER CHECK (bool_furniture >= 0 AND bool_furniture <= 1),
        bool_parking INTEGER CHECK (bool_parking >= 0 AND bool_parking <= 1),
        bool_terrace INTEGER CHECK (bool_terrace >= 0 AND bool_terrace <= 1),
        location_id INTEGER REFERENCES location_dim(id),
        type_id INTEGER REFERENCES type_dim(id),
        date_id INTEGER REFERENCES date_dim(id),
        source_id INTEGER REFERENCES source_dim(id)
    )
    """
    )


def create_date_dim(con: db.DuckDBPyConnection) -> None:
    """Create the date dimension table

    Args:
        con (db.DuckDBPyConnection): The connection to the database
    """
    con.execute(
        """CREATE TABLE IF NOT EXISTS date_dim(
                id INTEGER PRIMARY KEY NOT NULL,
                year INTEGER NOT NULL,
                month INTEGER CHECK (month >= 1 AND month <= 12))
                """
    )


def create_source_dim(con: db.DuckDBPyConnection) -> None:
    """Create the source dimension table

    Args:
        con (db.DuckDBPyConnection): The connection to the database
    """
    con.execute(
        """CREATE TABLE IF NOT EXISTS source_dim(
                id INTEGER PRIMARY KEY NOT NULL,
                source VARCHAR NOT NULL)
                """
    )


def create_location_dim(con: db.DuckDBPyConnection) -> None:
    """Create the location dimension table

    Args:
        con (db.DuckDBPyConnection): The connection to the database
    """
    con.execute(
        """CREATE TABLE IF NOT EXISTS location_dim(
                id INTEGER PRIMARY KEY NOT NULL,
                city VARCHAR NOT NULL,
                neighborhood VARCHAR)
                """
    )


def create_type_dim(con: db.DuckDBPyConnection) -> None:
    """Create the type dimension table

    Args:
        con (db.DuckDBPyConnection): The connection to the database
    """
    con.execute(
        """CREATE TABLE IF NOT EXISTS type_dim(
                id INTEGER NOT NULL PRIMARY KEY,
                type VARCHAR NOT NULL )
                """
    )


def main(database):
    con = setup_duckdb(database)
    create_date_dim(con)
    create_location_dim(con)
    create_type_dim(con)
    create_source_dim(con)
    create_property_facts(con)
    con.close()


if __name__ == "__main__":

    dev_dw = "./data/dw/datawarehouse.db"
    backup_dw = "./data/dw/backup_datawarehouse.db"

    main(dev_dw)
    main(backup_dw)
