import streamlit as st
import plotly.graph_objects as go
import random
from functools import lru_cache

st.set_page_config(page_title="축구선수 TOP10", layout="wide")

# ------------------------------
# 다크모드 / 라이트모드 전환
# ------------------------------
mode = st.toggle("🌙 다크모드")
if mode:
    bg_color = "#111111"
    font_color = "white"
else:
    bg_color = "white"
    font_color = "black"

page_bg = f"""
<style>
body {{
    background: {bg_color};
    color: {font_color};
}}
.player-card {{
    padding: 15px;
    border-radius: 15px;
    transition: 0.3s;
    box-shadow: 0px 0px 5px #00000020;
}}
.player-card:hover {{
    transform: scale(1.03);
    box-shadow: 0px 0px 20px #00000050;
}}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----------------------------------------------------
# 데이터
# ----------------------------------------------------
PLAYERS = { ... (너가 준 데이터 그대로) ... }

# ----------------------------------------------------
# 사진 캐시(에러 방지)
# ----------------------------------------------------
@lru_cache
def load_image(url):
    return url

# ----------------------------------------------------
# 선수 검색 기능
# ----------------------------------------------------
search = st.text_input("🔎 선수 검색", "")

if search != "":
    filtered = {k:v for k,v in PLAYERS.items() if search in k}
else:
    filtered = PLAYERS

# ----------------------------------------------------
# 포지션 필터
# ----------------------------------------------------
positions = list(set([p["position"] for p in PLAYERS.values()]))
selected_position = st.selectbox("포지션 필터", ["전체"] + positions)

if selected_position != "전체":
    filtered = {k:v for k,v in filtered.items() if v["position"] == selected_position}

# ----------------------------------------------------
# 자동 랭킹 계산 (능력치 평균 기준)
# ----------------------------------------------------
rank_scores = {name: sum(info["stats"].values())/5 for name, info in PLAYERS.items()}
ranked = sorted(rank_scores.items(), key=lambda x: x[1], reverse=True)

st.markdown("## 🏆 능력치 기반 자동 랭킹")
for i, (name, score) in enumerate(ranked, 1):
    st.write(f"**{i}. {name}** — 점수: {round(score,1)}")

st.markdown("---")

# ----------------------------------------------------
# 선수 선택
# ----------------------------------------------------
col1, col2 = st.columns(2)
player1_choice = col1.selectbox("선수 1 선택", list(filtered.keys()))
player2_choice = col2.selectbox("선수 2 선택", list(filtered.keys()))

player1 = filtered[player1_choice]
player2 = filtered[player2_choice]

# ----------------------------------------------------
# 능력치 커스텀
# ----------------------------------------------------
st.subheader("🎛 능력치 커스텀 (원하면 수정 가능)")

colA, colB = st.columns(2)
with colA:
    p1_stats = {}
    for k,v in player1["stats"].items():
        p1_stats[k] = st.slider(f"{player1_choice} - {k}", 0, 100, v)
with colB:
    p2_stats = {}
    for k,v in player2["stats"].items():
        p2_stats[k] = st.slider(f"{player2_choice} - {k}", 0, 100, v)

# ----------------------------------------------------
# 레이더 차트
# ----------------------------------------------------
categories = list(player1["stats"].keys())
fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=list(p1_stats.values()), theta=categories, fill='toself', name=player1_choice))
fig.add_trace(go.Scatterpolar(r=list(p2_stats.values()), theta=categories, fill='toself', name=player2_choice))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=True)
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# 자동 비교 분석
# ----------------------------------------------------
st.subheader("🧠 AI 비교 분석")

p1_total = sum(p1_stats.values())
p2_total = sum(p2_stats.values())

if p1_total > p2_total:
    st.write(f"🔥 **{player1_choice}** 가 전체적으로 더 우세합니다! (총합 {p1_total} vs {p2_total})")
elif p2_total > p1_total:
    st.write(f"🔥 **{player2_choice}** 가 전체적으로 더 우세합니다! (총합 {p2_total} vs {p1_total})")
else:
    st.write("⚖️ 두 선수는 능력치 평균이 거의 동일합니다!")

# ----------------------------------------------------
# 시즌 기록 라인 차트
# ----------------------------------------------------
st.subheader("📊 시즌 기록 비교")

season_fig = go.Figure()
season_fig.add_trace(go.Scatter(x=list(player1["season"].keys()), y=list(player1["season"].values()),
                                mode='lines+markers', name=player1_choice))
season_fig.add_trace(go.Scatter(x=list(player2["season"].keys()), y=list(player2["season"].values()),
                                mode='lines+markers', name=player2_choice))
st.plotly_chart(season_fig, use_container_width=True)

# ----------------------------------------------------
# 선수 카드
# ----------------------------------------------------
card1, card2 = st.columns(2)

with card1:
    st.markdown(f"<div class='player-card' style='background:{player1['team_color']}20;'>", unsafe_allow_html=True)
    st.image(load_image(player1["image"]), width=250)
    st.subheader(player1_choice)
    with st.expander("자세히 보기"):
        st.write(f"**클럽:** {player1['club']}")
        st.write(f"**국적:** {player1['nationality']}")
        st.write(f"**커리어:** {player1['career']}")
    st.markdown("</div>", unsafe_allow_html=True)

with card2:
    st.markdown(f"<div class='player-card' style='background:{player2['team_color']}20;'>", unsafe_allow_html=True)
    st.image(load_image(player2["image"]), width=250)
    st.subheader(player2_choice)
    with st.expander("자세히 보기"):
        st.write(f"**클럽:** {player2['club']}")
        st.write(f"**국적:** {player2['nationality']}")
        st.write(f"**커리어:** {player2['career']}")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 추천 기능
# ----------------------------------------------------
st.markdown("---")
if st.button("🎯 오늘의 선수 추천"):
    rname = random.choice(list(filtered.keys()))
    r = filtered[rname]
    st.write(f"### ⭐ 오늘의 추천: {rname}")
    st.image(load_image(r["image"]), width=300)
    st.write(f"클럽: {r['club']}")
    st.write(f"국적: {r['nationality']}")
    st.write(r["career"])
