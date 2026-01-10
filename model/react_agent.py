import re

from dotenv import load_dotenv

from llm.llm_client import HelloAgentsLLM
from tool.tool_executor import ToolExecutor

load_dotenv()

REACT_PROMPT_TEMPLATE = """
请注意，你是一个有能力调用外部工具的智能助手。

可用工具如下：
{tools}

请严格按照以下格式进行回应：
Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
Action: 你决定采取的行动，必须是以下格式之一：
- `{{tool_name}}[{{tool_input}}]`: 调用一个可用工具。
- `Finish[最终答案]`: 当你认为已经获得最终答案时。
- 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action后使用 finish(answer="...")来输出

现在，请开始解决一下问题:
Question: {question}
History: {history}
"""

class ReActAgent:
    def __init__(self, llm_client: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        self.llm_client = llm_client
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def _parse_output(self, text: str):
        """
        解析LLM的输出，提取Thought和Action。
        :param self:
        :param text:
        :return:
        """
        # (.*)捕获组负责提取关键字后的所有非换行内容
        thought_match = re.search(r"Thought: (.*)", text)
        action_match = re.search(r"Action: (.*)", text)
        # # group(1)：获取正则表达式中第一个捕获组 (.*) 匹配到的内容（即 Thought: 后面的原始内容，排除关键字本身）
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        """
        解析Action字符串，提取工具名称和输入。
        :param self:
        :param action_text:
        :return:
        """
        # - \w：正则元字符，匹配字母（大小写）、数字、下划线（等价于[a-zA-Z0-9_]），不匹配空格、特殊符号（如@、#等）；
        # - +：量词，表示匹配前面的\w 1 次或多次（至少 1 个字符，避免匹配空字符串）；
        # - ()：捕获组，将匹配到的关键字保存，后续可通过match.group(1)提取
        match = re.match(r"(\w+)\[(.*)\]", action_text)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def run(self, question: str):
        """
        运行ReAct智能体来回答一个问题
        :return:
        """
        self.history = [] # 每次运行时重置历史记录
        current_step = 0

        # 核心循环的实现
        # ReActAgent 的核心是一个循环，它不断地“格式化提示词 -> 调用LLM -> 执行动作 -> 整合结果”，直到任务完成或达到最大步数限制。
        while current_step < self.max_steps:
            current_step += 1
            print(f"--- 第{current_step}步 ---")

            # 1. 格式化提示词
            tool_desc = self.tool_executor.getAvailableTools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tool_desc,
                question=question,
                history=history_str
            )

            # 2， 调用LLM进行思考
            message = [{"role": "user", "content": prompt}]
            response_text = self.llm_client.think(messages=message)

            if not  message:
                print("错误： LLM未能返回有效响应。")
                break

            # 3. 解析LLM的输出
            thought, action = self._parse_output(response_text)

            if thought:
                print(f"思考: {thought}")

            if not action:
                print("警告：未能解析出有效的Action，流程终止。")
                break

            # 4. 执行Action
            if action.startswith("Finish"):
                # 如果是Finish指令，提取最终答案并结束
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1)
                print(f"最终答案：{final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                # ...处理无效Action格式...
                continue

            print(f"行动：{tool_name}[{tool_input}]")

            tool_function = self.tool_executor.getTool(tool_name)
            if not tool_function:
                observation = f"错误：未找到工具{tool_name}。"
            else:
                observation = tool_function(tool_input) # 调用真实工具


            print(f"观察：{observation}")

            # 将本轮的Action和Observation添加到历史记录中
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")

        # 循环结束
        print("已达到最大步数，流程终止。")
        return None

if __name__ == "__main__":
    llm_client = HelloAgentsLLM()
    tool_executor = ToolExecutor()
    agent = ReActAgent(llm_client, tool_executor)
    agent.run("请用中文回答：华为最新手机型号及主要卖点?")




