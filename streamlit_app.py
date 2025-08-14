# streamlit_app.py
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="Food Waste Management", layout="wide")

st.title("🥗 Local Food Waste Management Dashboard")

# --- Sidebar ---
st.sidebar.header("Data Source")
db_path = st.sidebar.text_input("SQLite Database Path", "food_waste.db")

# --- Connect to DB ---
@st.cache_data
def load_table(table_name):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# --- EDA ---
st.header("Exploratory Data Analysis")
tab1, tab2 = st.tabs(["Tables Overview", "Charts"])

with tab1:
    providers = load_table("providers")
    receivers = load_table("receivers")
    food_listings = load_table("food_listings")
    claims = load_table("claims")

    st.subheader("Providers")
    st.dataframe(providers)
    st.write(providers.describe())

    st.subheader("Receivers")
    st.dataframe(receivers)
    st.write(receivers.describe())

    st.subheader("Food Listings")
    st.dataframe(food_listings)
    st.write(food_listings.describe())

    st.subheader("Claims")
    st.dataframe(claims)
    st.write(claims.describe())

with tab2:
    # Example: Providers per city
    city_counts = providers['City'].value_counts()
    fig, ax = plt.subplots()
    city_counts.plot(kind='bar', ax=ax)
    ax.set_title("Providers per City")
    st.pyplot(fig)

    # Claims status pie chart
    status_counts = claims['Status'].value_counts()
    fig, ax = plt.subplots()
    status_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel("")
    st.pyplot(fig)

# --- Query Insights ---
st.header("Query Insights")
queries = {
    "Providers per City": "SELECT city, COUNT(*) as count FROM providers GROUP BY city ORDER BY count DESC",
    "Receivers per City": "SELECT city, COUNT(*) as count FROM receivers GROUP BY city ORDER BY count DESC",
    "Most Common Food Types": "SELECT food_type, COUNT(*) as count FROM food_listings GROUP BY food_type ORDER BY count DESC",
}

query_name = st.selectbox("Select a Query", list(queries.keys()))
if st.button("Run Query"):
    conn = sqlite3.connect(db_path)
    df_result = pd.read_sql_query(queries[query_name], conn)
    conn.close()

    st.dataframe(df_result)

    # Optional chart
    if "count" in df_result.columns:
        fig, ax = plt.subplots()
        df_result.set_index(df_result.columns[0])['count'].plot(kind='bar', ax=ax)
        st.pyplot(fig)
