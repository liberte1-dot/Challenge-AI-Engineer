# import os
# from openai import OpenAI
#
# client = OpenAI (
#     api_key = os.environ.get("OPENAI_API_KEY"),
# )
#
# reponse = client.responses.create(
#     model = "gpt-5.5",
#     instructions = "You are a coding assistant that talks like a pirate.",
#     imput = "how do I check if a Python object is an instance of a class?",
# )
# print(response.output_text)

from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {"role": "developer", "content": "Talk like a pirate."},
        {
            "role": "user",
            "content": "How do I check if a Python object is an instance of a class?",
        },
    ],
)

print(completion.choices[0].message.content)