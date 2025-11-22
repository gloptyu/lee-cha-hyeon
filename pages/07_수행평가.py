import streamlit as st

st.set_page_config(
    page_title="축구선수 TOP10",
    page_icon="⚽",
    layout="wide"
)

# ------------------------------
# 전체 배경 꾸미기 (그라데이션 + 블러)
# ------------------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0a0a 0%, #1b1b1b 50%, #303030 100%);
    background-size: cover;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.card-box {
    background: rgba(255, 255, 255, 0.08);
    padding: 18px;
    border-radius: 18px;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.15);
}
.text-shadow {
    text-shadow: 0px 0px 6px rgba(0,0,0,0.9);
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ------------------------------
# 선수 데이터
# ------------------------------
players = {
    "리오넬 메시": {
        "team_color": "#74acdf",
        "nation": "아르헨티나",
        "img": "https://i.imgur.com/2yaf2xB.jpg",
        "career": [
            "발롱도르 8회",
            "FC 바르셀로나 레전드 (득점, 도움 기록 다수 보유)",
            "아르헨티나 대표팀 주장",
            "월드컵 우승 (2022)",
            "챔피언스리그 4회 우승"
        ]
    },
    "크리스티아누 호날두": {
        "team_color": "#d91d1d",
        "nation": "포르투갈",
        "img": "https://i.imgur.com/4ZQZ4wN.jpeg",
        "career": [
            "발롱도르 5회",
            "UEFA 챔피언스리그 5회 우승",
            "대표팀 유로 우승",
            "역대 A매치 최다 득점 1위"
        ]
    },
    "네이마르": {
        "team_color": "#fedd00",
        "nation": "브라질",
        "img": "https://i.imgur.com/ntmE8Zq.jpeg",
        "career": [
            "브라질 A매치 최다 득점자(펠레 넘어섬)",
            "UCL 우승 (바르셀로나)",
            "리그 1 / 라리가 우승 다수"
        ]
    },
    "킬리안 음바페": {
        "team_color": "#001f70",
        "nation": "프랑스",
        "img": "https://i.imgur.com/WmB8eni.jpeg",
        "career": [
            "월드컵 우승 (2018)",
            "월드컵 준우승 (2022) 결승전 해트트릭",
            "리그 1 득점왕 다수",
            "10대부터 세계 최정상급으로 평가"
        ]
    },
    "케빈 더 브라위너": {
        "team_color": "#6cabdd",
        "nation": "벨기에",
        "img": "https://i.imgur.com/5AUhMPx.jpeg",
        "career": [
            "프리미어리그 assist 머신",
            "맨시티 트레블 주역(2023)",
            "유럽 최고 미드필더 중 한 명"
        ]
    },
    "레반도프스키": {
        "team_color": "#dc052d",
        "nation": "폴란드",
        "img": "https://i.imgur.com/GoIRUgS.jpeg",
        "career": [
            "분데스리가 득점왕 다수",
            "UCL 우승 (바이에른)",
            "한 경기 5골(9분) 세계 기록"
        ]
    },
    "손흥민": {
        "team_color": "#001b50",
        "nation": "대한민국",
        "img": "https://i.imgur.com/qIgZuTD.jpeg",
        "career": [
            "아시아 최초 EPL 득점왕",
            "챔스 준우승",
            "월드컵 3회 참가",
            "한국 축구 역사상 최고 선수 중 한 명"
        ]
    },
    "비니시우스 주니오르": {
        "team_color": "#ffffff",
        "nation": "브라질",
        "img": "https://i.imgur.com/CNnjHbG.jpeg",
        "career": [
            "UCL 우승 골",
            "라리가 우승 다수",
            "차세대 세계 최고 윙어"
        ]
    },
    "해리 케인": {
        "team_color": "#001b50",
        "nation": "잉글랜드",
        "img": "https://i.imgur.com/LEkLjV3.jpeg",
        "career": [
            "EPL 득점왕 3회",
            "잉글랜드 대표팀 최다 득점",
            "유럽에서도 최고 수준의 스트라이커"
        ]
    }
}

player_names = list(players.keys())

# ---------------------------------
# 선수 선택
# ---------------------------------
st.title("⚽ 축구선수 TOP10 카드")

selected = st.selectbox("선수를 선택하세요", player_names)

p = players[selected]

# 텍스트 컬러 자동 결정 (배경 대비)
def auto_text_color(bg):
    bg = bg.lstrip("#")
    r, g, b = int(bg[0:2],16), int(bg[2:4],16), int(bg[4:6],16)
    return "#000000" if (r+g+b) > 500 else "#FFFFFF"

text_color = auto_text_color(p["team_color"])

# ---------------------------------
# 선수 카드 UI
# ---------------------------------
st.markdown(f"""
<div class="card-box" style="border-left: 8px solid {p['team_color']};">
    <h2 style="color:{text_color}" class="text-shadow">{selected}</h2>
    <img src="{p['img']}" width="260" style="border-radius:14px; margin-bottom:10px;" />
    <p style="color:{text_color}; font-size:18px;" class="text-shadow"><b>국적:</b> {p['nation']}</p>
    <p style="color:{text_color}; font-size:18px;" class="text-shadow"><b>팀 컬러:</b> {p['team_color']}</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------
# 상세 커리어 박스
# ---------------------------------
st.markdown("### 🏆 커리어 상세")

career_html = "<ul>"
for c in p["career"]:
    career_html += f"<li class='text-shadow' style='color:white; font-size:18px;'>{c}</li>"
career_html += "</ul>"

st.markdown(f"""
<div class="card-box">
    {career_html}
</div>
""", unsafe_allow_html=True)
