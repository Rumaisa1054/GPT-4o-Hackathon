import replicate
import os


os.environ['REPLICATE_API_TOKEN'] = os.getenv('MINE')

use_model = "a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5"

def prompt_runer(prompt):
    try:
        output_generator = replicate.run(
            use_model,
            input={"prompt": prompt}
        )
        # Collect the outputs from the generator
        output = "".join(output_generator)
        
    except replicate.exceptions.ReplicateError as e:
        print(f"Replicate error: {e}")
        output = "Error in generation of reponse"
    except Exception as e:
        print(f"Unexpected error: {e}")
        #raise
        output = "Error in generation of reponse"
    return output
def generate_cours(topic):
    prompt_eng = f"Generate me a well-written course on: {topic}"
    return prompt_runer(prompt_eng)

#Function for generating the cours questions which takes the theme
def generate_evaluation_questions(course_content):
    prompt_eng = f"Based on the following course content, generate 10 evaluation questions . RETURN ONLY THE QUESTIONS IN RESPONSE:\n\n{course_content}"
    return prompt_runer(prompt_eng)

#Function for generating the question answers which takes the theme and user question
def answer_question(course_content, user_question):
    prompt_eng = f"Based on the following course content, answer the user's question:\n\nCourse content: {course_content}\n\nUser's question: {user_question}"
    print(prompt_eng)
    return prompt_runer(prompt_eng)

def evaluator(course_content, user_question,user_Ans):
    prompt_eng = f"Based on the following course content and the question, check if the user Answer is correct or not- Assign points of out 10 and Return POints - (SHORT AND PRECISE):\n\nCourse content: {course_content}\n\nQuestion: {user_question}\n\n User Answer: {user_Ans}"
    print(prompt_eng)
    return prompt_runer(prompt_eng)

def marks_and_comments(user_Anz,topic):
    prompt_eng = f"Given a set of tutor remarks on some answers provided by a student. Calculate the total score out of 100 and provide a summary of the marks for each question along with the total score achieved out of 100 by extracting the marks in the text and then adding them. Here are the questions and answers: {user_Anz} Please provide the marks for each question and the total score."
    print(prompt_eng)
    return prompt_runer(prompt_eng)
