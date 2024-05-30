import replicate
import os


os.environ['REPLICATE_API_TOKEN'] = "r8_8tgu21LprONdmHOqlZciw9gn1qwrLuz2u9qg9"

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
    prompt_eng = f"Based on the following course content, generate 10 evaluation questions:\n\n{course_content}"
    return prompt_runer(prompt_eng)

#Function for generating the question answers which takes the theme and user question
def answer_question(course_content, user_question):
    prompt_eng = f"Based on the following course content, answer the user's question:\n\nCourse content: {course_content}\n\nUser's question: {user_question}",
    return prompt_runer(prompt_eng)
    

topic = "explain me the force in physics"
print(generate_cours(topic))
