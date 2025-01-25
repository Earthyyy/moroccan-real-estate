from typing import List, Tuple

import duckdb

# import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

PATH_TO_DW = "./data/dw/datawarehouse.db"

st.title("Moroccan Real Estate Analytics")

st.subheader("For sale apartments market")

# TODO: link filters to visuals
# TODO: add docstrings and typing
# TODO: style graphs
# TODO: update page layout
# TODO: add year/month filter


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
            total_area BETWEEN ? AND ?
            AND
            n_bedrooms BETWEEN ? AND ?
    """
    with duckdb.connect(PATH_TO_DW) as conn:
        result = conn.execute(
            query,
            [
                cities_filter,
                *total_area_filter,
                *n_bedrooms_filter,
            ],
        )
        value = result.fetchone()
        return value[0] if value else None


@st.cache_data
def get_top10_expensive_cities():
    query = """
        SELECT
            ld.city,
            ROUND(AVG(pf.price), 2) average_price
        FROM
            property_facts pf
        JOIN
            location_dim ld
        ON
            pf.location_id = ld.id
        GROUP BY
            1
        ORDER BY
            2 DESC
        LIMIT 10
    """
    with duckdb.connect(PATH_TO_DW) as conn:
        result = conn.execute(query).fetchall()
        return pd.DataFrame(result, columns=["city", "average_price"])


@st.cache_data
def get_price_vs_total_area():  # TODO: load only a sample of data
    query = """
        SELECT
            price,
            total_area
        FROM
            property_facts
    """
    with duckdb.connect(PATH_TO_DW) as conn:
        results = conn.execute(query).fetchall()
        return pd.DataFrame(results, columns=["price", "total_area"])


@st.cache_data
def get_average_price_per_n_bedrooms():
    query = """
        SELECT
            n_bedrooms,
            AVG(price) average_price
        FROM
            property_facts
        GROUP BY
            1
        ORDER BY
            2 DESC
    """
    with duckdb.connect(PATH_TO_DW) as conn:
        results = conn.execute(query).fetchall()
        return pd.DataFrame(results, columns=["n_bedrooms", "average_price"])


@st.cache_data
def get_distinct_cities():
    query = """
        SELECT
            DISTINCT city
        FROM
            location_dim
    """
    with duckdb.connect(PATH_TO_DW) as conn:
        results = conn.execute(query).fetchall()
        return [row[0] for row in results]


@st.cache_data
def get_min_max_col(column: str):
    query = f"""
        SELECT
            MIN({column}),
            MAX({column})
        FROM
            property_facts
    """
    with duckdb.connect(PATH_TO_DW) as conn:
        return conn.execute(query).fetchone()


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
st.write(area_filter)

# bedrooms filter
min_n_bedrooms, max_n_bedrooms = get_min_max_col("n_bedrooms")
n_bedrooms_filter = st.sidebar.slider(
    "Bedrooms (Total)",
    min_value=min_n_bedrooms,
    max_value=max_n_bedrooms,
    value=(min_n_bedrooms, max_n_bedrooms),
)

# card component: average apartment price
average_price = (
    get_average_price(cities_filter, area_filter, n_bedrooms_filter) / 1_000_000
)
st.metric("Average Apartment Price", f"{average_price:.2f}M MAD")

# treemap graph: top 10 most expensive cities
average_price_per_city = get_top10_expensive_cities()
fig = px.treemap(
    average_price_per_city,
    path=["city"],
    values="average_price",
    title="Top 10 Most Expensive Cities",
)
st.plotly_chart(fig)

# scatterplot: price vs total_area
price_vs_total_area = get_price_vs_total_area()
st.scatter_chart(price_vs_total_area, x="total_area", y="price")

# barplot: average price per number of bedrooms group
average_price_per_n_bedrooms = get_average_price_per_n_bedrooms()
st.bar_chart(average_price_per_n_bedrooms, x="n_bedrooms", y="average_price")
