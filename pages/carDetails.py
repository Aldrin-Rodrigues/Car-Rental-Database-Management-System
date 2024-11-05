import streamlit as st
import os
import time
from datetime import datetime, timedelta
import random
import mysql.connector

if 'is_logged_in' not in st.session_state or not st.session_state.is_logged_in:
    st.warning("Please log in to access this page.")
    if st.button(f"Please Login", key=f"btn_login_signup"):
                    # st.session_state.selected_car = car
                    st.switch_page("pages/loginpage.py")
    st.stop()  # Stop further execution until login is successful
    
# def display_total():

def calculate_total(delivery_date, return_date, car_price):
    """Calculate total amount based on dates and car price"""
    total_days = (return_date - delivery_date).days
    base_amount = total_days * car_price
    
    # Calculate discount based on duration
    if total_days >= 30:
        discount = 0.15  # 15% for monthly rental
    elif total_days >= 7:
        discount = 0.10  # 10% for weekly rental
    else:
        discount = 0
    
    discount_amount = base_amount * discount
    tax = (base_amount - discount_amount) * 0.18  # 18% tax
    total_amount = base_amount - discount_amount + tax
    
    return {
        'base_amount': base_amount,
        'discount': discount,
        'discount_amount': discount_amount,
        'tax': tax,
        'total_amount': total_amount
    }

    
def generate_id(prefix, cursor, table, id_column):
    """Generate a unique 4-character ID with given prefix"""
    while True:
        # Generate random 2-digit number
        num = random.randint(0, 99)
        new_id = f"{prefix}{num:02d}"
        
        # Check if ID exists
        cursor.execute(f"SELECT {id_column} FROM {table} WHERE {id_column} = %s", (new_id,))
        if not cursor.fetchone():
            return new_id
        
def generate_int_id(cursr, table, id_column):
    while True:
        num = random.randint(0, 20)
        new_id = f"{num:04d}"
        
        cursr.execute(f"SELECT {id_column} FROM {table} WHERE {id_column} = %s", (new_id,))
        if not cursr.fetchone():
            return new_id

