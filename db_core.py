import pandas as pd
import streamlit as st
import psycopg2
from urllib.parse import urlparse

uri = st.secrets.db_credentials.URI

result = urlparse(uri)
hostname = result.hostname
database = result.path[1:]
username = result.username
pwd = result.password
port_id = result.port


@st.cache_resource
def init_connection():
    return psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id,
    )


con = init_connection()


def fetch_df(query: str, params=None):
    return pd.read_sql_query(query, con=con, params=params)


def fetch_one(query: str, params=None):
    df = fetch_df(query, params=params)
    if df.empty:
        return None
    return df.iloc[0].to_dict()


def execute(query: str, params=None):
    cur = con.cursor()
    try:
        cur.execute(query, params)
        con.commit()
    finally:
        cur.close()
