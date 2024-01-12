# Import modules
from deta import Deta
import os
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv(".env")
DETA_KEY = "b087ba26v2x_vXRLfJMxPpfJ84VgFBEG3WdRLAN4kSXt"

# Initialize with a project key
deta = Deta(DETA_KEY)

# Connect to database
db = deta.Base("ratings")

# This function will insert a period
def insert_period(slider_rating, user_ip):
    # Create a unique identifier for the period (not necessary in this project, but I'm using basically the same system from my last project)
    unique_id = str(uuid.uuid4())

    # Store the unique_id, slider_rating, and user_ip  
    data = {
        "id": unique_id,
        "rating": slider_rating,
        "user_ip": user_ip  
    }

    return db.put(data)


# This function will get the average rating of all users
def get_average_rating():
    # Get all ratings from the database
    all_ratings = list(db.fetch().items)
    
    # If there are no ratings, then return None
    if not all_ratings:
        return None
    
    # Calculate the average rating by adding them all up and dividing them by the number of ratings
    total_ratings = len(all_ratings)
    total_sum = sum(item["rating"] for item in all_ratings)
    average_rating = total_sum / total_ratings
    
    return average_rating


# This function will check if the user has already rated the app
def has_user_rated(user_ip):
    # Check if the user's IP has already rated the app
    result = db.fetch({"user_ip": user_ip})

    # If length is greater than 0, then it will return True, meaning that the user has already rated the app. Otherwise, if the length is 0, then it will return False (as 0 is not greater than 0)
    return len(list(result.items)) > 0
