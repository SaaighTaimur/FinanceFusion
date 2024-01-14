import streamlit as st
import yfinance as yf
import plotly.express as px
from datetime import datetime

from streamlit_lottie import st_lottie
import json
from streamlit_option_menu import option_menu

PAGE_TITLE = "Stock Tracker"
PAGE_ICON = "📈"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


# Load Lottie file
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

stocks_lottie = load_lottie("lotties/stocks.json")

def local_css(file_name):
    with open(file_name) as css:
        st.markdown("<style>{}</style>".format(css.read()), unsafe_allow_html=True)

local_css("styles/main.css")

st.title("Stock Tracker")

col1, col2 = st.columns(2, gap="small")

with col1:
    st.write("**Welcome to the Stock Tracker app!**")
    st.write("Enter any stock ticker in the left sidebar to view its price chart over a customizable time range (for example, Microsoft --> MSFT)")

    st.write("###")

    # Store the link to Yahoo Finance in a variable
    link = "https://ca.finance.yahoo.com/"

    # Link the Yahoo Finance website for users trying to find stock tickers
    st.write(f"Having trouble? You can find stock tickers on this **[website]({link}).**")
    
    st.write("---")

with col2:
    st_lottie(
    stocks_lottie,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",
)



with st.form("Ticker and Dates Form"):
    ticker = st.text_input("Ticker")
    default_start_date = datetime(2015, 1, 1)
    start_date = st.date_input("Start Date", default_start_date)
    end_date = st.date_input("End Date")

    submitted = st.form_submit_button("Submit")


if submitted:
    # Check if the user has entered a valid ticker
    if ticker:
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:

            ticker_yahoo = yf.Ticker(ticker)
            data_live = ticker_yahoo.history()
            last_quote = data["Close"].iloc[-1]
            st.subheader(ticker.upper())
            st.write(f"**Close Price = ${last_quote:.2f}**")


            # Make sure the data is not empty
            fig = px.line(data, x=data.index, y="Adj Close")
            st.plotly_chart(fig)

            st.subheader("Tips:")
            st.write("- 🔎 Left click and hold to zoom into a specific area of the graph")
            st.write("- ↔️ Left click and drag the axes to move the chart vertically or horizontally")
            st.write("- ⬇️ Click the camera icon to download the chart as a pdf ")
            st.write("- ✣ Click the four-arrow icon to pan around the chart")
            st.write("- 📉 Press the autoscale icon (left of the home symbol) to revert the graph to default settings")

        else:
            st.write("No data available for the given ticker and date range.")
    else:
        st.write("Please enter a valid ticker.")


