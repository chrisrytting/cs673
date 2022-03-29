import openai
import os
import interviewee
import openai_communicator

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    print("OpenAI API key not set")

template = "biographer"
ai_interface = openai_communicator.OpenAICommunicator

def run_interview():
    interview_subject = interviewee.Interviewee()
    interview_subject.summarize_person()
    run_background_exchange(interview_subject)

# Casual conversation about their background info, dynamic back-and-forth
def run_background_exchange(interview_subject):
    print("OK, let's get started!")
    prompt_question = ("I'm a " + template  + ", and I'm interviewing " + interview_subject.name + " today. " + interview_subject.name + " is"
        + interview_subject.age + " years old and from " + interview_subject.where_from + " originally. They now live in " + interview_subject.residence
        + " and their occupation is " + interview_subject.occupation + ". I thought " + interview_subject.name + " was a really interesting person, and "
        + "I wanted to know more about them and the information they gave me. Here is a question I would ask " + interview_subject.name + " next: ")
    response = ai_interface.call_openai(prompt_question)
    print(response)

# Begin
run_interview()
