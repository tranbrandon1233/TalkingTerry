from __future__ import print_function
import os
import BaseAgent
from dotenv import load_dotenv
import requests

from langchain.tools import tool

from urllib.parse import quote

load_dotenv()

CANVAS_API_TOKEN = os.getenv('CANVAS_API_TOKEN')
API_HOST = 'https://bruinlearn.ucla.edu/api'
SEARCH_PATH = '/v1/courses'

@tool
def get_enrolled_courses() -> list:
    """
    Queries the Canvas API for enrollment of classes for the student based from bruin learn.

    Returns: A list of classes that the user is enrolled in at UCLA
    """
    results = []
    url_params = {
        'enrollment_state': 'active'
    }
    url_params = url_params or {}
    url = '{0}{1}'.format(API_HOST, quote(SEARCH_PATH.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % CANVAS_API_TOKEN,
    }
    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)
    
    listCourses = []
    for course in response.json():
        listCourses.append(course['name'])

    return listCourses



