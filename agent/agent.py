from abc import ABC, abstractmethod
from typing import Optional, List

from hello_agents import HelloAgentsLLM

from config.config import Config
from message.message import Message


class Agent(ABC):
    """
    Agent基类
    """

    def __init__(
            self,
            name: str,
            llm: HelloAgentsLLM,
            system_prompt: Optional[str] = None,
            config: Optional[Config] = None
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.config = config
        self._history = List[Message] = []

    @abstractmethod
    def run(self, input_text: str, **kwargs) -> str:
        """
        运行Agent
        :param input_text:
        :param kwargs:
        :return:
        """
        pass

    def add_message(self, message: Message):
        """
        添加消息到历史记录
        :param message:
        :return:
        """
        self._history.append(message)

    def clear_history(self):
        """
        清空历史记录
        :return:
        """
        self._history.clear()

    def get_history(self):
        """
        获取历史记录
        :return:
        """
        return self._history

    def __str__(self) -> str:
        return f"Agent(name={self.name}, provide={self.llm.provider})"