def book_car(reg_no, dealership_id):
    # st.title("Book a Car")
    
    try:
        # Get car details
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cm.Name, cm.Price, cb.Name as Brand
            FROM car_model cm
            JOIN car_brand cb ON cm.Brand_id = cb.Brand_id
            WHERE cm.Reg_No = %s
        """, (reg_no,))
        car_details = cursor.fetchone()
        
        if not car_details:
            st.error("Car not found!")
            return
            
        car_name, car_price, car_brand = car_details
        
        # Display car details
        st.subheader(f"{car_brand} {car_name}")
        st.write(f"Registration Number: {reg_no}")
        st.write(f"Daily Rental Rate: ₹{car_price:,}")
        
        if 'payment_details' not in st.session_state:
            st.session_state.payment_details = None
        
        # Create form
        form = st.form("booking_form")
        with form:
            # Customer Details
            col1, col2 = st.columns(2)
            with col1:
                customer_name = st.text_input("Full Name*", key="name")
                phone_no = st.text_input("Phone Number*", key="phone")
                dl_number = st.text_input("Driving License Number*", key="dl")
                city = st.text_input("City", key="city")
            
            with col2:
                # has_pan = st.checkbox("Has PAN Card")
                # If checkbox is unchecked, clear the PAN number
                # if not has_pan:
                #     st.session_state.pan = ""  # Clear the PAN number from session state
                pan_number = st.text_input("PAN Card Number", key="pan")
                street_name = st.text_input("Street Name", key="street")
                pincode = st.text_input("Pincode*", key="pincode")
            
            st.subheader("Delivery Details")
            col1, col2 = st.columns(2)
            with col1:
                delivery_date = st.date_input("Delivery Date*", min_value=datetime.now().date())
                location = st.text_input("Delivery Location", value="BENGALURU")
            with col2:
                return_date = st.date_input("Return Date*", 
                                          min_value=delivery_date + timedelta(days=1),
                                          value=delivery_date + timedelta(days=1))
                poc = st.text_input("Point of Contact", key="poc", value="Aritro Doe", disabled=True)
            
            st.subheader("Payment Details")
            col1, col2 = st.columns(2)
            with col1:
                payment_mode = st.selectbox("Payment Mode*", 
                                          ["Credit Card", "Debit Card", "UPI", "Net Banking"])
                
                # Add Calculate Total button inside the form
                if st.form_submit_button("Calculate Total"):
                    st.session_state.payment_details = calculate_total(delivery_date, return_date, car_price)             
            
            with col2:
                # Display payment details based on session state
                if st.session_state.payment_details:
                    details = st.session_state.payment_details
                    base_amount, discount, discount_amount, tax, total_amount = st.session_state.payment_details.values()
                    st.write(f"Base Amount: ₹{details['base_amount']:,.2f}")
                    st.write(f"Discount ({details['discount']*100}%): ₹{details['discount_amount']:,.2f}")
                    st.write(f"Tax (18%): ₹{details['tax']:,.2f}")
                    st.write(f"**Total Amount: ₹{details['total_amount']:,.2f}**")
                else:
                    st.write("Click 'Calculate Total' to see payment details")
            
            submitted = form.form_submit_button("Confirm Booking")
        
        # At the beginning of the script, add this with your other session state initializations
        if 'booking_completed' not in st.session_state:
            st.session_state.booking_completed = False
            st.session_state.booking_details = None
            
        # Handle form submission outside the form block
        if submitted:
            required_fields = [customer_name, phone_no, dl_number, pincode, 
                             delivery_date, return_date]
            
            if not all(required_fields):
                st.error("Please fill all required fields marked with *")
                return
            
            if pan_number != "":
                        has_pan = True
                        #print (has_pan) in terminal
                        # print(has_pan)
            else:
                has_pan = False
                #print (has_pan) in terminal
                # print(has_pan)
            
            try:
                cursor = conn.cursor()
                print("in try transaction")
                
                # Start transaction
                cursor.execute("START TRANSACTION")
                
                # 1. Insert Customer
                customer_id = generate_id("C", cursor, "customer", "Customer_ID")
                cursor.execute("""
                    INSERT INTO customer 
                    (Customer_ID, Phone_No, Customer_Name, DL_Number, Pan_Card,
                    Pan_Card_Number, City, Street_Name, Pincode)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (customer_id, phone_no, customer_name, dl_number, 
                    1 if has_pan else 0, pan_number, city, street_name, pincode))
                print("customer done")
                
                # 2. Insert Delivery
                delivery_id = generate_int_id(cursor, "delivery", "Delivery_id")
                print(delivery_id)
                cursor.execute("""
                    INSERT INTO delivery 
                    (Delivery_id, Delivery_Date, Return_Date, Location, POC)
                    VALUES (%s, %s, %s, %s, %s)
                """, (delivery_id, delivery_date, return_date, location, poc))
                # delivery_id = cursor.lastrowid
                print("delivery done")
                
                # 3. Insert Payment
                transaction_id = generate_int_id(cursor, "payment", "Transaction_ID")
                cursor.execute("""
                    INSERT INTO payment 
                    (Transaction_ID, Payment_Date, Payment_Status, Mode, Discount, Tax)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (transaction_id, datetime.now().date(), 1, payment_mode, discount, tax))
                # transaction_id = cursor.lastrowid
                print("payment done")
                
                # 4. Insert Booking
                booking_id = generate_id("B", cursor, "booking", "Booking_ID")
                cursor.execute("""
                    INSERT INTO booking 
                    (Booking_ID, Booking_Date, Reg_No, Transaction_ID, 
                    Insurance_ID, Delivery_ID)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (booking_id, datetime.now().date(), reg_no, transaction_id,
                    1, delivery_id))  # Assuming Insurance_ID 1 is default
                print("booking done")
                
                # 5. Insert into connections table
                cursor.execute("""
                    INSERT INTO Connection 
                    (Dealership_ID, Customer_ID, Booking_ID)
                    VALUES (%s, %s, %s)
                """, (dealership_id, customer_id, booking_id))
                print("connection done")
                
                query = "UPDATE car_model SET is_available=0 WHERE Reg_No=%s"
                cursor.execute(query,(reg_no,))
                print("Made Car Unavailable")
                
                # Commit transaction
                conn.commit()
                print("transaction done")
                
                st.session_state.booking_completed = True
                st.session_state.booking_details = {
                    'booking_id': booking_id,
                    'transaction_id': transaction_id,
                    'total_amount': total_amount,
                    'customer_name': customer_name,
                    'car_brand': car_brand,
                    'car_name': car_name,
                    'reg_no': reg_no,
                    'delivery_date': delivery_date,
                    'return_date': return_date,
                    'location': location
                }
                
            except Exception as e:
                conn.rollback()
                st.error(f"Error processing booking: {str(e)}")

        if st.session_state.booking_completed:
            details = st.session_state.booking_details
            
            st.success(f"""
                Booking Confirmed!
                Booking ID: {details['booking_id']}
                Transaction ID: {details['transaction_id']}
                Total Amount: ₹{details['total_amount']:,.2f}
            """)
            
            # Add download button for booking confirmation
            booking_details = f"""
                Booking Confirmation
                -------------------
                Booking ID: {details['booking_id']}
                Customer Name: {details['customer_name']}
                Vehicle: {details['car_brand']} {details['car_name']}
                Registration: {details['reg_no']}
                Delivery Date: {details['delivery_date']}
                Return Date: {details['return_date']}
                Location: {details['location']}
                Total Amount: ₹{details['total_amount']:,.2f}
                
                Thank you for booking with us!
            """
            
            st.download_button(
                "Download Booking Confirmation",
                booking_details,
                file_name=f"{details['reg_no']}_booking_confirmation_{details['booking_id']}.txt"
            )
            
            st.success(f"Booking confirmed! Booking ID: {details['booking_id']}")
            
            if st.button("Book Another Car"):
                st.session_state.show_booking_form = False
                st.session_state.selected_car = None
                st.session_state.booking_completed = False
                st.session_state.booking_details = None
                st.rerun()
                    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        
