import streamlit as st
import folium
from streamlit_folium import st_folium

# 관광지 데이터
places = [
    {
        "name": "씽벨리르 국립공원 🌍",
        "location": [64.255, -21.129],
        "description": "유라시아판과 북아메리카판이 갈라지는 지점. 유네스코 세계유산으로 지정된 독특한 지질 지대입니다.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/e/e2/Thingvellir_National_Park%2C_Iceland_%2848807001837%29.jpg"
        ]
    },
    {
        "name": "게이시르 간헐천 💦",
        "location": [64.310, -20.302],
        "description": "스트로쿠르 간헐천이 5~10분 간격으로 물기둥을 뿜어올리는 세계적인 지열 관광지입니다.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/5/55/Strokkur_geyser_Iceland_2015.JPG"
        ]
    },
    {
        "name": "굴포스 폭포 🌈",
        "location": [64.327, -20.121],
        "description": "빙하수가 절벽 아래로 쏟아지는 장엄한 폭포로, 골든서클의 핵심 명소입니다.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/e/e1/Gullfoss_from_above.jpg"
        ]
    },
    {
        "name": "미바튼 지역 🌋",
        "location": [65.603, -16.998],
        "description": "화산과 지열이 만든 이국적인 풍경. 뜨거운 진흙탕과 용암 동굴이 펼쳐집니다.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/3/3f/Myvatn%2C_Iceland_-_panoramio.jpg"
        ]
    }
]

# 페이지 설정
st.set_page_config(page_title="🇮🇸 아이슬란드 지질 관광지 가이드", layout="wide")
st.title("🗺️ 아이슬란드 지질 명소 가이드")

# 사이드바 선택
st.sidebar.header("📍 관광지 선택")
selected_name = st.sidebar.radio("이동할 지질 명소를 고르세요", [p["name"] for p in places])
selected = next(p for p in places if p["name"] == selected_name)

# 지도 생성
m = folium.Map(location=selected["location"], zoom_start=7)
for place in places:
    folium.Marker(
        location=place["location"],
        tooltip=place["name"],
        popup=place["description"],
        icon=folium.Icon(color="red" if place["name"] == selected["name"] else "gray")
    ).add_to(m)
st_folium(m, width=1100, height=500)

# 설명 및 이미지 출력
st.markdown(f"## 🔍 {selected['name']}")
st.markdown(selected["description"])
st.markdown("### 📸 대표 이미지")
for img in selected["images"]:
    st.image(img, use_column_width=True)

