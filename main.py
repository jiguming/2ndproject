import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="아이슬란드 지질 관광지 가이드", layout="wide")

# 제목 및 설명
st.title("🇮🇸 아이슬란드의 주요 지질 관광지 가이드")
st.markdown("""
아이슬란드는 화산, 간헐천, 용암지대 등 다양한 지질 명소로 가득한 나라입니다.  
이 가이드에서는 대표적인 지질 관광지를 지도로 시각화하고, 각각의 특징을 친절하게 설명합니다.
""")

# 관광지 데이터
places = [
    {
        "name": "씽벨리르 국립공원 (Þingvellir)",
        "location": [64.255, -21.129],
        "description": "유네스코 세계유산으로 지정된 장소로, 유라시아판과 북아메리카판이 갈라지는 지점에 위치. 판의 경계를 직접 볼 수 있는 특별한 장소입니다."
    },
    {
        "name": "게이시르 간헐천 지대 (Geysir)",
        "location": [64.310, -20.302],
        "description": "세계적으로 유명한 간헐천 지역. 현재는 스트로쿠르(Strokkur) 간헐천이 활발하게 활동 중이며 5~10분마다 물기둥을 뿜어냅니다."
    },
    {
        "name": "굴포스 폭포 (Gullfoss)",
        "location": [64.327, -20.121],
        "description": "빙하수로 형성된 장엄한 폭포. '골든 서클' 관광 루트의 핵심이며, 빙하와 강이 만들어낸 지질학적 예술 작품."
    },
    {
        "name": "미바튼 지역 (Mývatn)",
        "location": [65.603, -16.998],
        "description": "화산 활동으로 형성된 아름다운 호수와 주변의 지열 지대. 끓는 진흙탕, 용암지대, 지열 분화구 등 다양한 지형이 존재."
    },
    {
        "name": "크라플라 화산 (Krafla)",
        "location": [65.717, -16.778],
        "description": "최근까지도 활동했던 화산. 주변에는 용암 평원과 지열지대가 광범위하게 분포."
    },
    {
        "name": "아우르바크 간헐천 지역 (Hveravellir)",
        "location": [64.867, -19.550],
        "description": "고지대에 위치한 아름다운 지열 지역. 간헐천, 뜨거운 연못, 지열 연기가 어우러진 이색적 풍경 제공."
    },
]

# 지도 초기화
m = folium.Map(location=[64.9631, -19.0208], zoom_start=6)

# 마커 추가
for place in places:
    folium.Marker(
        location=place["location"],
        popup=f"<b>{place['name']}</b><br>{place['description']}",
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)

# 지도 표시
st_data = st_folium(m, width=1200, height=700)

# 마무리 안내
st.markdown("---")
st.markdown("📍 다양한 생성형 AI 도구와 예제는 [gptonline.ai/ko](https://gptonline.ai/ko/)에서 확인해보세요!")