if "selected_car" in st.session_state:
    try:
        password = os.environ.get('dbmsPWD')
        database_name = os.environ.get('dname')
        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database=database_name
        )
        
        #chnage 4
        car = st.session_state.selected_car
        print(car)
        Status, Reg_no, Name, Color, No_of_seats, Price, Type, Brand = car
        st.title(f"Your {Brand} {Name}")

        # Display car image and details
        left, right = st.columns([2, 3])
        with left:
            try:
                st.image(f"Images/{Color}{Name}.jpeg", caption=f"{Brand} {Name}", width=400)
            except:
                st.image(f"Images/buggatti.jpeg", caption=f"{Brand} {Name}", width=400)
        with right:
            st.write(f"Type: {Type}")
            st.write(f"Color: {Color}")
            st.write(f"Seats: {No_of_seats}")
            st.write(f"Price: Rs. {Price}")

        # Initialize booking state
        if 'show_booking_form' not in st.session_state:
            st.session_state.show_booking_form = False

        # Show Book Car button only if form isn't shown
        if not st.session_state.show_booking_form:
            if st.button("Book Car"):
                st.session_state.show_booking_form = True
                st.rerun()

        # Show booking form if button was clicked
        if st.session_state.show_booking_form:
            book_car(Reg_no, "D1")
    except Exception as e:
        st.warning("No car selected. Redirecting to home...")
        time.sleep(1)
        st.switch_page("homepage.py")

# Redirect to main page if no car is selected
else:
    st.warning("No car selected. Redirecting to home...")
    time.sleep(1)
    st.switch_page("homepage.py")