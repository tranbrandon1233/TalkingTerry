from __future__ import print_function
import os
import BaseAgent
from dotenv import load_dotenv
import requests
import sys

from urllib.error import HTTPError
from urllib.parse import quote

load_dotenv()

API_KEY= os.getenv('YELP_API_KEY')

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'




def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, lat,long, radius,open_now):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'latitude': lat.replace(' ', '+'),
        'longitude': long.replace(' ', '+'),
        'radius': radius*1600,
        'open_now': open_now,
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def parse(response):
    for b in response['businesses']:
        print(b['name'])

def query_api(lat,long,rad,open_now):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY,lat,long,rad,open_now)

    parse(response)


def main():

    lat = '34.06999972'
    long = '-118.439789907'
    radius=2
    open_now = True


    try:
        query_api(lat,long, radius,open_now)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()