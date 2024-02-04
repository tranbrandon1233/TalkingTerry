import requests
from langchain.tools import tool
from Agent import Agent
from bs4 import BeautifulSoup
import pandas as pd
import random 
DEI_API_HOST = "https://www.ebsco.com/m/ee/Marketing/titleLists/qth-coverage.htm"

@tool
def get_DEI_info() -> str:
    '''
    Provides large array of books based on the topic of Diversity, Equity, and Inclusion and descriptions about them. Provide recommendations for books to read based on the user's interests.
    Arg:
        input (str): The input from the user.

    Returns: A string of book titles and details about them separated by commas (,)
    '''
    response = requests.request("GET", DEI_API_HOST)
    soup = BeautifulSoup(response.text, 'html.parser')
    longList = str(str(str(soup.prettify().split('<td class="d1">')).split('</td>')).split('<td class="d3">'))
    
    # Assuming your data is stored in a variable called data
    data = pd.Series(longList)

    # Replace the backslashes and single n's with empty strings
    data = data.replace(r'\\n', '', regex=True)
    data = data.replace(r'\\', '', regex=True)
    data = data.replace(r'", "', '', regex=True)
    data = data.replace(r'\',', '', regex=True)
    data = data.replace(r'\'', '', regex=True)
    data = data.replace(r'",', '', regex=True)
    data = data.replace(r'"', '', regex=True)
    data = data.replace(r'</tr>', '', regex=True)
    data = data.replace(r'<tr class="e">', '', regex=True)
    data = data.replace(r'<tr class=e>', '', regex=True)
    data = data.replace(r'<tr class=o>', '', regex=True)
    data = data.replace(r'<tr class="o"> ', '', regex=True)
    data = data.replace(r' Y ', '', regex=True)
    data = data.replace(r'  ', ' ', regex=True)
    final = ""
    realFinal = []
    # Print the cleaned data
    for i in str(str(data.values)).split(' '):
        if len(i) > 2:
            final += i + ' '
    final = final.split('Core')
    for book in final:
        if "Priority" in book:
            for eachBook in book.split('Priority'):
                final.append(eachBook)
    for i,book in enumerate(final):
        if i%3 == 0:
            realFinal.append(book)
    random.shuffle(realFinal)
    return str(realFinal)[1:-1]

tools = [get_DEI_info]
agent = Agent(tools)


@tool
def process_DEI_agent(input: str) -> str:
    """Provides large array of books based on the topic of Diversity, Equity, and Inclusion and descriptions about them. Provide recommendations for books to read based on the user's interests.
    Arg:
        input (str): The input from the user.

    Returns: A string of book titles and details about them separated by commas (,)
    """
    output = agent.invoke(input)
    return output

#print(process_DEI_agent('Can you recommend ten books on Diversity, Equity, and Inclusion involving the LGBTQ community?')) 
