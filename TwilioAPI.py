
from twilio.rest import Client
from dotenv import load_dotenv
import os
from langchain.tools import tool

load_dotenv()

@tool
def text_user(message:str,phone_number:str):
    """Sends a text message provided by the user to a phone number provided by the user.

    Args:
        message (str): The message provided by the user that will be sent to the phone number provided by the user.
        phone_number (str): The phone number provided by the user that the message will be sent to.
    """
    client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

    client.messages.create(
        from_='+18883267630',
        body=message,
        to="+1"+phone_number
    )

@tool
def call_user(message:str,phone_number:str):
    """Makes a phone call to a phone number provided by the user containing a message provided by the user.

    Args:
        phone_number (str): The phone number provided by the user that will be called.
        message (str): The message provided by the user that will be conveyed in the phone call.
    """
    client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
    client.calls.create(
                        twiml='<Response><Say>'+message+'</Say></Response>',
                        to='+1'+phone_number,
                        from_='+18883267630'
    )
          
