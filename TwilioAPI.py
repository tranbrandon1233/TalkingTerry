
from twilio.rest import Client
from dotenv import load_dotenv
import os
from langchain.tools import tool
from Agent import Agent
load_dotenv()

@tool
def text_user(message:str,phone_number:str)->str:
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
    return "Operation completed successfully."

@tool
def call_user(message:str,phone_number:str) -> str:
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
    return "Operation completed successfully."


# Define a list of tools
tools = [
    text_user,
    call_user
]

@tool
def process_phone_agent(input:str) -> str:
    """Asks the phone agent to process the input and return the output. The agent is able to a call or a text containing the message parameter and send it to the phone number specified by the phone_number parameter.
    
    Arg:
        message (str): The message to send.
        phone_number (str): The phone number to send the message to.
    
    Returns: A string of the operation completed successfully.
    """
    # Define a list of tools
    tools = [
        text_user,
        call_user
    ]
    agent = Agent(tools)
    output = agent.invoke(input)
    return output

# print(process_weather_agent('What is the humidity in New York?'))     
