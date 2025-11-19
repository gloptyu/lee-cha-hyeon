import streamlit as st

st.set_page_config(page_title="축구선수 TOP10", layout="centered")

# 로컬 이미지 기준 선수 데이터
PLAYERS = {
    "리오넬 메시": {
        "club": "인터 마이애미",
        "nationality": "아르헨티나",
        "team_color": "#FF5DA2",
        "image": "images/messi.jpg",
        "career": "바르셀로나에서 전설적인 커리어를 쌓고 PSG, 인터 마이애미로 이어진 세계 최고의 플레이메이커 및 드리블러. 발롱도르 다수 수상.",
    },
    "크리스티아누 호날두": {
        "club": "알나스르",
        "nationality": "포르투갈",
        "team_color": "#FFD700",
        "image": "images/ronaldo.jpg",
        "career": "맨유-레알-유벤투스를 거쳐 알나스르에서 활약 중. 역사상 가장 많은 공식 경기 골 중 하나를 기록한 괴물 공격수.",
    },
    "킬리안 음바페": {
        "club": "레알 마드리드",
        "nationality": "프랑스",
        "team_color": "#FFFFFF",
        "image": "images/mbappe.jpg",
        "career": "PSG와 프랑스 대표팀의 핵심이자 현재 레알 마드리드 에이스. 폭발적인 스피드와 득점력으로 월드클래스 입증.",
    },
    "네이마르": {
        "club": "산투스",
        "nationality": "브라질",
        "team_color": "#FFFFFF",
        "image": "images/neymar.jpg",
        "career": "기술과 창의성의 아이콘. 산투스–바르셀로나–PSG를 거쳐 다시 산투스로 복귀한 브라질 대표 슈퍼스타.",
    },
    "케빈 더 브라위너": {
        "club": "나폴리",
        "nationality": "벨기에",
        "team_color": "#00AEEF",
        "image": "images/debruyne.jpg",
        "career": "세계 최고 패서 중 하나. 맨시티의 황금기 주역 후 나폴리로 이적. 패스 · 시야 · 조율 능력 최상급.",
    },
    "모하메드 살라": {
        "club": "리버풀",
        "nationality": "이집트",
        "team_color": "#C8102E",
        "image": "images/salah.jpg",
        "career": "프리미어리그 최정상급 득점자. 빠른 스피드와 왼발 마무리가 강점. 리버풀의 살아있는 전설.",
    },
    "로베르트 레반도프스키": {
        "club": "FC 바르셀로나",
        "nationality": "폴란드",
        "team_color": "#A50044",
        "image": "images/lewandowski.jpg",
        "career": "역사급 골게터. 도르트문트–바이에른–바르셀로나로 이어진 커리어. 포지셔닝과 결정력의 교과서.",
    },
    "버질 반 다이크": {
        "club": "리버풀",
        "nationality": "네덜란드",
        "team_color": "#C8102E",
        "image": "images/vandijk.jpg",
        "career": "현대 축구 최고의 센터백 중 한 명. 피지컬, 리더십, 수비 안정성을 모두 갖춘 리버풀의 핵심.",
    },
    "루카 모드리치": {
        "club": "레알 마드리드",
        "nationality": "크로아티아",
        "team_color": "#FFFFFF",
        "image": "images/modric.jpg",
        "career": "중원 지배자. 레알 마드리드 미드필더로 오랜 기간 정상급 활약. 발롱도르 수상 경험.",
    },
    "얼링 홀란": {
        "club": "맨체스터 시티",
        "nationality": "노르웨이",
        "team_color": "#6CABDD",
        "image": "images/haaland.jpg",
        "career": "괴물적인 피지컬과 득점력. 도르트문트에서 성장 후 맨시티에서 EPL 기록을 갈아치우는 중.",
    },
}

st.title("⚽ 내 입맛대로 뽑은 축구선수 TOP10")
st.caption("선수를 선택하면 사진, 커리어, 국적, 팀컬러 기반 배경이 나타납니다.")

player_choice = st.selectbox("선수 선택", list(PLAYERS.keys()))
player = PLAYERS[player_choice]

# 배경색 CSS 적용
bg = player["team_color"]
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(180deg, {bg}22 0%, {bg}55 100%);
}}
.player-box {{
    background: rgba(255,255,255,0.8);
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
}}
</style>
""", unsafe_allow_html=True)

# 선수 카드
st.markdown("<div class='player-box'>", unsafe_allow_html=True)
st.image(player["image"], width=350)
st.subheader(player_choice)
st.write(f"**클럽:** {player['club']}")
st.write(f"**국적:** {player['nationality']}")
st.write(f"**커리어 요약:** {player['career']}")
st.markdown("---")
st.write("✨ **간지 포인트:** 사진까지 박혀서 바로 팬페이지 뺨치는 간지! 이 앱 켜는 순간 너도 감독급.")
st.markdown("</div>", unsafe_allow_html=True)

# 전체 순위 출력
st.markdown("---")
st.write("### 전체 TOP10")
for i, n in enumerate(PLAYERS.keys(), start=1):
    st.write(f"{i}. {n} — {PLAYERS[n]['club']} ({PLAYERS[n]['nationality']})")
