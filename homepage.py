import streamlit as st
import mysql.connector
from math import ceil
import os
import base64

# Encode the SVG as base64
def load_svg_as_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
if 'is_logged_in' not in st.session_state or not st.session_state.is_logged_in:
    st.warning("Please log in to access the main page.")
    if st.button(f"Please Login", key=f"btn_login_signup"):
                    # st.session_state.selected_car = car
                    st.switch_page("pages/loginpage.py")
    st.stop()  # Stop further execution until login is successful

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
        transition: transform 0.2s, box-shadow 0.2s;
        cursor: pointer;
        height: 275px;  /* Fixed height */
        overflow: hidden;  /* Prevent text overflow */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative
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
  background-color: blue;  #color of the top primemotors title
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
.logo {
    position: absolute;
    bottom: 5px;
    right: 5px;
    width: 40px; /* Adjust size as needed */
    height: auto;
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

st.sidebar.markdown("---")  # Add a horizontal line for separation
if st.sidebar.button("Logout"):
    st.session_state.is_logged_in = False
    st.session_state.current_form = None
    st.rerun()

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database=database_name
)

cursor = conn.cursor()
# query = "SELECT Name, Color, No_of_seats, Price, Type FROM car_model"
query = "SELECT cm.Name, cm.Color, cm.No_of_seats, cm.Price, cm.Type, cb.Name AS Brand \
    FROM car_model cm \
    JOIN car_brand cb ON cm.Brand_id = cb.Brand_id"
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
            Name, Color, No_of_seats, Price, Type, Brand = car
            
            # Display car details in a card format with button
            with cols[col]:
                # Create unique key using car_index
                svg_base64 = load_svg_as_base64(f"SVG/{Brand.lower()}.svg")
                unique_key = f"btn_{car_index}_{Name}"
                # Add the button
                st.markdown(f"""
                <div class="car-card">
                <h4>{Brand} {Name}</h4>
                <p><strong>Type:</strong> {Type}</p>
                <p><strong>Color:</strong> {Color}</p>
                <p><strong>Seats:</strong> {No_of_seats}</p>
                <p><strong>Price:</strong> Rs. {Price} </p>
                <img src="data:image/svg+xml;base64,{svg_base64}" alt="Brand Logo" class="logo">
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"View {Name}", key=f"btn_{car_index}_{Name}"):
                    st.session_state.selected_car = car
                    st.switch_page("pages/carDetails.py")

# Redirect to car detail page if a car is selected
if "selected_car" in st.session_state:
    st.session_state.remove("selected_car")

# Close the database connection
cursor.close()
conn.close()
