import os

from hello_agents import ToolRegistry


class MyAdvancedSearchTool:
    """
    自定义高级搜索工具类
    展示多源整合和智能选择的设计模式
    """

    def __init__(self):
        self.name = "my_advanced_search"
        self.description = "智能搜索工具，支持多个搜索源，自动选择最佳结果"
        self.search_sources = []
        self._setup_search_resources()

    def _setup_search_resources(self):
        """
        设置可用的搜索源
        :return:
        """
        # 检查Tavily可用性
        if os.getenv("TAVILY_API_KEY"):
            try:
                from tavily import TavilyClient
                self.tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
                self.search_sources.append("tavily")
                print(f"{self.name}：Tavily可用")
            except ImportError:
                print(f"{self.name}：Tavily不可用")

        # 检查SerpApi可用性
        if os.getenv("SERPAPI_API_KEY"):
            try:
                import serpapi
                self.search_sources.append("serpapi")
                print(f"{self.name}：SerpApi可用")
            except ImportError:
                print(f"{self.name}：SerpApi不可用")

        if self.search_sources:
            print(f"可用搜索源：{'.'.join(self.search_sources)}")
        else:
            print(f"{self.name}：无可用搜索源")

    def search(self, query: str) -> str:
        """
        执行智能搜索
        :param query:
        :return:
        """
        if not query.strip():
            return "错误：搜索查询不能为空"

        # 检查是否有可用的搜索源
        if not self.search_sources:
            return """❌ 没有可用的搜索源，请配置以下API密钥之一:

1. Tavily API: 设置环境变量 TAVILY_API_KEY
   获取地址: https://tavily.com/

2. SerpAPI: 设置环境变量 SERPAPI_API_KEY
   获取地址: https://serpapi.com/

配置后重新运行程序。"""

        print(f"开始搜索：{query}")

        # 尝试多个搜索源，返回最佳结果
        for source in self.search_sources:
            try:
                if source == "tavily":
                    result = self._search_with_tavily(query)
                    if result and "未找到" not in result:
                        return f"Tavily AI搜索结果:\n\n{result}"
                elif source == "serpapi":
                    result = self._search_with_serpapi(query)
                    if result and "未找到" not in result:
                        return f"SerpAPI Google搜索结果:\n\n{result}"
            except Exception as e:
                print(f"搜索源{source}发生错误：{e}")
                continue
        return "未找到结果, 请检查网络连接和API密钥设置"




    def _search_with_tavily(self, query: str) -> str:
        """
        使用Tavily搜索
        :param query:
        :return:
        """

        response = self.tavily_client.search(query=query, max_results=3)

        if response.get("answer"):
            result = f"AI直接答案：{response['answer']}\n\n"
        else:
            result = ""

        result += "相关结果"
        for i, item in enumerate(response.get('results', [])[:3], 1):
            result += f"[{i} {item.get('title', '')}]\n"
            result += f"   {item.get('content', '')[:150]}...\n\n"

        return result

    def _search_with_serpapi(self, query: str) -> str:
        """
        使用SerpApi搜索
        :param query:
        :return:
        """
        import serpapi
        search = serpapi.GoogleSearch({
            "q": query,
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "num": 3,
        })

        search_result = search.get_dict()
        if "organic_results" in search_result:
            result = ""
            for i, res in enumerate(search_result["organic_results"][:3], 1):
                result += f"[{i}] {res.get('title', '')}\n"
                result += f"   {res.get('snippet', '')}\n\n"
            return result
        else:
            return "未找到搜索结果"

def create_advanced_search_registry():
    """
    创建高级搜索工具
    :return:
    """
    search_tool = MyAdvancedSearchTool()

    registry = ToolRegistry()

    registry.register_function(
        name="advanced_search",
        description="高级搜索工具，整合Tavily和SerpAPI多个搜索源，提供更全面的搜索结果",
        func=search_tool.search

    )
    return registry
