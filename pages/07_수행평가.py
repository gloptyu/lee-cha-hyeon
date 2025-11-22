import streamlit as st
import plotly.graph_objects as go
import random

# -----------------------------
# 페이지 설정 + 배경 꾸미기
# -----------------------------
st.set_page_config(page_title="축구선수 TOP15", layout="wide")

# 배경 이미지 CSS
page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("https://images.unsplash.com/photo-1517927033932-b3d18e61fb3a");
    background-size: cover;
    background-position: center;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

.card {{
    backdrop-filter: blur(12px);
    background: rgba(0,0,0,0.55);
    padding: 15px;
    border-radius: 18px;
    transition: 0.25s;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.4);
}}
.card:hover {{
    transform: scale(1.03);
    box-shadow: 0px 0px 25px rgba(255,255,255,0.45);
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -----------------------------
# 선수 데이터베이스
# -----------------------------

PLAYERS = {
    "리오넬 메시": {
        "club": "인터 마이애미",
        "nationality": "아르헨티나",
        "team_color": "#FF5DA2",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Lionel_Messi_20180710.jpg",
        "career": """
● 바르셀로나 역대 최다 골  
● 발롱도르 8회  
● UCL 4회 우승  
● 월드컵 우승 (2022)  
● 라리가 10회 우승  
""",
        "stats": {"드리블": 95, "슈팅": 92, "패스": 91, "스피드": 88, "수비": 30},
        "position": "공격수",
        "season": {"골": 30, "도움": 20, "경기": 35}
    },

    "크리스티아누 호날두": {
        "club": "알나스르",
        "nationality": "포르투갈",
        "team_color": "#FFD700",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
        "career": """
● UEFA 챔스 최다 득점자  
● 발롱도르 5회  
● UCL 5회 우승  
● 유로 우승  
● 레알 마드리드 최다 득점자  
""",
        "stats": {"드리블": 89, "슈팅": 93, "패스": 82, "스피드": 87, "수비": 35},
        "position": "공격수",
        "season": {"골": 28, "도움": 15, "경기": 32}
    },

    "킬리안 음바페": {
        "club": "레알 마드리드",
        "nationality": "프랑스",
        "team_color": "#FFFFFF",
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Kylian_Mbapp%C3%A9_2022.jpg",
        "career": """
● 월드컵 우승(2018), 준우승(2022)  
● 역대 최연소 월드컵 결승 멀티골  
● PSG 통산 최다 득점  
● 프랑스 대표팀 핵심 공격수  
""",
        "stats": {"드리블": 90, "슈팅": 91, "패스": 80, "스피드": 95, "수비": 40},
        "position": "공격수",
        "season": {"골": 26, "도움": 18, "경기": 33}
    },

    "네이마르": {
        "club": "산투스",
        "nationality": "브라질",
        "team_color": "#FFD500",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/37/Neymar_2018.jpg",
        "career": """
● 브라질 국대 득점 1위  
● 바르셀로나 MSN 삼각편대  
● UCL 우승  
● 남미축구 최다 기대치의 스타  
""",
        "stats": {"드리블": 94, "슈팅": 86, "패스": 87, "스피드": 91, "수비": 30},
        "position": "공격수",
        "season": {"골": 22, "도움": 19, "경기": 30}
    },

    "케빈 더 브라위너": {
        "club": "맨시티",
        "nationality": "벨기에",
        "team_color": "#6CABDD",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Kevin_De_Bruyne_2018.jpg",
        "career": """
● 프리미어리그 최고 패서  
● EPL 도움왕 4회  
● UCL 우승  
● 맨시티 트레블 핵심  
""",
        "stats": {"드리블": 85, "슈팅": 88, "패스": 94, "스피드": 79, "수비": 50},
        "position": "미드필더",
        "season": {"골": 12, "도움": 21, "경기": 34}
    },

    "모하메드 살라": {
        "club": "리버풀",
        "nationality": "이집트",
        "team_color": "#C8102E",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Mohamed_Salah_2018.jpg",
        "career": """
● 프리미어리그 득점왕 3회  
● 리버풀 UCL 우승 주역  
● 아프리카 최고의 선수 3회  
""",
        "stats": {"드리블": 91, "슈팅": 90, "패스": 80, "스피드": 92, "수비": 35},
        "position": "공격수",
        "season": {"골": 27, "도움": 13, "경기": 33}
    },

    "레반도프스키": {
        "club": "바르셀로나",
        "nationality": "폴란드",
        "team_color": "#A50044",
        "image": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Robert_Lewandowski_2021.jpg",
        "career": """
● 분데스리가 최다 득점 기록  
● 바이에른 트레블 핵심  
● FIFA 올해의 선수  
""",
        "stats": {"드리블": 82, "슈팅": 95, "패스": 78, "스피드": 76, "수비": 40},
        "position": "공격수",
        "season": {"골": 34, "도움": 9, "경기": 36}
    },

    "반 다이크": {
        "club": "리버풀",
        "nationality": "네덜란드",
        "team_color": "#A31F34",
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/12/Virgil_van_Dijk_2019.jpg",
        "career": """
● 세계 최고의 센터백  
● 발롱도르 2위  
● 리버풀 UCL & EPL 우승 주역  
""",
        "stats": {"드리블": 60, "슈팅": 65, "패스": 82, "스피드": 70, "수비": 94},
        "position": "수비수",
        "season": {"골": 5, "도움": 3, "경기": 32}
    },
}

# -----------------------------
# UI 제목
# -----------------------------
st.title("⚽ 내 입맛대로 뽑은 축구선수 TOP15")

# -----------------------------
# 선수 선택
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    player1_name = st.selectbox("선수 1 선택", PLAYERS.keys())

with col2:
    player2_name = st.selectbox("선수 2 선택", PLAYERS.keys())

p1 = PLAYERS[player1_name]
p2 = PLAYERS[player2_name]

# -----------------------------
# 능력치 비교 레이더 차트
# -----------------------------
stats_cat = list(p1["stats"].keys())

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=list(p1["stats"].values()), theta=stats_cat, fill='toself', name=player1_name))
fig.add_trace(go.Scatterpolar(r=list(p2["stats"].values()), theta=stats_cat, fill='toself', name=player2_name))

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    template="plotly_dark"
)

