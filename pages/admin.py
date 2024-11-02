import streamlit as st
import time
import os
import mysql.connector
import pandas as pd

if 'admin' not in st.session_state or not st.session_state.admin:
    st.warning("Please log in as an admin to access this page.")
    if st.button(f"Please Login", key=f"btn_login_signup"):
                    st.switch_page("pages/loginpage.py")
    st.stop()  # Stop further execution until login is successful
# if 'is_logged_in' not in st.session_state or not st.session_state.is_logged_in:
#     st.warning("Please log in to access this page.")
#     if st.button(f"Please Login", key=f"btn_login_signup"):
#                     # st.session_state.selected_car = car
#                     st.switch_page("pages/loginpage.py")
#     st.stop()  # Stop further execution until login is successful


menu = ["Add Car", "Update Car Price", "Delete Car", "View All Cars", "Write a Query"]
choice = st.sidebar.selectbox("Menu", menu)
# st.sidebar.markdown("---")  # Add a horizontal line for separation
if st.sidebar.button("Logout"):
    st.session_state.admin = False
    st.session_state.is_logged_in = False
    st.session_state.current_form = None
    st.rerun()

password = os.environ.get('dbmsPWD')
database_name = os.environ.get('dname')
#Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database=database_name)



def add_Car():
    st.title("Add a new car")
    
    form_fields = {
        "car_registration": "",
        "car_engine_number": "",
        "car_chassis_number": "",
        "car_color": "",
        "car_brand": "",
        "car_model": "",
        "car_seats": 1,
        "car_price": 0,
        "car_type": "Sedan"
    }
    
    car_registration = st.text_input("Car Registration", key="car_registration")
    car_engine_number = st.text_input("Engine Number", key="car_engine_number")
    car_chassis_number = st.text_input("Chassis Number", key="car_chassis_number")
    car_color = st.text_input("Car Color", key="car_color")
    car_brand = st.text_input("Car Brand", key="car_brand")
    car_model = st.text_input("Car Model", key="car_model")
    car_seats = st.number_input("Number of Seats", min_value=1, max_value=10, key="car_seats")
    car_price = st.number_input("Price", min_value=0, key="car_price")
    car_type = st.selectbox("Car Type", ["Sedan", "SUV", "Hatchback", "Sports Car"], key="car_type")

    if st.button("Add Car"):
        try:
            cursor = conn.cursor()
            query = "INSERT INTO car_model (Reg_No, Engine_No, Chassis_No, Color, Name, No_of_seats, Price, Type, Brand_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, (SELECT Brand_id FROM car_brand WHERE Name = %s))"
            cursor.execute(query, (car_registration, car_engine_number, car_chassis_number, car_color, car_model, car_seats, car_price, car_type, car_brand))
            conn.commit()
            
            if cursor.rowcount > 0:
                st.success("Car added successfully!")
            else:
                st.warning("An error occurred. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    # Wait, then clear form fields
        # time.sleep(2)
        # for key in form_fields:
        #     st.session_state[key] = ""  # Clear each field

def Update_Car_Details():
    st.title("Update Car Details")
    
    form_fields = {
        "car_reg": "",
        "car_price": 0
    }
    
    for key, value in form_fields.items():
        if key not in st.session_state:
            st.session_state[key] = value
            
    car_reg = st.text_input("Enter Car Registration", key="car_reg")
    car_price = st.number_input("Enter New Price", min_value=0, key="car_price")
    
    if st.button("Update Car Details"):
        try:
            cursor = conn.cursor()
            cursor.callproc("UpdateCarPrice", (car_reg, car_price))
            conn.commit()

            if cursor.rowcount > 0:
                st.success("Car details updated successfully!")
            else:
                st.warning("No car found with the entered registration number. Please enter a valid registration number.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            
            
def Delete_Car():
    st.title("Delete Car")
    
    form_fields = {
        "car_reg": "",
    }
    
    for key, value in form_fields.items():
        if key not in st.session_state:
            st.session_state[key] = value
            
    car_reg = st.text_input("Enter Car Registration", key="car_reg")
    
    if st.button("Delete Car"):
        try:
            cursor = conn.cursor()
            query = "DELETE FROM car_model WHERE Reg_No = %s"
            cursor.execute(query, (car_reg,))
            conn.commit()

            # Check if any row was affected
            if cursor.rowcount > 0:
                st.success("Car deleted successfully!")
            else:
                st.warning("No car found with the entered registration number. Please enter a valid registration number.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            
        
def View_All_Cars():
    st.title("All Cars")
    
    cursor = conn.cursor()
    query = """
        SELECT 
            cm.Reg_No,
            cm.Name,
            cm.Color,
            cm.No_of_seats,
            cm.Price,
            cm.Type,
            cb.Name AS Brand
        FROM car_model cm
        JOIN car_brand cb ON cm.Brand_id = cb.Brand_id
    """
    cursor.execute(query)
    cars = cursor.fetchall()

    # Convert the data to a format suitable for a dataframe
    car_data = []
    for car in cars:
        Reg_No, Name, Color, No_of_seats, Price, Type, Brand = car
        car_data.append({
            "Registration": Reg_No,
            "Model": Name,
            "Brand": Brand,
            "Type": Type,
            "Color": Color,
            "Seats": No_of_seats,
            "Price (Rs.)": f"{Price:,}",  # Format price with commas
            "Actions": Reg_No  # We'll use this to create unique buttons
        })

    # Create DataFrame
    if car_data:
        df = pd.DataFrame(car_data)
        
        # Apply custom styling
        st.markdown("""
        <style>
        .stDataFrame table {
            width: 100%;
        }
        .stDataFrame td {
            text-align: left !important;
        }
        .stDataFrame th {
            text-align: left !important;
            background-color: #f0f2f6;
        }
        </style>
        """, unsafe_allow_html=True)

        # Create two columns for search and filter
        col1, col2 = st.columns(2)
        
        # Add search functionality
        with col1:
            search = st.text_input("Search cars", "")
            if search:
                df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

        # Add type filter
        with col2:
            types = df['Type'].unique()
            selected_type = st.selectbox("Filter by Type", ['All'] + list(types))
            if selected_type != 'All':
                df = df[df['Type'] == selected_type]

        # Display the table
        st.dataframe(
            df.drop('Actions', axis=1),  # Drop the Actions column as we'll handle it separately
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No cars found in the database.")    
        
def Query():
    st.title("Write a Query")
    
    query = st.text_area("Enter your query here", height=100)
    
    if st.button("Run Query"):
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            # conn.commit()
            
            if results:
                st.table(results)
            else:
                st.info("No results found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if choice == "Add Car":
    add_Car()
elif choice == "Update Car Price":
    Update_Car_Details()
elif choice == "Delete Car":
    Delete_Car()
elif choice == "View All Cars":
    View_All_Cars()
elif choice == "Write a Query":
    Query()
    
    