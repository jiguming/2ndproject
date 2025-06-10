import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="글로벌 시총 TOP10 주가 비교", layout="wide")
st.title("🌍 글로벌 시가총액 TOP10 기업의 최근 3년 주가 변화")

# 시총 TOP10 기준 기업 티커 목록 (2025년 기준 추정치)
company_dict = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    "Eli Lilly": "LLY"
}

selected_companies = st.multiselect("✅ 비교할 기업을 선택하세요", options=list(company_dict.keys()), default=list(company_dict.keys()))

# 날짜 범위 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=3 * 365)

# 데이터 가져오기 및 시각화
fig = go.Figure()

for name in selected_companies:
    ticker = company_dict[name]
    try:
        df = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
        if not df.empty:
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=name))
    except:
        st.warning(f"{name}의 데이터를 가져오는 데 실패했습니다.")

# 그래프 설정
fig.update_layout(
    title="📊 최근 3년간 주가 비교 (종가 기준)",
    xaxis_title="날짜",
    yaxis_title="주가 (USD or 각국 통화)",
    legend_title="기업명",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
