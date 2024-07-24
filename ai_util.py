import openai
import csv
db = "CustomerList.csv"

system_content = "You should recommend the related services. Be descriptive and helpful."

client = openai.OpenAI(
    api_key="a4c8bb7d54da4613b70d76d34fa2f90a",
    base_url="https://api.aimlapi.com",
)

def getRecommendation(command_text):
    prompt = ""
    with open(db, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rate = -1 if int(row["Rates"]) == 0 else float(row["SumRating"]) / int(row["Rates"])
            if rate == -1:
                prompt += ("Company " + row["Company"] + " does " + row["ServiceType"] + " and does not have any rate yet.")
            else:
                prompt += ("Company " + row["Company"] + " does " + row["ServiceType"] + " and its rating is " + str(rate) + ". ")
    prompt += f"Please recommend the companies that do {command_text} services."
    chat_completion = client.chat.completions.create(
        model = "mistralai/Mistral-7B-Instruct-v0.2",
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt},
        ],
        temperature = 0.7,
        max_tokens = 100,
    )
    print(prompt)
    return chat_completion.choices[0].message.content