# Import all necessary modules
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from streamlit_lottie import st_lottie

import json
import calendar
from datetime import datetime

import database as db


# Add page title, icon, and layout setting
page_title = "Budgeting Tool"
page_icon = "💰"
layout = "centered" 

# Configure page settings
st.set_page_config(page_title = page_title, page_icon = page_icon, layout = layout )

# Use st.title to create a title
st.title(page_title + " " + page_icon)

# Define a function to load the Lottie file (basically a gif)
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        # Use json to load the file
        return json.load(f)

### Introduction

# Create two columns
col1, col2 = st.columns(2, gap="small")

# Place the instructions in the first column
with col1: 
    st.write("\n**Instructions:**")
    st.write("- 📈 Select the \"Data Entry\" for inputting income and expense values.")
    st.write("- 📉 Select the \"Data Visualization\" for viewing helpful charts relating to your incomes and expenses.")
    st.write("- ⭐ NOTE: This information is stored in a Deta database. You will only be able to visualize data if you have entered it under \"Data Entry\. Furthermore, the correct username will be required, and if none is found, then no data will be displayed.")

    st.write("- ✨ Also, try to create a unique username so that your information is not easily accessible.")



# Define the lottie
money_lottie = load_lottie("lotties/budget.json")

# Add the lottie file in the second column
with col2:
    st_lottie(
    money_lottie,
)






# Create lists to store income and expense types
incomes = ["Monthly Salary/Wage", "Other Income"]
expenses = ["Rent", "Utilities", "Groceries", "Car", "Other Expenses", "Saving"]

# Add dropdown menus to select years and months (only 2023 and 2024 for now)
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])


# Use CSS to hide default elements (this part is not written by me, I don't remember CSS)
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



### Create a navigation menu
selected = option_menu(
    menu_title = None,
    # Include the two tabs (data entry and data visualization)
    options = ["Data Entry", "Data Visualization"],
    # Add icons and adjust orientation to horizontal (looks better)
    icons = ["pencil-fill", "bar-chart-fill"],
    orientation = "horizontal"
)

### DATA ENTRY
if selected == "Data Entry":

    # Create a form
    with st.form("entry_form", clear_on_submit=True):

        # Ask user to input username
        username = st.text_input("Type username: (don't press Enter just yet, or it will autocomplete the form)")

        # Create two columns
        col1, col2 = st.columns(2)
        # Retrieve the month the user selected in the first column
        col1.selectbox("Select Month:", months, key="month")
        # Do the same with the year, but in the second column
        col2.selectbox("Select Year:", years, key="year")

        "---"
        # Create an expander for all the different income types
        with st.expander("Income"):
            # Iterate through each income to create a number input for each
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
        
        # Create an expander for all the different expense types
        with st.expander("Expenses"):
            # Do the same for expenses
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)


        "---"
        # Create a save data button
        submitted = st.form_submit_button("Save Data")
        if submitted:
            # Save the period by joining the year and the month (with _ in the middle)
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"])
            
            # Use dict comprehension to iterate over incomes/expenses and get value for each income/expese
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}

            # Insert row into database
            db.insert_period(period, incomes, expenses, username)

            # Print success message
            st.success("Data saved!")



### DATA VISUALIZATION
if selected == "Data Visualization":
    # Header
    st.header("Data Visualization")
    
    # Enter username
    username = st.text_input("Enter username: (will not work if username not found in database)")

    # If user enters username, then execute this code
    if username:
        # Fetch all periods with the associated username
        periods = db.fetch_periods_by_username(username)
        
        # If periods are found, then run this code
        if periods:
            # Ask the user to select a period from all the ones that are found
            selected_period = st.selectbox("Select a period:", [period['key'] for period in periods])
            
            # If a period is selected, then display button to plot period
            if selected_period:
                submitted = st.button("Plot Period")
                
                # If button  pressed, then retrieve all necessary data from database and show visualizations
                if submitted:
                    # Get dictionary of data
                    period_data = db.get_period(selected_period)
                    if period_data:
                        # Return the expenses
                        expenses = period_data.get("expenses")
                        # Return the income
                        incomes = period_data.get("incomes")

                        # Create 3 stats: total income, total expense, and remaining budget (find using basic math)
                        total_income = sum(incomes.values())
                        total_expense = sum(expenses.values())
                        remaining_budget = total_income - total_expense
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Total Income", f"{total_income} CAD")
                        col2.metric("Total Expense", f"{total_expense} CAD")
                        col3.metric("Remaining Budget", f"{remaining_budget} CAD")


                        ### INCOME PIE CHARTS + BAR CHARTS
                        col1, col2 = st.columns(2)

                        # Create and display a pie chart for income distribution in the first column
                        with col1:
                            st.subheader("Income Distribution")
                            fig_income = go.Figure(data=[go.Pie(labels=list(incomes.keys()), values=list(incomes.values()))])
                            st.plotly_chart(fig_income, use_container_width=True)

                        # Create and display a bar chart showing different incomes
                        with col2:
                            fig_income = go.Figure(data=[go.Bar(x=list(incomes.keys()), y=list(incomes.values()))])
                            st.plotly_chart(fig_income, use_container_width=True)

                        # EXPENSE PIE CHARTS + BAR CHARTS      
                        col1, col2 = st.columns(2)

                        # Create and display a pie chart for expense distribution in the first column
                        with col1:
                            st.subheader("Expense Distribution")
                            fig_expense = go.Figure(data=[go.Pie(labels=list(expenses.keys()), values=list(expenses.values()))])
                            st.plotly_chart(fig_expense, use_container_width=True)

                        # Create and display a bar chart showing different expenses
                        with col2:
                            fig_expense = go.Figure(data=[go.Bar(x=list(expenses.keys()), y=list(expenses.values()))])
                            st.plotly_chart(fig_expense, use_container_width=True)
                        
                        ### CREATE A INCOME -> EXPENSE DISTRIBUTION CHART 
                        st.subheader("Income -> Expense Distribution Chart")
                        # Combine all income categories with Total Income and all expense categories
                        label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
                        # Create a list of values by combined incomes with expenses
                        value = list(incomes.values()) + list(expenses.values())
                        # Create a list for the index positions of the incomes
                        source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
                        # Every income will have the total income as the target. The expenses have their own index position as the target
                        target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]

                        # These 3 lines of code make the chart (its built-in)
                        link = dict(source=source, target=target, value=value)
                        node = dict(label=label, pad=20, thickness=30, color="#E694FF")
                        data = go.Sankey(link=link, node=node)

                        # Store the chart data
                        chart = go.Figure(data)
                        # Set constant dimensions
                        chart.update_layout(margin=dict(l=0, r=0, t=5, b=5))
                        # Plot the chart
                        st.plotly_chart(chart, use_container_width=True)

