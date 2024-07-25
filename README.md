# Customer-Service Slack Bot

## Features

- Built with Mistral v0.2 AI model
- Built with Python/Flask
- Built with Slack Event API to set up all Slack slash commands
- Sends the optimal companies that satisfy users’ commands
- Interact based on commands 

## Benefits

- Easy to get recommendation
- Easy to rate services
- Saves time
- Lightweight and low cost


## How to run

- Open an terminal and type `ngrok http 5000`
- Copy the _Forwarding URL_ and paste to [Slack App](https://api.slack.com/apps/)
- Open a new terminal and run [bot.py](bot.py)

## How to use

- `/recommendation <SERVICE>`: Return a list of corresponding services. For example, `/recommendation beauty`, `/recommendation ai`, `/recommendation healthcare`, etc.
- `/rate <COMPANY>`: Give the rate of a service/company. For example, `/rate Google`, `/rate Luminary`, `/rate KeyMe`, etc.
- `/rate <COMPANY> <SCORE 0-5>`:  Rate a service/company in a scale of 5. For example, `/rate Google 1`, `/rate Luminary 5`, `/rate KeyMe 3.7`, etc.

### Members

- Chengling Zheng
- Lauren Fitzharris
- Truong Dang