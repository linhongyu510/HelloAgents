from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable

from pydantic import BaseModel
from scripts.regsetup import description


class ToolParameter(BaseModel):
    """
    工具参数定义
    """
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

class Tool(ABC):
    """
    工具基类
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, parameters: Dict[str, Any]):
        """
        执行工具
        :param parameters:
        :return:
        """

    @abstractmethod
    def get_parameters(self) -> List[ToolParameter]:
        """
        获取工具参数定义
        :return:
        """
        pass

    def to_openai_schema(self) -> Dict[str, Any]:
        """
        转换为OpenAI function calling schema 格式
        用于FunctionCallAgent，使工具能够被OpenAI原生function calling使用
        Returns：符合OpenAI function calling标准的schema
        :return:
        """
        parameters = self.get_parameters()

        # 构建properties
        properties = {}
        required = []

        for param in parameters:
            # 基础属性定义
            prop = {
                "type": param.type,
                "description": param.description
            }

            # 如果有默认值，添加到描述中（OpenAI schema不支持default字段）
            if param.default is not None:
                prop["description"] = f"{param.description}(默认：{param.default})"

            # 如果是数组类型，添加items定义
            if param.type == "array":
                prop["items"] = {"type":"string"} # M默认字符串数组

            properties[param.name] = prop

            # 收集必须参数
            if param.required:
                required.append(param.name)

        return {
            "type": "function",
            "function" :{
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

class ToolRegistry:
    """
    HelloAgent工具注册表
    """

    def __init__(self):
        self._tools: dict[str, Tool] = {}
        self._functions: dict[str, dict[str, Any]] = {}

    def register_tool(self, tool: Tool):
        """
        注册Tool对象
        :param tool:
        :return:
        """
        if tool.name in self._tools:
            print(f"工具{tool.name} 已存在，将被覆盖。")
        self._tools[tool.name] = tool
        print(f"工具{tool.name} 注册成功。")

    def register_function(self, name: str, description: str, func: Callable[[str], str]):
        """
        直接注册函数作为工具
        :param name:
        :param description:
        :param func:
        :return:
        """

        if name in self._functions:
            print(f"函数{name} 已存在，将被覆盖。")

        self._functions[name] = {
            "description": description,
            "func": func
        }

        print(f"函数{name} 注册成功。")

    def get_tools_description(self) -> str:
        """
        获取所有的可用工具的格式化描述字符串
        :return:
        """
        descriptions = []

        # Tool对象描述
        for tool in self._tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")

        # 函数工具描述
        for name, info in self._functions.items():
            descriptions.append(f"- {name}: {info['description']}")

        return "\n".join(descriptions) if descriptions else "暂无可用工具"


