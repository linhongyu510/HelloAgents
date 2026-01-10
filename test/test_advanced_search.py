from dotenv import load_dotenv
from tool.my_advanced_search import create_advanced_search_registry, MyAdvancedSearchTool

load_dotenv()

def test_advanced_search():

    registry = create_advanced_search_registry()

    test_queries = [
        "Python编程语言的历史",
        "人工智能的最新发展",
        "2024年科技趋势"
    ]

    for i, query in enumerate(test_queries):
        print( f"测试用例 {i+1}: {query}")
        result = registry.execute_tool("advanced_search", query)
        print(f"结果: {result}\n")
        print(result)

def test_api_configuration():
    search_tool = MyAdvancedSearchTool()
    result = search_tool.search("机器学习算法")
    print(f"搜索结果 ：{result}")

def test_with_agent():
    print( "测试与SimpleAgent的集成")

    registry = create_advanced_search_registry()
    tools_desc = registry.get_tools_description()
    print( tools_desc)

if __name__ ==  "__main__":
    test_advanced_search()
    test_api_configuration()
    test_with_agent()