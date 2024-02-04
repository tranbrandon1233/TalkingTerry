import requests
from langchain.tools import tool
from Agent import Agent

GW_API_HOST = "https://global-warming.org/api/temperature-api"

@tool
def get_info() -> str:
    """Queries the Global Warming API for the global temperature anomaly in Celsius for a station in the ocean and on land. 


    Returns: A string of the trend the global temperature anomaly in Celsius from 1965 to 2023 for a station in the ocean and on land.
    """

    results = []

    response = requests.request("GET", GW_API_HOST)
    
    for  i,data in enumerate(response.json()['result'][-700:]):
        if i%12==0:
            results.append(data)
    return str(results)[1:-1]
    

tools = [get_info]
agent = Agent(tools)


@tool
def process_GW_agent(input: str) -> str:
    """Provides data from 1965 to 2023 of the global temperature anomaly in Celsius for a station in the ocean and on land. Analyze this trend and explain what it means for the future of the planet.
    Arg:
        input (str): The input from the user.

    Returns: A string of the trend the global temperature anomaly in Celsius from 1965 to 2023 for a station in the ocean and on land.
    """
    output = agent.invoke(input)
    return output

#print(process_GW_agent('What is the current trend of global warming on the planet?')) 
