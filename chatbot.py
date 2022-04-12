import os
from lmsampler import LMSampler
from subject import Subject
from pdb import set_trace as breakpoint


class SoulSearcher:
    def __init__(
        self,
        interviewer_style,
        lm="gpt2",
        temperature=0.7,
        pplm=False,
        bio_dry_run=False,
        dry_run=False,
        analysis_question_config="both",
    ):
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
        self.model = LMSampler(lm)
        self.subject = Subject(dry_run=bio_dry_run)
        self.temperature = temperature

        self.analysis_question_config = analysis_question_config
        self.analysis_question_config_dict = {
            "analysis": ["analysis"],
            "question": ["question"],
            "both": ["analysis", "question"],
        }

        self.templates = {
            "biographer": {
                "analysis": lambda subject_name, question, answer: (
                    f"I'm a biographer, and when I asked "
                    f"{subject_name} '{question}', they told me '{answer}'. "
                    f"When I heard that, I wanted to tell them"
                ),
                "question": lambda subject_name, question, answer: (
                    f"I'm a biographer, and when I asked "
                    f"{subject_name} '{question}', they told me '{answer}'. "
                    f'When I heard that, I wanted to ask them the question "'
                ),
            },
            "mother": {
                "analysis": lambda subject_name, question, answer: (
                    f"I'm {subject_name}'s mother, and when I asked them "
                    f"'{question}', they told me '{answer}'. "
                    f"When I heard that, I wanted to tell them"
                ),
                "question": lambda subject_name, question, answer: (
                    f"I'm {subject_name}'s mother, and when I asked them "
                    f"'{question}', they told me '{answer}'. "
                    f'When I heard that, I wanted to ask them the question "'
                ),
            },
            "journalist": {
                "analysis": lambda subject_name, question, answer: (
                    f"I'm a journalist, and when I asked "
                    f"{subject_name} '{question}', they told me '{answer}'. "
                    f"When I heard that, I wanted to tell them"
                ),
                "question": lambda subject_name, question, answer: (
                    f"I'm a journalist, and when I asked "
                    f"{subject_name} '{question}', they told me '{answer}'. "
                    f'When I heard that, I wanted to ask them the question "'
                ),
            },
            "poet": {
                "analysis": lambda subject_name, question, answer: (
                    f"I'm a poet, and when I asked "
                    f"{subject_name} '{question}', they told me '{answer}'. "
                    f"When I heard that, I wanted to tell them"
                ),
                "question": lambda subject_name, question, answer: (
                    f"I'm a poet, and when I asked "
                    f"{subject_name} '{question}', they told me '{answer}'. "
                    f'When I heard that, I wanted to ask them the question "'
                ),
            },
            "manager": {
                "analysis": lambda subject_name, question, answer: (
                    f"I'm {subject_name}'s manager, and when I asked them "
                    f"'{question}', they told me '{answer}'. "
                    f"When I heard that, I wanted to tell them"
                ),
                "question": lambda subject_name, question, answer: (
                    f"I'm {subject_name}'s manager, and when I asked them "
                    f"'{question}', they told me '{answer}'. "
                    f'When I heard that, I wanted to ask them the question "'
                ),
            },
            "grandfather": {
                "analysis": lambda subject_name, question, answer: (
                    f"I'm {subject_name}'s grandfather, and when I asked them "
                    f"'{question}', they told me '{answer}'. "
                    f"When I heard that, I wanted to tell them"
                ),
                "question": lambda subject_name, question, answer: (
                    f"I'm {subject_name}'s grandfather, and when I asked them "
                    f"'{question}', they told me '{answer}'. "
                    f'When I heard that, I wanted to ask them the question "'
                ),
            },
        }

        if interviewer_style not in self.templates:
            raise ValueError("Interviewer style not found")
        self.interviewer_style = interviewer_style
        self.carry_out_interview(dry_run=dry_run)

    def carry_out_interview(self, dry_run=False, evaluation=False):
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

        soul_searching_answers_evaluation = [
            "I like to make furniture. I find it very relaxing, very therapeutic, "
            "to work with my hands and to make something that exists in the "
            "physical world.",
            "Probably my high school English class. I was a big football player "
            "and felt like that was my identity, but I found out that I was much better "
            "at thinking and answering questions and writing than I was at tackling, "
            "and it's changed the course of my whole life.",
            "I had children. Raising children is the thing that made me feel "
            "that I had a real, meaningful role in the world.",
            "I really admire John Mayer, embarrassingly. He is a great musician, "
            "and he is a great intellect. He feels like a person that I'd "
            "really like in real life.",
            "I would tell my 18-year-old self that advice is highly over-rated, "
            "and the most important thoughts you'll ever find are your own, so "
            "to make them good, whatever that means to you.",
            "I love music, I love language, I love science, I love religion. I "
            "feel pretty basic when I talk about things that I love.",
            "A girlfriend gave me a book called 'The Crucible of Doubt' and symphony "
            "tickets for valentine's day. I felt very known that day.",
            "Again, the happiest day I've ever had was when my kids were born. "
            "I felt like everything changed that day.",
        ]

        if evaluation:
            templates = list(self.templates.keys())
        else:
            templates = [self.templates[self.interviewer_style]]
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
        for template in templates:
            for ix, question in enumerate(soul_searching_questions):
                print(question, q_options)
                if evaluation:
                    answer = soul_searching_answers_evaluation[ix]
                else:
                    answer = input()
                    if answer == "pass":
                        continue
                    elif answer == "end":
                        break
                conversation.append((question, answer))
                backstory = self.subject.print_backstory()
                while True:
                    # TODO pass in prompt according to analysis_question_config
                    for answer_type in self.analysis_question_config_dict[
                        analysis_question_config
                    ]:
                        prompt = backstory + '\n\n' + \
                            template[answer_type](
                                self.subject.name, question, answer)
                        if dry_run:
                            response = "I'm a bot, and I don't know what to say."
                        else:
                            response = self.model.sample_several(
                                prompt,
                                temperature=self.temperature,
                                n_tokens=50,
                                # stop_tokens=["\n"],
                            )
                            # response = openai.Completion.create(
                            #     engine="text-davinci-002",
                            #     prompt=prompt,
                            #     max_tokens=64,
                            #     stop=["\n"],
                            # )
                            # gpt3_followup = response.choices[0].text
                        print(f"Prompt: {prompt}\n\n{answer_type}: {response}")
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


if __name__ == "__main__":
    soulsearcher = SoulSearcher(
        "biographer", lm="gpt3-text-davinci-002", bio_dry_run=False, dry_run=False
    )
