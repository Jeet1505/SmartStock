import streamlit as st
from authentication import login, sign_up, is_logged_in, get_logged_in_user,login_user
from modules.module1 import run_module_1
from modules.module2 import run_module_2

# Load custom CSS for dark theme
st.markdown(
    """
    <link href="style/custom.css" rel="stylesheet" type="text/css">
    """, 
    unsafe_allow_html=True
)

def show_login_form():
    """Function to show login form."""
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state["user"] = username
            st.success("Logged in successfully!")
            st.experimental_rerun()  # Reload the page to show the modules
        else:
            st.error("Invalid credentials!")

def show_signup_form():
    """Show sign-up form."""
    st.title("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if password == confirm_password:
        if st.button("Sign Up"):
            if sign_up(username, email, password):
                st.success("User created successfully!")
                st.script_runner.rerun()  # Reload the app to show login
            else:
                st.error("Username already exists.")
    else:
        st.error("Passwords do not match.")


# Main page logic
if not is_logged_in():
    # Show login or sign up based on the user's choice
    login_or_signup = st.radio("Choose an option", ("Login", "Sign Up"))

    if login_or_signup == "Login":
        show_login_form()
    else:
        show_signup_form()
else:
    # If logged in, show the username and options to navigate to modules
    st.sidebar.header(f"Welcome, {get_logged_in_user()}!")

    option = st.sidebar.selectbox("Select Module", ["Home", "Module 1", "Module 2"])

    if option == "Home":
        st.title("Welcome to SmartStock")
        st.write("Select a module from the sidebar to get started.")

    elif option == "Module 1":
        st.title("Stock Comparison")
        run_module_1()

    elif option == "Module 2":
        st.title("Multimodal Chatbot")
        run_module_2()
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
def show_login():
    st.title("Login to SmartStock")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state['authenticated'] = True
            st.success("Login successful!")
        else:
            st.error("Invalid credentials.")
if st.session_state['authenticated']:
    st.success("You're logged in! Choose your action:")
    option = st.radio("What would you like to do?", ["Stock Comparison", "Gemini PDF Chatbot"])
    
    if option == "Stock Comparison":
        # run module 1
        import modules.module1 as m1
        m1.run_module()
    
    elif option == "Gemini PDF Chatbot":
        import modules.module2 as m2
        m2.run_module()
else:
    show_login()
