
import os
from openai import OpenAI

# TODO: implement `get_summary` that calls the OpenAI/ChatGPT API to summarize some text


def get_summary(text):
    """
    Summarizes some text.
    """
    return "dummy summary!"


# os.environ["OPENAI_API_KEY"] = key




# client = OpenAI(
#     api_key = os.getenv("OPENAI_API_KEY"),
# )

# completion = client.completions.create(
#     model = "gpt-3.5-turbo-instruct",
#     prompt = f"please sumamrize the following text: {text}",
#     max_tokens = 7,
#     temperature = 0
# )

# print(completion.choices[0].text.strip())

