from asyncio.log import logger
import dataclasses
from multiprocessing.connection import Client
from pathlib import Path
from pickle import TRUE
from urllib import response
from aiohttp import Payload
from dotenv import load_dotenv
from flask import request, Response

#python virtual environment
env_path = Path('.')/'.env' 
load_dotenv (dotenv_path = env_path)

import os
import slack
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
import re

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
slack_client = slack.WebClient(os.environ.get('SLACK_BOT_TOKEN'))
BOT_ID = slack_client.api_call("auth.test")['user_id']     

# Design the bot home page
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        # Call views.publish with the built-in client
        client.views_publish(
            # Use the user ID associated with the event
            user_id=event["user"],
            # Home tabs must be enabled in your app configuration
            view={
                "type": "home",
                "blocks": [ 
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "My main purpose is to provide you with steps to take if you have tested positive, provide helpful information on workplace safety, and to support you with current company strategies about COVID-19.\n:star::star::star::star:"
                            }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*What Can Purinina Help You With?*"
                            }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Tested Positive*\n🤒: Seek answers to paid leave and mental health queries if you have tested positive, or need to care for someone who has."
                            },
                            "accessory": {
                                "type": "image",
                                "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/c7ed05m9lC2EmA3Aruue7A/o.jpg",
                                "alt_text": "alt text for image"
                            }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Workplace Safety*\n😷: Investigate the measures being taken by The Daily News Company to limit the spread of COVID-19. "
                            },
                            "accessory": {
                                "type": "image",
                                "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/c7ed05m9lC2EmA3Aruue7A/o.jpg",
                                "alt_text": "alt text for image"
                            }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Help/Feedback*\n🚨: Send real-time feedback to our bot team and access human assistance for your workplace COVID-19 queries.\n :pushpin:: *Medical Emergency*, please call: `000`"
                            },
                            "accessory": {
                                "type": "image",
                                "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/c7ed05m9lC2EmA3Aruue7A/o.jpg",
                                "alt_text": "alt text for image"
                            }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Other Concerns*\n Please call the *National Coronavirus Helpline*: <fakelink.toUrl.com|1800 020 080>"
                            },
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "👀 Try it out by typing the `/task-list` command or say <fakelink.toUrl.com|'hi'> in the 'Messages' page to start a conversation with me. 💬(please use lowercase letters)"
                            },                   
                    },
                ]
            }
       )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


# Listens to incoming messages that contain "hello"
@app.message(re.compile("(hi|hello|hey|Hi|Hello|Hey)"))
def message_hello(message, context, say):
    # regular expression matches are inside of context.matches
    if context['matches'][0]:
    # say() sends a message to the channel where the event was triggered
        say(
        blocks=[ 
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "'G' day mate! 👋 My name is Purinina and I am your Daily News Company's COVID-19 bot. Feel free to call me Nina😊. My main purpose is to be an efficient, central hub for COVID-19 workplace information. I'm not a doctor and cannot diagnose your symptoms, so if you are unwell, please speak to your GP or dial 000 in case of emergencies 🏥.\n*Please select a concern:*"
                            }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Tested positive",
                                    "emoji": True
                                    },
                                    "value": "tested_positive",
                                    "action_id": "tested_positive_button"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Workplace safety",
                                    "emoji": True
                                    },
                                    "value": "workplace_safety",
                                    "action_id": "workplace_safety_button"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Help/Feedback",
                                    "emoji": True
                                    },
                                    "style": "primary",
                                    "value": "help",
                                    "action_id": "help_button"
                            }
						]
					},
					{
								"type": "section",
								"text": {
									"type": "mrkdwn",
									"text": "Type in `/task-list` for activating my task list menu."
									},
                    },
               ]
            )



# Your listener will be called every time an interactive component with the action_id "workplace_safety_button" is triggered
@app.action("workplace_safety_button")
def button_click(ack, say):
    ack()
    say(
        replace_original=False,
        blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":star::star::star::star:*Click your Workplace safety concerns*"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "While we cannot mandate the COVID-19 vaccination in this workplace, \
we highly recommend it as a way of keeping yourself and others safe ✅ 💪. Check out the vaccine options currently available to you! "
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Vaccination options"
				},
				"value": "vaccination_options",
				"action_id": "vaccination_options_button"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"emoji": True,
					"text": "3 clicks"
				}
			]
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "\nFind out where to source your RAT tests. 🔍"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "RAT tests"
				},
				"value": "rat_tests",
				"action_id": "rat_tests_button"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"emoji": True,
					"text": "10 clicks"
				}
			]
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Explore the strategies in place by The Daily News Company designed to keep you safe. 📋"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"emoji": True,
					"text": "Current workplace safety strategies"
				},
				"value": "current_strategies",
				"action_id": "current_strategies_button"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "No clicks"
				}
			]
		},
	   ]
	)






# Your listener will be called every time an interactive component with the action_id "help_button" is triggered
@app.action("help_button")
def button_click(ack, say):
    ack()
    say(
        blocks = [
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"multiline": True,
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "We would love to hear from you",
				"emoji": True
			}
		}
	]
	)








# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()