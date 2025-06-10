import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Streamlit 페이지 설정
st.set_page_config(page_title="글로벌 시총 TOP10 주가 비교", layout="wide")
st.title("🌍 글로벌 시가총액 TOP10 기업의 주가 수익률 비교")
st.info("선택한 기간의 첫 거래일을 100으로 환산하여 각 기업의 주가 수익률 추세를 비교합니다.")


# --- 데이터 및 함수 정의 ---
# 시총 TOP10 기준 기업 티커 목록 (2025년 기준 추정치)
COMPANY_DICT = {
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

# st.cache_data: 데이터 로딩 함수에 캐시 적용하여 중복 로딩 방지 (성능 향상)
@st.cache_data
def load_stock_data(ticker, start_date, end_date):
    """지정된 기간의 주식 데이터를 yfinance를 통해 로드합니다."""
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        if df.empty:
            return None
        return df
    except Exception as e:
        st.error(f"{ticker} 데이터를 가져오는 중 오류 발생: {e}")
        return None

# --- 사이드바: 사용자 입력 ---
with st.sidebar:
    st.header("⚙️ 옵션")
    
    # 1. 기업 선택
    selected_companies = st.multiselect(
        "✅ 비교할 기업을 선택하세요",
        options=list(COMPANY_DICT.keys()),
        default=["Apple", "Microsoft", "Nvidia", "TSMC"] # 기본 선택
    )

    # 2. 날짜 범위 선택
    st.markdown("---")
    date_range = st.selectbox(
        "📅 기간을 선택하세요",
        ["최근 1년", "최근 3년", "최근 5년", "전체 (최대)"],
        index=1 # 기본값 '최근 3년'
    )

# --- 날짜 범위 계산 ---
end_date = datetime.today()
if date_range == "최근 1년":
    start_date = end_date - timedelta(days=365)
elif date_range == "최근 3년":
    start_date = end_date - timedelta(days=3 * 365)
elif date_range == "최근 5년":
    start_date = end_date - timedelta(days=5 * 365)
else: # 전체
    start_date = datetime(2010, 1, 1) # yfinance가 제공하는 시작일

# --- 데이터 처리 및 시각화 ---
fig = go.Figure()
has_data = False

for name in selected_companies:
    ticker = COMPANY_DICT[name]
    df = load_stock_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

    if df is not None and not df.empty:
        # 주가 정규화 (첫 날 종가를 100으로 설정)
        df['Normalized Price'] = (df['Close'] / df['Close'].iloc[0]) * 100
        
        fig.add_trace(go.Scatter(
            x=df.index, 
            y=df['Normalized Price'], 
            mode='lines', 
            name=name,
            hovertemplate = f'<b>{name}</b><br>날짜: %{{x|%Y-%m-%d}}<br>수익률: %{{y:.2f}}<extra></extra>'
        ))
        has_data = True

# --- 그래프 레이아웃 설정 ---
fig.update_layout(
    title={
        'text': f"<b>주요 기업 주가 수익률 비교 ({date_range})</b>",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="날짜",
    yaxis_title="정규화된 주가 (시작일 = 100)",
    yaxis_tickformat=".0f",
    legend_title="기업명",
    height=600,
    hovermode="x unified" # 마우스 올렸을 때 모든 종목 정보 표시
)

# 데이터가 있을 때만 차트 표시
if has_data:
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("선택한 기업의 데이터를 불러올 수 없거나, 선택된 기업이 없습니다.")
