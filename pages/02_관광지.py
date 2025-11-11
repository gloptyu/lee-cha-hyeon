import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Seoul Top10 (Folium)", layout="wide")

# --- 데이터 ---
ATTRACTIONS = [
    {"name": "Gyeongbokgung Palace", "lat": 37.579617, "lon": 126.977041, "desc": "Grand palace of the Joseon dynasty; must-see historical site."},
    {"name": "Changdeokgung Palace & Secret Garden", "lat": 37.579377, "lon": 126.991047, "desc": "UNESCO site; beautiful gardens and palace architecture."},
    {"name": "Bukchon Hanok Village", "lat": 37.582600, "lon": 126.983000, "desc": "Traditional hanok neighborhood between palaces."},
    {"name": "N Seoul Tower (Namsan)", "lat": 37.551169, "lon": 126.988226, "desc": "Iconic tower with city views and romantic night lights."},
    {"name": "Myeongdong Shopping Street", "lat": 37.560975, "lon": 126.986016, "desc": "Famous shopping street with street food and cosmetics."},
    {"name": "Insadong", "lat": 37.574435, "lon": 126.984969, "desc": "Traditional street with tea houses and craft shops."},
    {"name": "Dongdaemun Design Plaza (DDP)", "lat": 37.566295, "lon": 127.009005, "desc": "Futuristic architecture and night markets."},
    {"name": "Hongdae", "lat": 37.556256, "lon": 126.922655, "desc": "Youth culture, music, cafes, and nightlife."},
    {"name": "Gangnam (COEX Mall)", "lat": 37.512021, "lon": 127.058567, "desc": "Upscale shopping and K-pop culture hub."},
    {"name": "Lotte World Tower", "lat": 37.512569, "lon": 127.102492, "desc": "Skyscraper with observation deck and mall."},
]

df = pd.DataFrame(ATTRACTIONS)

# --- 레이아웃 ---
col1, col2 = st.columns((1, 2))

with col1:
    st.title("🏙️ Seoul — Top 10 Attractions")
    st.markdown("서울의 대표 관광지 10곳을 Folium 지도로 표시합니다.")
    st.sidebar.header("설정")
    show_map = st.sidebar.checkbox("지도 표시", value=True)
    selected = st.sidebar.selectbox("하이라이트할 장소", ["전체 보기"] + df["name"].tolist())

with col2:
    if show_map:
        m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

        for i, row in df.iterrows():
            popup = f"<b>{row['name']}</b><br>{row['desc']}"
            color = "red" if selected == row["name"] else "blue"
            folium.Marker(
                [row["lat"], row["lon"]],
                popup=popup,
                tooltip=f"{i+1}. {row['name']}",
                icon=folium.Icon(color=color)
            ).add_to(m)

        if selected != "전체 보기":
            spot = df[df["name"] == selected].iloc[0]
            m.fit_bounds([(spot["lat"], spot["lon"]), (spot["lat"], spot["lon"])])

        st_folium(m, width=630, height=420)

        # 지도 아래 관광지 설명
        st.markdown("### 🗺️ 관광지 간단 설명")
        for i, row in df.iterrows():
            st.markdown(f"**{i+1}. {row['name']}** — {row['desc']}")
    else:
        st.info("사이드바에서 '지도 표시'를 체크하면 지도를 볼 수 있습니다.")

st.markdown("---")
st.caption("데이터 출처: VisitSeoul, Tripadvisor, Lonely Planet 등 공개 여행 자료 기반.")
