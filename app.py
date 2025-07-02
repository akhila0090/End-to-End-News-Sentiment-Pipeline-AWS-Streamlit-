import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Page config
st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>Latest News</h1>", unsafe_allow_html=True)

# Connect to DB and load data
def load_data():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        cursor.execute("SELECT published_at, source, sentiment_label, title FROM news_articles ORDER BY published_at DESC")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows)
        cursor.close()
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame()

# styling for sentiment
def color_sentiment(val):
    color = ''
    if val == "Positive":
        color = 'background-color: green; color: white; font-weight: bold'
    elif val == "Negative":
        color = 'background-color: red; color: white; font-weight: bold'
    elif val == "Neutral":
        color = 'background-color: lightgray; color: black; font-weight: bold'
    return color

# Display the table
df = load_data()
if not df.empty:
    styled_df = df.style.applymap(color_sentiment, subset=['sentiment_label'])
    st.dataframe(styled_df, use_container_width=True)
else:
    st.warning("No data available.")
