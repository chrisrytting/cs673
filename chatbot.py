import openai
import os
import sys

model = 'text-davinci-002'

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
    def __init__(self, interviewer_style, pplm=False, dry_run=False, analysis_question_config="both"):
        # Dry run as a CLI parameter.
        if num_args > 1 and sys.argv[1] == "dry_run":
            dry_run = True
        self.subject = Subject(dry_run=dry_run)

        self.analysis_question_config = analysis_question_config
        self.analysis_question_config_dict = {"analysis": [
            "analysis"], "question": ["question"], "both": ["analysis", "question"]}

        self.templates = {
            "biographer": {
                "analysis": lambda subject_name, question, answer: (
                    f"I'm a biographer, and when I asked "
                    f"{subject_name} '{question}', they told me '{answer}'. "
                    f"When I heard that, I thought"
                ),
                "question": lambda subject_name, question, answer: (
                    f"I'm a biographer, and when I asked "
                    f"{subject_name} '{question}', they told me '{answer}'. "
                    f"When I heard that, I wanted to ask them the question \""
                ),
            },
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
        analysis_question_config = self.analysis_question_config

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

        # Options to present to messenger/subject after soul-searcher has asked a question
        q_options = """
        Options:
        "pass" - Skip this question
        "end" - End the interview
        """

        # Options to present to messenger after soul-searcher has weighed in on subject's response to question
        a_options = """
        Options:
        Press enter to continue, else type
        "again" - to have soul-searcher resample the analysis / question
        "analysis" - to force soul-searcher to offer analysis instead of asking a follow-up question
        "question" - to force soul-searcher to offer a follow-up question instead of offering an analysis
        "both" - to have soul-searcher offer both an analysis and a follow-up question
        """
        for question in soul_searching_questions:
            print(
                question, q_options)
            answer = input()
            if answer == "pass":
                continue
            elif answer == "end":
                break
            conversation.append((question, answer))
            backstory = self.subject.print_backstory()
            while True:
                # TODO pass in prompt according to analysis_question_config
                for answer_type in self.analysis_question_config_dict[analysis_question_config]:
                    prompt = template[answer_type](
                        self.subject.name, question, answer)
                    if dry_run:
                        gpt3_followup = "I'm a bot, and I don't know what to say."
                    else:
                        response = openai.Completion.create(
                            engine="text-davinci-002", prompt=prompt, max_tokens=64, stop=["\n"])
                        gpt3_followup = response.choices[0].text
                    print(
                        f"Prompt: {prompt}\n\n{answer_type}: {gpt3_followup}")
                    breakpoint()
                print(a_options)
                messenger_input = input()
                if messenger_input == "":
                    break
                elif messenger_input == "again":
                    continue
                elif messenger_input == "analysis":
                    analysis_question_config = "analysis"
                    continue
                elif messenger_input == "question":
                    analysis_question_config = "question"
                    continue
                elif messenger_input == "both":
                    analysis_question_config = "both"
                    continue
            print("_______________________________\n")

        print("Thanks for the interview! It was nice getting to know you!")


interview = Interview("biographer", dry_run=True)
