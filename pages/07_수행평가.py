import streamlit as st
import plotly.graph_objects as go
import random

st.set_page_config(page_title="축구선수 TOP10", layout="wide")

# 선수 데이터 (포지션 + 시즌 기록 포함)
PLAYERS = {
    "리오넬 메시": {"club": "인터 마이애미", "nationality": "아르헨티나", "team_color": "#FF5DA2",
                    "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Lionel_Messi_20180710.jpg",
                    "career": "바르셀로나에서 전설적인 커리어를 쌓고 PSG, 인터 마이애미로 이어진 세계 최고의 플레이메이커 및 드리블러. 발롱도르 다수 수상.",
                    "stats": {"드리블": 95, "슈팅": 92, "패스": 91, "스피드": 88, "수비": 30},
                    "position": "공격수", "season": {"골": 30, "도움": 20, "경기": 35}},
    "크리스티아누 호날두": {"club": "알나스르", "nationality": "포르투갈", "team_color": "#FFD700",
                    "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
                    "career": "맨유-레알-유벤투스를 거쳐 알나스르에서 활약 중. 역사상 가장 많은 공식 경기 골 중 하나를 기록한 괴물 공격수.",
                    "stats": {"드리블": 89, "슈팅": 93, "패스": 82, "스피드": 87, "수비": 35},
                    "position": "공격수", "season": {"골": 28, "도움": 15, "경기": 32}},
    "킬리안 음바페": {"club": "레알 마드리드", "nationality": "프랑스", "team_color": "#FFFFFF",
                    "image": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Kylian_Mbapp%C3%A9_2022.jpg",
                    "career": "PSG와 프랑스 대표팀의 핵심이자 현재 레알 마드리드 에이스. 폭발적인 스피드와 득점력으로 월드클래스 입증.",
                    "stats": {"드리블": 90, "슈팅": 91, "패스": 80, "스피드": 95, "수비": 40},
                    "position": "공격수", "season": {"골": 26, "도움": 18, "경기": 33}},
    # ... 나머지 선수 동일 구조
}

st.title("⚽ 내 입맛대로 뽑은 축구선수 TOP10")

# 포지션 필터
positions = list(set([p["position"] for p in PLAYERS.values()]))
selected_position = st.selectbox("포지션 필터", ["전체"] + positions)

if selected_position != "전체":
    filtered_players = {k:v for k,v in PLAYERS.items() if v["position"] == selected_position}
else:
    filtered_players = PLAYERS

# 선수 선택과 비교
col1, col2 = st.columns(2)
with col1:
    player1_choice = st.selectbox("선수 1 선택", list(filtered_players.keys()))
with col2:
    player2_choice = st.selectbox("선수 2 선택", list(filtered_players.keys()))

player1 = filtered_players[player1_choice]
player2 = filtered_players[player2_choice]

# 능력치 레이더 차트
categories = list(player1["stats"].keys())
fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=list(player1["stats"].values()), theta=categories, fill='toself', name=player1_choice))
fig.add_trace(go.Scatterpolar(r=list(player2["stats"].values()), theta=categories, fill='toself', name=player2_choice))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=True)
st.subheader(f"능력치 비교: {player1_choice} vs {player2_choice}")
st.plotly_chart(fig, use_container_width=True)

# 시즌 기록 비교 막대 차트
st.subheader("시즌 기록 비교")
st.bar_chart({player1_choice: player1["season"], player2_choice: player2["season"]})

# 선수 카드
col1, col2 = st.columns(2)
with col1:
    st.image(player1["image"], width=250)
    st.subheader(player1_choice)
    st.write(f"**클럽:** {player1['club']}")
    st.write(f"**국적:** {player1['nationality']}")
    st.write(f"**커리어:** {player1['career']}")
with col2:
    st.image(player2["image"], width=250)
    st.subheader(player2_choice)
    st.write(f"**클럽:** {player2['club']}")
    st.write(f"**국적:** {player2['nationality']}")
    st.write(f"**커리어:** {player2['career']}")

# 랜덤 추천 버튼
st.markdown("---")
if st.button("오늘의 선수 추천"):
    random_player_name = random.choice(list(filtered_players.keys()))
    random_player = filtered_players[random_player_name]
    st.write(f"🎯 오늘 추천 선수: {random_player_name}")
    st.image(random_player["image"], width=250)
    st.write(f"**클럽:** {random_player['club']}")
    st.write(f"**국적:** {random_player['nationality']}")
    st.write(f"**커리어:** {random_player['career']}")

# 전체 TOP10 목록
st.markdown("---")
st.write("### 전체 TOP10")
for i, n in enumerate(PLAYERS.keys(), start=1):
    st.write(f"{i}. {n} — {PLAYERS[n]['club']} ({PLAYERS[n]['nationality']})")
