from asyncio.log import logger
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
from slack_bolt import App, Respond
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.errors import SlackApiError
import re

# Initializes your app with your bot token and socket mode handler
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
slack_client = slack.WebClient(os.environ.get('SLACK_BOT_TOKEN'))
BOT_ID = slack_client.api_call("auth.test")['user_id']     


# Commands enable users to interact with your app with a `/ `
@app.command("/task-list")
def repeat_text(ack, say):
    # Acknowledge command request
    ack()
    say(
        blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Hey there 👋 I'm Purinina and I am your Daily News Company's COVID-19 bot.\nThere are three main concerns that I can support with:*"
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
				"text": "*Tested positive Menu*"
			}
		},
        {
			"type": "divider"
		},
        {
			"type": "actions",
			"elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Needing sick leave",
                                    "emoji": True
                                    },
								    "style": "primary",
                                    "value": "sick_leave",
                                    "action_id": "sick_leave_button"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Caring for someone with COVID-19",
                                    "emoji": True
                                    },
                                    "value": "caring",
                                    "action_id": "caring_button"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Looking after your mental health",
                                    "emoji": True
                                    },
                                    "value": "mental health",
                                    "action_id": "mental_health_button"
                            }
						]
		},
        {
			"type": "actions",
			"elements": [
                            {
                                "type": "button",
				                "text": {
					            "type": "plain_text",
					            "text": "Sick leave requirement",
					            "emoji": True
			                   	},
				            "value": "sick_leave_requirement",
			             	"action_id": "sick_leave_requirement_button"
                            },
                            {"type": "button",
				                "text": {
					            "type": "plain_text",
				            	"text": "Out of sick leave",
					            "emoji": True
				                },
			                  	"value": "out_of_sick",
			                 	"action_id": "out_of_sick_button"
                            },
						]
		},
        {
			"type": "divider"
		},
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Workplace safety menu*"
			}
		},
        {
			"type": "actions",
			"elements": [
                            {
                                "type": "button",
				                "text": {
					            "type": "plain_text",
				            	"emoji": True,
					           "text": "Vaccination options"
				           },
				               "value": "vaccination_options",
				               "action_id": "vaccination_options_button",
				               "style": "primary",
                            },
                            {
                                "type": "button",
				               "text": {
				            	"type": "plain_text",
				             	"emoji": True,
				            	"text": "RAT tests"
			                    	},
				               "value": "rat_tests",
				               "action_id": "rat_tests_button"
                            },
                            {
                                    "type": "button",
				                    "text": {
					                "type": "plain_text",
					                "emoji": True,
					                "text": "Current workplace safety strategies"
				                },
				                 "value": "current_strategies",
				                "action_id": "current_strategies_button"
                            },
						]
		},
    ]
)

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
                            "text": "G'day mate! 👋 My name is Purinina. My main purpose is to provide you with steps to take if you have tested positive, provide helpful information on workplace safety, and to support you with current company strategies about COVID-19.\n:star::star::star::star:"
                            }
                    },
                    {
			           "type": "context",
		              	"elements": [
			                  	{
					            "type": "image",
					            "image_url": "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png",
					            "alt_text": "placeholder"
			            	}
		             	]
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
                            "text": "👀 Try it out by typing the `/task-list` command or say <fakelink.toUrl.com|'hi'> in the 'Messages' page to start a conversation with me. \n💬 Please use lowercase letters"
                            },                   
                    },
                ]
            }
       )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")



# When a user joins the workspace, send a message in a predefined channel
@app.event("member_joined_channel")
def member_joined_channel(event, say):
    bot_team_channel_id = "your-team-id"
    user_id = event["user"]
    text = f"Welcome to the bot team, <@{user_id}>! 🎉 My name is Purinina and I am your Daily News Company's COVID-19 bot. Feel free to call me Nina😊. \
You can wake me up in this channel by @Purinina or sending direct command “/task-list” on my 'Messages' page. \n💬 Please use lowercase letters"
    say(text=text, channel=bot_team_channel_id)


