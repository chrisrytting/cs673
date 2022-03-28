import os
from lmsampler import LMSampler
from subject import Subject
from pdb import set_trace as breakpoint

class SoulSearcher:
    def __init__(self, interviewer_style, lm = 'gpt2', temperature = 0.7, pplm=False, dry_run=False):
        """
        interviewer_style: str - which persona SoulSearcher uses to analyze/question the subject
            'biographer'
            'mother'
            'journalist'
            'poet'
            'manager'
            'grandfather'
        lm: str - which language model to use
            'gpt2'
            'gpt2-medium'
            'gpt2-large'
            'gpt2-xl'
            'distilgpt2'
            'EleutherAI/gpt-j-6B'
            'EleutherAI/gpt-neo-2.7B'
            'EleutherAI/gpt-neo-1.3B'
            'EleutherAI/gpt-neo-125M'
            'j1-jumbo'             #Jurassic
            'j1-large' 
            'gpt3-ada'
            'gpt3-babbage'
            'gpt3-curie'
            'gpt3-davinci'
            'gpt3-text-davinci-001'
            'gpt3-text-davinci-002'
        temperature: float between 0 and 1
        pplm: bool - whether to use plug and play language model by Uber AI
        dry_run: bool - whether to use the real model or not
        """
        self.subject = Subject(dry_run=dry_run)
        self.lm = lm
        self.temperature = temperature

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
        model = LMSampler(self.lm)
        breakpoint()
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


if __name__=="__main__":
    soulsearcher = SoulSearcher("biographer", lm='gpt2-xl', dry_run=True)
