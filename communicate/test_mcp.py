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

# 连接到社区提供的文件系统服务器
fs_tool = MCPTool(
    name="filesystem",
    description="访问本地文件系统",
    server_command=["npx","-y","@modelcontextprotocol/server-filesystem","."]
)

agent.add_tool(fs_tool)

custom_tool = MCPTool(
    name="custom_server",
    description="自定义业务逻辑服务器",
    server_command=["python", "my_mcp_server.py"]
)
agent.add_tool(custom_tool)

response = agent.run("请读取my_README.md文件，并总结其中的主要内容")
print(response)

