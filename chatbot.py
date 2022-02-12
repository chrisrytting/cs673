import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']

subject_name = 'Dan Ventura'

questions = [
    "What is your name?",
    "What do you like to do for fun?",
    "Where are you from?",
    "How old are you?",
    "What is the most important thing that ever happened to you?",
    "What is the accomplishment your are most proud of?",
    "Who is the person you admire the most?",
    "What is the thing you would tell an 18-year old version of yourself?",
    "What are your greatest passions in life?",
    "What is the best gift that you've ever been given?",
    "What has been the happiest time of your life so far?",
]

# Templates
templates = {
    "biographer": lambda answer: (f"I'm a biographer, and when I asked "
                                  f"{subject_name} '{question}', they told me "
                                  f"When I heard that, I thought '{answer}'"),
    "mother": lambda answer: (f"I'm {subject_name}'s mother, and when I asked them "
                              f"'{question}', they told me that '{answer}'. "
                              f"When I heard that, my reaction was"),
    "journalist": lambda answer: (f"I'm a journalist, and when I asked "
                                  f"{subject_name} '{question}', they told me "
                                  f"When I heard that, I thought '{answer}'"),
    "poet": lambda answer: (f"I'm a poet, and when I asked "
                                  f"{subject_name} '{question}', they told me "
                                  f"When I heard that, I felt '{answer}'"),
    "manager": lambda answer: (f"I'm {subject_name}'s manager, and when I asked them "
                              f"'{question}', they told me that '{answer}'. "
                              f"When I heard that, my reaction was"),
    "grandfather": lambda answer: (f"I'm {subject_name}'s grandfather, and when I asked them "
                              f"'{question}', they told me that '{answer}'. "
                              f"When I heard that, I wanted to know"),
}


for question in questions:
    print(question)
    answer = input()
    for label, template in templates.items():
        prompt = template(answer)
        response = openai.Completion.create(engine="davinci", prompt=question)
        print(response.choices[0].text)
