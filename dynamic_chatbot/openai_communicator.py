from asyncio.windows_events import NULL
import openai

class OpenAICommunicator:
    def call_openai(prompt, stop=None, presence_penalty=0, frequency_penalty=0):
        # Run OpenAI with the newest DaVinci engine.
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=2048, stop=stop, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty).choices[0].text
        return response