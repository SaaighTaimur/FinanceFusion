# Import all the necessary modules
import streamlit as st
import json
from streamlit_lottie import st_lottie

# Set page configuration
st.set_page_config(
    page_title="FinanceFusion",
    page_icon="💸"
)

# Create a function to load the Lottie file
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
        
# Call the function    
working_lottie = load_lottie("lotties/working.json")

# Create a function to load the CSS
def local_css(file_name):
    with open(file_name) as css:
        st.markdown("<style>{}</style>".format(css.read()), unsafe_allow_html=True)

# Load the CSS by inputting the path of the file
local_css("styles/main.css")

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


# Show the lottie and set its configurations
st_lottie(
    working_lottie,
    speed=1,
    reverse=False,
    loop=True,
    quality="low",
)

# Sidebar Message
st.sidebar.success("Select a page above")
