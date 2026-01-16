import os 
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
import google.genai as genai
import time 
from IPython.display import Image
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
time.sleep(20)


api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

#Defining an agent 
class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
        # 1️⃣ Build conversation text for Gemini
    history_text = "\n".join(
        f"User: {m.content}" if isinstance(m, HumanMessage) else f"AI: {m.content}"
        for m in state["messages"]
    )
    
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=history_text)
    state["messages"].append(AIMessage(content=response.text))
    print(f"\nAI: {response.text}")
    return state 
graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent_2 = graph.compile()
agent_image = agent_2.get_graph().draw_mermaid_png()
Path("agent_2_image.png").write_bytes(agent_image)
print("Agent saved...")

conversation_history = []
user_input = input("Enter: ")
while user_input.strip().lower() != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent_2.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter: ")
with open("logging.txt", "w") as file:
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"User: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n")
    file.write("End of Conversation")
print("Conversation save to logging.txt")
    