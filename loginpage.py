import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="PrimeMotors",
    page_icon="🚗",
    layout="wide"
)

# Initialize session state variables
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'current_form' not in st.session_state:
    st.session_state.current_form = None
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

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
    
    if st.session_state.is_logged_in:
        st.write("You are logged in!")
        if st.button("Logout"):
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