#@Purinina in a slack channel
@app.event("app_mention")
def event_test(event, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there, I am your workplace COVID-19 information bot, my name is Purinina <@{event['user']}>!\
                    \n*Please select a concern:*"
                },
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
        ],
    )

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
                            "text": "'G' day mate! 👋 My name is Purinina and I am your Daily News Company's COVID-19 bot. Feel free to call me Nina😊. \
My main purpose is to be an efficient, central hub for COVID-19 workplace information. I'm not a doctor and cannot diagnose your symptoms, so if you are unwell, please speak to your GP or dial 000 in case of emergencies 🏥.\n*Please select a concern:*"
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
               ]
            )




# Your listener will be called every time an interactive component with the action_id "tested_positive_button" is triggered
@app.action("tested_positive_button")
def button_click(ack, say):
    ack()
    say(
        blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Hi, there! :wave:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "There are three main concerns your workplace has identified relating to a positive test result:"
			}
		},
	    {
            "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Needing sick leave",
                                    "emoji": True
                                    },
								    "style": "primary",
                                    "value": "sick_leave",
                                    "action_id": "sick_leave_button"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Caring for someone with COVID-19",
                                    "emoji": True
                                    },
                                    "value": "caring",
                                    "action_id": "caring_button"
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Looking after your mental health",
                                    "emoji": True
                                    },
                                    "value": "mental health",
                                    "action_id": "mental_health_button"
                            }
						]
					},
	]
)

# Your listener will be called every time an interactive component with the action_id "sick_leave_button" is triggered
@app.action("sick_leave_button")
def button_click(ack, say):
        say(
        blocks= [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "• *Needing sick leave* \nFor concern: What are the COVID-19 sick leave requirements at The Daily News Company?"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Sick leave requirement",
					"emoji": True
				},
				"value": "sick_leave_requirement",
				"action_id": "sick_leave_requirement_button"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "For concern: What if I am out of sick leave? "
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Out of sick leave",
					"emoji": True
				},
				"value": "out_of_sick",
				"action_id": "out_of_sick_button"
			}
		},
        {
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Alternatively, please call the HR department at: xxxx ☎️",
				"emoji": True
			}
		}
	]
)

# Your listener will be called every time an interactive component with the action_id "sick_leave_requirement_button" is triggered
@app.action("sick_leave_requirement_button")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "If you are a full or part-time employee at The Daily News Company and have tested positive to COVID-19 (or awaiting a test result/ been impacted directly by isolation guidelines), you may be eligible to access paid, COVID-19 sick-leave ✅. \
                        \nPlease be aware that The Daily News Company requires employees to provide a medical certificate for verification purposes 📋. This can be accessed via a telehealth appointment with your local GP ☎️. \
                        \nIf you have any further questions or concerns, please contact HR, or alternatively, visit the Australian Government COVID-19 Fair Work website here:https://coronavirus.fairwork.gov.au/coronavirus-and-australian-workplace-laws/pay-leave-and-stand-downs/quarantine-self-isolation \
                        \nType in `/task-list` for activating my task list menu."
                        },
            }
        ],
	)

# Your listener will be called every time an interactive component with the action_id "out_of_sick_button" is triggered
@app.action("out_of_sick_button")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "Please do not worry if you are out of sick leave! You may still be entitled to another form of paid leave. \
If not, you also have the option of taking unpaid leave during this time 💙. Please speak directly with HR to confirm leave options currently available to you ✅. \
    \nType in `/task-list` for activating my task list menu."},
            }
        ],
	)

# Your listener will be called every time an interactive component with the action_id "mental_health_button" is triggered
@app.action("mental_health_button")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "In moments like this, it is important to be connected with those who are there to help. \
Lifeline, one of Australia's most prominent mental health charities, is here for you during this upsetting and complicated time. 💙 \
\nI recommend talking to a real human being (I wish I was more than simply a bot!) who can help to empower you through this challenge, \
please visit Lifeline's website below for more information, or speak to them directly on 13 11 14:💬https://www.lifeline.org.au/get-help/information-and-support/covid-19/ \
                        \nType in `/task-list` for activating my task list menu."
                        },
            }
        ],
	)


