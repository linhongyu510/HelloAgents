import os

from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import MCPTool

from dotenv import load_dotenv
load_dotenv("../.env")

llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)
agent = SimpleAgent(
    name="助手",
    llm=llm
)

mcp_tool = MCPTool(name="calculator")
agent.add_tool(mcp_tool)

response = agent.run("计算25 乘以 16")
print(response)