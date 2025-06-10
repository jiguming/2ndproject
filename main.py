import streamlit as st
import folium
from streamlit_folium import st_folium

# --- Astropy 라이브러리 임포트 ---
import astropy.units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
from astropy import constants as const

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Astropy 달 탐사 가이드",
    page_icon="🔭",
    layout="wide"
)

# --- 데이터: Astropy 객체로 재구성 ---
# 이제 좌표는 SkyCoord 객체로, 크기는 단위(u.km)를 붙여 관리합니다.


LOCATIONS_ASTRO = {
    "고요의 바다 (아폴로 11호 착륙지)": {
        "sky_coord": SkyCoord(lon=23.47297*u.deg, lat=0.67408*u.deg, frame='moon', radius=MOON_RADIUS),
        "info": "...", # 정보 텍스트는 이전과 동일
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Aldrin_with_experiment.jpg/800px-Aldrin_with_experiment.jpg"
    },
    "티코 충돌구 (Tycho Crater)": {
        "sky_coord": SkyCoord(lon=-11.21*u.deg, lat=-43.43*u.deg, frame='moon', radius=MOON_RADIUS),
        "diameter": 85 * u.km,
        "info": "...", # 정보 텍스트는 이전과 동일
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Tycho_crater_on_the_Moon.jpg/1024px-Tycho_crater_on_the_Moon.jpg"
    },
    "코페르니쿠스 충돌구 (Copernicus Crater)": {
        "sky_coord": SkyCoord(lon=-20.01*u.deg, lat=9.62*u.deg, frame='moon', radius=MOON_RADIUS),
        "diameter": 93 * u.km,
        "info": "...", # 정보 텍스트는 이전과 동일
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Copernicus_crater_LROC.png/1024px-Copernicus_crater_LROC.png"
    },
    "폭풍의 대양 (Oceanus Procellarum)": {
        "sky_coord": SkyCoord(lon=-57.4*u.deg, lat=18.4*u.deg, frame='moon', radius=MOON_RADIUS),
        "info": "...", # 정보 텍스트는 이전과 동일
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Oceanus_Procellarum_LROC.jpg/1024px-Oceanus_Procellarum_LROC.jpg"
    },
    "아페닌 산맥 (Montes Apenninus)": {
        "sky_coord": SkyCoord(lon=-3.67*u.deg, lat=18.91*u.deg, frame='moon', radius=MOON_RADIUS),
        "info": "...", # 정보 텍스트는 이전과 동일
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Apollo_15_landing_site_overview_from_orbit.jpg"
    }
}
# (각 Location의 info 텍스트는 공간상 생략했습니다. 이전 코드에서 복사해서 채워주세요.)

# Folium 지도 표시에 사용할 위도/경도 리스트
def get_folium_coords(astro_location):
    s_coord = astro_location['sky_coord']
    return [s_coord.lat.value, s_coord.lon.value]

# --- 앱 UI 구성 ---
st.title("🔭 Astropy 연동 달 탐사 가이드")
st.markdown("`Astropy` 라이브러리를 활용하여 과학적인 계산 기능을 추가한 달 탐사 가이드입니다.")

# --- 사이드바 ---
with st.sidebar:
    st.header("🚀 탐험지 선택")
    location_name = st.selectbox(
        "가고 싶은 곳을 고르세요:",
        options=list(LOCATIONS_ASTRO.keys())
    )
    
    st.markdown("---")

    # --- 기능 2: 거리 계산기 ---
    st.header("📏 달 표면 거리 계산기")
    start_point = st.selectbox("출발지:", options=list(LOCATIONS_ASTRO.keys()), index=0)
    end_point = st.selectbox("도착지:", options=list(LOCATIONS_ASTRO.keys()), index=1)
    
    if st.button("거리 계산"):
        coord1 = LOCATIONS_ASTRO[start_point]['sky_coord']
        coord2 = LOCATIONS_ASTRO[end_point]['sky_coord']
        
        # 두 지점의 각도 차이 계산
        separation_angle = coord1.separation(coord2)
        # 각도와 반지름을 이용해 거리 계산 (s = r * θ)
        distance = (separation_angle.to(u.rad).value * MOON_RADIUS).to(u.km)
        
        st.success(f"**{start_point}**에서 **{end_point}**까지의 거리는 약 **{distance.value:.2f} km** 입니다.")

    st.markdown("---")

    # --- 기능 3: 실시간 달 위치 ---
    st.header("🛰️ 현재 달의 위치")
    # 관측 위치: 서울 (EarthLocation)
    seoul = EarthLocation(lat='37.5665'*u.deg, lon='126.9780'*u.deg, height=38*u.m)
    
    # 현재 시간
    now = Time.now()
    
    # 서울에서 본 현재 시간의 달의 위치 계산 (고도/방위각 프레임)
    moon_altaz = SkyCoord(now, frame='moon', location=seoul).transform_to(AltAz(obstime=now, location=seoul))
    
    st.info(f"**관측 기준:** 서울\n\n**현재 시간:** {now.to_datetime().strftime('%Y-%m-%d %H:%M:%S')}")
    st.metric(label="달의 고도 (Altitude)", value=f"{moon_altaz.alt.deg:.2f}°")
    st.metric(label="달의 방위각 (Azimuth)", value=f"{moon_altaz.az.deg:.2f}°")
    st.caption("고도: 지평선 위 각도. 90°가 천정입니다.\n방위각: 북쪽(0°)에서 동쪽으로 잰 각도입니다.")


# 선택된 장소의 정보 가져오기
selected_location = LOCATIONS_ASTRO[location_name]
coords = get_folium_coords(selected_location) # Folium용 좌표 추출
info_text = selected_location["info"]
image_url = selected_location["image"]

# --- 메인 화면 ---
col1, col2 = st.columns([0.6, 0.4])

moon_tiles = "https://s3.amazonaws.com/opmbuilder/301_moon/tiles/w/{z}/{x}/{y}.png"
moon_attribution = "LRO/LROC/GSFC/ASU"

with col1:
    st.subheader(f"🛰️ {location_name} 상세 탐험 지도")
    m_detail = folium.Map(location=coords, zoom_start=6, tiles=moon_tiles, attr=moon_attribution)
    folium.Marker(
        location=coords,
        popup=f"<strong>{location_name}</strong>",
        tooltip="클릭해서 자세히 보기",
        icon=folium.Icon(color='red', icon='rocket', prefix='fa')
    ).add_to(m_detail)
    st_folium(m_detail, width=800, height=600)

with col2:
    st.subheader("📖 상세 정보")
    st.image(image_url, caption=f"{location_name}의 모습")
    st.markdown(info_text, unsafe_allow_html=True)
