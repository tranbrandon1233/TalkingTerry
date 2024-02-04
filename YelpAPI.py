import os
from dotenv import load_dotenv
import requests

from langchain.tools import tool
from datetime import datetime
from urllib.parse import quote
from Agent import Agent
import time

load_dotenv()

API_KEY = os.getenv('YELP_API_KEY')
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
SEARCH_PATH_EVENTS = '/v3/events'



def get_places(location:str, radius:int, category:str) -> str:
    """Queries the Yelp API for up to five open businesses based the input values from the user, including location, radius from user in miles, and categor(ies) of the location the user wants to go to.

    Args:
        location (str): The location of the user.
        radius(int): The radius from the user in miles.
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
    
    return response.json()



@tool
def find_businesses(location:str, radius:int, category:str) -> str:
    """Queries the Yelp API for up to five open businesses based the input values from the user, including location, radius from user in miles, and categor(ies) of the location the user wants to go to. 
    Args:
        location (str): The location of the user.
        radius(int): The radius from the user in miles.
        category(str): The category of the location the user wants to go to.
        
    Returns: A string of up to five businesses that are open in the location within the specified raidus in miles that the user wants to go to.
    """
    places =get_places(location, radius, category)
    for b in places['businesses']:
        if b['name'] not in results:
            results.append(b['name'])
    return str(results[:5])[1:-1]

@tool
def find_reviews(location:str, radius:int, category:str, name:str) -> str:
    """Queries the Yelp API for up to three reviews based on the past input values from your memory. This includes location, radius, and name of the business from the user of the business they want reviews from.

    Args:
        location (str): The location of the user.
        radius (int): The radius of the business from the user in miles.
        category(str): The category of the location the user wants to go to.
        name(str): The name of the business the user wants reviews from.
    
    Returns: A string of up to three reviews.
    """
    places = get_places(location, radius, category)
    for business in places['businesses']:
        if business['name'] == name:
           business_id= business['id']
           break

    SEARCH_PATH_REVIEWS = '/v3/businesses/{0}/reviews'.format(business_id)
    
    results = {}
    allReviews =[]
    url_params = {
        'sort_by': 'newest',
        'business_id_or_alias': business_id
    }
    url_params = url_params or {}
    url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH_REVIEWS.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }
    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    reviewsDictionary=response.json()
    for review in reviewsDictionary['reviews']:
        allReviews.append(review['text'])

    return str(allReviews)[1:-1]


@tool
def find_events(location:str, radius: int) -> str:
    """Queries the Yelp API for up to five ongoing Events based the input values from the user, including location and radius from user in miles of the location the user wants to go to.

    Args:
        location (str): The location of the user.
        radius (int): The radius of the business from the user in miles.
    
    Returns: A string of up to five events that are open in the location within the raidus in miles that the user wants to go to.
    """
    results = {}
    allEvents =[]
    url_params = {
        'location': location.replace(' ', '+'),
        'radius': int(radius*1600),
        'sort_by': 'desc',
        
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
            results[event['name']] = event['description']

    for key in list(results.keys()):
        allEvents.append([key])
        allEvents[-1].append(results[key])

    return str(allEvents[:4])
    

tools = [
    find_businesses,
    find_events,
    find_reviews
]
@tool
def process_yelp_agent(input:str) -> str:
    """Queries the Yelp API for up to five open businesses based the input values from the user, including location, radius from user in miles, and category of the location the user wants to go to, up to five events
   based the input values from the user, including location, radius from user in miles, or up to three reviews based on the past input values from your memory based in the location, radius, and name of the business from your memory of the business the user wants reviews from.

        Remember the location, radius, and category of the businesses. 
         Args:
            input (str): The user's query.
      
    Returns: A string of up to five businesses that are open in the location within the raidus in miles that the user wants to go to, a string of up to five events near the user, or three reviews from a business requested by the user.
    """
    # Define a list of tools
    tools = [
        find_businesses,
        find_events,
        find_reviews
    ]
    agent = Agent(tools)
    output = agent.invoke(input)
    return output


print(process_yelp_agent('What is an open event within a 5 mile radius of Los Angeles?')) 
