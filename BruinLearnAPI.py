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
SEARCH_PATH_ANOUNCEMENTS = '/v1/announcements'

def get_course_info() -> str:
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

    return requests.request('GET', url, headers=headers, params=url_params).json()

@tool
def get_enrolled_courses() -> str:
    """
    Queries the Canvas API for enrollment of classes for the student based from bruin learn.

    Returns: A list of classes that the user is enrolled in at UCLA
    """
    resp = get_course_info()
    listCourses = []
    for course in resp:
        
        listCourses.append(course['name'])

    return str(listCourses)[1:-1]

@tool
def get_announcements() -> str:
    """
    Queries the Canvas API for the latest announcement for each course for the student based from BruinLearn.


    Returns: A string of the latest announcements of each course
    """
    course_info = get_course_info()
    ids=[]
    listAnnouncements = []
    for dictionary in course_info:
        ids.append(dictionary['id'])
    
    for course_id in ids:
        url_params = {
            'context_codes': 'course_'+str(course_id),
            'latest_only': True
        }
        url_params = url_params or {}
        url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH_ANOUNCEMENTS.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % CANVAS_API_TOKEN,
        }
        #print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers, params=url_params)
        
        
        for announcement in response.json():
            listAnnouncements.append(announcement['title'])

    return str(listAnnouncements)[1:-1]

# Define a list of tools
tools = [
    get_enrolled_courses,
    get_announcements
]

@tool
def process_bruinlearn_agent(input:str) -> str:
    """Asks the BruinLearn agent to find the current classes the user is enrolled in or the latest announcements for each course.
    
    Returns: A string of the current classes the user is enrolled in or a string of the latest announcements for each course.
    """
    # Define a list of tools
    tools = [
        get_enrolled_courses,
        get_announcements
    ]
    agent = Agent(tools)
    output = agent.invoke(input)
    return output

#print(process_bruinlearn_agent('What are my current classes, and what are their latest announcements?')) 

