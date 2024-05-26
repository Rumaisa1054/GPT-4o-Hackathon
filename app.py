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
    st.title("Logged In as {}".format(username))

    # Input options
    st.header("Enter Term")
    term = st.text_input("Enter term here")

    # Chat area
    st.header("Chat Area")
    chat_text = st.text_area("Chat with us", "")

    # Save course as PDF
    if st.button("Save Course as PDF"):
        save_as_pdf()

    # Notify completion and start evaluation
    if st.button("Notify completion and start evaluation"):
        notify_completion(username)

def save_as_pdf():
    # Add code to save the course content as PDF
    st.success("Course saved as PDF")

def notify_completion(username):
    # Add code to notify completion and start evaluation
    st.success("Completion notified and evaluation started")

# Main function to handle login, registration, and logged-in UI
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        logged_in_ui(st.session_state.username)
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("Go to", ("Login", "Register"))

        if page == "Login":
            st.title("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if authenticate_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password")

        elif page == "Register":
            st.title("Register")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Register"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif username_exists(new_username):
                    st.error("Username already exists. Please choose another one.")
                else:
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
                    conn.commit()
                    st.success("Registration successful for {}".format(new_username))
                    st.session_state.logged_in = True
                    st.session_state.username = new_username
                    st.experimental_rerun()

if __name__ == "__main__":
    main()
