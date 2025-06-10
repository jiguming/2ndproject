import streamlit as st
import folium
from streamlit_folium import st_folium

import astropy.units as u
from astropy.coordinates import Angle, AltAz, EarthLocation, get_body
from astropy.time import Time

# --- 설정 ---
MOON_RADIUS = 1737.4 * u.km

st.set_page_config(
    page_title="🌕 달 지질 탐사 가이드 & 퀴즈",
    layout="wide"
)

# --- 장소 데이터 ---
LOCATIONS = {
    "고요의 바다 (아폴로 11호 착륙지)": {
        "lat": 0.67408 * u.deg,
        "lon": 23.47297 * u.deg,
        "info": "1969년 아폴로 11호가 착륙한 최초의 달 탐사 지점. 평탄한 현무암 지대.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Aldrin_with_experiment.jpg/800px-Aldrin_with_experiment.jpg"
    },
    "티코 충돌구": {
        "lat": -43.43 * u.deg,
        "lon": -11.21 * u.deg,
        "info": "보름달에서 밝게 보이는 광조를 가진 대형 충돌구.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Tycho_crater_on_the_Moon.jpg/1024px-Tycho_crater_on_the_Moon.jpg"
    },
    "코페르니쿠스 충돌구": {
        "lat": 9.62 * u.deg,
        "lon": -20.01 * u.deg,
        "info": "계단식 구조와 중앙 봉우리를 가진 고전적 충돌구.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Copernicus_crater_LROC.png/1024px-Copernicus_crater_LROC.png"
    },
    "폭풍의 대양": {
        "lat": 18.4 * u.deg,
        "lon": -57.4 * u.deg,
        "info": "달에서 가장 넓은 '바다'로 다양한 지질 활동의 흔적이 있는 지역.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Oceanus_Procellarum_LROC.jpg/1024px-Oceanus_Procellarum_LROC.jpg"
    },
    "아페닌 산맥": {
        "lat": 18.91 * u.deg,
        "lon": -3.67 * u.deg,
        "info": "아폴로 15호가 탐사한 험준한 산악지대.",
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Apollo_15_landing_site_overview_from_orbit.jpg"
    }
}

# --- 위치 변환 함수 ---
def get_coords(loc):
    return [loc["lat"].value, loc["lon"].value]

# --- 메인 제목 ---
st.title("🌕 달 지질 탐사 가이드 + 퀴즈")

# --- 좌측 탐험 선택 ---
with st.sidebar:
    st.header("🚀 탐사 장소 선택")
    selected_name = st.selectbox("탐사할 장소:", LOCATIONS.keys())
    selected = LOCATIONS[selected_name]

    st.image(selected["image"], caption=selected_name)
    st.markdown(f"🧾 {selected['info']}")

    st.markdown("---")
    st.header("📏 표면 거리 계산")
    start = st.selectbox("출발지", LOCATIONS.keys(), key="start")
    end = st.selectbox("도착지", LOCATIONS.keys(), key="end")

    if st.button("거리 측정"):
        s_lat, s_lon = LOCATIONS[start]["lat"], LOCATIONS[start]["lon"]
        e_lat, e_lon = LOCATIONS[end]["lat"], LOCATIONS[end]["lon"]
        delta_sigma = Angle(
            ((s_lat - e_lat)**2 + ((s_lon - e_lon) * u.cos((s_lat + e_lat)/2))**2)**0.5
        )
        distance = (delta_sigma.to(u.rad).value * MOON_RADIUS).to(u.km)
        st.success(f"{start} → {end} 거리: {distance.value:.2f} km")

    st.markdown("---")
    st.header("🌝 서울에서의 달 위치")
    now = Time.now()
    seoul = EarthLocation(lat=37.5665*u.deg, lon=126.9780*u.deg, height=38*u.m)
    moon = get_body("moon", now, location=seoul)
    moon_altaz = moon.transform_to(AltAz(obstime=now, location=seoul))
    st.metric("고도 (Altitude)", f"{moon_altaz.alt.deg:.1f}°")
    st.metric("방위각 (Azimuth)", f"{moon_altaz.az.deg:.1f}°")

# --- 메인 지도 ---
col1, col2 = st.columns([0.6, 0.4])

with col1:
    st.subheader(f"🗺️ {selected_name} 지도")
    moon_tiles = "https://s3.amazonaws.com/opmbuilder/301_moon/tiles/w/{z}/{x}/{y}.png"
    m = folium.Map(location=get_coords(selected), zoom_start=6, tiles=moon_tiles, attr="LRO/LROC/GSFC/ASU")
    folium.Marker(location=get_coords(selected), tooltip=selected_name, popup=selected["info"]).add_to(m)
    st_folium(m, width=800, height=500)

with col2:
    st.subheader("🧠 달 탐사 퀴즈")
    
    quiz_q = "🚀 아폴로 11호가 착륙한 장소는 어디인가요?"
    quiz_options = [
        "티코 충돌구",
        "고요의 바다 (아폴로 11호 착륙지)",
        "폭풍의 대양",
        "코페르니쿠스 충돌구"
    ]
    quiz_answer = "고요의 바다 (아폴로 11호 착륙지)"
    
    user_choice = st.radio(quiz_q, quiz_options)
    
    if st.button("정답 확인"):
        if user_choice == quiz_answer:
            st.success("🎉 정답입니다! 훌륭해요!")
            st.balloons()
        else:
            st.error("😢 오답입니다. 다시 시도해보세요!")

st.markdown("---")
st.caption("이 앱은 Streamlit, Folium, Astropy를 기반으로 구성된 지질학 교육 콘텐츠입니다.")
