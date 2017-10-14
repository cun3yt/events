# Slack Bot for Events

Have slack a bot to give you hints about weekend events.

## Installation

This is a Django application built with Python 3.6.

* Create virtual environment with Python 3.6
* Run `pip install -r requirements`
* Install ngrok for local development: `brew cask install ngrok`
* Run Django application: `./manage runserver`
* Run ngrok on the port Django's localhost port (default: 8000): `ngrok http 8000`
* Specify the URL end points to ngrok.io that is given when you ran ngrok.