# Your listener will be called every time an interactive component with the action_id "caring_button" is triggered
@app.action("caring_button")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "Here at The Daily News Company, we respect and understand the importance of caring for an unwell loved one 💙. \
That's why, in alignment with the Australian Government's Fair Work policy, you, as a full-time or part-time employee, are able to access Paid Carer's Leave ✅. \
                        \nFor more information, please visit the Fair Work webpage related to COVID-19:https://coronavirus.fairwork.gov.au/coronavirus-and-australian-workplace-laws/pay-leave-and-stand-downs/sick-and-carers-leave\
                        \nIf you need to put in an application for Care's Leave based on COVID-19, please get in touch with relevant staff at The Daily News Company 👍. \
                        \nType in `/task-list` for activating my task list menu."
                    },
            }
        ],
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
				"text": ":star::star::star::star:\n*Click your Workplace safety concerns*"
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
				"action_id": "vaccination_options_button",
				"style": "primary",
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


# Your listener will be called every time an interactive component with the action_id "rat_tests_button" is triggered
@app.action("rat_tests_button")
def button_click(ack, say):
    ack()
    say(
        replace_original=False,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "A Rapid Antigen Test (otherwise known as a 'RAT') is a DIY COVID-19 test that can be done from your own home, and will produce a positive ✅ or negative ❌ result. \
RATs are an important tool for navigating the virus as it spreads throughout the community, and are important to have on-hand if you develop symptoms 🤒. Due to demand, however, they can be challenging to source. \
\nIn GREAT news, The Daily News Company offers free RAT tests to all of our employees. Isn't that fantastic? 🥳 Simply get in contact with the administrative office and you'll be able to gain access for all your testing needs.\
                        \nType in `/task-list` for activating my task list menu."
                        },
            }
        ],
	)

# Your listener will be called every time an interactive component with the action_id "current_strategies_button" is triggered
@app.action("current_strategies_button")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "The Daily News Company is currently employing a range of strategies to limit the spread of COVID-19 in our workplace. \
These include making sure that employees are working 1.5m apart 📏, providing ample supply of alcohol-based hand sanitiser in all office spaces, as well as regularly cleaning and stocking bathroom facilities 🧼. \
These strategies are aligned with the recommendations made by Safe Work Australia ✅. We are also encouraging all employees to carry a mask on their person, and to wear it in close-speaking settings 😷. \
For more information, feel free to check out the Safe Work Australia website: https://covid19.swa.gov.au/covid-19-information-workplaces/industry-information/office/hygiene#heading--2--tab-toc-what_do_i_need_to_consider_when_providing_hygiene_facilities \
                        \nType in `/task-list` for activating my task list menu."
                        },
            }
        ],
	)


