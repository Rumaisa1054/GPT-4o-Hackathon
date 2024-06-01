import streamlit as st
import hackathon_api as api
import sqlite3
from fpdf import FPDF

# Create or connect to the SQLite database
conn = sqlite3.connect('user.db')
c = conn.cursor()

# Create a table to store user information if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT)''')
conn.commit()

# Create a table to store user quiz scores if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS quiz_scores
             (username TEXT, course TEXT, score TEXT,
              FOREIGN KEY(username) REFERENCES users(username))''')
conn.commit()

# Function to check if a username already exists
def username_exists(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

# Function to authenticate user
def authenticate_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content.encode('latin1', 'replace').decode('latin1'))
    
    pdf_output = pdf.output(dest='S').encode('latin1')  # Output as a string
    return pdf_output

topic = ""
# Function to handle course content and PDF generation/download
def course_content_ui():
    global topic
    st.title("Course Content")
    
    st.header("Enter Topic")
    topic = st.text_input("Enter topic here")

    if topic:
        st.subheader("Course Content for {}".format(topic))
        course_content = api.generate_cours(topic)
        st.write(course_content)
        
        # Store course content in session state
        st.session_state.topic = topic
        st.session_state.course_content = course_content
        
        pdf_data = generate_pdf(course_content)
        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name="course_content.pdf",
            mime="application/pdf",
            key="download_pdf_button"
        )

# Function to handle chat about confusion
def chat_ui():
    st.title("Chat Your Confusions")

    # Initialize chat history for chat tab
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Display chat messages from history on a container
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("What is your confusion?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
    
        response = api.answer_question(st.session_state.course_content, prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.chat_messages.append({"role": "assistant", "content": response})

def quiz_ui():
    st.session_state.text = ""
    global topic
    st.title("Start the Quiz")
    
    # Check if course_content is available in session state
    if "course_content" not in st.session_state:
        st.error("No course content available. Please enter a topic in the 'Course Content' tab first.")
        return
    
    course_content = st.session_state.course_content
    
    # Initialize chat history for quiz tab
    if "quiz_messages" not in st.session_state:
        st.session_state.quiz_messages = []

    # Display chat messages from history on a container
    for message in st.session_state.quiz_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Generate evaluation questions
    if "questions" not in st.session_state:
        questions = api.generate_evaluation_questions(course_content)
        
        st.session_state.questions = [q.strip() for q in questions.split("\n") if q.strip()]
        st.session_state.questions.pop(0)
        if len(st.session_state.questions) > 10:
            st.session_state.questions = st.session_state.questions[:10]
        st.session_state.question_index = 0
        st.session_state.total_marks = 0
        st.session_state.user_answers = []

    # Process the quiz
    if st.session_state.question_index < len(st.session_state.questions):
        current_question = st.session_state.questions[st.session_state.question_index]
        
        with st.chat_message("assistant"):
            st.markdown(f"Quiz Question {st.session_state.question_index + 1}: {current_question}")

        if user_answer := st.chat_input("Your Answer:"):
            # Store user's answer
            st.session_state.user_answers.append(user_answer)
            st.session_state.quiz_messages.append({"role": "user", "content": user_answer})

            # Evaluate user's answer
            marks_response = api.evaluator(course_content, current_question, user_answer)
            
            # Extract marks from the response
            

            
            st.session_state.quiz_messages.append({"role": "assistant", "content": marks_response})
            st.session_state.text = st.session_state.text + "\n\n\n Question : "+ current_question + "\n\n\nAnswer : " + user_answer

            st.session_state.question_index += 1
            st.experimental_rerun()

    else:
        
        with st.chat_message("assistant"):
            p = api.marks_and_comments( st.session_state.text,st.session_state.topic)
            st.markdown(p)


        # Store the quiz score in the database
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("INSERT INTO quiz_scores (username, course, score) VALUES (?, ?, ?)",
                  (st.session_state.username, st.session_state.topic, p))
        conn.commit()
        conn.close()

        # Reset quiz session state
        del st.session_state.text
        del st.session_state.questions
        del st.session_state.question_index
        del st.session_state.total_marks
        del st.session_state.user_answers

# Function to display user info and quiz scores
def user_info_ui():
    st.title("User Info")
    
    c.execute("SELECT * FROM users WHERE username=?", (st.session_state.username,))
    user_info = c.fetchone()
    
    if user_info:
        st.write(f"Username: {user_info[0]}")
    
        st.subheader("Quiz Scores")
        c.execute("SELECT course, score FROM quiz_scores WHERE username=?", (st.session_state.username,))
        scores = c.fetchall()
        
        if scores:
            for course, score in scores:
                st.write(f"Course: {course}, Score: {score}")
        else:
            st.write("No quiz scores available.")
    else:
        st.write("User information not available.")

# Logged-in UI
def logged_in_ui(username):
    st.sidebar.title("Navigation")
    tab = st.sidebar.radio("Select a tab", ("Course Content", "Chat", "Quiz Chat", "User Info"))

    if tab == "Course Content":
        course_content_ui()
    elif tab == "Chat":
        chat_ui()
    elif tab == "Quiz Chat":
        quiz_ui()
    elif tab == "User Info":
        user_info_ui()

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
