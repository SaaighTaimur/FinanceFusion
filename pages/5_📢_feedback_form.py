# Import all necessary modules
import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
import database_feedback as dbf


# Store the page icon and title in variables
PAGE_TITLE = "Feedback Form"
PAGE_ICON = "📢"


# Set the page configuration to the title and icon variables defined above
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


# Create a function to load the lottie gif
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        # Use json to load the file
        return json.load(f)

# Load the lottie
feedback_lottie = load_lottie("lotties/feedback.json")

# Create a function to load the css file
def local_css(file_name):
    with open(file_name) as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

# Call the function and give the css file as the argument
local_css("styles/main.css")

# Set page header
st.title("🗣️ Feedback Form")

# Create 2 columns
col1, col2 = st.columns(2, gap="small")

# Place the instructions in the first column
with col1: 
    st.subheader("\n**Thank you for using this app!**")
    st.write("-⭐ Rate the app out of 5!")
    st.write("-📢 Send any feedback regarding glitches or issues you may be facing to **saaightaimur2@gmail.com**")

# In the second column, place the lottie
with col2:
    st_lottie(
    feedback_lottie,
)

### RATING WEBSITE

# Function to get user's IP address (so that they dont rate the app twice). Use requests for this.
def get_user_ip():
    try:
        return requests.get('https://api64.ipify.org').text
    except requests.RequestException:
        return None

# Store the IP in user_ip variable
user_ip = get_user_ip()

# Set already rated to True if a user_ip exists, and if it is already present in the Deta database file
already_rated = user_ip is not None and dbf.has_user_rated(user_ip)

a, b, c = st.columns(3, gap="small")
with a: 
    if already_rated:
        st.write("You cannot rate again as have already rated the app. Thank you for your feedback!")
    else:
        with a:
            # Create a form
            with st.form("entry_form", clear_on_submit=True):

                # Place a slider in the first column
                slider_rating = st.slider("**Rate the app!**",1,5)

                # Create a button to submit the form
                submitted = st.form_submit_button("Rate!")
                if submitted:
                    # Save the user's IP in the database and print a success message
                    dbf.insert_period(slider_rating, user_ip)
                    st.success("Thank you for your feedback!")

with c:
    average_rating = dbf.get_average_rating()

    # Display the average rating (if it exists)
    if average_rating is not None:
        st.write(f"**Average Rating: {average_rating:.1f} / 5**")

        # Display stars based on the average rating
        stars = "⭐️" * int(average_rating)
        st.write(stars)
    else:
        st.write("No ratings available yet.")


