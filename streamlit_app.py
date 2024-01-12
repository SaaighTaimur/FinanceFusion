import streamlit as st
import json
from streamlit_lottie import st_lottie

# Set page configuration
st.set_page_config(
    page_title="FinanceFusion",
    page_icon="💸"
)

# Load Lottie file
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
working_lottie = load_lottie("lotties/working.json")



# Header
st.image("banner_with_slogan.png")

# Introduction
st.write("""
Welcome to FinanceFusion, your all-in-one financial companion! Explore the following features:

- 💰 **Budget Tool:** Manage your finances effectively.
- 📈 **Stock Tracker:** Keep an eye on your favorite stocks.
- 📊 **Stock Comparison:** Compare different stocks at a glance.

We appreciate your feedback! Please use the 📢 feedback form available to share your thoughts.
""")


# Show lottie
st_lottie(
    working_lottie,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",
)

# Sidebar Message
st.sidebar.success("Select a page above")
