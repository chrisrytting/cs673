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

# Begin
run_interview()