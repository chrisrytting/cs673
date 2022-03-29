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
    print("Welcome to the interview! Let's get started with some quick info about you!")
    interview_subject = interviewee.Interviewee()
    interview_subject.summarize_person()
    run_background_exchange(interview_subject)

# How the AI remembers all information without running out of room in its tokens:
# It creates a summary in 100 words or less.
def summarize_knowledge(interview_subject, all_knowledge):
    prompt_summary = (all_knowledge + "\n A summary of what I know about " + interview_subject.name
        + ", and what we've talked about so far, in 100 words or less: \"")
    returned_summary = ai_interface.call_openai(prompt_summary, "\"")
    print("SUMMARY: " + returned_summary)
    return returned_summary

def continuation_respond(interview_subject, previous_question, recent_response, summary):
    prompt_continuation = ("I'm a " + template + ", and I'm interviewing " + interview_subject.name + " today. " + summary + " When I told "
        + interview_subject.name + " \"" + previous_question + "\", they told me \"" + recent_response + "\". I thought that this was a great response, and I wanted to learn more! "
        + "This is how I would respond back: \"")
    returned_continuation = ai_interface.call_openai(prompt_continuation, "\"")
    return returned_continuation

def continuation_decide(interview_subject, previous_question, recent_response, summary):
    prompt_continuation = ("I'm a " + template + ", and I'm interviewing " + interview_subject.name + " today. " + summary + " When I told "
        + interview_subject.name + " \"" + previous_question + "\", they told me \"" + recent_response + "\". I thought that this was a great response! ")
    if should_conclude_loop(interview_subject):
        return "B"
    returned_continuation = ai_interface.call_openai(prompt_continuation, "\"")
    return returned_continuation

def should_conclude_loop(interview_subject):
    prompt_continue_decision = ("I then decided to either choose option A, continue to ask " + interview_subject.name + " more about this, or B, move on "
        + " to the next question. I will write a single letter for my choice, either A or B:")
    returned_decision = ai_interface.call_openai(prompt_continue_decision)
    return returned_decision == "B" or returned_decision == "b"

def background_loop(interview_subject, previous_question, all_knowledge, response):
    ai_summary = summarize_knowledge(interview_subject, all_knowledge)
    ai_input = continuation_respond(interview_subject, previous_question, response, ai_summary)
    user_response = input("\n" + ai_input + "\n")
    all_knowledge += "\n" + ai_input + "\n" + interview_subject.name + " responded, \""
    ai_summary = summarize_knowledge(interview_subject, all_knowledge)
    ai_input = continuation_decide(interview_subject, ai_input, user_response, ai_summary)
    if ai_input == "B":
        return "Transition"
    user_response = input("\n" + ai_input + "\n")
    return user_response

# Casual conversation about their background info, dynamic back-and-forth
def run_background_exchange(interview_subject):
    print("OK, thank you for all that! Let's move on to the questions!")
    prompt_question = ("I'm a " + template  + ", and I'm interviewing " + interview_subject.name + " today. " + interview_subject.name + " is"
        + interview_subject.age + " years old and from " + interview_subject.where_from + " originally. They now live in " + interview_subject.residence
        + " and their occupation is " + interview_subject.occupation + ". I thought " + interview_subject.name + " was a really interesting person, and "
        + "I wanted to know more about them and the information they gave me. Here is a question I would ask " + interview_subject.name + " next: \"")
    generated_question1 = ai_interface.call_openai(prompt_question, "\"")
    user_response = input(generated_question1 + "\n")
    ai_analysis = (interview_subject.name + " responded, \"" + user_response + "\". I thought that this was a great response! This is how I would respond back: \"")
    generated_question2 = ai_interface.call_openai(ai_analysis, "\"")
    user_response = input("\n" + generated_question2 + "\n")
    all_knowledge = (prompt_question + "\n" + generated_question1 + "\n" + ai_analysis + "\n" + generated_question2 + " " + interview_subject.name + " responded, \""
        + user_response)
    background_loop(interview_subject, generated_question2, all_knowledge, user_response)
    # while not should_conclude_loop(interview_subject):
    #     background_loop()

# Begin
run_interview()
