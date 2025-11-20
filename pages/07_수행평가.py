import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(page_title="축구 선수 TOP10 비교", layout="wide")

st.title("⚽ 축구 선수 TOP10 비교 & 추천 시스템 (커리어 포함)")

# -----------------------
# 1. 축구 선수 DB (커리어/수상 추가)
# -----------------------
data = {
    "이름": ["손흥민", "리오넬 메시", "크리스티아누 호날두", "킬리안 음바페", "네이마르",
             "케빈 더 브라위너", "모하메드 살라", "로베르트 레반도프스키", "버질 반 다이크", "이강인"],
    "클럽": ["토트넘", "인터 마이애미", "알나스르", "레알 마드리드", "산투스",
             "나폴리", "리버풀", "FC 바르셀로나", "리버풀", "마요르카"],
    "국적": ["대한민국", "아르헨티나", "포르투갈", "프랑스", "브라질",
             "벨기에", "이집트", "폴란드", "네덜란드", "대한민국"],
    "스피드": [95, 88, 87, 96, 91, 79, 92, 76, 70, 87],
    "드리블": [93, 95, 89, 90, 94, 85, 91, 82, 60, 88],
    "슈팅": [85, 92, 93, 91, 86, 88, 90, 95, 65, 80],
    "패스": [82, 91, 82, 80, 87, 94, 80, 78, 82, 90],
    "수비": [40, 30, 35, 40, 30, 50, 35, 40, 94, 45],
    "골": [22, 30, 28, 26, 22, 12, 27, 34, 5, 10],
    "도움": [12, 20, 15, 18, 19, 21, 13, 9, 3, 8],
    "경기": [34, 35, 32, 33, 30, 34, 33, 36, 32, 30],
    "커리어": [
        "토트넘 주전 공격수, 프리미어리그 골든부트 수상",
        "바르셀로나·PSG·인터 마이애미 활약, 발롱도르 7회 수상",
        "맨유·레알·유벤투스·알나스르, UEFA 챔피언스리그 우승 경험",
        "PSG·프랑스 대표팀 주전, 월드컵 우승",
        "산투스·바르셀로나·PSG, FIFA 컨페더레이션컵 우승",
        "맨체스터 시티 핵심, EPL 최다 도움 기록",
        "리버풀 핵심, 프리미어리그 득점왕",
        "도르트문트·바이에른·바르셀로나, FIFA 클럽 월드컵 우승",
        "리버풀 센터백, UEFA 챔피언스리그 우승",
        "발렌시아 유스 출신, 마요르카 주전"
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
# 2. 선수 선택 (축구 선수 전용)
# -----------------------
selected_players = st.sidebar.multiselect(
    "비교할 선수 선택 (축구 선수만)",
    df["이름"],
    default=[df["이름"][0], df["이름"][1]]
)

if len(selected_players) < 2:
    st.warning("선수를 최소 2명 이상 선택하세요!")
    st.stop()

compare_df = df[df["이름"].isin(selected_players)]

# -----------------------
# 3. 레이더 차트
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
# 4. 시즌 기록 막대 차트
# -----------------------
st.subheader("📊 시즌 기록 비교")
season_data = compare_df.set_index("이름")[["골", "도움", "경기"]].T
st.bar_chart(season_data)

# -----------------------
# 5. 선수 카드 + 커리어 표시
# -----------------------
st.subheader("🃏 선수 카드 (클럽·국적·커리어 포함)")
cols = st.columns(len(compare_df))
for i, (_, row) in enumerate(compare_df.iterrows()):
    with cols[i]:
        st.image(row["이미지"], width=200)
        st.subheader(row["이름"])
        st.write(f"클럽: {row['클럽']}")
        st.write(f"국적: {row['국적']}")
        st.write(f"🏆 커리어/수상: {row['커리어']}")

# -----------------------
# 6. AI 비교 분석
# -----------------------
st.subheader("🤖 AI 비교 분석")
compare_df["총합"] = compare_df[categories].sum(axis=1)
winner = compare_df.sort_values("총합", ascending=False).iloc[0]
st.success(f"🏅 예상 최강 선수: **{winner['이름']}** (총합 능력치: {winner['총합']})")

# -----------------------
# 7. 오늘의 추천 선수
# -----------------------
st.subheader("🎯 오늘의 추천 선수")
random_player = compare_df.sample(1).iloc[0]
st.info(f"추천 선수: **{random_player['이름']}**")
st.image(random_player["이미지"], width=200)
st.write(f"클럽: {random_player['클럽']}")
st.write(f"국적: {random_player['국적']}")
st.write(f"🏆 커리어/수상: {random_player['커리어']}")
