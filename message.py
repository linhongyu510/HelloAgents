"""
消息系统
"""
import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel
from typing_extensions import Literal

# Literal作用是强制变量只能取指定的字面量值，相当于 “枚举限制”
MessageRole = Literal["user", "assistant", "system", "tool"]

class Message(BaseModel):
    """
    消息类
    """

    content: str
    role:MessageRole
    timestamp: datetime = None
    metadata: Optional[Dict[str, Any]] = None

    def __init__(self, content: str, role: MessageRole, **kwargs):
        super().__init__(
            content=content,
            role=role,
            timestamp=kwargs.get("timestamp", datetime.now()),
            metadata=kwargs.get("metadata", {})
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        转换为字典格式（OpenAI API格式）
        :return:
        """
        return {
            "role": self.role,
            "content": self.content
        }

    def __str__(self) -> str:
        return f"[{self.role}] {self.content}"



