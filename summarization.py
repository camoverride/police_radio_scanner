
import os
from openai import OpenAI



# client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"),)

PROMPT = """
The following is the transcription of a police radio conversation. The conversation was recorded on a noisy radio, which means the transcription will have inaccuracies. For instance, the word "copy" is often incorrectly transcribed as "coffee." Additionally, words or phrases that occur at the beginning or end of the transcription might be clipped, as this is where the recording began or ended. Also, there are ads inserted into the conversations. If you see an add, don't describe it, simply write "NOW FOR A COMMERCIAL BREAK!"

I want you to summarize this conversation. Use declarative sentences. Do not express uncertainty. Use the present tense only. Be concise but accurate. Pay special attention to times, locations, and the identities of individuals. Try to identify any crimes or weird events that happened. If there is a violent or aggressive situation, make sure to describe it. Below is the police radio transcription:


"""


def get_summary(text):
    """
    Summarizes some text.
    """
    return text
    completion = client.completions.create(
        model = "gpt-3.5-turbo-instruct",
        prompt = f"{PROMPT}: {text}",
        max_tokens = 10,
        temperature = 0
    )

    return completion.choices[0].text.strip()



if __name__ == "__main__":
    dummy_convo = ""

    response = get_summary(dummy_convo)

    print(response)
