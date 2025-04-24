import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import importlib

# Streamlit Page Settings
st.set_page_config(page_title="SmartStock - AI Investment Agent", page_icon="📈", layout="centered")

# Custom CSS
st.markdown("""
<style>
body, .main {
    background-color: #0e1117;
    color: #ffffff;
}

input, textarea, select {
    background-color: #1c1e26 !important;
    color: #ffffff !important;
    border: 1px solid #333 !important;
    border-radius: 8px !important;
    padding: 10px !important;
}

.stButton > button {
    background-color: #22c55e !important;
    color: white !important;
    border-radius: 6px !important;
    font-weight: bold !important;
}

.stButton > button:hover {
    background-color: #16a34a !important;
}

.stTextInput > div > div > input {
    background-color: #1c1e26 !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)


# Dummy DB in session state
if "users" not in st.session_state:
    st.session_state.users = {
        "jeet": "password123",
        "admin": "admin123",
        "testuser": "test123"
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Sidebar switch
page = st.sidebar.selectbox("🔐 Choose Page", ["Login", "Sign Up"])

# If not logged in
if not st.session_state.logged_in:
    st.title("🚀 Welcome to SmartStock 📈")
    st.caption("Your AI-Powered Stock Analysis & Chatbot")
    st.divider()
    add_vertical_space(2)

    if page == "Login":
        st.subheader("🔓 Login to your account")

        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")

        if st.button("Login 🔥"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.success("Logged in successfully! 🎯")
                st.session_state.logged_in = True
                st.session_state.username = username
            else:
                st.error("Invalid username or password! ❌")

    elif page == "Sign Up":
        st.subheader("🆕 Create New Account")

        new_username = st.text_input("👤 New Username")
        new_password = st.text_input("🔑 New Password", type="password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password")

        if st.button("Sign Up 🚀"):
            if new_username in st.session_state.users:
                st.error("Username already exists! ❌")
            elif new_password != confirm_password:
                st.error("Passwords do not match! ❌")
            elif new_username == "" or new_password == "":
                st.error("Fields cannot be empty! ⚠️")
            else:
                st.session_state.users[new_username] = new_password
                st.success("Account created successfully! 🎉 Please login now.")

# After login

else:
    st.title(f"👋 Welcome, {st.session_state.username}!")
    st.subheader("Choose a Module to Begin 📚")

    selected_option = st.radio("🔍 Select a Module", ["Home", "Stock Comparison", "Chatbot"], horizontal=True)

    if selected_option == "Home":
        st.info("Welcome to SmartStock. Please choose a module from above to proceed.")
    
    elif selected_option == "Stock Comparison":
        mod1 = importlib.import_module("modules.module1")
        mod1.run()  # call the run() function you’ll define inside module1.py
    
    elif selected_option == "Chatbot":
        mod2 = importlib.import_module("modules.module2")
        mod2.run()

    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.success("Logged out successfully.")
        st.rerun()