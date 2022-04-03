import openai_communicator
import string_manipulation
from termcolor import colored

class Interviewee:
    # Encapsulates the person being interviewed.
    def __init__(self):
        # Set member variables.
        self.name = input("What is your name? ")
        self.where_from = input("Where are you from originally? ")
        self.age = input("How old are you? ")
        self.residence = input("Where do you live now? ")
        self.occupation = input("What do you do for work? ")
        self.ai_interface = openai_communicator.OpenAICommunicator
        self.str_manip = string_manipulation.StringManipulator
        # Handle dynamic input.
        self.name = self.extract_name()
        self.where_from = self.extract_where_from()
        self.age = self.extract_age()
        self.residence = self.extract_residence()
        self.occupation = self.extract_occupation()

    # the purpose of these functions is using GPT-3 to dynamically select the attribute based on the user input, instead of grabbing it verbatim.
    # so if the user says "I'm Alex", the chatbot will refer to them as "Alex", minus the "I'm".
    def extract_name(self):
        name_prompt = "I'm a biographer, and I'm interviewing someone. I asked them what their name was, and they said \"" + self.name + ".\" I responded in one word -- their name is \""
        dynamic_name = self.ai_interface.call_openai(name_prompt, [".\"", "."])
        dynamic_name = self.str_manip.remove_punctuation(dynamic_name)
        dynamic_name = dynamic_name.split()[0]
        return dynamic_name

    def extract_where_from(self):
        where_from_prompt = "I'm a biographer, and I'm interviewing " + self.name + ". I asked them where they were from originally, and they said \"" + self.where_from + "\". I answered, saying only one short sentence: " + self.name + " is from"
        dynamic_where_from = self.ai_interface.call_openai(where_from_prompt, [".\"", "."])
        dynamic_where_from = self.str_manip.remove_punctuation(dynamic_where_from)
        return dynamic_where_from

    def extract_age(self):
        age_prompt = "I'm a biographer, and I'm interviewing " + self.name + ". I asked them what their age was, and they said \"" + self.age + "\". I was asked how many years " + self.name + " has lived. I said one number only:"
        dynamic_age = self.ai_interface.call_openai(age_prompt, [".\"", ".", "!"])
        dynamic_age = dynamic_age.split()[0]
        dynamic_age = self.str_manip.remove_spaces(dynamic_age)
        dynamic_age = self.str_manip.remove_quotes(dynamic_age)
        # invalid age handling?
        return dynamic_age

    def extract_residence(self):
        residence_prompt = "I'm a biographer, and I'm interviewing " + self.name + ". I asked them where they are currently living, and they said \"" + self.residence + "\" From this, I determined that " + self.name + " is from the following location:"
        dynamic_residence = self.ai_interface.call_openai(residence_prompt, [".\"", ".", "!"])
        dynamic_residence = self.str_manip.remove_newlines_only(dynamic_residence)
        return dynamic_residence

    def extract_occupation(self):
        # is not always doing 3 words or less, esp. complicated careers such as "bioinformatics"
        occupation_prompt = "I'm a biographer, and I'm interviewing " + self.name + ". I asked them what their occupation was, and they said " + self.occupation + ". " + "I can summarize their career in three words or less: " + self.name + " is a"
        dynamic_occupation = self.ai_interface.call_openai(occupation_prompt, [".\"", ".", "!"])
        return dynamic_occupation

    def summarize_person(self):
        print("\nThanks, that's all great info!\n")
        print(colored("\nGoing on record: I will be interviewing " + self.name + " today. " + self.name + " is " + self.age + " years old and is from " + self.where_from + " originally. They now live in " + self.residence + " and their occupation is " + self.occupation + ".\n", "green"))
