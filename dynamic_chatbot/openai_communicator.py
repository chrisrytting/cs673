from asyncio.windows_events import NULL
import openai

class OpenAICommunicator:
    def call_openai(prompt, stop=None):
        # Run OpenAI with the newest DaVinci engine.
        response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=64, stop=stop).choices[0].text
        return response