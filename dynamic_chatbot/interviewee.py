import re
import openai_communicator

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
        # Handle dynamic input.
        self.name = self.extract_name()
        self.where_from = self.extract_where_from()
        self.age = self.extract_age()

    # abstract these 3 out to another class
    def remove_punctuation(self, str):
        return re.sub(r'[^\w\s]', "", str)
    
    def remove_spaces(self, str):
        return re.sub('\s+', "", str)

    def remove_quotes(self, str):
        return str.replace('"' , "")

    def extract_name(self):
        name_prompt = "I'm a biographer, and I'm interviewing someone. I asked them what their name was, and they said \"" + self.name + ".\" I responded in one word -- their name is \""
        dynamic_name = self.ai_interface.call_openai(name_prompt, [".\"", "."])
        dynamic_name = self.remove_punctuation(dynamic_name)
        dynamic_name = dynamic_name.split()[0]
        print("This is the dynamic name: " + dynamic_name)
        return dynamic_name

    def extract_where_from(self):
        where_from_prompt = "I'm a biographer, and I'm interviewing " + self.name + ". I asked them where they were from originally, and they said \"" + self.where_from + "\". I answered, saying only one short sentence: " + self.name + " is from"
        dynamic_where_from = self.ai_interface.call_openai(where_from_prompt, [".\"", "."])
        dynamic_where_from = self.remove_punctuation(dynamic_where_from)
        print("This is the dynamic place where they're from: " + dynamic_where_from)
        return dynamic_where_from

    def extract_age(self):
        age_prompt = "I'm a biographer, and I'm interviewing " + self.name + ". I asked them what their age was, and they said \"" + self.age + "\". I was asked how many years " + self.name + " has lived. I said one number only:"
        dynamic_age = self.ai_interface.call_openai(age_prompt, [".\"", ".", "!"])
        dynamic_age = dynamic_age.split()[0]
        dynamic_age = self.remove_spaces(dynamic_age)
        dynamic_age = self.remove_quotes(dynamic_age)
        # invalid age handling?
        print("This is the dynamic age: " + dynamic_age)
        return dynamic_age
