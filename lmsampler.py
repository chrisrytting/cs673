# from lmsampler_baseclass import LMSamplerBaseClass
# from lm_gpt3 import LM_GPT3
# from lm_gpt2 import LM_GPT2
# from lm_gptj import LM_GPTJ
# from lm_gptneo import LM_GPTNEO
# from lm_bert import LM_BERT
# from lm_jurassic import LM_JURASSIC

from lmsampler_baseclass import LMSamplerBaseClass
from lm_gpt3 import LM_GPT3
from lm_gpt2 import LM_GPT2
from lm_gptj import LM_GPTJ
from lm_gptneo import LM_GPTNEO
from lm_jurassic import LM_JURASSIC
import datetime

from pdb import set_trace as breakpoint

# from . import lmsampler_baseclass
# from . import lm_gpt3
# from . import lm_gpt2
# from . import lm_gptj
# from . import lm_gptneo
# from . import lm_bert
# from . import lm_jurassic
def lmsamplertest():
    prompt = "My name is"
    # Open a text file whose title starts with test and ends with the current date.
    with open("test" + str(datetime.date.today()) + ".txt", "w") as text_file:
        for model_name in [
            "gpt2",
            "gpt2-medium",
            "gpt2-large",
            "gpt2-xl",
            "distilgpt2",
            "EleutherAI/gpt-j-6B",
            "EleutherAI/gpt-neo-2.7B",
            "EleutherAI/gpt-neo-1.3B",
            "EleutherAI/gpt-neo-125M",
            "j1-jumbo" "j1-large",  # Jurassic,
            "gpt3-ada",
            "gpt3-babbage",
            "gpt3-curie",
            "gpt3-davinci",
            "gpt3-text-davinci-001",
            "gpt3-text-davinci-002",
        ]:
            model = LMSampler(model_name)
            completion = model.sample_several(prompt, 0.7, 10)
            completion_description = f"{model_name} wrote {completion}"
            print(completion_description)
            text_file.write(completion_description + "\n" + "=" * 50 + "\n")
            del model


class LMSampler(LMSamplerBaseClass):
    """
    Class to wrap all other LMSampler classes. This way, we can instantiate just by passing a model name, and it will initialize the corresponding class.
    """

    def __init__(self, model_name):
        self.model_name = model_name
        super().__init__(model_name)
        """
        Supported models:
            - GPT-3: 'gpt3-ada', 'gpt3-babbage', 'gpt3-curie', 'gpt3-davinci', 'ada', 'babbage', 'curie', 'davinci', 'text-davinci-001', 'text-davinci-002'
            - GPT-2: 'gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl', 'distilgpt2'
            - GPT-J: 'EleutherAI/gpt-j-6B'
            - GPT-Neo: 'EleutherAI/gpt-neo-2.7B', 'EleutherAI/gpt-neo-1.3B', 'EleutherAI/gpt-neo-125M'
            - BERT: 'bert-base-uncased', 'bert-base-cased'
            - Jurassic: 'j1-jumbo', 'j1-large'
        """
        if model_name in [
            "gpt3-ada",
            "gpt3-babbage",
            "gpt3-curie",
            "gpt3-davinci",
            "ada",
            "babbage",
            "curie",
            "davinci",
            "gpt3-text-davinci-001",
            "gpt3-text-davinci-002",
            "text-davinci-001",
            "text-davinci-002",
        ]:
            self.model = LM_GPT3(model_name)
        elif model_name in [
            "gpt2",
            "gpt2-medium",
            "gpt2-large",
            "gpt2-xl",
            "distilgpt2",
        ]:
            self.model = LM_GPT2(model_name)
        elif model_name in ["EleutherAI/gpt-j-6B"]:
            self.model = LM_GPTJ(model_name)
        elif model_name in [
            "EleutherAI/gpt-neo-2.7B",
            "EleutherAI/gpt-neo-1.3B",
            "EleutherAI/gpt-neo-125M",
        ]:
            self.model = LM_GPTNEO(model_name)
        elif model_name in ["j1-jumbo", "j1-large"]:
            self.model = LM_JURASSIC(model_name)
        else:
            raise ValueError(f"Model {model_name} not supported.")

    def send_prompt(self, prompt, n_probs=100):
        return self.model.send_prompt(prompt, n_probs)

    def sample_several(self, prompt, temperature=0, n_tokens=10):
        return self.model.sample_several(prompt, temperature, n_tokens)


if __name__ == "__main__":
    # model_name = 'gpt3-ada'
    # print(sampler.send_prompt('In 2016, I voted for', 5))
    lmsamplertest()
