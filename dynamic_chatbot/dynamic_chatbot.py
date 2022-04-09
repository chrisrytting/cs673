import openai
import os
import interviewee
import openai_communicator
import string_manipulation
from termcolor import colored

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    print("OpenAI API key not set")

template = "biographer"
ai_interface = openai_communicator.OpenAICommunicator
string_manipulator = string_manipulation.StringManipulator
soul_searching_questions = [
    "What do you like to do for fun?",
    "What is the most important thing that ever happened to you?",
    "What is the accomplishment you are most proud of?",
    "Who is the person you admire the most?",
    "What is the thing you would tell an 18-year old version of yourself?",
    "What are your greatest passions in life?",
    "What is the best gift that you've ever been given?",
    "What has been the happiest time of your life so far?",
]

def run_interview():
    print("Welcome to the interview! I'm a " + template + ", and I am really excited for our chat today. Let's get started with some quick info about you!")
    interview_subject = interviewee.Interviewee()
    interview_subject.summarize_person()
    background_knowledge = run_background_exchange(interview_subject)
    ai_transition = transition_to_soul_search(background_knowledge, soul_searching_questions[0])
    run_soul_search_exchange(interview_subject, ai_transition, background_knowledge)

# How the AI remembers all information without running out of room in its tokens:
# It creates a summary in 100 words or less.
def summarize_knowledge(interview_subject, all_knowledge):
    prompt_summary = (all_knowledge + "\n A summary of what I know about " + interview_subject.name
        + ", and what we've talked about so far, in 100 words or less: \"")
    returned_summary = ai_interface.call_openai(prompt_summary, "\"")
    return returned_summary

def is_question(sentence):
    prompt = ("Is this a question: \"" + sentence + "\" Answer yes or no:")
    response = ai_interface.call_openai(prompt)
    return response.lower() == "yes"

def should_conclude_loop(interview_subject, prompt):
    prompt_continue_decision = (prompt + "\nI then decided to either choose option A, continue to ask " + interview_subject.name + " more about this, or B, move on "
        + " to the next question. I will write a single letter for my choice, either A or B:")
    returned_decision = ai_interface.call_openai(prompt_continue_decision)
    returned_decision = string_manipulator.remove_spaces(returned_decision)
    return returned_decision == "B" or returned_decision == "b"

def simple_continue(prompt):
    prompt += ("\nI thought that this was a great response! This is how I would respond back to continue the interview: \"")
    to_return = ai_interface.call_openai(prompt, ["\"", "?"], 1, 2)
    if to_return[len(to_return) - 1] != "." and to_return[len(to_return) - 1] != "!":
        to_return += "?"
    return to_return

def background_loop(interview_subject, previous_question, all_knowledge, response):
    ai_response = simple_continue(all_knowledge)
    user_response = input(colored(ai_response + "\n", "yellow"))
    all_knowledge += ai_response + user_response
    if user_response == "exit":
        quit()
    prompt = (interview_subject.name + " responded, \"" + user_response + ".\" ")
    all_knowledge += prompt
    ai_response2 = simple_continue(all_knowledge)
    user_response2 = input(colored(ai_response2 + "\n", "yellow"))
    all_knowledge += ai_response2 + user_response2
    if user_response2 == "exit":
        quit()
    summary = summarize_knowledge(interview_subject, all_knowledge)
    # Summary loop
    new_knowledge = (summary + "\nI asked " + interview_subject.name + " \"" + ai_response2 + "\". " + interview_subject.name + " responded, \"" + user_response2 + "\".")
    ai_response3 = simple_continue(new_knowledge)
    user_response3 = input(colored(ai_response3 + "\n", "magenta"))
    if user_response3 == "exit":
        quit()
    new_knowledge += ai_response3 + user_response3
    should_ask_more_questions = not should_conclude_loop(interview_subject, new_knowledge)
    should_continue = should_ask_more_questions
    while should_continue:
        current_summary = summarize_knowledge(interview_subject, new_knowledge)
        new_knowledge = current_summary
        ai_response4 = simple_continue(new_knowledge)
        user_response4 = input(colored(ai_response4 + "\n", "cyan"))
        if user_response4 == "exit":
            quit()
        new_knowledge += ai_response4 + user_response4
        # If it's not a question, then it's just a friendly analysis, and we should not proceed further as this will cause repetitive responses.
        if not is_question(ai_response4):
            should_continue = False
            break
        should_continue = not should_conclude_loop(interview_subject, new_knowledge)
    return new_knowledge

# Casual conversation about their background info, dynamic back-and-forth
def run_background_exchange(interview_subject):
    print(colored("OK, let's move on to the rest of the interview! Just type \"exit\" to quit.", "yellow"))
    prompt_question = ("I'm a " + template  + ", and I'm interviewing " + interview_subject.name + " today. " + interview_subject.name + " is "
        + interview_subject.age + " years old and from " + interview_subject.where_from + " originally. They now live in " + interview_subject.residence
        + " and their occupation is " + interview_subject.occupation + ". I thought " + interview_subject.name + " was a really interesting person, and "
        + "I wanted to know more about them and the information they gave me. Here is a new question I would ask " + interview_subject.name + " next: \"")
    generated_question1 = ai_interface.call_openai(prompt_question, ["\"", "?"], 1, 2)
    user_response = input(colored(generated_question1 + "\n", "yellow"))
    if user_response == "exit":
        quit()
    ai_analysis = (interview_subject.name + " responded, \"" + user_response + "\". I thought that this was a great response! This is how I would respond back: \"")
    generated_question2 = ai_interface.call_openai(prompt_question + generated_question1 + ai_analysis, ["\"", "?"], 1, 2)
    user_response = input(colored(generated_question2 + "\n", "yellow"))
    if user_response == "exit":
        quit()
    all_knowledge = (prompt_question + "\n" + generated_question1 + "\n" + ai_analysis + "\n" + generated_question2 + " " + interview_subject.name + " responded, \""
        + user_response + "\".")
    new_knowledge = background_loop(interview_subject, generated_question2, all_knowledge, user_response)
    return new_knowledge

