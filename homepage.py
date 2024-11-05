import streamlit as st
import mysql.connector
from math import ceil
import os
import base64

# Encode the SVG as base64
def load_svg_as_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
st.set_page_config(layout="wide")

def Calculate_total_available():
    query = "SELECT COUNT(*) as count FROM car_model WHERE is_available=1"
    cursor.execute(query)
    values = cursor.fetchall()
    return values[0][0]
    

# st.markdown(
#     """
#     <style>
#     /* Set background color for the main content */
#     .stApp {
#         background-color: #1D3557;  /* Replace with your desired background color */
#     }
#     /* Set background color for the sidebar */
#     section[data-testid="stSidebar"] {
#         background-color: #457B9D;  /* Replace with your desired sidebar color */
#         color: white;  /* Adjust text color for better contrast */
#     }
#     /* Customize text in the sidebar */
#     section[data-testid="stSidebar"] .css-17eq0hr {
#         color: white;  /* Text color */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
    
if 'is_logged_in' not in st.session_state or not st.session_state.is_logged_in:
    st.warning("Please log in to access the main page.")
    if st.button(f"Please Login", key=f"btn_login_signup"):
                    # st.session_state.selected_car = car
                    st.switch_page("pages/loginpage.py")
    st.stop()  # Stop further execution until login is successful

password = os.environ.get('dbmsPWD')
database_name = os.environ.get('dname')

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

.car-card.unavailable {
    background-color: #e9ecef;
    opacity: 0.7;
    pointer-events: none;
}

.car-card:not(.unavailable):hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.unavailable-label {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: #dc3545;
    color: white;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
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
  background-color: teal;  #color of the top primemotors title
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

.btn-view {
    width: 100%;
    padding: 8px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    background-color: #0F2D69;
    color: white;
    margin-top: 10px;
}

.btn-view.unavailable {
    background-color: #6c757d;
    cursor: not-allowed;
    opacity: 0.6;
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



# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database=database_name
)

cursor = conn.cursor()

# Get unique values for filters
cursor.execute("SELECT DISTINCT Name FROM car_brand")
brands = [brand[0] for brand in cursor.fetchall()]
cursor.execute("SELECT DISTINCT No_of_seats FROM car_model")
seats = [seat[0] for seat in cursor.fetchall()]
cursor.execute("SELECT DISTINCT Type FROM car_model")
types = [type[0] for type in cursor.fetchall()]
cursor.execute("SELECT MIN(Price), MAX(Price) FROM car_model")
min_price, max_price = cursor.fetchall()[0]
cursor.execute("SELECT DISTINCT Color FROM car_model")
colors = [color[0] for color in cursor.fetchall()]

# Sidebar filters
st.sidebar.header("Filters")


price_range = st.sidebar.slider(
    "Price Range (Rs.)",
    min_value=float(min_price),
    max_value=float(max_price),
    value=(float(min_price), float(max_price))
)

selected_brand = st.sidebar.selectbox(
    "Brand",
    ["All"] + brands
)

selected_seats = st.sidebar.selectbox(
    "Number of Seats",
    ["All"] + seats
)

selected_type = st.sidebar.selectbox(
    "Vehicle Type",
    ["All"] + types
)

selected_color = st.sidebar.selectbox(
    "Color",
    ["All"] + colors
)

# st.sidebar.markdown("---")  # Add a horizontal line for separation
if st.sidebar.button("Logout"):
    st.session_state.admin = False
    st.session_state.is_logged_in = False
    st.session_state.current_form = None
    st.rerun()
    
    
############
# Build the WHERE clause based on selected filters
where_clauses = []
params = []

if selected_brand != "All":
    where_clauses.append("cb.Name = %s")
    params.append(selected_brand)

if selected_seats != "All":
    where_clauses.append("cm.No_of_seats = %s")
    params.append(selected_seats)

if selected_type != "All":
    where_clauses.append("cm.Type = %s")
    params.append(selected_type)

if selected_color != "All":
    where_clauses.append("cm.Color = %s")
    params.append(selected_color)

where_clauses.append("cm.Price BETWEEN %s AND %s")
params.extend([price_range[0], price_range[1]])


###### change 1
# Construct the final query
query = """
    SELECT cm.is_available, cm.Reg_No, cm.Name, cm.Color, cm.No_of_seats, cm.Price, cm.Type, cb.Name AS Brand 
    FROM car_model cm 
    JOIN car_brand cb ON cm.Brand_id = cb.Brand_id
"""

if where_clauses:
    query += " WHERE " + " AND ".join(where_clauses)

# Execute the filtered query
cursor.execute(query, tuple(params))
cars = cursor.fetchall()

#############


# cursor = conn.cursor()
# # query = "SELECT Name, Color, No_of_seats, Price, Type FROM car_model"
# query = "SELECT cm.Name, cm.Color, cm.No_of_seats, cm.Price, cm.Type, cb.Name AS Brand \
#     FROM car_model cm \
#     JOIN car_brand cb ON cm.Brand_id = cb.Brand_id"
# cursor.execute(query)
# cars = cursor.fetchall()

# total_cars = Calculate_total_available()
# Calculate total number of rows needed
total_Cars = Calculate_total_available()
cars_per_row = 4
total_cars = len(cars) #16
total_rows = ceil(total_cars / cars_per_row) #4

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
            
            ## CHANGE 2
            Status, Reg_no, Name, Color, No_of_seats, Price, Type, Brand = car
            
            ## CHANGE 3
            # Display car details in a card format with button
            with cols[col]:
                # Create unique key using car_index
                svg_base64 = load_svg_as_base64(f"SVG/{Brand.lower()}.svg")
                unique_key = f"btn_{car_index}_{Name}"
                
                 # Add unavailable class if Status is 0
                availability_class = "unavailable" if Status == 0 else ""
                unavailable_label = '<span class="unavailable-label">Not Available</span>' if Status == 0 else ''
                
                
                 # Create the card with conditional styling
                st.markdown(f"""
                <div class="car-card {availability_class}">
                {unavailable_label}
                <h4>{Brand} {Name}</h4>
                <p><strong>Type:</strong> {Type}</p>
                <p><strong>Color:</strong> {Color}</p>
                <p><strong>Seats:</strong> {No_of_seats}</p>
                <p><strong>Price:</strong> Rs. {Price}</p>
                <img src="data:image/svg+xml;base64,{svg_base64}" alt="Brand Logo" class="logo">
                </div>
                """, unsafe_allow_html=True)

                 # Only make the button functional if the car is available
                if Status == 1:
                    if st.button(f"View {Name}", key=f"btn_{car_index}_{Name}"):
                        st.session_state.selected_car = car
                        st.switch_page("pages/carDetails.py")
                else:
                    # Display a disabled button for unavailable cars
                    st.markdown(f"""
                    <button class="btn-view unavailable" disabled>
                        Unavailable!
                    </button>
                    """, unsafe_allow_html=True)

# Redirect to car detail page if a car is selected
if "selected_car" in st.session_state:
    st.session_state.selected_car = False

# Close the database connection
cursor.close()
conn.close()
