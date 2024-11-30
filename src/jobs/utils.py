from pyspark.sql import SparkSession
from pyspark.sql import types as T

COLUMNS = [
    "url",
    "n_bedrooms",
    "n_bathrooms",
    "total_area",
    "living_area",
    "floor",
    "price",
    "monthly_syndicate_price",
    "city",
    "neighborhood",
    "type",
    "year",
    "month",
    "source",
    "bool_elevator",
    "bool_balcony",
    "bool_heating",
    "bool_air_conditioning",
    "bool_concierge",
    "bool_equipped_kitchen",
    "bool_furniture",
    "bool_parking",
    "bool_security",
    "bool_terrace",
]

# schemas

DF_SCHEMA = T.StructType(
    [
        T.StructField("url", T.StringType(), nullable=False),
        T.StructField("n_bedrooms", T.IntegerType(), nullable=True),
        T.StructField("n_bathrooms", T.IntegerType(), nullable=True),
        T.StructField("total_area", T.IntegerType(), nullable=True),
        T.StructField("living_area", T.IntegerType(), nullable=True),
        T.StructField("floor", T.IntegerType(), nullable=True),
        T.StructField("price", T.IntegerType(), nullable=True),
        T.StructField("monthly_syndicate_price", T.DoubleType(), nullable=True),
        T.StructField("city", T.StringType(), nullable=False),
        T.StructField("neighborhood", T.StringType(), nullable=False),
        T.StructField("type", T.StringType(), nullable=False),
        T.StructField("year", T.IntegerType(), nullable=False),
        T.StructField("month", T.IntegerType(), nullable=False),
        T.StructField("source", T.StringType(), nullable=False),
        T.StructField("bool_elevator", T.IntegerType(), nullable=True),
        T.StructField("bool_balcony", T.IntegerType(), nullable=True),
        T.StructField("bool_heating", T.IntegerType(), nullable=True),
        T.StructField("bool_air_conditioning", T.IntegerType(), nullable=True),
        T.StructField("bool_concierge", T.IntegerType(), nullable=True),
        T.StructField("bool_equipped_kitchen", T.IntegerType(), nullable=True),
        T.StructField("bool_furniture", T.IntegerType(), nullable=True),
        T.StructField("bool_parking", T.IntegerType(), nullable=True),
        T.StructField("bool_security", T.IntegerType(), nullable=True),
        T.StructField("bool_terrace", T.IntegerType(), nullable=True),
    ]
)


def spark_setup(app_name: str = "ETL") -> SparkSession:
    duckdb_jdbc_jar = "./libs/duckdb_jdbc.jar"
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.jars", duckdb_jdbc_jar)
        .config("spark.driver.extraClassPath", duckdb_jdbc_jar)
        .getOrCreate()
    )
