import streamlit as st
import folium
from streamlit_folium import st_folium

# --- 페이지 설정 ---
st.set_page_config(
    page_title="달나라 지질 탐험 가이드",
    page_icon="🌕",
    layout="wide"
)

# --- 데이터 ---
# 달의 주요 지질 관광지에 대한 정보 (좌표, 설명, 이미지 URL)
# 좌표는 [위도, 경도] 형식입니다.
LOCATIONS = {
    "고요의 바다 (아폴로 11호 착륙지)": {
        "coords": [0.67408, 23.47297],
        "info": """
        ### 인류의 위대한 첫걸음
        1969년 7월 20일, 아폴로 11호의 달 착륙선 '이글'호가 이곳에 착륙했습니다. 닐 암스트롱과 버즈 올드린이 인류 최초로 달 표면에 발을 내디딘 역사적인 장소입니다. 
        '고요의 바다'는 실제 바다가 아니라, 수십억 년 전 용암이 흘러넘쳐 형성된 거대한 현무암 평원입니다. 표면이 비교적 평탄하여 초기 달 탐사선의 착륙 지점으로 선택되었습니다.
        - **지질학적 특징:** 현무암질의 월면석, 미세한 월면토(레골리스)
        - **탐사 중요도:** 인류 달 착륙의 상징적인 장소, 월석 샘플 채취
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Aldrin_with_experiment.jpg/800px-Aldrin_with_experiment.jpg"
    },
    "티코 충돌구 (Tycho Crater)": {
        "coords": [-43.43, -11.21],
        "info": """
        ### 달에서 가장 밝게 빛나는 '별'
        티코 충돌구는 달의 남반구에서 가장 눈에 띄는 지형 중 하나입니다. 약 1억 8백만 년 전에 형성된 비교적 '젊은' 충돌구로, 지름이 약 85km에 달합니다. 
        이곳이 유명한 이유는 충돌 시 분출된 물질들이 만든 '광조(Ray System)'가 무려 1,500km 이상 뻗어나가기 때문입니다. 보름달이 뜰 때면 지구에서도 맨눈으로 희미하게 볼 수 있을 정도로 밝게 빛납니다.
        - **지질학적 특징:** 중앙에 솟아오른 봉우리(Central Peak), 밝은 광조, 충격 용융물
        - **탐사 중요도:** 젊은 충돌구의 형성 과정과 달 표면 물질 연구
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Tycho_crater_on_the_Moon.jpg/1024px-Tycho_crater_on_the_Moon.jpg"
    },
    "코페르니쿠스 충돌구 (Copernicus Crater)": {
        "coords": [9.62, -20.01],
        "info": """
        ### '달의 군주'라 불리는 충돌구
        코페르니쿠스 충돌구는 달의 근지구면(지구를 향한 면)에 위치한 매우 인상적인 충돌구입니다. 약 8억 년 전에 형성되었으며, 지름은 93km에 달합니다. 
        망원경으로 보면 계단식으로 무너져 내린 테라스 형태의 내부 벽과 복잡한 중앙 봉우리 군을 선명하게 볼 수 있어 '달의 군주(The Monarch of the Moon)'라는 별명을 가지고 있습니다. 아폴로 12호 탐사 당시, 코페르니쿠스 충돌구에서 비롯된 것으로 추정되는 광조의 물질을 채취하기도 했습니다.
        - **지질학적 특징:** 계단식 내부 벽, 복잡한 중앙 봉우리, 넓게 퍼진 광조
        - **탐사 중요도:** 중기 연령대 충돌구의 구조 연구, 광조 물질 분석
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Copernicus_crater_LROC.png/1024px-Copernicus_crater_LROC.png"
    },
    "폭풍의 대양 (Oceanus Procellarum)": {
        "coords": [18.4, -57.4],
        "info": """
        ### 달에서 가장 거대한 '바다'
        '폭풍의 대양'은 달의 서쪽에 위치한 가장 큰 '바다'입니다. 면적이 약 4백만 km²로, 지구의 지중해보다도 훨씬 넓습니다. 이곳은 단일 충돌로 형성된 것이 아니라, 여러 화산 활동과 용암 흐름이 복합적으로 작용하여 만들어진 거대한 현무암 지대입니다.
        내부에는 아리스타르코스 고원과 같은 화산 활동의 증거가 풍부하며, KREEP 지형(칼륨, 희토류 원소, 인이 풍부한 지형)이 집중되어 있어 달의 지질학적 진화 과정을 연구하는 데 매우 중요한 장소입니다.
        - **지질학적 특징:** 광활한 현무암 평원, KREEP 지형, 다수의 주름 능선(Wrinkle ridges)
        - **탐사 중요도:** 달의 화산 활동과 열적 진화 연구
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Oceanus_Procellarum_LROC.jpg/1024px-Oceanus_Procellarum_LROC.jpg"
    },
    "아페닌 산맥 (Montes Apenninus)": {
        "coords": [18.91, -3.67],
        "info": """
        ### 아폴로 15호가 탐험한 거대 산맥
        아페닌 산맥은 '비의 바다(Mare Imbrium)'의 남동쪽 가장자리를 따라 굽이치는 거대한 산맥입니다. 약 39억 년 전, 비의 바다를 만든 거대 충돌의 여파로 형성되었습니다. 
        지구의 알프스 산맥처럼 험준하며, 일부 봉우리의 높이는 5,000m에 달합니다. 아폴로 15호는 이 산맥의 기슭에 착륙하여 최초로 월면차(Lunar Rover)를 사용, 산맥의 암석과 '해들리 협곡'을 탐사하며 달의 초기 지각 물질에 대한 중요한 단서를 얻었습니다.
        - **지질학적 특징:** 거대 충돌 분지의 테두리, 고대의 지각 물질(아노르토사이트), 깊은 협곡
        - **탐사 중요도:** 거대 충돌 분지 형성 과정, 달의 초기 지각 연구
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Apollo_15_landing_site_overview_from_orbit.jpg"
    }
}

# --- 앱 UI 구성 ---
st.title("🌕 달나라 지질 탐험 인터랙티브 가이드")
st.markdown("왼쪽 **드롭다운 메뉴**에서 탐험하고 싶은 장소를 선택하세요. Folium으로 구현된 **달 지도** 위에 위치가 표시되고, 아래에는 해당 장소에 대한 **자세한 설명과 사진**이 나타납니다.")

# --- 사이드바 ---
with st.sidebar:
    st.header("🚀 탐험지 선택")
    # 드롭다운 메뉴 생성
    location_name = st.selectbox(
        "가고 싶은 곳을 고르세요:",
        options=list(LOCATIONS.keys())
    )

# 선택된 장소의 정보 가져오기
selected_location = LOCATIONS[location_name]
coords = selected_location["coords"]
info_text = selected_location["info"]
image_url = selected_location["image"]

# --- 메인 화면 ---

# 두 개의 컬럼으로 레이아웃 분할 (지도 | 정보)
col1, col2 = st.columns([0.6, 0.4]) # 지도 60%, 정보 40% 비율

with col1:
    st.subheader(f"📍 {location_name} 위치")

    # Folium 지도 생성
    # 달 지도를 위한 커스텀 타일셋 URL
    # LROC WMS Global Mosaic 타일을 사용합니다.
    tiles_url = "https://cartocdn-basemaps-a.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png" # 예시용 어두운 지도
    moon_tiles = "https://s3.amazonaws.com/opmbuilder/301_moon/tiles/w/{z}/{x}/{y}.png"
    moon_attribution = "LRO/LROC/GSFC/ASU"
    
    # 지도 객체 생성. 선택된 장소를 중심으로 표시
    m = folium.Map(location=coords, zoom_start=5, tiles=moon_tiles, attr=moon_attribution)

    # 마커 추가
    folium.Marker(
        location=coords,
        popup=f"<strong>{location_name}</strong>",
        tooltip=location_name,
        icon=folium.Icon(color='red', icon='rocket', prefix='fa')
    ).add_to(m)

    # Streamlit에 지도 표시
    st_folium(m, width=800, height=600)

with col2:
    st.subheader("상세 정보")
    st.image(image_url, caption=f"{location_name}의 모습")
    st.markdown(info_text, unsafe_allow_html=True)


st.markdown("---")
st.info("이 가이드는 Streamlit과 Folium을 사용하여 제작되었습니다. 달 지도 데이터는 LROC WMS Global Mosaic에서 제공받았습니다.")
