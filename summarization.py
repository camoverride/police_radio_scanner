import os
from openai import OpenAI



PROMPT_PREFIX = """
Please summarize the following text. It is a transcription of a police radio conversation with several speakers. There will be transcription errors. Use declarative sentences. Use the present tense. Try to use short sentences with periods. Use confident language. Pay close attention to the crimes and odd events.
"""


def get_summary(data):
    """
    Feeds the prompt_prefix (which describes the task) and the recordings data
    to the OpenAI API to get a summarization.
    """

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{PROMPT_PREFIX}\n\n {data}",
            }
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content



if __name__ == "__main__":

    # Test API call
    test_data = """
    teaching and i can be contacted via farce vehicles registered address fishy    i'm a dispatch you enjoy myself taking to i'm taking  lg realize the dorling old army think as long as we're going on keys you can find out fault our funding for the are of park we we have to have your crew's coming here we have a couple are both need transport both are covered positive|teaching and i can be contacted via farce vehicles registered address fishy    i'm a dispatch you enjoy myself taking to i'm taking  lg realize the dorling old army think as long as we're going on keys you can find out fault our funding for the are of park we we have to have your crew's coming here we have a couple are both need transport both are covered positive
    """

    summary = get_summary(PROMPT_PREFIX,test_data)

    print(summary)
