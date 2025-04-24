import streamlit as st
import streamlit_extras
from streamlit_extras.add_vertical_space import add_vertical_space

# Dummy user database
if "users" not in st.session_state:
    st.session_state.users = {
        "jeet": "password123",
        "admin": "admin123",
        "testuser": "test123"
    }

# Check if user is already logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Streamlit Page Settings
st.set_page_config(page_title="SmartStock - AI Investment Agent", page_icon="📈", layout="centered")

# Custom CSS for UI
st.markdown(
    """
   <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        padding: 8px;
        border-radius: 5px;
    }
</style>

    """,
    unsafe_allow_html=True
)

# Page Switcher: Login or Sign Up
page = st.sidebar.selectbox("🔐 Choose Page", ["Login", "Sign Up"])

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
                st.experimental_rerun()
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

else:
    st.title(f"👋 Welcome, {st.session_state.username}!")
    st.subheader("Choose a Module to Begin 📚")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📈 Stock Comparison (Module 1)"):
            st.switch_page("module1.py")

    with col2:
        if st.button("🤖 Stock Chatbot (Module 2)"):
            st.switch_page("module2.py")

    add_vertical_space(2)
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.success("Logged out successfully.")
        st.experimental_rerun()
