import streamlit as st
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
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


menu = ["Add Car", "Update Car Price","Update Car Status", "Delete Car", "View All Cars", "Write a Query", "Service Data"]
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
        "car_type": "Sedan",
        "car_lastService": "",
        "car_nextService": "",
        "car_serviceCost": 0
    }
    
    #change 5 default is_available to 0
    car_registration = st.text_input("Car Registration", key="car_registration")
    car_engine_number = st.text_input("Engine Number", key="car_engine_number")
    car_chassis_number = st.text_input("Chassis Number", key="car_chassis_number")
    car_color = st.text_input("Car Color", key="car_color")
    car_brand = st.text_input("Car Brand", key="car_brand")
    car_brand_id = st.text_input("Car Brand ID", key="car brand id")
    car_model = st.text_input("Car Model", key="car_model")
    car_seats = st.number_input("Number of Seats", min_value=1, max_value=10, key="car_seats")
    car_price = st.number_input("Price", min_value=0, key="car_price")
    car_type = st.selectbox("Car Type", ["Sedan", "SUV", "Hatchback", "Sports Car", "MPV"], key="car_type")
    car_available = st.number_input("Availability", key="car_available", value=0)
    car_lastService = st.date_input("Car Last Serviced On", key="car_lastService")
    car_nextService = st.date_input("Car Next Service On", key="car_nextService", value=car_lastService + relativedelta(months=6), disabled=True)
    car_serviceCost = st.number_input("Cost Of Last Service", key="car_serviceCost", value=0)

    if st.button("Add Car"):
        try:
            ##change 6 add variable is_available
            cursor = conn.cursor()
            # query = "INSERT INTO car_model (Reg_No, Engine_No, Chassis_No, Color, Name, No_of_seats, Price, Type, Brand_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, (SELECT Brand_id FROM car_brand WHERE Name = %s))"
            query1 = "INSERT INTO car_model (Reg_No, Engine_No, Chassis_No, Color, Name, No_of_seats, Price, Type, Brand_ID, is_available) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query1, (car_registration, car_engine_number, car_chassis_number, car_color, car_model, car_seats, car_price, car_type, car_brand_id, car_available))
            subquery = "SELECT (SELECT Service_ID FROM service ORDER BY Service_ID DESC LIMIT 1) + 1 AS New_Service_ID;"
            cursor.execute(subquery)
            result = cursor.fetchall()[0][0]
            query2 = "INSERT INTO service (Service_ID, Last_service_Date, Next_service_Date, Last_service_cost, Reg_No) VALUES (%s, %s, %s, %s, %s);"
            cursor.execute(query2, (result, car_lastService, car_nextService, car_serviceCost, car_registration))
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
            
##CHANGE 6
#add fucniton to make car available

