# PartyBot: A Bot for Setting Music Queues

## Description:

As part of the course "Cognitive Challenge", of IE's Master in Big Data and Business Analytics, this group project integrates IBM's Watson Assistant with Spotify in order to create an interactive chatbot which can define Spotify playlists based on user-specified moods and users.

## Spotify.py:

This script is in charge of connecting with a Spotify account via the spotipy Python library. This library makes accessing the Spotify API much easier. The functions in this script work with defining a playlist associated to the bot and filling it up with tracks from other playlists, which are specified by the user by means of moods and other users. Also, this script can reset this playlist or shuffle it.

**Sources:**
* Spotify for Developers, *Web API Reference*, <https://developer.spotify.com/documentation/web-api/reference-beta/#category-search>
* Morioh, *How to Extract Data using Spotify’s API, Python and Spotipy*, <https://morioh.com/p/31b8a607b2b0>
* spotipy, *Welcome to Spotipy!*, <https://spotipy.readthedocs.io/en/2.16.1/>


## WatsonIntegrator.py:

This second script makes use of the IBM Watson API, to send requests to a programmed assistant. This assistant has been programmed to respond via text, to be outputted to the user, but also with a coded message which the script Chatbot.py interprets in order to call certain functions. For example, let's say a new music queue is set, a user specifying that the mood for the playlist is "Christmas", the event for the playlist is "Dinner", and the people attending the event are only "Alejandro". Then, this IBM assistant is programmed to return, besides the text intended for the user:

`function:NewQueue,Christmas,Alejandro,Dinner`

Then, this script separates, from the assistant's response, the text message intended for the user, and the functional code intended for Chatbot.py.

**Sources:**
* IBM Cloud API Docs, *Watson Assistant V2*, <https://cloud.ibm.com/apidocs/assistant/assistant-v2?code=python>

## Chatbot.py:

On the one hand, this script interprets all function codes emmitted by the IBM assistant. These functions include, logging in to Spotify, setting up a new music queue for a new event, adding tracks from specified artists to the current queue, adding tracks from a specified playlist to the current queue, showing all upcoming tracks, and shuffling the queue.

On the other hand, this script also takes care of the integration with a predefined Telegram bot, which is employed as a UI for the project. This is done by storing all user input in a buffer, which is emptied every time a request is sent to the IBM assistant, as well as by storing all prompts to be printed in another buffer, which is emptied every time an output is presented in the Telegram Bot.

## app.py

This last script connects the Python implementation with an existing Telgram bot. It makes use of ngrok in order to set a webhook, and the Python Telegram API in order to link the webhook with the Telegram bot.

**Sources:**
* Toptal Developers, *Building Your First Telegram Bot: A Step by Step Guide*, <https://www.toptal.com/python/telegram-bot-tutorial-python>
* codeburst.io, *Building your first Chat Application using Flask in 7 minutes*, <https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d>