# Your listener will be called every time an interactive component with the action_id "vaccination_options_button" is triggered
@app.action("vaccination_options_button")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "😊I'm glad to hear you're interested in learning more about the COVID-19 vaccination, which The Daily News Company has encouraged as part of its return-to-work policy ✅."
                        },
		    },
		    {
			"type": "actions",
			"elements": [
				{
					"type": "checkboxes",
					"initial_options": [
						{
							"text": {
								"type": "mrkdwn",
								"text": "~*Get ready to know more about vaccination💉📚*~"
							},
							"value": "option 1"
						}
					],
					"options": [
						{
							"text": {
								"type": "mrkdwn",
								"text": "~*Get ready to know more about vaccination💉📚*~"
							},
							"value": "option 1"
						},
					]
				}
			    ],
			},
			{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ":muscle::syringe:"
			},
			"accessory": {
				"type": "checkboxes",
				"options": [
					{
							"text": {
								"type": "mrkdwn",
								"text": "*Why does The Daily News Company want me to be vaccinated?*"
							},
							"value": "option 2",
						},
				],
				"action_id": "option_2"
			          }
		    },
			{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "🔍"
			},
			"accessory": {
				"type": "checkboxes",
				"options": [
					{
							"text": {
								"type": "mrkdwn",
								"text": "*What vaccines are currently available for me to receive?*"
							},
							"value": "option 3",
						},
				],
				"action_id": "option_3"
			          }
		    },
			{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "💉🩹"
			},
			"accessory": {
				"type": "checkboxes",
				"options": [
					{
							"text": {
								"type": "mrkdwn",
								"text": "*How can I receive my vaccination?*"
							},
							"value": "option 4",
						},
				],
				"action_id": "option_4"
			          }
		    },
			{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "📚"
			},
			"accessory": {
				"type": "checkboxes",
				"options": [
					{
							"text": {
								"type": "mrkdwn",
								"text": "*Where can I read more information on the COVID-19 vaccination?*"
							},
							"value": "option 5",
						},
				],
				"action_id": "option_5"
			          }
		    },
			{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "😟"
			},
			"accessory": {
				"type": "checkboxes",
				"options": [
					{
							"text": {
								"type": "mrkdwn",
								"text": "*Who do I need to speak to if I have concerns?*"
							},
							"value": "option 6",
						},
				],
				"action_id": "option_6"
			          }
		    },
        ],
	)


# Your listener will be called every time an interactive component with the action_id "option_2" is triggered
@app.action("option_2")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
			"type": "divider"
		    },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "The Daily News Company cannot mandate the COVID-19 vaccination, however we strongly encourage it in order to protect the most vulnerable in our workplace, as well as reducing the risk of your own severe illness if you come into contact with the virus ✅ 🤧. \
If you'd like to know more, feel free to take a look at the Safe Work Australia website, where you can explore the community benefits of widespread vaccination: https://covid19.swa.gov.au/covid-19-information-workplaces/industry-information/general-industry-information/vaccination"},
                "accessory": {
				       "type": "button",
                       "text": {
                                "type": "plain_text",
                                "text": "Back to Vaccination options",
                                "emoji": True
                            },
                "value": "vaccination_options_button",
                "action_id": "vaccination_options_button"
                },
            },
         ]
	)

# Your listener will be called every time an interactive component with the action_id "option_3" is triggered
@app.action("option_3")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
			"type": "divider"
		    },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "In Australia, we have four vaccines that you can choose from: AstraZeneca, Moderna, Pfizer and Novovax ✅. You can read more about them here: https://www.health.gov.au/initiatives-and-programs/covid-19-vaccines/approved-vaccines"
                    },
                "accessory": {
				       "type": "button",
                       "text": {
                                "type": "plain_text",
                                "text": "Back to Vaccination options",
                                "emoji": True
                            },
                "value": "vaccination_options_button",
                "action_id": "vaccination_options_button"
                },
            }
        ],
	)


# Your listener will be called every time an interactive component with the action_id "option_4" is triggered
@app.action("option_4")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
			"type": "divider"
		    },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "The best way to receive your vaccination is by firstly booking an appointment through your GP, or a relevant government health website 💻 🏥. While I cannot book a vaccination for you, you can go to this website here which will start you on your journey: https://www.health.gov.au/initiatives-and-programs/covid-19-vaccines?gclid=Cj0KCQjwheyUBhD-ARIsAHJNM-PYNfEeVxpCdy_6fc5AR8r3KhlnapzpPzxJ8JWvFDtUkhaQl0w8r8caAmkiEALw_wcB&gclsrc=aw.ds \
                        "},
                "accessory": {
				       "type": "button",
                       "text": {
                                "type": "plain_text",
                                "text": "Back to Vaccination options",
                                "emoji": True
                            },
                "value": "vaccination_options_button",
                "action_id": "vaccination_options_button"
                },
            }
        ],
	)


