from agentscope.message import Msg

# 消息的标准结构
message = Msg(
    name = "Alice",
    content="Hello, Bob!",
    role="user",
    metadata={
        "timestamp": "2024-01-15T10:30:00Z",
        "message_type": "text",
        "priority": "normal"
    }
)

from agentscope.agent import AgentBase

class CustomAgent(AgentBase):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        # 智能体初始化逻辑

    def reply(self, x: Msg) -> Msg:
        # 智能体的核心响应逻辑
        response = self.model(x.content)
        return Msg(
            name=self.name,
            content=response,
            role="assistant"
        )

    def observe(self, x: Msg) -> None:
        # 智能体的观察逻辑（可选）
        self.memory.add(x)

