import duckdb

# import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Moroccan Real Estate Analytics")

st.subheader("For sale apartments market")


@st.cache_data
def get_average_price():
    query = """
        SELECT
            AVG(price)
        FROM
            property_facts
    """
    with duckdb.connect("./data/dw/datawarehouse.db") as conn:
        result = conn.execute(query)
        return result.fetchone()[0]


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
    with duckdb.connect("./data/dw/datawarehouse.db") as conn:
        result = conn.execute(query).fetchall()
        return pd.DataFrame(result, columns=["city", "average_price"])


@st.cache_data
def get_price_vs_total_area():
    query = """
        SELECT
            price,
            total_area
        FROM
            property_facts
    """
    with duckdb.connect("./data/dw/datawarehouse.db") as conn:
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
    with duckdb.connect("./data/dw/datawarehouse.db") as conn:
        results = conn.execute(query).fetchall()
        return pd.DataFrame(results, columns=["n_bedrooms", "average_price"])


# TODO: update page layout


# TODO: style graphs


# TODO: add filter widgets on sidebar


# add card component: average apartment price
average_price = get_average_price() / 1_000_000
st.metric("Average Apartment Price", f"{average_price:.2f}M MAD")

# add treemap graph: top 10 most expensive cities
average_price_per_city = get_top10_expensive_cities()
fig = px.treemap(
    average_price_per_city,
    path=["city"],
    values="average_price",
    title="Top 10 Most Expensive Cities",
)
st.plotly_chart(fig)

# add scatterplot: price vs total_area
price_vs_total_area = get_price_vs_total_area()
st.scatter_chart(price_vs_total_area, x="total_area", y="price")

# add barplot: average price per number of bedrooms group
average_price_per_n_bedrooms = get_average_price_per_n_bedrooms()
st.bar_chart(average_price_per_n_bedrooms, x="n_bedrooms", y="average_price")
