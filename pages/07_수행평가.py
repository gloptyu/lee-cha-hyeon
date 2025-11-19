import streamlit as st

st.set_page_config(page_title="Top10 Footballers — Stylish Picks", layout="centered")

PLAYERS = {
    "Lionel Messi": {
        "club": "Inter Miami",
        "nationality": "Argentina",
        "team_color": "#FF5DA2",  # Inter Miami pink
        "career": (
            "World-class forward — multiple Ballon d'Ors, long spells at Barcelona (legend), Paris Saint-Germain, and Inter Miami. "
            "Known for dribbling, vision, and free-kicks."
        ),
    },
    "Cristiano Ronaldo": {
        "club": "Al Nassr",
        "nationality": "Portugal",
        "team_color": "#FFD700",  # Al Nassr yellow (primary)
        "career": (
            "Elite goal-scorer across Sporting CP, Manchester United, Real Madrid, Juventus, and Al Nassr. "
            "Explosive, great in the air, and a clutch finisher."
        ),
    },
    "Kylian Mbappé": {
        "club": "Real Madrid",
        "nationality": "France",
        "team_color": "#FFFFFF",  # Real Madrid white
        "career": (
            "Pacy forward who starred for Monaco and PSG before moving to Real Madrid. "
            "Exceptional speed, finishing, and big-game impact."
        ),
    },
    "Neymar Jr.": {
        "club": "Santos",
        "nationality": "Brazil",
        "team_color": "#FFFFFF",  # Santos white
        "career": (
            "Flair-filled Brazilian forward — rose to fame at Santos, starred at Barcelona and PSG, and returned to Santos. "
            "Creative dribbler and playmaker."
        ),
    },
    "Kevin De Bruyne": {
        "club": "Napoli",
        "nationality": "Belgium",
        "team_color": "#00AEEF",  # Napoli sky blue
        "career": (
            "World-class midfielder, known for vision and passing; long success at Manchester City before joining Napoli. "
            "Master of through-balls and set-piece deliveries."
        ),
    },
    "Mohamed Salah": {
        "club": "Liverpool",
        "nationality": "Egypt",
        "team_color": "#C8102E",  # Liverpool red
        "career": (
            "Prolific winger/forward at Liverpool with excellent goal return. "
            "Rapid, clinical and a constant threat on the right flank."
        ),
    },
    "Robert Lewandowski": {
        "club": "FC Barcelona",
        "nationality": "Poland",
        "team_color": "#A50044",  # Barcelona garnet (primary)
        "career": (
            "Clinical centre-forward — Bayern Munich icon, later Barcelona. "
            "Reliable finishing, movement and physical presence in the box."
        ),
    },
    "Virgil van Dijk": {
        "club": "Liverpool",
        "nationality": "Netherlands",
        "team_color": "#C8102E",  # Liverpool red
        "career": (
            "Dominant centre-back; leadership and aerial strength. Key figure in Liverpool's recent successes."
        ),
    },
    "Luka Modrić": {
        "club": "Real Madrid",
        "nationality": "Croatia",
        "team_color": "#FFFFFF",  # Real Madrid white
        "career": (
            "Elegant midfield maestro known for control, passing and game management. Long-serving Real Madrid playmaker."
        ),
    },
    "Erling Haaland": {
        "club": "Manchester City",
        "nationality": "Norway",
        "team_color": "#6CABDD",  # Man City sky blue
        "career": (
            "Phenomenal goalscoring striker — rapid rise at Salzburg and Dortmund, then Manchester City. "
            "Powerful, clinical and lethal in the box."
        ),
    },
}

st.title("⚽ Top 10 Footballers — 내 입맛대로 뽑은 순위")
st.caption("선수 선택하면 해당 선수의 커리어·국적·팀컬러(배경) 보여줍니다.")

player_choice = st.selectbox("선수 고르기", list(PLAYERS.keys()))
player = PLAYERS[player_choice]

# Apply background color to the whole page using CSS
bg_color = player["team_color"]
page_css = f'''
<style>
    .stApp {{
        background: linear-gradient(180deg, {bg_color}10 0%, {bg_color}20 100%);
        color: #111;
    }}
    .player-card {{
        background: rgba(255,255,255,0.85);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }}
    .badge {{
        display:inline-block;
        padding:6px 10px;
        border-radius:999px;
        font-weight:600;
        margin-top:6px;
    }}
</style>
'''
st.markdown(page_css, unsafe_allow_html=True)

# Player card
with st.container():
    st.markdown(f"<div class='player-card'>", unsafe_allow_html=True)
    st.markdown(f"### {player_choice}")
    st.markdown(f"**클럽(팀컬러):** {player['club']} — <span class='badge' style='background:{player['team_color']};color:#fff'>{player['team_color']}</span>")
    st.markdown(f"**국적:** {player['nationality']}")
    st.markdown(f"**커리어 요약:** {player['career']}")

    # Small playful line about "간지"
    st.markdown("---")
    st.markdown("**간지 포인트:** 이 선수 셔츠에 네가 이 앱을 쓰면 간지 폭발! ✨\n\n" 
                "(참고: 여기 '너'는 사용자, '나'는 이 앱의 추천 가이드일 뿐이에요 😎)")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer with ordering
st.markdown("---")
st.write("**전체 Top10 (내 입맛대로)**")
for i, name in enumerate(PLAYERS.keys(), start=1):
    st.write(f"{i}. {name} — {PLAYERS[name]['club']} ({PLAYERS[name]['nationality']})")

st.sidebar.title("About")
st.sidebar.info("이 작은 앱은 예시용입니다. 팀컬러는 대표 색상(주로 홈 유니폼 컬러)을 사용했습니다.")

# Small export button to copy player info
if st.button("이 선수 정보 복사하기 (클립보드)"):
    info_text = f"{player_choice} | {player['club']} | {player['nationality']} | {player['career']}"
    st.write("복사된 텍스트:\n", info_text)
    # 실제 클립보드 복사는 브라우저 사이드 스크립트가 필요해서 여기서는 표시만 합니다.
