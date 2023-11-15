# HR-Chatbot-Using-RASA
Create a chatbot for efficient HR communication using RASA.

RASA
Rasa is an open source machine learning framework for building AI assistants and chatbots. Mostly you don’t need any programming language experience to work in Rasa. Although there is something called “Rasa Action Server” where you need to write code in Python, that mainly used to trigger External actions like Calling Google API or REST API etc.


           Install Rasa Open Source
conda create -n rasa-app python=3.6

conda env list

conda activate rasa-app

pip3 install rasa

This page explains the basics of building an assistant with Rasa and shows the structure of a Rasa project. You can test it out right here without installing anything.

     
The first step is to create a new Rasa project. To do this, run:

rasa init --no-prompt

The rasa init command creates all the files that a Rasa project needs and trains a simple bot on some sample data. If you leave out the --no-prompt flag you will be asked some questions about how you want your project to be set up.

This creates the following files:

__init__.py →an empty file that helps python find your actions

actions.py →code for your custom actions

config.yml ‘*’ →configuration of your NLU and Core models

credentials.yml →details for connecting to other services

data/nlu.md ‘*’ →your NLU training data

data/stories.md ‘*’ →your stories

domain.yml ‘*’ →your assistant’s domain

endpoints.yml →details for connecting to channels like fb messenger

models/<timestamp>.tar.gz →your initial model

READ : https://medium.com/voice-tech-podcast/how-to-create-chatbot-using-rasa-82954e141ae7
