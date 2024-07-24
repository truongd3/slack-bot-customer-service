import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter

import ai_util

import helper
import csv
db = "CustomerList.csv"

env_path = Path(".")/".env"

load_dotenv(dotenv_path = env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token = os.environ["SLACK_TOKEN"])

message_counts = {}

BOT_ID = client.api_call("auth.test")["user_id"]

# @slack_event_adapter.on('message')
# def message(payload):
#     event = payload.get('event', {})
#     channel_id = event.get('channel')
#     user_id = event.get('user')
#     text = event.get('text')

#     if BOT_ID != user_id:
#         if user_id in message_counts:
#             message_counts[user_id] += 1
#         else:
#             message_counts[user_id] = 1
#         client.chat_postMessage(channel = channel_id, text = "Hey {user_name}, {text}".format(user_name = client.users_info(user=user_id)['user']['name'], text = text))

@app.route("/message-count", methods=["POST"])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get("channel_id")
    message_count = message_counts.get(user_id, 0)
    client.chat_postMessage(channel=channel_id, text=f"Number of messages: {message_count}")
    return Response(), 200

@app.route("/recommendation", methods=["GET", "POST"])
def recommendation():
    data = request.form
    command_text = data.get('text')
    answer = ai_util.getRecommendation(command_text)
    client.chat_postMessage(channel="#test", text=answer)
    return Response(), 200

@app.route("/rate", methods=["GET", "POST"])
def rate():
    data = request.form
    channel_id = data.get("channel_id")
    command_text = data.get('text')
    params = helper.split(command_text)
    # Get rate
    if len(params) == 1:
        with open(db, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if params[0].lower() in row["Company"].lower():
                    company = row["Company"]
                    if int(row["Rates"]) == 0:
                        client.chat_postMessage(channel=channel_id, text=f"No Rate Yet for {company}")
                    else:
                        rate = float(row["SumRating"]) / int(row["Rates"])
                        client.chat_postMessage(channel=channel_id, text=f"{company} is rated {rate}")
                    return Response(), 200
            client.chat_postMessage(channel=channel_id, text=f"Company/Service {params[0]} Not Found")
            return Response(), 404
    # Give rate
    elif len(params) == 2:
        company = params[0]
        rate = float(params[1])
        found = False
        if rate > 5 or rate < 0:
            client.chat_postMessage(channel=channel_id, text="Rate should be in range of 0 and 5.")
            return Response(), 404
        
        with open(db, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        for row in data:
            if row['Company'].lower() == params[0].lower():
                row['SumRating'] = str(float(row['SumRating']) + rate)
                row["Rates"] = str(int(row["Rates"]) + 1)
                new_rate = float(row["SumRating"]) / int(row["Rates"])
                client.chat_postMessage(channel=channel_id, text=f"Rate updated for {company}: {new_rate}")
                found = True
                break
        if found == False:
            client.chat_postMessage(channel=channel_id, text=f"Company/Service {company} Not Found")
            return Response(), 404
        with open(db, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return Response(), 200
    # Invalid
    else:
        client.chat_postMessage(channel=channel_id, text="Invalid number of paraments. Try again")
        return Response(), 404

if __name__ == "__main__":
    app.run(debug = True)