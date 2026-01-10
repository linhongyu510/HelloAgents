import os

from dotenv import  load_dotenv
from hello_agents import HelloAgentsLLM, SimpleAgent

load_dotenv()

llm = HelloAgentsLLM(
    model=os.getenv("LLM_MODEL_ID"),
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
    temperature=0.5
)

agent = SimpleAgent(
    name="AI助手",
    llm=llm,
    system_prompt="你是一个有用的AI助手"
)

response = agent.run("你好，请介绍一下自己")
print(response)

from hello_agents.tools import CalculatorTool
calculator = CalculatorTool()

response = agent.run("请帮我计算 2 + 3 * 4")
print(response)

print(f"历史消息数：{len(agent.get_history())}")