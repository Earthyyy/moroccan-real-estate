from typing import List, Tuple

import duckdb

# import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from config import Config

# TODO: improve code organization and error handling

st.set_page_config(
    page_title=Config.PAGE_TITLE, page_icon=Config.PAGE_ICONE, layout="wide"
)

st.title(Config.PAGE_TITLE)
st.subheader("For sale apartments market")


@st.cache_data
def get_average_price(
    cities_filter: List[str],
    total_area_filter: Tuple[int, int],
    n_bedrooms_filter: Tuple[int, int],
) -> float:
    """Get the average apartment price to display in the card metric

    Args:
        cities_filter (List[str]): The cities list to filter on
        total_area_filter (Tuple[int, int]): A tuple with min and max for total_area
        n_bedrooms_filter (Tuple[int, int]): A tuple with min and max for n_bedrooms

    Returns:
        float: The average price
    """
    query = """
        SELECT
            AVG(pf.price)
        FROM
            property_facts pf
        JOIN
            location_dim ld
        ON
            pf.location_id = ld.id
        WHERE
            ld.city IN ?
            AND
            pf.total_area BETWEEN ? AND ?
            AND
            pf.n_bedrooms BETWEEN ? AND ?
    """
    with duckdb.connect(Config.PATH_TO_DW) as conn:
        result = conn.execute(
            query,
            [
                cities_filter,
                *total_area_filter,
                *n_bedrooms_filter,
            ],
        ).fetchone()
        return result[0] if result else None


@st.cache_data
def get_top10_expensive_cities(
    total_area_filter: Tuple[int, int],
    n_bedrooms_filter: Tuple[int, int],
) -> pd.DataFrame:
    """Get the top 10 most expensive cities based on the average apartment price

    Args:
        total_area_filter (Tuple[int, int]): A tuple with min and max for total_area
        n_bedrooms_filter (Tuple[int, int]): A tuple with min and max for n_bedrooms

    Returns:
        pd.DataFrame: Resulting table
    """
    query = """
        SELECT
            ld.city,
            AVG(pf.price)
        FROM
            property_facts pf
        JOIN
            location_dim ld
        ON
            pf.location_id = ld.id
        WHERE
            pf.total_area BETWEEN ? AND ?
            AND
            pf.n_bedrooms BETWEEN ? AND ?
        GROUP BY
            1
        ORDER BY
            2 DESC
        LIMIT 10
    """
    with duckdb.connect(Config.PATH_TO_DW) as conn:
        result = conn.execute(
            query,
            [
                *total_area_filter,
                *n_bedrooms_filter,
            ],
        ).fetchall()
        return pd.DataFrame(result, columns=["city", "average_price"])


@st.cache_data
def get_price_vs_total_area(
    cities_filter: List[str],
    total_area_filter: Tuple[int, int],
    n_bedrooms_filter: Tuple[int, int],
) -> pd.DataFrame:
    """Get the price and total_area facts

    Args:
        cities_filter (List[str]): The cities list to filter on
        total_area_filter (Tuple[int, int]): A tuple with min and max for total_area
        n_bedrooms_filter (Tuple[int, int]): A tuple with min and max for n_bedrooms

    Returns:
        pd.DataFrame: Resulting table
    """
    query = """
        SELECT
            pf.price,
            pf.total_area
        FROM
            property_facts pf
        JOIN
            location_dim ld
        ON
            pf.location_id = ld.id
        WHERE
            ld.city IN ?
            AND
            pf.total_area BETWEEN ? AND ?
            AND
            pf.n_bedrooms BETWEEN ? AND ?
    """
    with duckdb.connect(Config.PATH_TO_DW) as conn:
        result = conn.execute(
            query,
            [
                cities_filter,
                *total_area_filter,
                *n_bedrooms_filter,
            ],
        ).fetchall()
        return pd.DataFrame(result, columns=["price", "total_area"])


