import openai
import os

try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except:
    print("OpenAI API key not set")


class Subject():
    def __init__(self, dry_run=False):
        if dry_run:
            self.name = "Chris"
            self.origin = "Orem"
            self.age = "30"
            self.occupation = "Software Engineer"
            self.residence = "New York"
        else:
            self.name = input("What is your name? ")
            self.origin = input("Where are you from originally? ")
            self.age = input("How old are you? ")
            self.residence = input("Where do you live now? ")
            self.occupation = input("What do you do for work? ")
            

    def print_backstory(self):
        return (f"This is an interview with {self.name}. "
                f"{self.name} is {self.age} years old and is from {self.origin} originally. "
                f"{self.name} lives in {self.residence}, and their occupation is {self.occupation}.")


class Interview():
    def __init__(self, interviewer_style, pplm=False):
        self.subject = Subject(dry_run=False) # change dry run to True if you want default responses

        self.templates = {
            "biographer": lambda subject_name, question, answer: (f"I'm a biographer, and when I asked "
                                                                  f"{subject_name} '{question}', they told me '{answer}'. "
                                                                  f"When I heard that, I thought"),
            "mother": lambda subject_name, question, answer: (f"I'm {subject_name}'s mother, and when I asked them "
                                                              f"'{question}', they told me '{answer}'. "
                                                              f"When I heard that, my reaction was"),
            "journalist": lambda subject_name, question, answer: (f"I'm a journalist, and when I asked "
                                                                  f"{subject_name} '{question}', they told me '{answer}'. "
                                                                  f"When I heard that, I thought"),
            "poet": lambda subject_name, question, answer: (f"I'm a poet, and when I asked "
                                                            f"{subject_name} '{question}', they told me '{answer}'. "
                                                            f"When I heard that, I felt '{answer}'"),
            "manager": lambda subject_name, question, answer: (f"I'm {subject_name}'s manager, and when I asked them "
                                                               f"'{question}', they told me '{answer}'. "
                                                               f"When I heard that, my reaction was"),
            "grandfather": lambda subject_name, question, answer: (f"I'm {subject_name}'s grandfather, and when I asked them "
                                                                   f"'{question}', they told me '{answer}'. "
                                                                   f"When I heard that, I wanted to know"),
        }

        if interviewer_style not in self.templates:
            raise ValueError("Interviewer style not found")
        self.interviewer_style = interviewer_style
        self.carry_out_interview()

    def carry_out_interview(self):
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

        template = self.templates[self.interviewer_style]
        conversation = []
        for question in soul_searching_questions:
            print(question)
            answer = input()
            # answer = "frolick"
            conversation.append((question, answer))
            backstory = self.subject.print_backstory()
            prompt = template(self.subject.name, question, answer)
            prompt = "\n\n".join((backstory, prompt))
            print(prompt)
            # breakpoint()
            response = openai.Completion.create(
                engine="davinci", prompt=question)
            print(response.choices[0].text)


interview = Interview("biographer")
