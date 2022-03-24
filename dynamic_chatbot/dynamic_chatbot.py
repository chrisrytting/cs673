import openai
import os
import sys
import interviewee

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    print("OpenAI API key not set")

num_args = len(sys.argv)

def run_interview():
    interview_subject = interviewee.Interviewee()
    interview_subject.summarize_person()
    run_background_exchange()

# Casual conversation about their background info, dynamic back-and-forth
def run_background_exchange():
    pass

# Begin
run_interview()