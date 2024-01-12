# Import necessary modules
from deta import Deta
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

# Initialize with a project key
deta = Deta(DETA_KEY)

# Connect to database
db = deta.Base("monthly_reports")


# Insert a row (the key is the unique identifier)
def insert_period(period, incomes, expenses, username):
    return db.put({"key": period, "incomes": incomes, "expenses": expenses, "username": username})



def fetch_periods_by_username(username):
    try:
        # Query the database to fetch periods for the specified username
        periods = db.fetch({"username": username})
        
        if periods:
            return periods.items  # Return the fetched periods
        else:
            return []  # If no periods found, return an empty list
    except Exception as e:
        # Handle exceptions, such as connection errors or malformed responses
        st.error(f"Error fetching periods: {e}")
        return []  # Return an empty list in case of an error
    
# Return all rows
def fetch_all_periods():
    # Returns a dictionary of all periods
    res = db.fetch()
    return res.items

# Return a specific row
def get_period(period):
    # If there is no period, then the function will throw a None value
    return db.get(period)


