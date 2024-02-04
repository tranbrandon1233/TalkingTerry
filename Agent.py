from WeatherAPI import find_weather_condition, find_temp, find_humidity, find_precip, find_wind_speed
from YelpAPI import find_businesses
from BruinLearnAPI import get_enrolled_courses
from langchain.agents import tools
from langchain_openai import ChatOpenAI


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


tools = [find_weather_condition, find_temp, find_humidity, find_precip, find_wind_speed, find_businesses, get_enrolled_courses]

llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are very powerful assistant, but don't know current events",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.with_tools(tools)

from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

list(agent_executor.stream({"input": "What are my current classes?"}))
'''
class Agent:
    def __init__(self, tools):
        """tools should be list of functions"""
        prompt = hub.pull("hwchase17/openai-tools-agent")
        llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
        agent = create_openai_tools_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    def invoke(self, message):
        response =  self.executor.invoke({
            "input": message,
        })
        
        return response['output']
'''