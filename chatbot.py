import openai
import os
import sys

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    print("OpenAI API key not set")

num_args = len(sys.argv)

class Subject:
    """Class for getting to know the subject's background info"""

    def __init__(self, dry_run=False):
        if dry_run:
            self.name = "Chris"
            self.origin = "Orem"
            self.age = "30"
            self.residence = "New York"
            self.occupation = "Software Engineer"
            print("\nDoing a dry run. Auto-populating background info.")
        else:
            self.name = input("What is your name? ")
            self.origin = input("Where are you from originally? ")
            self.age = input("How old are you? ")
            self.residence = input("Where do you live now? ")
            self.occupation = input("What do you do for work? ")

        print(
            "\n\nGreat, that's all really helpful to know. Let's get started on the interview!\n\n"
        )

    def print_backstory(self):
        """Convert the subject's info to a descriptive natural language paragraph"""
        return (
            f"This is an interview with {self.name}. "
            f"{self.name} is {self.age} years old and is from {self.origin} originally. "
            f"{self.name} lives in {self.residence}, and their occupation is {self.occupation}."
        )


class Interview:
    def __init__(self, interviewer_style, pplm=False, dry_run=False):
        # Dry run as a CLI parameter.
        if num_args > 1 and sys.argv[1] == "dry_run":
            dry_run = True
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
            print(question, "\n(You can say 'pass' to skip this question or 'exit' to skip all questions)")
            answer = input()
            if answer == "pass":
                continue
            elif answer == "exit":
                break
            conversation.append((question, answer))
            backstory = self.subject.print_backstory()
            prompt = template(self.subject.name, question, answer)
            prompt = "\n\n".join((backstory, prompt))
            print(prompt)
            if dry_run:
                gpt3_followup = "I'm a bot, and I don't know what to say."
            else:
                response = openai.Completion.create(engine="text-davinci-001", prompt=prompt, max_tokens=64, stop=["."])
                gpt3_followup = response.choices[0].text
            print(gpt3_followup + ".\n")
            # Follow-up. Starting with 1 question and 1 analysis for now.
            follow_up_question = "I then asked " + self.subject.name
            if dry_run:
                follow_up_question += " absolutely nothing. "
                print(follow_up_question)
            else:
                follow_up_question += " the following question: \""
                follow_up_question += openai.Completion.create(engine="text-davinci-001", prompt=prompt + gpt3_followup + follow_up_question, max_tokens=64, stop=["?\""]).choices[0].text
                print(follow_up_question + "?\"\n")
            follow_up_answer = ""
            if dry_run:
                follow_up_answer += "And I did not run an analysis."
            else:
                answer_from_user = input("\n")
                if answer_from_user == "pass":
                    continue
                elif answer_from_user == "exit":
                    break
                follow_up_answer += follow_up_question + " and their response was '" + answer_from_user + "' When I heard that, I thought"
                follow_up_answer += openai.Completion.create(engine="text-davinci-001", prompt=follow_up_answer, max_tokens=64, stop=["."]).choices[0].text
            print("\n" + follow_up_answer + ".\n")
            print("_______________________________\n")

        print("Thanks for the interview! It was nice getting to know you!")


interview = Interview("biographer", dry_run=False)
