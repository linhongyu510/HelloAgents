from typing import List, Dict, Any

from hello_agents import ToolRegistry
from tiktoken.load import check_hash


class ToolChain:
    """
    工具链，支持多个工具的顺序执行
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.steps: List[Dict[str, Any]] = []

    def add_step(self, tool_name: str, input_template: str, output_key: str = None):
        """
        添加工具执行步骤
        :param tool_name: 工具名称
        :param input_template:  输入模板，支持变量替换
        :param output_key: 输出结果的键名，用于后续步骤引用
        :return:
        """

        self.steps.append({
            "tool_name": tool_name,
            "input_template": input_template,
            "output_key": output_key or f"step_{len(self.steps)}_result"
        })

    def execute(self, registry: ToolRegistry, initial_input: str, context: Dict[str, Any] = None) -> str:
        """
        执行工具链
        :param registry:
        :param initial_input:
        :param context:
        :return:
        """
        context = context or {}
        context["input"] = initial_input

        for i, step in enumerate(self.steps, 1):
            tool_name = step["tool_name"]
            input_template = step["input_template"]
            output_key = step["output_key"]

            # 替换模板中的变量
            try:
                tool_input = input_template.format(**context)
            except KeyError as e:
                return f"工具链执行失败：模板变量{e}未找到"

            print(f"  步骤{i}: 使用{tool_name} 处理'{tool_input[:50]}...")

            # 执行工具
            result = registry.execute_tool(tool_name, tool_input)
            context[output_key] = result

            print(f"    步骤{i} 结果：{result[:50]}...")

        # 返回最后一步的结果
        final_result = context[self.steps[-1]["output_key"]]
        print(f"工具链'{self.name}'执行完成")
        return final_result

class ToolChainManager:
    """
    工具链管理器
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.chains: Dict[str, ToolChain] = {}

    def register_chain(self, chain:ToolChain):
        """
        注册工具链
        :param chain:
        :return:
        """
        self.chains[chain.name] = chain
        print(f"已注册工具链：{chain.name}")

    def execute_chain(self, chain_name: str, input_data: str, context: Dict[str, Any] = None) -> str:
        """
        执行指定的工具链
        :param chain_name:
        :param input_data:
        :param context:
        :return:
        """
        if chain_name not in self.chains:
            return f"工具链{chain_name}未注册"

        chain = self.chains[chain_name]
        return chain.execute(self.registry, input_data, context)

    def list_chains(self) -> List[str]:
        """
        列出所有工具链
        :return:
        """
        return list(self.chains.keys())


def create_research_chain() -> ToolChain:
    """
    创建一个研究工具链： 搜索 -> 计算 -> 总结
    :return:
    """

    chain = ToolChain(
        name="research_and_calculate",
        description="搜索信息并进行相关计算"
    )

    # 步骤1：搜索信息
    chain.add_step(
        tool_name="search",
        input_template="{input}",
        output_key="search_result"
    )

    # 步骤2：基于搜索结果进行计算（如果需要）
    chain.add_step(
        tool_name="my_calculator",
        input_template="根据以下信息计算相关数值:{search_result}",
        output_key="calculation_result"
    )
    return chain

if __name__ == "__main__":
    # 测试工具链创建
    chain = create_research_chain()
    print(f"工具链 '{chain.name}' 创建成功")
    print(f"描述: {chain.description}")
    print(f"步骤数: {len(chain.steps)}")




