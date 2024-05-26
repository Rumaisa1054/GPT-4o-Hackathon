import streamlit as st
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('user.db')
c = conn.cursor()

# Create a table to store user information if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT)''')
conn.commit()

# Function to check if a username already exists
def username_exists(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

# Function to authenticate user
def authenticate_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

# Logged-in UI
def logged_in_ui(username):
    st.title("Logged")
    st.write("Welcome to the logged-in page, {}!".format(username))
    # Add your logged-in UI components here

# Main function to handle login, registration, and logged-in UI
def main():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")
    register_button = st.button("Register")

    if login_button:
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            logged_in_ui(username)
        else:
            st.error("Invalid username or password")
    elif register_button:
        if username_exists(username):
            st.error("Username already exists. Please choose another one.")
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            st.success("Registration successful for {}".format(username))
            st.session_state.logged_in = True
            logged_in_ui(username)

if __name__ == "__main__":
    main()
