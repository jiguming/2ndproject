import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="🇮🇸 아이슬란드 지질 명소 가이드", layout="wide")

# 스타일 적용 (배경 색상과 제목 꾸미기)
st.markdown(
    """
    <style>
    body {
        background-color: #e7f0f7;
    }
    .title {
        font-size: 48px;
        color: #004e7c;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="title">🌋 아이슬란드의 지질 명소 안내서 🇮🇸</p>', unsafe_allow_html=True)

st.markdown("""
아이슬란드는 지구의 살아있는 역사를 품고 있는 나라입니다. 🔥  
이 가이드는 주요 지질 명소를 지도로 시각화하고, 각 명소로 이동할 수 있는 버튼도 제공합니다! 🗺️  
""")

# 관광지 데이터 (더 추가함)
places = [
    {"name": "씽벨리르 국립공원 🌍", "location": [64.255, -21.129],
     "description": "판 구조론을 직접 목격할 수 있는 유네스코 세계유산 지역."},
    {"name": "게이시르 간헐천 지대 💦", "location": [64.310, -20.302],
     "description": "세계에서 가장 유명한 간헐천 지대 중 하나. '스트로쿠르'가 주요 간헐천."},
    {"name": "굴포스 폭포 🌈", "location": [64.327, -20.121],
     "description": "거대한 빙하수 폭포. '골든 서클'의 필수 코스!"},
    {"name": "미바튼 지역 🌋", "location": [65.603, -16.998],
     "description": "화산지형, 지열지대, 그리고 아름다운 호수의 조화."},
    {"name": "크라플라 화산 🔥", "location": [65.717, -16.778],
     "description": "최근까지 활동했던 화산. 용암 분출 흔적이 잘 보존됨."},
    {"name": "아우르바크 간헐천 지역 🌫️", "location": [64.867, -19.550],
     "description": "산악 지대의 비밀스러운 간헐천 온천."},
    {"name": "스카프타펠 국립공원 🏔️", "location": [64.016, -16.966],
     "description": "빙하와 화산의 조화를 이룬 독특한 국립공원."},
    {"name": "라키 용암지대 🌑", "location": [64.100, -18.200],
     "description": "1783년 대분화로 생성된 거대한 용암지대."},
    {"name": "헤클라 화산 ⛰️", "location": [63.989, -19.671],
     "description": "아이슬란드에서 가장 활발한 화산 중 하나."},
    {"name": "스나이펠스요쿨 빙하화산 ❄️", "location": [64.808, -23.776],
     "description": "쥘 베른의 『지구 속 여행』 배경이 된 전설의 화산."},
]

# 사이드바에 버튼 배치
st.sidebar.title("🧭 관광지로 바로 이동하기")
selected_place = st.sidebar.radio("관광지 목록", [place["name"] for place in places])

# 선택한 관광지 위치 추출
selected_data = next((p for p in places if p["name"] == selected_place), None)
map_center = selected_data["location"] if selected_data else [64.9631, -19.0208]

# 폴리움 지도 생성
m = folium.Map(
    location=map_center,
    zoom_start=7,
    tiles="Stamen Terrain",
    attr="Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors"
)

# 마커 추가
for place in places:
    folium.Marker(
        location=place["location"],
        popup=f"<b>{place['name']}</b><br>{place['description']}",
        tooltip=place["name"],
        icon=folium.Icon(color="blue", icon="info-sign"),
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=1100, height=700)

# 설명란
if selected_data:
    st.markdown("---")
    st.markdown(f"## 🔍 {selected_data['name']}")
    st.markdown(f"{selected_data['description']}")

# 하단 안내
st.markdown("---")
st.markdown("📌 이 가이드는 [gptonline.ai/ko](https://gptonline.ai/ko/)에서 제공하는 생성형 AI 활용 예제입니다!")
