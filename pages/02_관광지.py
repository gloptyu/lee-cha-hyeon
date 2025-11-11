"""
Streamlit app: Seoul Top10 Tourist Spots (folium)
File: app.py

How to use:
1. Create a new repo (GitHub) with this file named `app.py`.
2. Add a `requirements.txt` file (content shown below) to the repo.
3. Deploy to Streamlit Cloud (https://share.streamlit.io) by connecting the GitHub repo.

This single-file app shows a Folium map with the top-10 Seoul attractions (popular with foreign visitors), lists details in the sidebar,
and lets users center/highlight any attraction. The markers include popups and brief descriptions.

Dependencies (also included in requirements.txt below):
- streamlit
- folium
- streamlit-folium
- pandas

"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="Seoul Top10 (Folium)", layout="wide")

# --- Data: top 10 Seoul attractions (popular with foreign visitors) ---
ATTRACTIONS = [
    {"name": "Gyeongbokgung Palace", "lat": 37.579617, "lon": 126.977041, "desc": "Grand palace of the Joseon dynasty; must-see historical site."},
    {"name": "Changdeokgung Palace & Secret Garden", "lat": 37.579377, "lon": 126.991047, "desc": "UNESCO site; beautiful gardens and palace architecture."},
    {"name": "Bukchon Hanok Village", "lat": 37.582600, "lon": 126.983000, "desc": "Traditional hanok neighborhood nestled between palaces."},
    {"name": "N Seoul Tower (Namsan)", "lat": 37.551169, "lon": 126.988226, "desc": "Iconic city-view tower with observation decks and lights at night."},
    {"name": "Myeongdong Shopping Street", "lat": 37.560975, "lon": 126.986016, "desc": "Bustling shopping district famous for cosmetics and street food."},
    {"name": "Insadong", "lat": 37.574435, "lon": 126.984969, "desc": "Cultural street known for traditional crafts, tea houses, galleries."},
    {"name": "Dongdaemun Design Plaza (DDP)", "lat": 37.566295, "lon": 127.009005, "desc": "Futuristic architecture, night markets, and fashion malls."},
    {"name": "Hongdae (Hongik University Area)", "lat": 37.556256, "lon": 126.922655, "desc": "Youth culture, live music, cafés, and nightlife."},
    {"name": "Gangnam (COEX Mall & area)", "lat": 37.512021, "lon": 127.058567, "desc": "Upscale shopping, entertainment, and K-pop culture hubs."},
    {"name": "Lotte World Tower (Jamsil)", "lat": 37.512569, "lon": 127.102492, "desc": "Skyscraper with observation deck, aquarium, and luxury mall."},
]

# Convert to DataFrame for clean display
df = pd.DataFrame(ATTRACTIONS)

# --- Streamlit layout ---
col1, col2 = st.columns((1, 2))

with col1:
    st.title("Seoul — Top 10 Attractions (for foreign visitors)")
    st.markdown("간단한 설명과 Folium 지도(마커 포함)를 제공합니다. 오른쪽에서 지도를 확인하세요.")

    st.sidebar.header("설정")
    show_map = st.sidebar.checkbox("지도 표시", value=True)
    selected = st.sidebar.selectbox("하이라이트할 장소 선택", ["전체 보기"] + df['name'].tolist())
    show_list = st.sidebar.checkbox("장소 목록 보기", value=True)

    if show_list:
        st.subheader("Top 10 목록")
        for i, row in df.iterrows():
            st.markdown(f"**{i+1}. {row['name']}** — {row['desc']}")

with col2:
    if not show_map:
        st.info("사이드바에서 '지도 표시'를 체크하면 지도를 볼 수 있습니다.")
    else:
        # Center map on Seoul
        seoul_center = (37.5665, 126.9780)
        m = folium.Map(location=seoul_center, zoom_start=12)

        # Add markers
        for i, row in df.iterrows():
            popup_html = f"<b>{row['name']}</b><br>{row['desc']}"
            tooltip = f"{i+1}. {row['name']}"

            # If this is the selected spot, make a larger/different icon
            if selected == row['name']:
                folium.Marker(
                    location=(row['lat'], row['lon']),
                    popup=popup_html,
                    tooltip=tooltip,
                    icon=folium.Icon(color='red', icon='info-sign'),
                ).add_to(m)

                # zoom in a bit
                m.location = (row['lat'], row['lon'])
                m.zoom_start = 15

            else:
                folium.Marker(
                    location=(row['lat'], row['lon']),
                    popup=popup_html,
                    tooltip=tooltip,
                    icon=folium.Icon(color='blue', icon='ok-sign'),
                ).add_to(m)

        # Add a small minimap and layer control
        try:
            from folium.plugins import MiniMap
            minimap = MiniMap(toggle_display=True)
            m.add_child(minimap)
        except Exception:
            pass

        # Render map in Streamlit
        st_folium(m, width=900, height=600)

# --- Footer / notes ---
st.markdown("---")
st.caption("데이터 출처: VisitSeoul, Tripadvisor, Lonely Planet 등 공개 여행 자료를 기반으로 편집(예시 좌표 포함).\n앱 코드와 requirements.txt를 그대로 복사하여 Streamlit Cloud에 배포하세요.")


# =====================
# requirements.txt (copy this into a separate file named requirements.txt)
# =====================
#
# streamlit
# folium
# streamlit-folium
# pandas
#
# Optional (if you want to pin versions):
# streamlit==1.26.0
# folium==0.14.0
# streamlit-folium==0.12.2
# pandas==2.2.0
#
# ---------------------
# End of file
# ---------------------
