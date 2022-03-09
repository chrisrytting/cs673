import openai
import os

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    print("OpenAI API key not set")


class Subject:
    """Class for getting to know the subject's background info"""

    def __init__(self, dry_run=False):
        if dry_run:
            self.name = "Chris"
            self.origin = "Orem"
            self.age = "30"
            self.residence = "New York"
            self.occupation = "Software Engineer"
        else:
            print("What is your name?")
            self.name = input()
            print("Where are you from originally?")
            self.origin = input()
            print("How old are you?")
            self.age = input()
            print("Where do you live now?")
            self.residence = input()
            print("What do you do for work?")
            self.occupation = input()

        print(
            "\n\nGreat, that's all really helpful to know. Let's get started on the interview!\n\n"
        )

    def print_backstory(self):
        """Convert the subject's info to a descriptive natural language pargraph"""
        return (
            f"This is an interview with {self.name}. "
            f"{self.name} is {self.age} years old and is from {self.origin} originally. "
            f"{self.name} lives in {self.residence}, and their occupation is {self.occupation}."
        )


class Interview:
    def __init__(self, interviewer_style, pplm=False, dry_run=False):
        self.subject = Subject(dry_run=dry_run)

        self.templates = {
            "biographer": lambda subject_name, question, answer: (
                f"I'm a biographer, and when I asked "
                f"{subject_name} '{question}', they told me '{answer}'. "
                f"When I heard that, I thought"
            ),
            "mother": lambda subject_name, question, answer: (
                f"I'm {subject_name}'s mother, and when I asked them "
                f"'{question}', they told me '{answer}'. "
                f"When I heard that, my reaction was"
            ),
            "journalist": lambda subject_name, question, answer: (
                f"I'm a journalist, and when I asked "
                f"{subject_name} '{question}', they told me '{answer}'. "
                f"When I heard that, I thought"
            ),
            "poet": lambda subject_name, question, answer: (
                f"I'm a poet, and when I asked "
                f"{subject_name} '{question}', they told me '{answer}'. "
                f"When I heard that, I felt '{answer}'"
            ),
            "manager": lambda subject_name, question, answer: (
                f"I'm {subject_name}'s manager, and when I asked them "
                f"'{question}', they told me '{answer}'. "
                f"When I heard that, my reaction was"
            ),
            "grandfather": lambda subject_name, question, answer: (
                f"I'm {subject_name}'s grandfather, and when I asked them "
                f"'{question}', they told me '{answer}'. "
                f"When I heard that, I wanted to know"
            ),
        }

        if interviewer_style not in self.templates:
            raise ValueError("Interviewer style not found")
        self.interviewer_style = interviewer_style
        self.carry_out_interview(dry_run=dry_run)

    def carry_out_interview(self, dry_run=False):
        soul_searching_questions = [
            "What do you like to do for fun?",
            "What is the most important thing that ever happened to you?",
            "What is the accomplishment your are most proud of?",
            "Who is the person you admire the most?",
            "What is the thing you would tell an 18-year old version of yourself?",
            "What are your greatest passions in life?",
            "What is the best gift that you've ever been given?",
            "What has been the happiest time of your life so far?",
        ]

        template = self.templates[self.interviewer_style]
        conversation = []
        for question in soul_searching_questions:
            print(question, "\n(You can say 'pass' to skip this question)")
            answer = input()
            if answer == "pass":
                continue
            conversation.append((question, answer))
            backstory = self.subject.print_backstory()
            prompt = template(self.subject.name, question, answer)
            prompt = "\n\n".join((backstory, prompt))
            print(prompt)
            if dry_run:
                gpt3_followup = "I'm a bot, and I don't know what to say."
            else:
                response = openai.Completion.create(engine="davinci", prompt=question)
                gpt3_followup = response.choices[0].text
            print(gpt3_followup)
        print("Thanks for the interview! It was nice getting to know you!")


interview = Interview("biographer", dry_run=True)