# Your listener will be called every time an interactive component with the action_id "option_5" is triggered
@app.action("option_5")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
			"type": "divider"
		    },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "💻 If you want to know more about receiving the vaccine, or have concerns about safety, please make sure you read information from a reputable source, such as the Australian Government Health website: https://www.health.gov.au/initiatives-and-programs/covid-19-vaccines/approved-vaccines/safety-side-effects#:~:text=COVID%2D19%20vaccinations%20are%20safe,vaccine%20safety%20and%20side%20effects \
                        "},
                "accessory": {
				       "type": "button",
                       "text": {
                                "type": "plain_text",
                                "text": "Back to Vaccination options",
                                "emoji": True
                            },
                "value": "vaccination_options_button",
                "action_id": "vaccination_options_button"
                },
            }
        ],
	)


# Your listener will be called every time an interactive component with the action_id "option_6" is triggered
@app.action("option_6")
def button_click(ack, say):
    ack()
    say(
        blocks=[
            {
			"type": "divider"
		    },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "If you are concerned about getting the vaccine, or wish to discuss any related issues, please have a chat with your GP 🏥 ☎️. \
                        "},
                "accessory": {
				       "type": "button",
                       "text": {
                                "type": "plain_text",
                                "text": "Back to Vaccination options",
                                "emoji": True
                            },
                "value": "vaccination_options_button",
                "action_id": "vaccination_options_button"
                },
            }
        ],
	)


# Listens to incoming messages that contain "thanks"
@app.message(re.compile("(thx|tha|happy|Tha|Thx)"))
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
				"text": "You're very welcome! Glad I could help😊.\nType in `/task-list` for activating my task list menu."
			},
		},
        ]
)


# Listens to incoming messages that contain "thanks"
@app.message(re.compile("(great|helpful|helping|support|nice)"))
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
				"text": "I'm so happy I could assist you today!😊.\nType in `/task-list` for activating my task list menu."
			},
		},
        ]
)


# Listens to incoming messages that contain "thanks"
@app.message(re.compile("(bye|see)"))
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
				"text": "No worries! Bye!😊.\nType in `/task-list` for activating my task list menu."
			},
		},
        ]
)

# Listens to incoming messages that contain bad language
@app.message(re.compile("(fuck|Fuck|Silly|idiot|stupid|silly|suck|Hell|hell|HELL)"))
def message_hello(ack, context, message, say):
    # regular expression matches are inside of context.matches
      if context['matches'][0]:
    # say() sends a message to the channel where the event was triggered
        say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": f"I'm sorry, but that language goes against our company culture ☹️. Please revise your language! <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "let's have a respectful conversation"},
                    "action_id": "respectful_conversation_button",
                    "style": "danger",
                }
            }
        ],
    )

@app.message(re.compile("(pathetic|hopeless|bad|useless)"))
def message_hello(ack, context, message, say):
    # regular expression matches are inside of context.matches
      if context['matches'][0]:
    # say() sends a message to the channel where the event was triggered
        say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": f"I'm sorry you feel that way, but that language isn't appropriate here ☹️. Remember, I'm only trying to help, so please use polite language! <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "let's have a respectful conversation"},
                    "action_id": "respectful_conversation_button",
                    "style": "danger",
                }
            }
        ],
    )

# Your listener will be called every time an interactive component with the action_id "respectful_conversation_button" is triggered
@app.action("respectful_conversation_button")
def button_click(ack, respond):
    ack()
    respond(
        replace_original=True,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn", 
                    "text": "Thank you!😊 Type in `/task-list` for activating my task list menu."
                    },
            }
        ],
	)


# Listens to incoming messages that contain "covid symptoms"
@app.message(re.compile("(nose|throat|headache|fever|Diarrhea|pain|breathing|tiredness|cough|breath)"))
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
				"text": "Unfortunately, I cannot diagnose those symptoms. Please contact your GP if you are concerned or feeling unwell. ☎️ 🤒 \nType in `/task-list` for activating my task list menu."
			},
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
