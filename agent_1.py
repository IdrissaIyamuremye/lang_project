
from langchain.chat_models.base import BaseChatModel
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import google.genai as genai
from openai import OpenAI
import os 
from IPython.display import display, Image
from pathlib import Path
import time
time.sleep(20)

load_dotenv()  
api_key=os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

load_dotenv()
class AgentState(TypedDict):
    messages: List[HumanMessage]
    response: str

def process(state: AgentState) ->AgentState:
    response  = client.models.generate_content(model="gemini-3-flash-preview",contents=f"{state['messages']}")
    state["response"] = response.text
    print(response.text)
    return state

graph = StateGraph(AgentState)
graph.add_node("processor", process)
graph.add_edge(START, "processor")
graph.add_edge("processor", END)
agent = graph.compile()


graph_png = agent.get_graph().draw_mermaid_png()
agent_graph = Path("agent_png.png").write_bytes(graph_png)
print("Agent graph saved...")

user_input = input("Enter: ")

while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    