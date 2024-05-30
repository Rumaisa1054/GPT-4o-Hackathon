import hackathon_api as api


topic = "explain me the force in physics"
course_content = api.generate_cours(topic)

api.generate_evaluation_questions(course_content)

user_question = "Define acceleration for me"
api.answer_question(course_content, user_question)
