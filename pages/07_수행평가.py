import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="스포츠 선수 비교 시스템", layout="wide")

st.title("🏆 스포츠 선수 비교 & 분석 시스템")

# -----------------------
# 1. 선수 DB
# -----------------------
data = {
    "이름": ["손흥민", "메시", "호날두", "김연아", "르브론 제임스", "스테판 커리", "음바페", "네이마르", "해리 케인", "이강인"],
    "종목": ["축구", "축구", "축구", "피겨스케이팅", "농구", "농구", "축구", "축구", "축구", "축구"],
    "스피드": [95, 88, 89, 92, 85, 90, 96, 93, 88, 87],
    "기술": [93, 99, 94, 98, 90, 99, 95, 97, 89, 92],
    "파워": [86, 80, 95, 78, 98, 85, 90, 83, 88, 75],
    "지능": [92, 99, 92, 97, 98, 95, 91, 90, 93, 96],
}
df = pd.DataFrame(data)

# -----------------------
# 2. 선수 선택
# -----------------------
st.sidebar.header("⚙️ 비교 설정")
selected_players = st.sidebar.multiselect("비교할 선수 선택 (2~4명)", df["이름"], default=["손흥민", "메시"])

if len(selected_players) < 2:
    st.warning("선수를 최소 2명 이상 선택하세요!")
    st.stop()

compare_df = df[df["이름"].isin(selected_players)]

# -----------------------
# 3. 레이더 차트
# -----------------------
st.subheader("📌 선수 능력치 레이더 차트")

categories = ["스피드", "기술", "파워", "지능"]
fig = go.Figure()

for _, row in compare_df.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=[row[c] for c in categories],
        theta=categories,
        fill='toself',
        name=row["이름"]
    ))

fig.update_layout(height=500, showlegend=True)
st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 4. 세부 능력치 표
# -----------------------
st.subheader("📊 선수 능력치 비교 표")
st.dataframe(compare_df.set_index("이름"))

# -----------------------
# 5. 바 차트 (기술 능력 비교)
# -----------------------
st.subheader("🔥 기술 능력 비교 그래프")

fig2 = go.Figure(data=[
    go.Bar(
        x=compare_df["이름"],
        y=compare_df["기술"]
    )
])

fig2.update_layout(yaxis_title="기술 능력치")
st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# 6. 간단한 경기력 예측 모델
# -----------------------
st.subheader("🔮 경기력 예측 (샘플)")

compare_df["예측 점수"] = (
    compare_df["스피드"] * 0.25 +
    compare_df["기술"] * 0.35 +
    compare_df["파워"] * 0.2 +
    compare_df["지능"] * 0.2
)

winner = compare_df.sort_values("예측 점수", ascending=False).iloc[0]

st.success(f"🏅 *예측 결과*: **{winner['이름']}** 선수가 가장 높은 경기력을 기록할 것으로 예상됩니다!")

# -----------------------
# 7. 선수 추천 기능
# -----------------------
st.subheader("🤖 AI 기반 선수 추천")

option = st.selectbox("원하는 스타일을 선택하세요", ["스피드형", "기술형", "파워형", "밸런스형"])

if option == "스피드형":
    best = df.sort_values("스피드", ascending=False).iloc[0]
elif option == "기술형":
    best = df.sort_values("기술", ascending=False).iloc[0]
elif option == "파워형":
    best = df.sort_values("파워", ascending=False).iloc[0]
else:
    df["합계"] = df[["스피드", "기술", "파워", "지능"]].sum(axis=1)
    best = df.sort_values("합계", ascending=False).iloc[0]

st.info(f"👉 추천 선수: **{best['이름']}** (종목: {best['종목']})")

# -----------------------
# 8. 종목 설명
# -----------------------
st.subheader("📘 종목 설명")

sports_info = {
    "축구": "축구는 스피드, 기술, 지능의 균형이 매우 중요한 팀 스포츠입니다.",
    "피겨스케이팅": "피겨는 예술성과 점프·스핀 기술의 정확성이 모두 요구됩니다.",
    "농구": "농구는 파워, 점프력, 경기 지능이 크게 작용하는 종목입니다."
}

for sport in compare_df["종목"].unique():
    st.write(f"### 🏟 {sport}")
    st.write(sports_info[sport])
