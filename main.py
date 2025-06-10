import streamlit as st
import folium
from streamlit_folium import st_folium

import astropy.units as u
from astropy.coordinates import Angle, get_moon, EarthLocation, AltAz
from astropy.time import Time

# --- 설정: 달 반지름 정의 ---
MOON_RADIUS = 1737.4 * u.km

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Astropy 달 탐사 가이드",
    page_icon="🌕",
    layout="wide"
)

# --- 장소 정보 정의 ---
LOCATIONS_ASTRO = {
    "고요의 바다 (아폴로 11호 착륙지)": {
        "lat": 0.67408 * u.deg,
        "lon": 23.47297 * u.deg,
        "info": """
        ### 인류의 위대한 첫걸음
        1969년 7월 20일, 아폴로 11호의 달 착륙선 '이글'호가 이곳에 착륙했습니다. 닐 암스트롱과 버즈 올드린이 인류 최초로 달 표면에 발을 내디딘 역사적인 장소입니다.
        - **지질학적 특징:** 현무암질 월면석, 월면토
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Aldrin_with_experiment.jpg/800px-Aldrin_with_experiment.jpg"
    },
    "티코 충돌구 (Tycho Crater)": {
        "lat": -43.43 * u.deg,
        "lon": -11.21 * u.deg,
        "info": """
        ### 달에서 가장 밝은 충돌구
        티코는 지름 약 85km의 젊은 충돌구로, 보름달 때 밝은 광조가 특징입니다.
        - **지질학적 특징:** 중앙 봉우리, 광조
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Tycho_crater_on_the_Moon.jpg/1024px-Tycho_crater_on_the_Moon.jpg"
    },
    "코페르니쿠스 충돌구 (Copernicus Crater)": {
        "lat": 9.62 * u.deg,
        "lon": -20.01 * u.deg,
        "info": """
        ### 달의 군주
        계단식 내부 구조와 중앙 봉우리가 뚜렷한 대형 충돌구입니다.
        - **지질학적 특징:** 계단식 벽, 복잡한 중앙 구조
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Copernicus_crater_LROC.png/1024px-Copernicus_crater_LROC.png"
    },
    "폭풍의 대양 (Oceanus Procellarum)": {
        "lat": 18.4 * u.deg,
        "lon": -57.4 * u.deg,
        "info": """
        ### 달에서 가장 큰 '바다'
        거대한 현무암질 평원이며 KREEP 물질이 풍부한 지역입니다.
        - **지질학적 특징:** 광활한 현무암 지대
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Oceanus_Procellarum_LROC.jpg/1024px-Oceanus_Procellarum_LROC.jpg"
    },
    "아페닌 산맥 (Montes Apenninus)": {
        "lat": 18.91 * u.deg,
        "lon": -3.67 * u.deg,
        "info": """
        ### 아폴로 15호의 탐사지
        험준한 고산지대로, 달 초기 지각물질 연구에 중요합니다.
        - **지질학적 특징:** 아노르토사이트, 협곡
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Apollo_15_landing_site_overview_from_orbit.jpg"
    }
}

# --- 좌표 변환 함수 ---
def get_folium_coords(location):
    return [location["lat"].value, location["lon"].value]

# --- UI 구성 ---
st.title("🌕 Astropy 기반 달 탐사 가이드")
st.markdown("Astropy와 Folium을 활용한 과학적이고 직관적인 달 탐사 지도입니다.")

with st.sidebar:
    st.header("🚀 탐험지 선택")
    location_name = st.selectbox("가고 싶은 장소를 선택하세요:", options=list(LOCATIONS_ASTRO.keys()))

    st.markdown("---")
    st.header("📏 달 표면 거리 계산기")
    start = st.selectbox("출발지:", options=list(LOCATIONS_ASTRO.keys()), index=0)
    end = st.selectbox("도착지:", options=list(LOCATIONS_ASTRO.keys()), index=1)

    if st.button("거리 계산"):
        start_lat = LOCATIONS_ASTRO[start]["lat"]
        start_lon = LOCATIONS_ASTRO[start]["lon"]
        end_lat = LOCATIONS_ASTRO[end]["lat"]
        end_lon = LOCATIONS_ASTRO[end]["lon"]

        # 대략적인 구면 거리 계산
        delta_sigma = Angle(
            ((start_lat - end_lat)**2 + ((start_lon - end_lon) * u.cos((start_lat + end_lat)/2))**2)**0.5
        )
        distance = (delta_sigma.to(u.rad).value * MOON_RADIUS).to(u.km)

        st.success(f"**{start}** → **{end}** 거리: **{distance.value:.2f} km**")

    st.markdown("---")
    st.header("🌝 현재 달의 위치 (지구 기준)")

    seoul = EarthLocation(lat=37.5665*u.deg, lon=126.9780*u.deg, height=38*u.m)
    now = Time.now()

    moon = get_moon(now, location=seoul)
    moon_altaz = moon.transform_to(AltAz(obstime=now, location=seoul))

    st.metric("달의 고도 (Altitude)", f"{moon_altaz.alt.deg:.2f}°")
    st.metric("달의 방위각 (Azimuth)", f"{moon_altaz.az.deg:.2f}°")
    st.caption("※ 서울 기준. 고도: 천정 기준 각도, 방위각: 북쪽 기준 시계방향 각도.")

# --- 본문 지도 및 설명 ---
selected = LOCATIONS_ASTRO[location_name]
coords = get_folium_coords(selected)

col1, col2 = st.columns([0.6, 0.4])

moon_tiles = "https://s3.amazonaws.com/opmbuilder/301_moon/tiles/w/{z}/{x}/{y}.png"
moon_attribution = "LRO/LROC/GSFC/ASU"

with col1:
    st.subheader(f"🗺️ {location_name} 지도")
    m = folium.Map(location=coords, zoom_start=6, tiles=moon_tiles, attr=moon_attribution)
    folium.Marker(
        location=coords,
        tooltip=location_name,
        popup=location_name,
        icon=folium.Icon(color='red', icon='star')
    ).add_to(m)
    st_folium(m, width=800, height=500)

with col2:
    st.subheader("📖 상세 설명")
    st.image(selected["image"], caption=location_name)
    st.markdown(selected["info"], unsafe_allow_html=True)

st.markdown("---")
st.info("이 웹앱은 Streamlit, Folium, Astropy를 이용하여 제작되었습니다. 지도 타일은 LROC Global Mosaic을 기반으로 합니다.")
