from __future__ import print_function
import os
from dotenv import load_dotenv
import requests
from Agent import Agent

from langchain.tools import tool

from urllib.parse import quote

load_dotenv()

CANVAS_API_TOKEN = os.getenv('CANVAS_API_TOKEN')
API_HOST = 'https://bruinlearn.ucla.edu/api'
SEARCH_PATH = '/v1/courses'

@tool
def get_enrolled_courses() -> str:
    """
    Queries the Canvas API for enrollment of classes for the student based from bruin learn.

    Returns: A list of classes that the user is enrolled in at UCLA
    """
    url_params = {
        'enrollment_state': 'active'
    }
    url_params = url_params or {}
    url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % CANVAS_API_TOKEN,
    }
    #print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    
    listCourses = []
    for course in response.json():
        listCourses.append(course['name'])

    return str(listCourses)[1:-1]

# Define a list of tools
tools = [
    get_enrolled_courses
]

@tool
def process_bruinlearn_agent(input:str) -> str:
    """Asks the BruinLearn agent to find the current classes the user is enrolled in.
    
    Returns: A string of the current current classes the user is enrolled in.
    """
    # Define a list of tools
    tools = [
        get_enrolled_courses
    ]
    agent = Agent(tools)
    output = agent.invoke(input)
    return output

#print(process_bruinlearn_agent('What are my current classes?')) 