# New knowledge should not include the continuation decision text
def transition_to_soul_search(new_knowledge, next_question):
    transition_prompt = (new_knowledge + "I then decided to move onto the next question. The next question is \"" + 
        next_question + "\" This is how I will transition smoothly, making sure to ask that question: \"")
    ai_transition = ai_interface.call_openai(transition_prompt, ["?", "\""])
    return ai_transition

def send_clarification_prompt(prompt, interview_subject):
    clarification_prompt = (prompt + "\nI told " + interview_subject.name + ", \"")
    clarification_response = ai_interface.call_openai(clarification_prompt, "\"")
    return clarification_response

def send_soul_searching_prompt(prompt, interview_subject):
    soul_searching_prompt = (prompt + "\nI thought this was a great response! I want to search the depths of " 
        + interview_subject.name + "'s soul, and explore what they said. This is how I would respond, not repeating what I said before: \"")
    soul_searching_response = ai_interface.call_openai(soul_searching_prompt, ["\"", "?"], 1, 2)
    return soul_searching_response

def is_clarification_request(interview_subject, summary):
    prompt = ("\nWas " + interview_subject.name + " (A) answering my question, or (B) asking for clarification on my question? Answer in one letter:")
    ai_ascertaining = ai_interface.call_openai(summary + prompt)
    return ai_ascertaining == "b" or ai_ascertaining == "B" 

def transition_to_next_soul_searching_question(all_info, index, interview_subject):
    transition_prompt = ("\nThe next question is \"" + soul_searching_questions[index] + "\" This is how I will smoothly transition from " + 
        interview_subject.name + "'s last response to the next question, analyzing what they said too: \"")
    ai_transition = ai_interface.call_openai(all_info + transition_prompt, ["\"", "?"])
    return ai_transition

def soul_searching_loop(interview_subject, question, response, summary, question_number):
    background_info = ("I'm a " + template + ", and I'm interviewing " + interview_subject.name + " today. I think "
        + interview_subject.name + " is a really interesting person, and I am enjoying this interview. " + summary
        + "\nI asked, \"" + question + "\".\n" + interview_subject.name + " responded, \"" + response + "\".")
    # The background info should include the most recently asked question at the end.
    if is_clarification_request(interview_subject, background_info):
        ai_speech = send_clarification_prompt(background_info, interview_subject)
        user_response = input(colored(ai_speech + "\n", "red"))
        if user_response == "exit":
            quit()
        all_info = (background_info + "\nI told " + interview_subject.name + ", \"" + ai_speech + "." + interview_subject.name + " responded, \"" + user_response + "\".")
    else:
        ai_speech = send_soul_searching_prompt(background_info, interview_subject)
        user_response = input(colored(ai_speech + "\n", "red"))
        if user_response == "exit":
            quit()
        all_info = (background_info + "\nI thought this was a great response! I want to search the depths of " 
            + interview_subject.name + "'s soul, and explore what they said. This is how I would respond, not repeating what I said before: \"" + ai_speech + "\". "
            + interview_subject.name + " responded, \"" + user_response + "\".")
    counter = 0
    while counter < 2 or not should_conclude_loop(interview_subject, all_info):
        if is_clarification_request(interview_subject, all_info):
            ai_speech = send_clarification_prompt(all_info, interview_subject)
            user_response = input(colored(ai_speech + "\n", "red"))
            if user_response == "exit":
                quit()
            all_info = (all_info + "\nI told " + interview_subject.name + ", \"" + ai_speech + "." + interview_subject.name + " responded, \"" + user_response + "\".")
        else:
            ai_speech = send_soul_searching_prompt(all_info, interview_subject)
            user_response = input(colored(ai_speech + "\n", "red"))
            if user_response == "exit":
                quit()
            all_info = (all_info + "\nI thought this was a great response! I want to search the depths of " 
                + interview_subject.name + "'s soul, and explore what they said. This is how I would respond, not repeating what I said before: \"" + ai_speech + "\". "
                + interview_subject.name + " responded, \"" + user_response + "\".")
            print("all info: " + all_info)
            # Ending on a statement
            if not is_question(ai_speech):
                break
        counter += 1
    # Next: Should transition
    ai_transition = transition_to_next_soul_searching_question(all_info, question_number, interview_subject)
    user_response = input(colored(ai_transition + "\n", "magenta", attrs=["bold"]))
    if user_response == "exit":
        quit()
    all_info += ai_transition
    all_info = summarize_knowledge(interview_subject, all_info)
    return user_response, all_info, ai_transition

def run_soul_search_exchange(interview_subject, ai_transition, background_knowledge):
    # Purpose: Iterate through all soul-searching questions, interpolating, analyzing, and coming up with new questions.
    user_response = input(colored(ai_transition + "\n", "cyan", attrs=["bold"]))
    if user_response == "exit":
        quit()
    summary = summarize_knowledge(interview_subject, background_knowledge)
    question_number = 0
    while question_number < len(soul_searching_questions):
        user_response, summary, ai_transition = soul_searching_loop(interview_subject, ai_transition, user_response, summary, question_number)
        question_number += 1

# Begin
run_interview()
