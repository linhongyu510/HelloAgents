import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

# 初始化Tavily客户端
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def test_tavily():
    try:
        print("开始测试Tavily API...")
        response = tavily_client.search(
            query="明天北京天气和景点",
            search_depth="basic",
            max_results=5,
            include_answer=True
        )
        print("API调用成功！")
        print("搜索结果:", response)
        print("答案:", response["answer"])
    except Exception as e:
        print(f"API调用失败: {e}")

if __name__ == "__main__":
    test_tavily()