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

# Login Page
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Check login credentials
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if c.fetchone() is not None:
            st.success("Logged in as {}".format(username))
            # Store username in session state for redirection
            st.session_state.username = username
            st.experimental_rerun()  # Force rerun to perform redirection
        else:
            st.error("Invalid username or password")

# Registration Page
def register():
    st.title("Register")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        # Check if username already exists
        if username_exists(new_username):
            st.error("Username already exists. Please choose another one.")
        # Check if passwords match
        elif new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            # Add new user to the database
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()
            st.success("Registration successful for {}".format(new_username))

# Main function to switch between login and registration pages
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Login", "Register"))
    if page == "Login":
        login()
    elif page == "Register":
        register()

    # Redirect to logged.py if logged in
    if hasattr(st.session_state, 'username'):
        redirect_url = "logged.py?username={}".format(st.session_state.username)
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=/{redirect_url}">', unsafe_allow_html=True)

if __name__ == "__main__":
    main()