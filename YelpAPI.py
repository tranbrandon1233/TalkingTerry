import os
from dotenv import load_dotenv
import requests

from langchain.tools import tool

from urllib.parse import quote
from Agent import Agent

load_dotenv()

API_KEY = os.getenv('YELP_API_KEY')
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
SEARCH_PATH_EVENTS ='/v3/events'
#@tool
def find_businesses(location:str, radius: float, categories:list) -> str:
        """Queries the Yelp API for up to five open businesses based the input values from the user, including location, radius from user in miles, and categor(ies) of the location the user wants to go to.

        Args:
            location (str): The location of the user.
            radius (float): The radius of the business from the user in miles. The maximum is 25 miles.
            categories (list): The type of business the user wants to go to. The first letter of each word MUST be capitalized.
        
        Returns: A string of up to five businesses that are open in the location within the raidus in miles that the user wants to go to.
        """
        results = []
        url_params = {
            'location': location.replace(' ', '+'),
            'radius': radius*1600,
            'open_now': True,
            'categories': categories,
        }
        url_params = url_params or {}
        url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % API_KEY,
        }
        print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers, params=url_params)

        for b in response.json()['businesses']:
            results.append(b['name'])
        return str(results[:5])[1:-1]


@tool
def process_weather_agent(input: str) -> str:
    """Asks the weather agent to process the input and return the output. The agent is able to find the current weather condition, temperature, humidity, precipitation, and wind speed of the city the user is in.
    
    Arg:
        input (str): The city of the user.
    
    Returns: A string of the current weather condition, temperature, humidity, precipitation, and wind speed of the city the user is in.
    """
    # Define a list of tools
    tools = [
        find_businesses,
        find_events
    ]
    agent = Agent(tools)
    output = agent.invoke(input)
    return output

# print(process_weather_agent('What is the humidity in New York?')) 
