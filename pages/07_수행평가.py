import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(page_title="⚽ 축구 선수 TOP10", layout="wide")

# -----------------------
# 페이지 배경 CSS
# -----------------------
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background: url("https://images.unsplash.com/photo-1521412644187-c49fa049e84d?auto=format&fit=crop&w=1470&q=80");
background-size: cover;
}
[data-testid="stHeader"] {background-color: rgba(0,0,0,0);}
[data-testid="stToolbar"] {right: 2rem;}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("⚽ 축구 선수 TOP10 비교 & 추천 (팀컬러 강조)")

# -----------------------
# 선수 데이터 + 팀 컬러
# -----------------------
data = {
    "이름": ["손흥민", "리오넬 메시", "크리스티아누 호날두", "킬리안 음바페", "네이마르",
             "케빈 더 브라위너", "모하메드 살라", "로베르트 레반도프스키", "버질 반 다이크", "이강인"],
    "클럽": ["토트넘", "인터 마이애미", "알나스르", "레알 마드리드", "산투스",
             "나폴리", "리버풀", "FC 바르셀로나", "리버풀", "마요르카"],
    "국적": ["대한민국", "아르헨티나", "포르투갈", "프랑스", "브라질",
             "벨기에", "이집트", "폴란드", "네덜란드", "대한민국"],
    "팀컬러": ["#041E42", "#FF5DA2", "#FFD700", "#FFFFFF", "#00AEEF",
               "#00AEEF", "#C8102E", "#A50044", "#C8102E", "#0033A0"],
    "스피드": [95, 88, 87, 96, 91, 79, 92, 76, 70, 87],
    "드리블": [93, 95, 89, 90, 94, 85, 91, 82, 60, 88],
    "슈팅": [85, 92, 93, 91, 86, 88, 90, 95, 65, 80],
    "패스": [82, 91, 82, 80, 87, 94, 80, 78, 82, 90],
    "수비": [40, 30, 35, 40, 30, 50, 35, 40, 94, 45],
    "골": [22, 30, 28, 26, 22, 12, 27, 34, 5, 10],
    "도움": [12, 20, 15, 18, 19, 21, 13, 9, 3, 8],
    "경기": [34, 35, 32, 33, 30, 34, 33, 36, 32, 30],
    "커리어": [
        ["토트넘 주전 공격수", "프리미어리그 골든부트 수상"],
        ["바르셀로나·PSG·인터 마이애미", "발롱도르 7회 수상"],
        ["맨유·레알·유벤투스·알나스르", "UEFA 챔피언스리그 우승 경험"],
        ["PSG·프랑스 대표팀 주전", "월드컵 우승"],
        ["산투스·바르셀로나·PSG", "FIFA 컨페더레이션컵 우승"],
        ["맨체스터 시티 핵심", "EPL 최다 도움 기록"],
        ["리버풀 핵심", "프리미어리그 득점왕"],
        ["도르트문트·바이에른·바르셀로나", "FIFA 클럽 월드컵 우승"],
        ["리버풀 센터백", "UEFA 챔피언스리그 우승"],
        ["발렌시아 유스 출신", "마요르카 주전"]
    ],
    "이미지": [
        "https://upload.wikimedia.org/wikipedia/commons/2/2e/Son_Heung-min_2022.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8c/Lionel_Messi_20180710.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/5/5c/Kylian_Mbapp%C3%A9_2022.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/37/Neymar_2018.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0a/Kevin_De_Bruyne_2018.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0c/Mohamed_Salah_2018.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/7/7b/Robert_Lewandowski_2021.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/12/Virgil_van_Dijk_2019.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/0/0f/Lee_Gang-in_2021.jpg"
    ]
}

df = pd.DataFrame(data)

# -----------------------
# 선수 선택
# -----------------------
selected_players = st.sidebar.multiselect(
    "비교할 선수 선택",
    df["이름"],
    default=[df["이름"][0], df["이름"][1]]
)

if len(selected_players) < 2:
    st.warning("선수를 최소 2명 이상 선택하세요!")
    st.stop()

compare_df = df[df["이름"].isin(selected_players)]

# -----------------------
# 레이더 차트
# -----------------------
st.subheader("📌 능력치 레이더 차트")
categories = ["스피드", "드리블", "슈팅", "패스", "수비"]
fig = go.Figure()
for _, row in compare_df.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=[row[c] for c in categories],
        theta=categories,
        fill='toself',
        name=row["이름"]
    ))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True)
st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 선수 카드 (팀 컬러 적용)
# -----------------------
st.subheader("🃏 선수 카드")
cols = st.columns(len(compare_df))
for i, (_, row) in enumerate(compare_df.iterrows()):
    card_color = row["팀컬러"]
    with cols[i]:
        st.markdown(
            f"""
            <div style="background-color:{card_color};padding:10px;border-radius:15px;text-align:center;">
            <img src="{row['이미지']}" width="180" style="border-radius:15px;">
            <h4 style="color:white">{row['이름']}</h4>
            <p style="color:white">클럽: {row['클럽']}</p>
            <p style="color:white">국적: {row['국적']}</p>
            </div>
            """, unsafe_allow_html=True
        )

# -----------------------
# 커리어/수상 상세 정보
# -----------------------
st.subheader("🏆 선수 커리어 & 수상 상세 정보")
for _, row in compare_df.iterrows():
    st.write(f"**{row['이름']}**")
    for item in row["커리어"]:
        st.markdown(f"- {item}")
