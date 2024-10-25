import streamlit as st
import mysql.connector
from math import ceil
import os

password = os.environ.get('dbmsPWD')
database_name = os.environ.get('dname')

st.set_page_config(layout="wide")

# Define sticky header CSS
sticky_header = """
<style>
.car-card {
        background-color: #0F2D69;  /* Background color */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        transition: transfrom 0.2s, box-shadow 0.2s;
        cursor: pointer;
    }
    .car-card:hover {
        transform: translateY(-5px);  /* Slight lift effect */
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);  /* Shadow effect */
    }
    a {
        text-decoration: none;
        color: inherit;
    }
    .car-card h4 {
        color: #2c3e50;  /* Heading color */
    }
    .car-card p {
        color: #34495e;  /* Text color */
    }
    .car-card strong {
        color: ##0F2D69;  /* Label color */
    }
.sticky {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  background-color: #0F2D69;
  color: white;
  padding: 10px;
  font-size: 20px;
  z-index: 100;
  border-bottom: 2px solid #ccc;
  text-align: center;
}
.content {
  height: 2000px;
}
.car-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    margin: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.car-card h4 {
    color: #0F2D69;
    margin-bottom: 10px;
}
</style>
"""

# Apply the CSS
st.markdown(sticky_header, unsafe_allow_html=True)

# Add the sticky header
st.markdown('<div class="sticky">PrimeMotors</div>', unsafe_allow_html=True)

# Add the rest of your content
st.title("Welcome to PrimeMotors")
st.header("Available Cars")
menu = ["Add Car", "Search Car", "Update Car Status"]
choice = st.sidebar.selectbox("Menu", menu)

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database=database_name
)

cursor = conn.cursor()
query = "SELECT Name, Color, No_of_seats, Price, Type FROM car_model"
cursor.execute(query)
cars = cursor.fetchall()

# Calculate total number of rows needed
total_cars = len(cars)
cars_per_row = 4
total_rows = ceil(total_cars / cars_per_row)

# Create grid layout
for row in range(total_rows):
    # Create three columns for each row
    cols = st.columns(4)
    
    # Fill each column with car details
    for col in range(cars_per_row):
        car_index = row * cars_per_row + col
        
        # Check if we still have cars to display
        if car_index < total_cars:
            car = cars[car_index]
            Name, Color, No_of_seats, Price, Type = car
            
            # Display car details in a card format with button
            with cols[col]:
                # Create unique key using car_index
                
                unique_key = f"btn_{car_index}_{Name}"
                # Add the button
                st.markdown(f"""
                <div class="car-card">
                    <h4>{Name}</h4>
                    <p><strong>Type:</strong> {Type}</p>
                    <p><strong>Color:</strong> {Color}</p>
                    <p><strong>Seats:</strong> {No_of_seats}</p>
                    <p><strong>Price:</strong> {Price:} Rs.</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"View {Name}", key=unique_key):
                    st.session_state.selected_car = Name
                    st.write(f"Selected Car: {Name}")

# Close the database connection
cursor.close()
conn.close()
