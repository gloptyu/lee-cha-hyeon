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

.white-box {{
    background: rgba(255,255,255,0.92);
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
}}

</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)


# -----------------------------
# 선수 데이터베이스 (TOP15)
# -----------------------------
PLAYERS = {
    "리오넬 메시": {
        "club": "인터 마이애미",
        "nationality": "아르헨티나",
        "team_color": "#FF5DA2",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Lionel_Messi_20180710.jpg",
        "career": """● 바르셀로나 역대 최다 골  
● 발롱도르 8회  
● 월드컵 우승  
● 라리가 10회 우승""",
        "stats": {"드리블": 95, "슈팅": 92, "패스": 91, "스피드": 88, "수비": 30},
        "position": "공격수",
        "season": {"골": 30, "도움": 20, "경기": 35}
    },

    "크리스티아누 호날두": {
        "club": "알나스르",
        "nationality": "포르투갈",
        "team_color": "#FFD700",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
        "career": """● UEFA 챔스 최다 득점  
● 발롱도르 5회  
● UCL 5회 우승  
● 레알 최다 득점자""",
        "stats": {"드리블": 89, "슈팅": 93, "패스": 82, "스피드": 87, "수비": 35},
        "position": "공격수",
        "season": {"골": 28, "도움": 15, "경기": 32}
    },

    "킬리안 음바페": {
        "club": "레알 마드리드",
        "nationality": "프랑스",
        "team_color": "#FFFFFF",
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Kylian_Mbapp%C3%A9_2022.jpg",
        "career": """● 월드컵 우승  
● 프랑스 국대 핵심  
● PSG 최다 득점자""",
        "stats": {"드리블": 90, "슈팅": 91, "패스": 80, "스피드": 95, "수비": 40},
        "position": "공격수",
        "season": {"골": 26, "도움": 18, "경기": 33}
    },

    "네이마르": {
        "club": "산투스",
        "nationality": "브라질",
        "team_color": "#FFD500",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/37/Neymar_2018.jpg",
        "career": """● 브라질 국대 득점 1위  
● 바르셀로나 MSN  
● 남미 최고 스타""",
        "stats": {"드리블": 94, "슈팅": 86, "패스": 87, "스피드": 91, "수비": 30},
        "position": "공격수",
        "season": {"골": 22, "도움": 19, "경기": 30}
    },

    "케빈 더 브라위너": {
        "club": "맨시티",
        "nationality": "벨기에",
        "team_color": "#6CABDD",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Kevin_De_Bruyne_2018.jpg",
        "career": """● EPL 도움왕 4회  
● 프리미어리그 최고 패서  
● 맨시티 핵심""",
        "stats": {"드리블": 85, "슈팅": 88, "패스": 94, "스피드": 79, "수비": 50},
        "position": "미드필더",
        "season": {"골": 12, "도움": 21, "경기": 34}
    },

    "모하메드 살라": {
        "club": "리버풀",
        "nationality": "이집트",
        "team_color": "#C8102E",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Mohamed_Salah_2018.jpg",
        "career": """● EPL 득점왕 3회  
● UCL 우승  
● 리버풀 레전드""",
        "stats": {"드리블": 91, "슈팅": 90, "패스": 80, "스피드": 92, "수비": 35},
        "position": "공격수",
        "season": {"골": 27, "도움": 13, "경기": 33}
    },

    "레반도프스키": {
        "club": "바르셀로나",
        "nationality": "폴란드",
        "team_color": "#A50044",
        "image": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Robert_Lewandowski_2021.jpg",
        "career": """● 분데스리가 최다 득점  
● FIFA 올해의 선수  
● 세계 최정상 스트라이커""",
        "stats": {"드리블": 82, "슈팅": 95, "패스": 78, "스피드": 76, "수비": 40},
        "position": "공격수",
        "season": {"골": 34, "도움": 9, "경기": 36}
    },

    "반 다이크": {
        "club": "리버풀",
        "nationality": "네덜란드",
        "team_color": "#A31F34",
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/12/Virgil_van_Dijk_2019.jpg",
        "career": """● 세계 최고 센터백  
● 발롱도르 2위  
● 리버풀 우승 주역""",
        "stats": {"드리블": 60, "슈팅": 65, "패스": 82, "스피드": 70, "수비": 94},
        "position": "수비수",
        "season": {"골": 5, "도움": 3, "경기": 32}
    },

    # ----------------------------
    # 🔥 여기부터 추가된 선수들
    # ----------------------------
    "손흥민": {
        "club": "토트넘",
        "nationality": "대한민국",
        "team_color": "#001C58",
        "image": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Son_Heung-min_2018.jpg",
        "career": """● 아시아 최초 EPL 득점왕  
● 대한민국 주장  
● 토트넘 핵심 스타""",
        "stats": {"드리블": 90, "슈팅": 92, "패스": 83, "스피드": 94, "수비": 45},
        "position": "공격수",
        "season": {"골": 24, "도움": 11, "경기": 34}
    },

    "카림 벤제마": {
        "club": "알 이티하드",
        "nationality": "프랑스",
        "team_color": "#F6C700",
        "image": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Karim_Benzema_2018.jpg",
        "career": """● 발롱도르 수상  
● 레알 마드리드 UCL 5회  
● 라리가 최정상 공격수""",
        "stats": {"드리블": 87, "슈팅": 92, "패스": 85, "스피드": 78, "수비": 40},
        "position": "공격수",
        "season": {"골": 31, "도움": 12, "경기": 35}
    },

    "안투안 그리즈만": {
        "club": "AT 마드리드",
        "nationality": "프랑스",
        "team_color": "#D50C2D",
        "image": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Antoine_Griezmann_2018.jpg",
        "career": """● 월드컵 우승  
● 스페인 국대 핵심  
● 아틀레티코 레전드""",
        "stats": {"드리블": 88, "슈팅": 89, "패스": 90, "스피드": 82, "수비": 60},
        "position": "공격수",
        "season": {"골": 21, "도움": 17, "경기": 34}
    },

    "루카 모드리치": {
        "club": "레알 마드리드",
        "nationality": "크로아티아",
        "team_color": "#FFFFFF",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Luka_Modric_2018.jpg",
        "career": """● 발롱도르 수상  
● 레알 마드리드 미드필더  
● 월드컵 준우승""",
        "stats": {"드리블": 87, "슈팅": 78, "패스": 92, "스피드": 70, "수비": 65},
        "position": "미드필더",
        "season": {"골": 7, "도움": 12, "경기": 34}
    },

    "티보 쿠르투아": {
        "club": "레알 마드리드",
        "nationality": "벨기에",
        "team_color": "#FFFFFF",
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/12/Thibaut_Courtois_2018_%28cropped%29.jpg",
        "career": """● 세계 최고 GK  
● UCL 우승  
● 라리가 우승 다수""",
        "stats": {"드리블": 10, "슈팅": 15, "패스": 40, "스피드": 50, "수비": 98},
        "position": "골키퍼",
        "season": {"선방": 102, "클린시트": 20, "경기": 38}
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
    p1_name = st.selectbox("선수 1 선택", PLAYERS.keys())
with col2:
    p2_name = st.selectbox("선수 2 선택", PLAYERS.keys())

p1 = PLAYERS[p1_name]
p2 = PLAYERS[p2_name]

# -----------------------------
# 능력치 비교 레이더 차트
# -----------------------------
stats_cat = list(p1["stats"].keys())

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=list(p1["stats"].values()), theta=stats_cat, fill='toself', name=p1_name))
fig.add_trace(go.Scatterpolar(r=list(p2["stats"].values()), theta=stats_cat, fill='toself', name=p2_name))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, template="plotly_dark")

