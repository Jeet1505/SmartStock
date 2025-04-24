import json
import streamlit as st
import requests
# Mock database for users
USER_DB = "users.json"

def load_users():
    """Load users from the mock database (users.json)."""
    try:
        with open(USER_DB, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    """Save users to the mock database (users.json)."""
    with open(USER_DB, "w") as file:
        json.dump(users, file)

def is_logged_in():
    """Check if the user is logged in by checking session state."""
    return "user" in st.session_state

def get_logged_in_user():
    """Return the username of the logged-in user."""
    return st.session_state["user"] if is_logged_in() else None

def login(username, password):
    """Handle user login."""
    users = load_users()
    if username in users and users[username]["password"] == password:
        return True
    return False

def sign_up(username, email, password):
    """Handle user signup."""
    users = load_users()
    if username in users:
        return False  # Username already exists

    # Save new user
    users[username] = {"email": email, "password": password}
    save_users(users)
    return True
def login_user(username, password):
    url = "http://127.0.0.1:8000/accounts/api/login/"
    response = requests.post(url, json={"username": username, "password": password})
    return response.status_code == 200
