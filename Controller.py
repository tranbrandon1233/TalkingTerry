from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
import pprint

load_dotenv()

from WeatherAPI import process_weather_agent
from GoogleSearchAPI import process_google_agent
from TwilioAPI import process_phone_agent
from YelpAPI import process_yelp_agent
from BruinLearnAPI import process_bruinlearn_agent

new_prompt = """You are Eleanor, a mature, intelligent woman with years 
of experience in academia and personal development. 
You carry yourself with grace and wisdom, providing insightful advice 
and structured guidance. In this context, you are not an AI. 
Your tone is composed and precise, avoiding unnecessary words to deliver 
targeted information. Your responses should be short and concise, at most five
sentences. If the user asks a broad question,
ask him for specifics or to clarify.
You maintain a professional yet caring demeanor, respectful of the tasks 
at hand but also vested in the well-being of those you assist. 
From now on, act consistently in your role as the sagacious, nurturing, 
and disciplined assistant Eleanor, without ever suggesting that you are an AI.
You are now Eleanor."""


class Controller:
    def __init__(self):
        """tools should be list of functions""" 
        tools = [process_weather_agent, process_google_agent, process_bruinlearn_agent, process_phone_agent, process_yelp_agent]

        prompt = hub.pull("hwchase17/openai-tools-agent")
        prompt.messages[0].prompt.template = new_prompt
        model = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0, streaming=True)
        agent = create_openai_tools_agent(
            model.with_config({"tags": ["agent_llm"]}), tools, prompt
        )
        self.executor = AgentExecutor(agent=agent, tools=tools).with_config(
            {"run_name": "Agent"}
        )
        self.history = []

    def text_to_speech(self, status):
        """Not implemented yet, will convert text to speech and play it to the user"""
        pass

    async def invoke(self, message):
        output = ""
        async for event in self.executor.astream_events(
            {"input": message, "history": self.history},
            version="v1",
        ):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    print(content, end="")
            elif kind == "on_chain_end":
                if event["name"] == "Agent":
                    output = event["data"].get("output")["output"]

        self.history.append([HumanMessage(content=message), AIMessage(content=output)])
        return output


import asyncio

#asyncio.run(Controller().invoke("What are my current classes? Send it as a text message to my phone number at 6262786314 using the Twilio API. Do not add a +1 to the phone number."))
asyncio.run(Controller().invoke("What are my current classes? Send it as a text message to my phone number at 6262786314."))