def Update_Car_Status():
    st.title("Update Car Availability")
    
    form_fields = {
        "car_reg": "",
        "Status": 0
    }
    
    for key, value in form_fields.items():
        if key not in st.session_state:
            st.session_state[key] = value
            
    car_reg = st.text_input("Enter Car Registration", key="car_reg")
    car_availability = st.number_input("Status", min_value=0, key="car_availability")
    
    if st.button("Update Car status"):
        try:
            cursor = conn.cursor()
            cursor.callproc("UpdateCarStatus", (car_reg, car_availability))
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
            query1 = "DELETE FROM car_model WHERE Reg_No = %s"
            cursor.execute(query1, (car_reg,))
            conn.commit()

            # Check if any row was affected
            if cursor.rowcount > 0:
                st.success("Car deleted successfully!")
            else:
                st.warning("No car found with the entered registration number. Please enter a valid registration number.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            


# def View_All_Cars():
#     st.title("All Cars")
    
#     cursor = conn.cursor()
#     query = """
#         SELECT 
#             cm.Reg_No,
#             cm.Name,
#             cm.Color,
#             cm.No_of_seats,
#             cm.Price,
#             cm.Type,
#             cb.Name AS Brand
#         FROM car_model cm
#         JOIN car_brand cb ON cm.Brand_id = cb.Brand_id
#     """
#     cursor.execute(query)
#     cars = cursor.fetchall()

#     # Convert the data to a format suitable for a dataframe
#     car_data = []
#     for car in cars:
#         Reg_No, Name, Color, No_of_seats, Price, Type, Brand = car
#         car_data.append({
#             "Registration": Reg_No,
#             "Model": Name,
#             "Brand": Brand,
#             "Type": Type,
#             "Color": Color,
#             "Seats": No_of_seats,
#             "Price (Rs.)": f"{Price:,}",  # Format price with commas
#             "Actions": Reg_No  # We'll use this to create unique buttons
#         })

#     # Create DataFrame
#     if car_data:
#         df = pd.DataFrame(car_data)
        
#         # Apply custom styling
#         st.markdown("""
#         <style>
#         .stDataFrame table {
#             width: 100%;
#         }
#         .stDataFrame td {
#             text-align: left !important;
#         }
#         .stDataFrame th {
#             text-align: left !important;
#             background-color: #f0f2f6;
#         }
#         </style>
#         """, unsafe_allow_html=True)

#         # Create two columns for search and filter
#         col1, col2 = st.columns(2)
        
#         # Add search functionality
#         with col1:
#             search = st.text_input("Search cars", "")
#             if search:
#                 df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

#         # Add type filter
#         with col2:
#             types = df['Type'].unique()
#             selected_type = st.selectbox("Filter by Type", ['All'] + list(types))
#             if selected_type != 'All':
#                 df = df[df['Type'] == selected_type]

#         # Display the table
#         st.dataframe(
#             df.drop('Actions', axis=1),  # Drop the Actions column as we'll handle it separately
#             hide_index=True,
#             use_container_width=True
#         )
#     else:
#         st.info("No cars found in the database.")  
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
            cm.is_available,
            cb.Name AS Brand
        FROM car_model cm
        JOIN car_brand cb ON cm.Brand_id = cb.Brand_id
    """
    cursor.execute(query)
    cars = cursor.fetchall()
    
    # Convert the data to a format suitable for a dataframe
    car_data = []
    for car in cars:
        Reg_No, Name, Color, No_of_seats, Price, Type, is_available, Brand = car
        car_data.append({
            "Registration": Reg_No,
            "Model": Name,
            "Brand": Brand,
            "Type": Type,
            "Color": Color,
            "Seats": No_of_seats,
            "Price (Rs.)": f"{Price:,}",  # Format price with commas
            "Status": "Available" if is_available == 1 else "Not Available",
            "Actions": Reg_No  # We'll use this to create unique buttons
        })

    # Create DataFrame
    if car_data:
        df = pd.DataFrame(car_data)
        
        # Apply custom styling with updated status colors
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
            .available {
                color: green;
                font-weight: bold;
            }
            .not-available {
                color: red;
                font-weight: bold;
            }
            </style>
        """, unsafe_allow_html=True)

        # Create three columns for search, type filter, and availability filter
        col1, col2, col3 = st.columns(3)

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

        # Add availability filter
        with col3:
            availability = st.selectbox("Filter by Availability", ['All', 'Available', 'Not Available'])
            if availability != 'All':
                df = df[df['Status'] == availability]

        # Style the Status column
        def style_status(val):
            color = 'green' if val == 'Available' else 'red'
            return f'color: {color}; font-weight: bold'

        # Apply styling to the DataFrame
        styled_df = df.drop('Actions', axis=1).style.applymap(
            style_status,
            subset=['Status']
        )

        # Display the table
        st.dataframe(
            styled_df,
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
            
def View_Due_Services():
    st.title("Vehicles Due for Service")
    
    # Get current date
    current_date = datetime.now().date()
    
    # Create cursor and execute query to get vehicles due for service
    # Join with car_model to get vehicle details
    cursor = conn.cursor()
    query = """
        SELECT 
            s.Service_ID,
            s.Reg_No,
            cm.Name as Model_Name,
            cb.Name as Brand_Name,
            s.Last_service_Date,
            s.Next_service_Date,
            s.Last_service_cost,
            DATEDIFF(s.Next_service_Date, CURRENT_DATE) as Days_Until_Due
        FROM service s
        JOIN car_model cm ON s.Reg_No = cm.Reg_No
        JOIN car_brand cb ON cm.Brand_id = cb.Brand_id
        WHERE s.Next_service_Date IS NOT NULL
        ORDER BY Days_Until_Due ASC
    """
    cursor.execute(query)
    services = cursor.fetchall()

    if services:
        # Convert to DataFrame
        service_data = []
        for service in services:
            Service_ID, Reg_No, Model_Name, Brand_Name, Last_service_Date, Next_service_Date, Last_service_cost, Days_Until_Due = service
            
            # Determine status and color
            if Days_Until_Due < 0:
                status = "Overdue"
                status_color = "red"
            elif Days_Until_Due <= 7:
                status = "Due This Week"
                status_color = "orange"
            elif Days_Until_Due <= 30:
                status = "Due This Month"
                status_color = "yellow"
            else:
                status = "Upcoming"
                status_color = "green"
            
            service_data.append({
                "Service ID": Service_ID,
                "Registration": Reg_No,
                "Vehicle": f"{Brand_Name} {Model_Name}",
                "Last Service": Last_service_Date.strftime('%Y-%m-%d') if Last_service_Date else "N/A",
                "Next Service": Next_service_Date.strftime('%Y-%m-%d') if Next_service_Date else "N/A",
                "Days Until Due": Days_Until_Due,
                "Status": status,
                "Last Cost": f"₹{Last_service_cost:,}" if Last_service_cost else "N/A"
            })

        df = pd.DataFrame(service_data)
        
        # Add filters
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=['Overdue', 'Due This Week', 'Due This Month', 'Upcoming'],
                default=['Overdue', 'Due This Week']
            )
        
        with col2:
            days_threshold = st.slider(
                "Show vehicles due within days",
                min_value=31,
                max_value=90,
                value=50
            )
        
        # Apply filters
        filtered_df = df[
            (df['Status'].isin(status_filter)) &
            (df['Days Until Due'] <= days_threshold)
        ]
        
        # Custom styling
        st.markdown("""
        <style>
        .overdue {
            color: red;
            font-weight: bold;
        }
        .due-soon {
            color: orange;
            font-weight: bold;
        }
        .due-month {
            color: #B7B72E;
        }
        .upcoming {
            color: green;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Due Services", len(filtered_df))
        with col2:
            overdue_count = len(filtered_df[filtered_df['Status'] == 'Overdue'])
            st.metric("Overdue Services", overdue_count)
        with col3:
            due_week = len(filtered_df[filtered_df['Status'] == 'Due This Week'])
            st.metric("Due This Week", due_week)
        with col4:
            due_month = len(filtered_df[filtered_df['Status'] == 'Due This Month'])
            st.metric("Due This Month", due_month)
        
        # Display the table
        if not filtered_df.empty:
            st.dataframe(
                filtered_df.style.apply(lambda x: [
                    'color: red' if x['Status'] == 'Overdue' else
                    'color: orange' if x['Status'] == 'Due This Week' else
                    'color: #B7B72E' if x['Status'] == 'Due This Month' else
                    'color: green'
                    for i in x
                ], axis=1),
                hide_index=True,
                use_container_width=True
            )
            
            # Add action buttons for each service
            st.markdown("### Actions")
            for idx, row in filtered_df.iterrows():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{row['Vehicle']}** (Reg: {row['Registration']})")
                with col2:
                    st.write(f"Next Service: {row['Next Service']}")
                with col3:
                    if st.button("Mark Complete", key=f"complete_{row['Service ID']}"):
                        try:
                            # Calculate next service date (e.g., 6 months from now)
                            next_service = current_date + timedelta(days=180)
                            
                            cursor = conn.cursor()
                            update_query = """
                                UPDATE service 
                                SET Last_service_Date = CURRENT_DATE,
                                    Next_service_Date = %s
                                WHERE Service_ID = %s
                            """
                            cursor.execute(update_query, (next_service, row['Service ID']))
                            conn.commit()
                            
                            if cursor.rowcount > 0:
                                st.success(f"Service marked as completed for {row['Vehicle']}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.warning("Failed to update service record.")
                        except Exception as e:
                            st.error(f"Error updating service record: {str(e)}")
        else:
            st.info("No vehicles found matching the current filters.")
    else:
        st.info("No vehicles are currently due for service.")

if choice == "Add Car":
    add_Car()
elif choice == "Update Car Price":
    Update_Car_Details()
elif choice == "Update Car Status":
    Update_Car_Status()
elif choice == "Delete Car":
    Delete_Car()
elif choice == "View All Cars":
    View_All_Cars()
elif choice == "Write a Query":
    Query()
elif choice == "Service Data":
    View_Due_Services()

    
    