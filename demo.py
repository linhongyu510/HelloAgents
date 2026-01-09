"""
比特币价格显示应用
功能：实时显示比特币价格、24小时变化趋势，支持手动刷新
技术栈：Streamlit + CoinGecko API + requests
"""

import streamlit as st
import requests
import time
from datetime import datetime
import pytz

# 页面配置
st.set_page_config(
    page_title="比特币价格追踪器",
    page_icon="₿",
    layout="centered"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #F7931A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .price-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .current-price {
        font-size: 3.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .change-positive {
        color: #00FF00;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .change-negative {
        color: #FF4444;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .refresh-btn {
        background-color: #F7931A;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    .refresh-btn:hover {
        background-color: #e08217;
        transform: translateY(-2px);
    }
    .last-updated {
        color: #666;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False


class BitcoinPriceTracker:
    """比特币价格追踪器类"""

    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"
        self.params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd',
            'include_24hr_change': 'true',
            'include_24hr_vol': 'true',
            'include_last_updated_at': 'true'
        }
        self.timeout = 10  # 请求超时时间（秒）

    def get_bitcoin_data(self):
        """
        从CoinGecko API获取比特币数据

        Returns:
            dict: 包含价格和变化数据，或None表示失败
        """
        try:
            response = requests.get(
                self.api_url,
                params=self.params,
                timeout=self.timeout
            )
            response.raise_for_status()  # 检查HTTP错误

            data = response.json()

            if 'bitcoin' not in data:
                st.error("API返回数据格式异常")
                return None

            return data['bitcoin']

        except requests.exceptions.Timeout:
            st.error("请求超时，请检查网络连接")
            return None
        except requests.exceptions.ConnectionError:
            st.error("网络连接错误，请检查网络")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP错误: {e}")
            return None
        except Exception as e:
            st.error(f"获取数据时发生错误: {str(e)}")
            return None

    def format_price(self, price):
        """格式化价格显示"""
        if price >= 1000:
            return f"${price:,.2f}"
        else:
            return f"${price:.2f}"

    def format_change(self, change):
        """格式化变化值显示"""
        return f"{change:+.2f}%"

    def format_timestamp(self, timestamp):
        """格式化时间戳"""
        if timestamp:
            dt = datetime.fromtimestamp(timestamp, pytz.UTC)
            local_dt = dt.astimezone(pytz.timezone('Asia/Shanghai'))
            return local_dt.strftime("%Y-%m-%d %H:%M:%S")
        return "未知时间"


def display_price_info(price_data, tracker):
    """显示价格信息"""

    # 主标题
    st.markdown('<div class="main-header">₿ 比特币价格追踪器</div>', unsafe_allow_html=True)

    # 价格卡片
    current_price = price_data.get('usd', 0)
    price_change = price_data.get('usd_24h_change', 0)
    price_change_amount = current_price * (price_change / 100) if price_change else 0

    st.markdown('<div class="price-container">', unsafe_allow_html=True)
    st.markdown('<div style="font-size: 1.2rem;">当前价格 (USD)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="current-price">{tracker.format_price(current_price)}</div>', unsafe_allow_html=True)

    # 显示涨跌信息
    if price_change > 0:
        st.markdown(f'''
            <div class="change-positive">
                ↑ {tracker.format_change(price_change)} 
                (${price_change_amount:+.2f})
            </div>
        ''', unsafe_allow_html=True)
    elif price_change < 0:
        st.markdown(f'''
            <div class="change-negative">
                ↓ {tracker.format_change(price_change)} 
                (${price_change_amount:+.2f})
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div style="color: #666; font-weight: bold;">
                {tracker.format_change(price_change)} 
                (${price_change_amount:+.2f})
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # 详细信息
    with st.container():
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown("### 📊 24小时数据")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="价格变化",
                value=tracker.format_change(price_change),
                delta=f"${price_change_amount:+.2f}"
            )

        with col2:
            volume = price_data.get('usd_24h_vol', 0)
            if volume >= 1_000_000_000:
                volume_str = f"${volume / 1_000_000_000:.2f}B"
            elif volume >= 1_000_000:
                volume_str = f"${volume / 1_000_000:.2f}M"
            else:
                volume_str = f"${volume:,.0f}"

            st.metric(
                label="24小时交易量",
                value=volume_str
            )

        st.markdown('</div>', unsafe_allow_html=True)


def main():
    """主函数"""

    # 创建追踪器实例
    tracker = BitcoinPriceTracker()

    # 侧边栏配置
    with st.sidebar:
        st.markdown("### ⚙️ 设置")

        # 自动刷新选项
        auto_refresh = st.checkbox(
            "启用自动刷新",
            value=st.session_state.auto_refresh,
            help="每30秒自动刷新数据"
        )

        if auto_refresh != st.session_state.auto_refresh:
            st.session_state.auto_refresh = auto_refresh
            st.rerun()

        st.markdown("---")
        st.markdown("### 📈 数据来源")
        st.markdown("数据来自 [CoinGecko API](https://www.coingecko.com/)")
        st.markdown("---")
        st.markdown("### ℹ️ 关于")
        st.markdown("""
        这是一个比特币价格追踪应用，提供：
        - 实时比特币价格
        - 24小时价格变化
        - 手动/自动刷新功能
        """)

    # 主界面
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # 刷新按钮
        if st.button("🔄 刷新数据", use_container_width=True, type="primary"):
            with st.spinner("正在获取最新数据..."):
                price_data = tracker.get_bitcoin_data()
                if price_data:
                    st.session_state.last_refresh = time.time()
                    st.success("数据已更新！")
                    time.sleep(0.5)  # 短暂显示成功消息
                    st.rerun()

        # 获取并显示数据
        with st.spinner("正在加载比特币数据..."):
            price_data = tracker.get_bitcoin_data()

            if price_data:
                display_price_info(price_data, tracker)

                # 显示最后更新时间
                last_updated = price_data.get('last_updated_at')
                if last_updated:
                    formatted_time = tracker.format_timestamp(last_updated)
                    st.markdown(f'<div class="last-updated">最后更新: {formatted_time}</div>', unsafe_allow_html=True)

                # 自动刷新逻辑
                if st.session_state.auto_refresh:
                    time.sleep(30)
                    st.rerun()
            else:
                st.error("无法获取比特币数据，请检查网络连接或稍后重试。")

                # 显示重试按钮
                if st.button("🔄 重试", use_container_width=True):
                    st.rerun()


if __name__ == "__main__":
    main()