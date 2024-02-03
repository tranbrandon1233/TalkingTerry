from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
    
class Controller:
    def __init__(self, tools):
        """tools should be list of functions"""
        prompt = hub.pull("hwchase17/openai-tools-agent")
        llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
        agent = create_openai_tools_agent(llm, tools, prompt)
        self.executor = AgentExecutor(agent, tools)
        self.history = []
        
    def update_status(self, status):
        """Not implemented yet, should do a quick status update to the user"""
        pass
    
    def invoke(self, message):
        output =  self.executor.invoke({
            "input": message,
            "history": self.history 
        })
        
        self.history.append([
            HumanMessage(message),
            AIMessage(output)
        ])
        
        return output