st.subheader("📊 능력치 레이더 차트 비교")
st.plotly_chart(fig)

# -----------------------------
# 시즌 기록 그래프
# -----------------------------
st.subheader("📌 시즌 기록 비교")
st.bar_chart({p1_name: p1["season"], p2_name: p2["season"]})

# -----------------------------
# 선수 카드
# -----------------------------
st.subheader("🃏 선수 카드")

colA, colB = st.columns(2)
for col, (name, data) in zip([colA, colB], [(p1_name, p1), (p2_name, p2)]):
    card_html = f"""
    <div class="card">
        <img src="{data['image']}" width="220" style="border-radius:10px;"><br>
        <h3 style="color:white;">{name}</h3>
        <p style="color:white;">클럽: {data['club']}</p>
        <p style="color:white;">국적: {data['nationality']}</p>
        <p style="color:white; font-size:17px;">{data['career']}</p>
    </div>
    """
    col.markdown(card_html, unsafe_allow_html=True)

# -----------------------------
# 랜덤 추천
# -----------------------------
st.markdown("---")
if st.button("오늘의 추천 선수 🎯"):
    rp = random.choice(list(PLAYERS.keys()))
    pdata = PLAYERS[rp]

    st.markdown(
        f"""
        <div class="white-box">
            <h3>🎯 오늘의 추천 선수 : {rp}</h3>
            <img src="{pdata['image']}" width="220" style="border-radius:10px;">
            <p><b>클럽:</b> {pdata['club']}</p>
            <p><b>국적:</b> {pdata['nationality']}</p>
            <p><b>수상/커리어:</b><br>{pdata['career']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# 전체 선수 목록
# -----------------------------
st.markdown("---")
st.subheader("📌 전체 선수 목록")

st.markdown("<div class='white-box'>", unsafe_allow_html=True)
for i, n in enumerate(PLAYERS.keys(), start=1):
    st.write(f"{i}. {n} — {PLAYERS[n]['club']} ({PLAYERS[n]['nationality']})")
st.markdown("</div>", unsafe_allow_html=True)
