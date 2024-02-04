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
@tool
def find_businesses(location:str, radius:int, category:str) -> str:
        """Queries the Yelp API for up to five open businesses based the input values from the user, including location, radius from user in miles, and categor(ies) of the location the user wants to go to.

        Args:
            location (str): The location of the user.
            radius(float): The radius from the user in miles.
            category(str): The category of the location the user wants to go to.
            
        Returns: A string of up to five businesses that are open in the location within the specified raidus in miles that the user wants to go to.
        """
        results = []
        url_params = {
            'location': location.replace(' ', '+'),
            'radius': radius*1600,
            'open_now': True,
            'categories': category,
        }
        url_params = url_params or {}
        url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % API_KEY,
        }
        #print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers, params=url_params)
        for b in response.json()['businesses']:
            if b['name'] not in results:
                results.append(b['name'])
        return str(results[:5])[1:-1]

tools = [
    find_businesses,
]
@tool
def process_yelp_agent(input:str) -> str:
    """Queries the Yelp API for up to five open businesses based the input values from the user, including location, radius from user in miles, and categor(ies) of the location the user wants to go to.
         Args:
            input (str): The user's query.
      
    Returns: A string of up to five businesses that are open in the location within the raidus in miles that the user wants to go to.
    """
    # Define a list of tools
    tools = [
        find_businesses,
    ]
    agent = Agent(tools)
    output = agent.invoke(input)
    return output

print(process_yelp_agent('What is an open business within a 15 mile radius of Los Angeles?')) 