st.subheader("📊 능력치 레이더 차트 비교")
st.plotly_chart(fig)

# -----------------------------
# 시즌 기록 막대 그래프
# -----------------------------
st.subheader("📌 시즌 기록 비교")
st.bar_chart({
    player1_name: p1["season"],
    player2_name: p2["season"]
})

# -----------------------------
# ✨ 선수 카드 (업그레이드 버전)
# -----------------------------
st.subheader("🃏 선수 카드")

colA, colB = st.columns(2)
for col, (name, data) in zip([colA, colB], [(player1_name, p1), (player2_name, p2)]):

    card_html = f"""
    <div class="card">
        <img src="{data['image']}" width="200" style="border-radius:10px;"><br>
        <h3 style="color:white;">{name}</h3>
        <p style="color:white;">클럽: {data['club']}</p>
        <p style="color:white;">국적: {data['nationality']}</p>
        <p style="color:white; font-size:17px;">{data['career']}</p>
    </div>
    """
    col.markdown(card_html, unsafe_allow_html=True)

# -----------------------------
# 랜덤 추천 선수
# -----------------------------
st.markdown("---")
if st.button("오늘의 추천 선수 🎯"):
    rp = random.choice(list(PLAYERS.keys()))
    pdata = PLAYERS[rp]
    st.subheader(f"🎯 오늘의 선택 : {rp}")
    st.image(pdata["image"], width=220)
    st.write(pdata["career"])

# -----------------------------
# 전체 리스트
# -----------------------------
st.markdown("---")
st.subheader("📌 전체 선수 목록")
for i, n in enumerate(PLAYERS.keys(), start=1):
    st.write(f"{i}. {n} - {PLAYERS[n]['club']} ({PLAYERS[n]['nationality']})")
