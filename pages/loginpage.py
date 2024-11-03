import streamlit as st
import time
import mysql.connector
import os

admin_username = "admin"
admin_password = "admin"

# Set the page configuration
st.set_page_config(
    page_title="PrimeMotors",
    page_icon="🚗",
    layout="wide"
)

password = os.environ.get('dbmsPWD')
database_name = os.environ.get('dname')
#Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database=database_name)

def update_login(username, password):
    cursor = conn.cursor()
    query = "INSERT INTO login values(%s, %s)"
    cursor.execute(query, (username, password))
    conn.commit()

def get_users():
    cursor = conn.cursor()
    query = "SELECT * FROM login"
    cursor.execute(query)
    results = cursor.fetchall()
    credentials_dict = {row[0]: row[1] for row in results}
    return credentials_dict
    
credentials = get_users()

# Initialize session state variables
if 'users' not in st.session_state:
    st.session_state.users = credentials
if 'current_form' not in st.session_state:
    st.session_state.current_form = None
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'admin' not in st.session_state:
    st.session_state.admin = False

def create_header():
    """Create the header with logo and title"""
    header = st.container()
    with header:
        cols = st.columns([1, 4])
        with cols[0]:
            try:
                st.image("merc logo.jpeg", width=100)
            except:
                st.warning("Logo not found. Please ensure 'merc logo.jpeg' exists in the app directory.")
        with cols[1]:
            st.title("PrimeMotors")
    st.divider()

def signup(username, password):
    """Handle user registration"""
    if not username or not password:
        st.error("Please fill in all fields!")
        return False
    if username in st.session_state.users:
        st.error("Username already exists!")
        return False
    st.session_state.users[username] = password
    update_login(username, password)
    return True

def login(username, password):
    """Handle user login"""
    if not username or not password:
        st.error("Please fill in all fields!")
        return False
    if username not in st.session_state.users:
        st.error("Username not found!")
        return False
    if st.session_state.users[username] != password:
        st.error("Incorrect password!")
        return False
    return True

def show_login_form():
    """Display login form"""
    with st.form("login_form"):
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit_button = st.form_submit_button("Login")
        with col2:
            switch_to_signup = st.form_submit_button("Need to Register?")
        
        if submit_button:
            if login(username, password):
                st.session_state.is_logged_in = True
                st.session_state.current_form = None
                if username == admin_username:
                    st.session_state.admin = True
                    st.success(f"Welcome Sir/Madam! You are now logged in as an admin.")
                    st.rerun()
                st.success(f"Welcome {username}!")
                st.rerun()
                
        if switch_to_signup:
            st.session_state.current_form = "signup"
            st.rerun()

def show_signup_form():
    """Display registration form"""
    with st.form("signup_form"):
        st.subheader("Register")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            submit_button = st.form_submit_button("Register")
        with col2:
            switch_to_login = st.form_submit_button("Already Registered?")
        
        if submit_button:
            if password != confirm_password:
                st.error("Passwords don't match!")
            elif signup(username, password):
                st.success("Registration successful! Please login.")
                st.session_state.current_form = "login"
                st.rerun()
                
        if switch_to_login:
            st.session_state.current_form = "login"
            st.rerun()

def main():
    """Main application logic"""
    create_header()
    
    if st.session_state.admin:
        st.write("You are logged in as admin!")
        time.sleep(1)
        st.switch_page("pages/admin.py")
        if st.button("Logout"):
            st.session_state.admin = False
            st.session_state.is_logged_in = False
            st.session_state.current_form = None
        st.rerun()
            
    if st.session_state.is_logged_in:
        st.write("You are logged in!")
        time.sleep(1)
        st.switch_page("homepage.py")
        if st.button("Logout"):
            st.session_state.admin = False
            st.session_state.is_logged_in = False
            st.session_state.current_form = None
            st.rerun()
    else:
        if st.session_state.current_form == "login":
            show_login_form()
        elif st.session_state.current_form == "signup":
            show_signup_form()
        else:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Login", use_container_width=True):
                    st.session_state.current_form = "login"
                    st.rerun()
            with col2:
                if st.button("Register", use_container_width=True):
                    st.session_state.current_form = "signup"
                    st.rerun()

if __name__ == "__main__":
    main()