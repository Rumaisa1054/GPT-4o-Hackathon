import streamlit as st
import sqlite3
from fpdf import FPDF

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

# Function to handle course content
def course_content_ui():
    st.title("Course Content")
    
    st.header("Enter Topic")
    topic = st.text_input("Enter topic here")

    if topic:
        st.subheader("Course Content for {}".format(topic))
        course_content = "This is the hardcoded course content for the topic: {}".format(topic)
        st.write(course_content)

        if st.button("Download Course as PDF"):
            pdf_data = generate_pdf(course_content)
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="course_content.pdf",
                mime="application/pdf"
            )

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    
    pdf_output = pdf.output(dest='S').encode('latin1')  # 'S' means output as a string
    return pdf_output

# Function to handle chat about confusion
def chat_ui():
    st.title("Chat Area")
    chat_text = st.text_area("Chat with us about your confusion")

    if st.button("Send"):
        st.success("Your message has been sent")

# Function to handle quiz chat
def quiz_ui():
    st.title("Quiz Chat")
    quiz_text = st.text_area("Chat with us about the quiz")

    if st.button("Send"):
        st.success("Your message has been sent")

# Logged-in UI
def logged_in_ui(username):
    st.sidebar.title("Navigation")
    tab = st.sidebar.radio("Select a tab", ("Course Content", "Chat", "Quiz Chat"))

    if tab == "Course Content":
        course_content_ui()
    elif tab == "Chat":
        chat_ui()
    elif tab == "Quiz Chat":
        quiz_ui()

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
