import openai
openai.api_key = "sk-proj-VHNSMoTUcBMHw5ZJGRhbT3BlbkFJyYq8R1S0NxcoNwPyrBB0"
# from openai import OpenAI
# client = OpenAI()

def getResponse(prompt):
    response = openai.Completion.create(
        engine = "gpt-3.5",  # Specify the engine (e.g., "text-davinci-003")
        prompt = prompt,
        max_tokens = 1000  # Adjust the maximum number of tokens in the response as needed
    )
    answer = response.choices[0].text.strip()

    # completion = openai.chat.completions.create(
    #     model = "gpt-3.5",
    #     messages = [
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Hello!"}
    #     ]
    # )

    # print(completion.choices[0].message)
    return answer
