import ast
import math
import operator
import os

# from tool import ToolRegistry

from hello_agents import ToolRegistry

def my_calculate(expression: str) -> str:
    """
    简单的数学计算函数
    :return:
    """

    def _eval_node(node, operators, funcitons):
        """
        简单的表达式求值
        :param node:
        :param operators:
        :param funcitons:
        :return:
        """
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = _eval_node(node.left, operators, funcitons)
            right = _eval_node(node.right, operators, funcitons)
            op = operators.get(type(node.op))
            return op(left, right)
        elif isinstance(node, ast.Call):
            func_name = node.func.id
            if func_name in functions:
                args = [_eval_node(arg, operators, funcitons) for arg in node.args]
                return functions[func_name](*args)
        elif isinstance(node, ast.Name):
            if node.id in functions:
                return functions[node.id]
    if not expression.strip():
        return "无效的表达式"

    # 支持的基本计算
    operators = {
        ast.Add : operator.add,
        ast.Sub : operator.sub,
        ast.Mult : operator.mul,
        ast.Div : operator.truediv,
    }

    # 支持的基本函数
    functions = {
        'sqrt': math.sqrt,
        'pi': math.pi
    }


    try:
        node = ast.parse(expression, mode='eval')
        result = _eval_node(node.body, operators, functions)
        return str(result)
    except:
        return "计算失败"


def create_calculator_registry():
    """
    创建包含计算器的工具注册表
    :return:
    """
    # 注册计算器函数
    registry = ToolRegistry()
    registry.register_function(
        name="my_calculator",
        description="简单的数学计算工具，支持基本运算和sqrt函数",
        func=my_calculate
    )

    return registry
from dotenv import load_dotenv

load_dotenv()


def test_calculator_tool():
    """
    测试自定义计算器工具
    :return:
    """

    # 创建包含计算器的注册表
    registry = create_calculator_registry()
    print("测试自定义计算器工具\n")

    test_cases = [
        "2 + 3",
        "10 - 4",
        "5 * 6",
        "8 / 2",
        "sqrt(16)",
    ]

    for i, expression in enumerate(test_cases):
        print(f"测试用例 {i+1}: {expression}")
        result = registry.execute_tool("my_calculator", expression)
        print(f"结果: {result}\n")

def test_with_simple_agent():
    """
    测试与SimpleAgent的集成
    :return:
    """

    from hello_agents import HelloAgentsLLM

    llm = HelloAgentsLLM(
        model=os.getenv("LLM_MODEL_ID"),
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL")
    )

    registry = create_calculator_registry()

    print("测试与SimpleAgent的集成\n")

    user_question = "请帮我计算 sqrt(16) + 2 * 3"

    print(f"用户问题: {user_question}")

    calc_result = registry.execute_tool("my_calculator", "sqrt(16) + 2 * 3")
    print(f"计算结果: {calc_result}")

    final_messages = [
        {"role": "user",
         "content": f"计算结果是{calc_result}. 请用自然语言回答用户的问题：{user_question}"
         }
    ]

    print(f"正在使用LLM进行回答...")
    response = llm.think(final_messages)
    for chunk in response:
        print(chunk, end="", flush=True)

    print()

if __name__ == "__main__":
    # 测试自定义计算器工具
    test_calculator_tool()
    # 测试与SimpleAgent的集成
    test_with_simple_agent()