@st.cache_data
def get_average_price_per_n_bedrooms(
    cities_filter: List[str],
    total_area_filter: Tuple[int, int],
    n_bedrooms_filter: Tuple[int, int],
) -> pd.DataFrame:
    """Get the average price for each group of bedrooms number

    Args:
        cities_filter (List[str]): The cities list to filter on
        total_area_filter (Tuple[int, int]): A tuple with min and max for total_area
        n_bedrooms_filter (Tuple[int, int]): A tuple with min and max for n_bedrooms

    Returns:
        pd.DataFrame: Resulting table
    """
    query = """
        SELECT
            pf.n_bedrooms,
            AVG(pf.price)
        FROM
            property_facts pf
        JOIN
            location_dim ld
        ON
            pf.location_id = ld.id
        WHERE
            ld.city IN ?
            AND
            pf.total_area BETWEEN ? AND ?
            AND
            pf.n_bedrooms BETWEEN ? AND ?
        GROUP BY
            1
        ORDER BY
            2 DESC
    """
    with duckdb.connect(Config.PATH_TO_DW) as conn:
        result = conn.execute(
            query,
            [
                cities_filter,
                *total_area_filter,
                *n_bedrooms_filter,
            ],
        ).fetchall()
        return pd.DataFrame(result, columns=["n_bedrooms", "average_price"])


@st.cache_data
def get_distinct_cities() -> List[str]:
    """Get the distinct cities from the location dim table

    Returns:
        List[str]: List of cities
    """
    query = """
        SELECT
            DISTINCT city
        FROM
            location_dim
    """
    with duckdb.connect(Config.PATH_TO_DW) as conn:
        result = conn.execute(query).fetchall()
        return [row[0] for row in result]


@st.cache_data
def get_min_max_col(column: str) -> Tuple[int, int]:
    """Get the min and max values of a numerical column

    Args:
        column (str): Column name in the fact table

    Returns:
        Tuple[int, int]: Tuple containing two values, min and max
    """
    query = f"""
        SELECT
            MIN({column}),
            MAX({column})
        FROM
            property_facts
    """
    with duckdb.connect(Config.PATH_TO_DW) as conn:
        result = conn.execute(query).fetchone()
        return (int(result[0]), int(result[1])) if result else (0, 0)


# city filter
cities = get_distinct_cities()
cities_filter = st.sidebar.multiselect("City", sorted(cities))
if not cities_filter:
    cities_filter = cities

# area filter
min_area, max_area = get_min_max_col("total_area")
area_filter = st.sidebar.slider(
    "Area (Total)", min_value=min_area, max_value=max_area, value=(min_area, max_area)
)

# bedrooms filter
min_n_bedrooms, max_n_bedrooms = get_min_max_col("n_bedrooms")
n_bedrooms_filter = st.sidebar.slider(
    "Bedrooms (Total)",
    min_value=min_n_bedrooms,
    max_value=max_n_bedrooms,
    value=(min_n_bedrooms, max_n_bedrooms),
)

# data and graph elements
average_price = (
    get_average_price(cities_filter, area_filter, n_bedrooms_filter) / 1_000_000
)
average_price_per_n_bedrooms = get_average_price_per_n_bedrooms(
    cities_filter, area_filter, n_bedrooms_filter
)
price_vs_total_area = get_price_vs_total_area(
    cities_filter, area_filter, n_bedrooms_filter
)
average_price_per_city = get_top10_expensive_cities(area_filter, n_bedrooms_filter)
fig = px.treemap(
    average_price_per_city,
    path=["city"],
    values="average_price",
    title="Top 10 Most Expensive Cities",
)

# page layout

# card component: average apartment price
st.metric("Average Apartment Price", f"{average_price:.2f}M MAD")

col1, _, col2 = st.columns([1, .1, 1])
# scatterplot: price vs total_area
col1.scatter_chart(
    price_vs_total_area,
    x="total_area",
    y="price",
    x_label="Total Area (m²)",
    y_label="Price (MAD)",
    width=300,
    height=300
)
# barplot: average price per number of bedrooms group
col2.bar_chart(
    average_price_per_n_bedrooms,
    x="n_bedrooms",
    y="average_price",
    x_label="Price (MAD)",
    y_label="# Bedrooms",
    horizontal=True,
    width=300,
    height=300
)

# treemap graph: top 10 most expensive cities
st.plotly_chart(fig)
