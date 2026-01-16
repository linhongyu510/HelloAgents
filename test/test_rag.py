# import os
#
# from hello_agents import HelloAgentsLLM, SimpleAgent, ToolRegistry
# from dotenv import load_dotenv
# from hello_agents.tools import MemoryTool, RAGTool
#
# load_dotenv()
#
# # 创建LLM示例
# llm = HelloAgentsLLM(
#     model=os.getenv("LLM_MODEL_ID"),
#     api_key=os.getenv("LLM_API_KEY"),
#     base_url=os.getenv("LLM_BASE_URL")
# )
#
# # 创建Agent
# agent = SimpleAgent(
#     name="智能助手",
#     llm=llm,
#     system_prompt="你是一个有记忆和检索能力的AI助手"
# )
#
# # 创建工具注册表
# tool_registry = ToolRegistry()
#
# # 添加记忆工具
# memory_tool = MemoryTool(user_id="user123")
# tool_registry.register_tool(memory_tool)
#
# # 添加RAG工具
# rag_tool = RAGTool(knowledge_base_path="./knowledge_base")
# tool_registry.register_tool(rag_tool)
#
# # 为Agent配置工具
# agent.tool_registry = tool_registry
#
# # 开始对话
# response = agent.run("你好！请记住我叫林宏宇，我是一名Python开发者")
# print(response)
import os

from hello_agents import HelloAgentsLLM, SimpleAgent, ToolRegistry
from dotenv import load_dotenv

load_dotenv()

# 创建LLM示例
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)

# 创建Agent
agent = SimpleAgent(
    name="智能助手",
    llm=llm,
    system_prompt="你是一个有记忆和检索能力的AI助手"
)

# 创建工具注册表
tool_registry = ToolRegistry()

# 尝试添加记忆工具，如果失败则跳过
try:
    from hello_agents.tools import MemoryTool
    memory_tool = MemoryTool(user_id="user123")
    tool_registry.register_tool(memory_tool)
    print("MemoryTool 已成功初始化")
except Exception as e:
    print(f"警告：无法初始化MemoryTool，可能是Qdrant服务问题: {e}")

# 添加RAG工具
try:
    from hello_agents.tools import RAGTool
    rag_tool = RAGTool(knowledge_base_path="./knowledge_base")
    tool_registry.register_tool(rag_tool)
    print("RAGTool 已成功初始化")
except Exception as e:
    print(f"警告：无法初始化RAGTool: {e}")

# 为Agent配置工具
agent.tool_registry = tool_registry

# 开始对话
response = agent.run("你好！请记住我叫林宏宇，我是一名Python开发者")
print(response)

response = agent.run("你好！我是谁")
print(response)