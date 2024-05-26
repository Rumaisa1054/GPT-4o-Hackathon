import streamlit as st
import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('user.db')
c = conn.cursor()

# Create a table to store user information if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT)''')
conn.commit()

# Function to authenticate user
def authenticate_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

# Logged-in UI
def logged_in_ui(username):
    st.title("Logged")
    st.write("Welcome to the logged-in page, {}!".format(username))
    # Add your logged-in UI components here

# Main function to display the login form and redirect if logged in
def main():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_user(username, password):
            redirect_url = "logged.py?username={}".format(username)
            st.markdown(f'<meta http-equiv="refresh" content="0;URL=/{redirect_url}">', unsafe_allow_html=True)
        else:
            st.error("Invalid username or password")

if __name__ == "__main__":
    main()

