前面我们学习了如何直接使用 MCP 客户端。但在实际应用中，我们更希望让智能体自动调用 MCP 工具，而不是手动编写调用代码。HelloAgents 提供了MCPTool包装器，让 MCP 服务器无缝集成到智能体的工具链中。

（1）MCP 工具的自动展开机制

HelloAgents 的MCPTool有一个特性：自动展开。当你添加一个 MCP 工具到 Agent 时，它会自动将 MCP 服务器提供的所有工具展开为独立的工具，让 Agent 可以像调用普通工具一样调用它们。

方式 1：使用内置演示服务器

我们在之前实现过计算器的工具函数，在这里将他转化为 MCP 的服务。这是最简单的使用方式。

from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import MCPTool

agent = SimpleAgent(name="助手", llm=HelloAgentsLLM())

# 无需任何配置，自动使用内置演示服务器
mcp_tool = MCPTool(name="calculator")
agent.add_tool(mcp_tool)
# ✅ MCP工具 'calculator' 已展开为 6 个独立工具

# 智能体可以直接使用展开后的工具
response = agent.run("计算 25 乘以 16")
print(response)  # 输出：25 乘以 16 的结果是 400
Copy to clipboardErrorCopied
自动展开后的工具：

calculator_add - 加法计算器
calculator_subtract - 减法计算器
calculator_multiply - 乘法计算器
calculator_divide - 除法计算器
calculator_greet - 友好问候
calculator_get_system_info - 获取系统信息
Agent 调用时只需提供参数，例如：[TOOL_CALL:calculator_multiply:a=25,b=16]，系统会自动处理类型转换和 MCP 调用。

方式 2：连接外部 MCP 服务器

在实际项目中，你需要连接到功能更强大的 MCP 服务器。这些服务器可以是：

社区提供的官方服务器（如文件系统、GitHub、数据库等）
你自己编写的自定义服务器（封装业务逻辑）
from hello_agents import SimpleAgent, HelloAgentsLLM
from hello_agents.tools import MCPTool

agent = SimpleAgent(name="文件助手", llm=HelloAgentsLLM())

# 示例1：连接到社区提供的文件系统服务器
fs_tool = MCPTool(
    name="filesystem",  # 指定唯一名称
    description="访问本地文件系统",
    server_command=["npx", "-y", "@modelcontextprotocol/server-filesystem", "."]
)
agent.add_tool(fs_tool)

# 示例2：连接到自定义的 Python MCP 服务器
# 关于如何编写自定义MCP服务器，请参考10.5章节
custom_tool = MCPTool(
    name="custom_server",  # 使用不同的名称
    description="自定义业务逻辑服务器",
    server_command=["python", "my_mcp_server.py"]
)
agent.add_tool(custom_tool)

# Agent现在可以自动使用这些工具！
response = agent.run("请读取my_README.md文件，并总结其中的主要内容")
print(response)
Copy to clipboardErrorCopied
当使用多个 MCP 服务器时，务必为每个 MCPTool 指定不同的 name，这个 name 会作为前缀添加到展开的工具名前，避免冲突。例如：name="fs" 会展开为 fs_read_file、fs_write_file 等。如果你需要编写自己的 MCP 服务器来封装特定的业务逻辑，请参考 10.5 节内容。