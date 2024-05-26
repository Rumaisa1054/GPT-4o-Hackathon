import streamlit as st
import os

def main(username):
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

if __name__ == "__main__":
    # Retrieve username from query parameters
    query_params = st.experimental_get_query_params()
    username = query_params["username"][0] if "username" in query_params else "Guest"
    main(username)
