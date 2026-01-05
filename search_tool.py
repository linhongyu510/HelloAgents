import os

from serpapi import  SerpApiClient

from dotenv import load_dotenv
load_dotenv()

def search(query: str) -> str:
    """
    一个基于SerpAPi的实战网页搜索引擎工具
    它会智能地解析搜索结果，优先返回直接答案或知识图谱信息。
    :param query:
    :return:
    """
    print(f"正在执行[SerpAPi]网页搜索{query}")

    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "错误：SERPAPI_API_KEY未在.env文件中配置。"

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "cn",
            "hl": "zh-cn"
        }

        client = SerpApiClient(params)
        results = client.get_dict()


        # 智能解析：优先寻找最直接的答案
        if "answer_box_list" in results: # answer_box（Google的答案摘要框）
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results: # answer_box（Google的答案摘要框）
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]: # knowledge_graph（知识图谱）
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i + 1} {res.get('title', '')}\n{res.get('snippet', '')}]"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)

        return f"对不起，没有找到关于{query}的信息"
    except Exception as e:
        return f"搜索时发生错误：{e}"

from tool_executor import ToolExecutor

if __name__ == "__main__":
    # 1. 初始化工具执行器
    toolExecutor = ToolExecutor()

    # 2. 注册实战搜索工具
    search_description = "一个网页搜索引擎。"
    toolExecutor.registerTool("Search", search_description, search)

    # 3. 打印可用的工具
    print("\n --- 可用的工具 ---")
    print(toolExecutor.getAvailableTools())

    # 4. 智能体的Action调用，输入一个实时性的问题
    print("\n--- 执行 Action: Search['英伟达最新的GPU型号是什么'] ---")
    tool_name = "Search"
    tool_input = "英伟达最新的GPU型号是什么"

    tool_function =  toolExecutor.getTool(tool_name)
    if tool_function:
        observation = tool_function(tool_input)
        print("--- 观察（Observation）---")
        print(observation)
    else:
        print(f"错误：工具{tool_name}不存在。")

