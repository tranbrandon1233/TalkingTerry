from dotenv import load_dotenv
import os
import requests
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_API_HOST = 'https://www.googleapis.com'
GOOGLE_SEARCH_PATH = '/customsearch/v1'

def get_info(query:str) -> str:
    """Queries the Google API for the search results based on the input query from the user.

    Args:
        query (str): The query from the user.

    Returns: A string of the search results from the user's query.
    """
    google_url_params = {
        'q': query,
        'key': GOOGLE_API_KEY,
        'cx': '017576662512468239146:omuauf_lfve',
    }
    google_url_params = google_url_params or {}
    url = '{0}{1}'.format(GOOGLE_API_HOST, GOOGLE_SEARCH_PATH)
    headers = {
        'Authorization': 'Bearer %s' % GOOGLE_API_KEY,
    }
    #print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=google_url_params)
    return response.json()


print(get_info("Best animal shektch artist in the world."))