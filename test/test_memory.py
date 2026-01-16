# import os
#
# from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry
# from hello_agents.tools import MemoryTool
#
# from dotenv import load_dotenv
# load_dotenv()
# # 创建具有记忆能力的Agent
# llm = HelloAgentsLLM(
#     model=os.getenv("LLM_MODEL_ID"),
#     api_key=os.getenv("LLM_API_KEY"),
#     base_url=os.getenv("LLM_BASE_URL")
# )
#
# agent = SimpleAgent(name="记忆助手", llm=llm)
#
# # 创建记忆工具
# try:
#     from hello_agents.tools import MemoryTool
#     memory_tool = MemoryTool(user_id="user123")
# except Exception as e:
#     print(f"创建记忆工具失败: {e}")
#
# tool_registry = ToolRegistry()
# tool_registry.register_tool(memory_tool)
# agent.tool_registry = tool_registry
# # 体验记忆功能
# print("=== 添加多个记忆 ===")
#
# # 添加第一个记忆
# try:
#     result1 = memory_tool.execute("add", content="用户张三是一名Python开发者，专注于机器学习和数据分析",
#                               memory_type="semantic", importance=0.8)
# except Exception as e:
#     print(f"添加记忆失败: {e}")
# print(f"记忆1: {result1}")
#
# # 添加第二个记忆
# try:
#     result2 = memory_tool.execute("add", content="李四是前端工程师，擅长React和Vue.js开发", memory_type="semantic",
#                               importance=0.7)
# except Exception as e:
#     print(f"添加记忆失败: {e}")
# print(f"记忆2: {result2}")
#
# # 添加第三个记忆
# try:
#     result3 = memory_tool.execute("add", content="王五是产品经理，负责用户体验设计和需求分析", memory_type="semantic",
#                               importance=0.6)
# except Exception as e:
#     print(f"添加记忆失败: {e}")
# print(f"记忆3: {result3}")
#
# print("\n=== 搜索特定记忆 ===")
# # 搜索前端相关的记忆
# print("🔍 搜索 '前端工程师':")
# try:
#     result = memory_tool.execute("search", query="前端工程师", limit=3)
# except Exception as e:
#     print(f"搜索失败: {e}")
# # result = memory_tool.execute("search", query="前端工程师", limit=3)
# # print(result)
#
# print("\n=== 记忆摘要 ===")
# try:
#     result = memory_tool.execute("summary")
#     print(result)
# except Exception as e:
#     print(f"获取摘要失败: {e}")

import os
from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry
from dotenv import load_dotenv

# 加载.env配置
load_dotenv()

# 创建LLM（这部分不受Qdrant影响，可正常执行）
llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)

agent = SimpleAgent(name="记忆助手", llm=llm)

# 创建记忆工具（完善异常处理，避免变量未定义）
memory_tool = None  # 先初始化变量，避免NameError
try:
    from hello_agents.tools import MemoryTool
    memory_tool = MemoryTool(user_id="user123")
    print("✅ MemoryTool 初始化成功")
except Exception as e:
    print(f"❌ 创建记忆工具失败: {e}")
    print("💡 提示：请先修改底层Qdrant连接代码，跳过本地连接尝试")

# 创建工具注册表并注册工具（增加变量检查）
tool_registry = ToolRegistry()
if memory_tool is not None:  # 只有初始化成功才注册
    tool_registry.register_tool(memory_tool)
    agent.tool_registry = tool_registry
else:
    print("⚠️ 记忆工具未初始化，跳过工具注册，Agent将无记忆功能")

# 体验记忆功能（所有操作前都检查memory_tool是否可用）
print("\n=== 添加多个记忆 ===")
if memory_tool is not None:
    # 添加第一个记忆
    try:
        result1 = memory_tool.execute(
            "add",
            content="用户张三是一名Python开发者，专注于机器学习和数据分析",
            memory_type="semantic",
            importance=0.8
        )
        print(f"记忆1: {result1}")
    except Exception as e:
        print(f"添加记忆1失败: {e}")

    # 添加第二个记忆
    try:
        result2 = memory_tool.execute(
            "add",
            content="李四是前端工程师，擅长React和Vue.js开发",
            memory_type="semantic",
            importance=0.7
        )
        print(f"记忆2: {result2}")
    except Exception as e:
        print(f"添加记忆2失败: {e}")

    # 添加第三个记忆
    try:
        result3 = memory_tool.execute(
            "add",
            content="王五是产品经理，负责用户体验设计和需求分析",
            memory_type="semantic",
            importance=0.6
        )
        print(f"记忆3: {result3}")
    except Exception as e:
        print(f"添加记忆3失败: {e}")

    print("\n=== 搜索特定记忆 ===")
    # 搜索前端相关的记忆
    print("🔍 搜索 '前端工程师':")
    try:
        result = memory_tool.execute("search", query="前端工程师", limit=3)
        print(result)
    except Exception as e:
        print(f"搜索失败: {e}")

    print("\n=== 记忆摘要 ===")
    try:
        result = memory_tool.execute("summary")
        print(result)
    except Exception as e:
        print(f"获取摘要失败: {e}")
else:
    print("❌ 无可用的记忆工具，跳过所有记忆操作")