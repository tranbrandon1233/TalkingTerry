import os
from dotenv import load_dotenv
import requests

# from langchain.tools import tool

from urllib.parse import quote
# from Agent import Agent

load_dotenv()

API_KEY = os.getenv('YELP_API_KEY')
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
SEARCH_PATH_EVENTS = '/v3/events'
    
# @tool
def find_businesses(location:str, radius: float, categories:list) -> list:
        """Queries the Yelp API for up to five open businesses based the input values from the user, including location, radius from user in miles, and categor(ies) of the location the user wants to go to.

        Args:
            location (str): The location of the user.
            radius (float): The radius of the business from the user in miles.
            categories (list): The type of business the user wants to go to.
        
        Returns: A list of up to five businesses that are open in the location within the raidus in miles that the user wants to go to.
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
        return results[:4]

def find_events(location:str, radius: float) -> list:
    """Queries the Yelp API for up to five ongoing Events based the input values from the user, including location and radius from user in miles of the location the user wants to go to.

    Args:
        location (str): The location of the user.
        radius (float): The radius of the business from the user in miles.
    
    Returns: A list of up to five events that are open in the location within the raidus in miles that the user wants to go to.
    """
    results = {}
    allEvents =[]
    url_params = {
        'location': location.replace(' ', '+'),
        'radius': radius*1600,
        
    }
    url_params = url_params or {}
    url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH_EVENTS.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }
    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    
    
    for event in response.json()['events']:
        if event['name'] not in results:
            results[event['name']] = [event['description']]
            for timeDate in event['time_start'].split('T'):
                results[event['name']].append(timeDate)

    for key in list(results.keys()):
        allEvents.append([key])
        for descriptionTime in results[key]: 
            allEvents[-1].append(descriptionTime)

    return str(allEvents[:4])