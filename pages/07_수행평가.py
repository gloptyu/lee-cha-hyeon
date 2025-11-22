import streamlit as st

st.set_page_config(
    page_title="TOP 15 축구선수",
    page_icon="⚽",
    layout="wide"
)

# ------------------------------
# 배경 (그라데이션 + 블러 카드)
# ------------------------------
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0a0a 0%, #1b1b1b 50%, #303030 100%);
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.card-box {
    background: rgba(255, 255, 255, 0.07);
    padding: 18px;
    border-radius: 16px;
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.15);
}
.text-shadow {
    text-shadow: 0 0 6px rgba(0,0,0,0.9);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)


# ------------------------------
# 선수 데이터 (TOP 15)
# ------------------------------
players = {
    "리오넬 메시": {
        "team_color": "#74acdf",
        "nation": "아르헨티나",
        "img": "https://i.imgur.com/Q0oZqzU.jpeg",
        "career": [
            "발롱도르 8회",
            "월드컵 우승 (2022)",
            "챔피언스리그 4회 우승",
            "바르셀로나 전설(득점·도움 기록 보유)"
        ]
    },
    "크리스티아누 호날두": {
        "team_color": "#d91d1d",
        "nation": "포르투갈",
        "img": "https://i.imgur.com/H0Z7m1Q.jpeg",
        "career": [
            "발롱도르 5회",
            "챔피언스리그 5회 우승",
            "유로 우승",
            "A매치 역대 최다 득점"
        ]
    },
    "네이마르": {
        "team_color": "#fedd00",
        "nation": "브라질",
        "img": "https://i.imgur.com/Y1k2F3A.jpeg",
        "career": [
            "브라질 A매치 최다 득점",
            "UCL 우승 (바르셀로나)",
            "리그 우승 다수"
        ]
    },
    "킬리안 음바페": {
        "team_color": "#001f70",
        "nation": "프랑스",
        "img": "https://i.imgur.com/2yCPz1F.jpeg",
        "career": [
            "월드컵 우승 (2018)",
            "월드컵 결승전 해트트릭 (2022)",
            "리그 1 득점왕 다수"
        ]
    },
    "손흥민": {
        "team_color": "#001b50",
        "nation": "대한민국",
        "img": "https://i.imgur.com/OD8Xc1d.jpeg",
        "career": [
            "EPL 득점왕 (아시아 최초)",
            "챔피언스리그 준우승",
            "아시아 최고 선수"
        ]
    },
    "로베르트 레반도프스키": {
        "team_color": "#dc052d",
        "nation": "폴란드",
        "img": "https://i.imgur.com/vN8W8vj.jpeg",
        "career": [
            "분데스리가 득점왕 다수",
            "UCL 우승 (바이에른)",
            "9분 5골 기록"
        ]
    },
    "케빈 더 브라위너": {
        "team_color": "#6cabdd",
        "nation": "벨기에",
        "img": "https://i.imgur.com/dJtVJYT.jpeg",
        "career": [
            "맨시티 트레블 주역",
            "프리미어리그 최정상 MF",
            "엄청난 패스 시야"
        ]
    },
    "비니시우스 주니오르": {
        "team_color": "#ffffff",
        "nation": "브라질",
        "img": "https://i.imgur.com/qbcgrq0.jpeg",
        "career": [
            "UCL 우승 결승 결승골",
            "라리가 우승 다수",
            "차세대 월드클래스 윙어"
        ]
    },
    "해리 케인": {
        "team_color": "#001b50",
        "nation": "잉글랜드",
        "img": "https://i.imgur.com/wZtbgIc.jpeg",
        "career": [
            "EPL 득점왕 3회",
            "잉글랜드 대표팀 최다 득점",
            "유럽 최고 스트라이커"
        ]
    },
    "모하메드 살라": {
        "team_color": "#d00000",
        "nation": "이집트",
        "img": "https://i.imgur.com/3T7q8B8.jpeg",
        "career": [
            "UCL 우승",
            "프리미어리그 우승",
            "글로벌 인기 No.1 아프리카 선수"
        ]
    },
    "루카 모드리치": {
        "team_color": "#ffffff",
        "nation": "크로아티아",
        "img": "https://i.imgur.com/b1J1VAd.jpeg",
        "career": [
            "발롱도르 수상 (2018)",
            "UCL 다수 우승",
            "월드컵 준우승"
        ]
    },
    "엘링 홀란드": {
        "team_color": "#6cabdd",
        "nation": "노르웨이",
        "img": "https://i.imgur.com/5rB2RP3.jpeg",
        "career": [
            "EPL 득점왕",
            "챔피언스리그 득점 1위",
            "괴물 피지컬·골결정력"
        ]
    },
    "카림 벤제마": {
        "team_color": "#ffffff",
        "nation": "프랑스",
        "img": "https://i.imgur.com/ooP1HUV.jpeg",
        "career": [
            "발롱도르",
            "UCL 다수 우승",
            "라리가 득점왕"
        ]
    },
    "주드 벨링엄": {
        "team_color": "#ffffff",
        "nation": "잉글랜드",
        "img": "https://i.imgur.com/ZqkU5Ui.jpeg",
        "career": [
            "레알 마드리드 핵심 MF",
            "라리가 MVP급 활약",
            "차세대 발롱도르 후보"
        ]
    },
    "안토안 그리즈만": {
        "team_color": "#a50044",
        "nation": "프랑스",
        "img": "https://i.imgur.com/r2L3Jxl.jpeg",
        "career": [
            "월드컵 우승(2018)",
            "유로 준우승",
            "AT마드리드 에이스"
        ]
    }
}

player_names = list(players.keys())


# ---------------------------------
# 선수 선택
# ---------------------------------
st.title("⚽ TOP 15 축구선수 카드")

selected = st.selectbox("선수를 선택하세요", player_names)

p = players[selected]

# 텍스트 컬러 자동 계산
def auto_text_color(bg):
    bg = bg.lstrip("#")
    r,g,b = int(bg[0:2],16), int(bg[2:4],16), int(bg[4:6],16)
    return "#000000" if (r+g+b) > 500 else "#FFFFFF"

text_color = auto_text_color(p["team_color"])


# ---------------------------------
# 카드 UI
# ---------------------------------
st.markdown(f"""
<div class="card-box" style="border-left: 8px solid {p['team_color']}">
    <h2 style="color:{text_color}" class="text-shadow">{selected}</h2>
    <img src="{p['img']}" width="260" style="border-radius:14px;margin-bottom:10px;" />
    <p style="color:{text_color};font-size:18px;" class="text-shadow"><b>국적:</b> {p['nation']}</p>
    <p style="color:{text_color};font-size:18px;" class="text-shadow"><b>팀 컬러:</b> {p['team_color']}</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------
# 커리어 박스
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
