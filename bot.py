import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path(".")/".env"
load_dotenv(dotenv_path = env_path)

app = Flask(__name__)

client = slack.WebClient(token = os.environ["SLACK_TOKEN"])

client.chat_postMessage(channel = "#test", text = "Hellow Team 6")

if __name__ == "__main__":
    app.run(debug = True)