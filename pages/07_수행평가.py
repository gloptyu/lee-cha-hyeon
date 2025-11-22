# 완전판: 축구 선수 비교 + 인터랙티브 기능 모음
# 붙여넣고 streamlit run app.py 로 실행하세요.

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
import math
from functools import lru_cache

st.set_page_config(page_title="⚽ Ultimate Player Comparator", layout="wide")

# ---------------------------
# CSS: 전체 스타일, 카드 애니메이션, 배지 스타일
# ---------------------------
st.markdown(
    """
    <style>
    /* 페이지 배경: 축구장 + 어둡게 오버레이 */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1508098682722-e99c43a406b2?auto=format&fit=crop&w=1500&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        filter: saturate(1.05);
    }
    /* 반투명 컨테이너로 가독성 확보 */
    .app-container {
        background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(0,0,0,0.25));
        padding: 16px;
        border-radius: 10px;
    }

    /* 카드 */
    .player-card {
        border-radius: 14px;
        overflow: hidden;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        cursor: pointer;
        box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    }
    .player-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 12px 30px rgba(0,0,0,0.35);
    }
    .player-overlay {
        background: rgba(0,0,0,0.58);
        padding: 12px;
        color: white;
    }
    .stat-badge {
        display:inline-block;
        padding:6px 10px;
        margin:4px;
        border-radius:999px;
        background: rgba(255,255,255,0.08);
        color: white;
        font-weight:700;
        font-size:12px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
    }
    .legend-badge { background: linear-gradient(90deg,#ffd700,#ff7a00); color:#111; }
    .worldclass-badge { background: linear-gradient(90deg,#00d2ff,#0066ff); color:#fff; }
    .good-badge { background: linear-gradient(90deg,#8affc1,#00b388); color:#063; }

    /* header tweaks */
    header[data-testid="stHeader"] {background: rgba(0,0,0,0.1);}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# 데이터: TOP 선수 (이미지, 팀컬러, 상세 커리어 포함)
# ---------------------------
PLAYERS = {
    "손흥민": {
        "club": "토트넘",
        "nation": "대한민국",
        "team_color": "#001B5E",
        "image": "https://upload.wikimedia.org/wikipedia/commons/2/2e/Son_Heung-min_2022.jpg",
        "stats": {"스피드":95,"드리블":93,"슈팅":85,"패스":82,"수비":40},
        "season": {"골":22,"도움":12,"경기":34},
        "career": [
            "토트넘 주전 공격수 (프리미어리그 주전)",
            "대한민국 대표팀 핵심, 아시아 챔피언십 활약",
            "프리미어리그서 꾸준한 득점과 도움"
        ]
    },
    "리오넬 메시": {
        "club": "인터 마이애미",
        "nation": "아르헨티나",
        "team_color": "#FF5DA2",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Lionel_Messi_20180710.jpg",
        "stats": {"스피드":88,"드리블":95,"슈팅":92,"패스":91,"수비":30},
        "season": {"골":30,"도움":20,"경기":35},
        "career": [
            "바르셀로나에서 전설적 커리어",
            "발롱도르 다수 수상(역대 최다 수준)",
            "PSG 및 인터 마이애미 활약"
        ]
    },
    "크리스티아누 호날두": {
        "club": "알나스르",
        "nation": "포르투갈",
        "team_color": "#FFD700",
        "image": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
        "stats": {"스피드":87,"드리블":89,"슈팅":93,"패스":82,"수비":35},
        "season": {"골":28,"도움":15,"경기":32},
        "career": [
            "맨유·레알·유벤투스 등 주요 클럽에서 득점왕 다수",
            "역대 최다 공식골 도전자",
            "올라운드 피지컬·결정력"
        ]
    },
    "킬리안 음바페": {
        "club": "레알 마드리드",
        "nation": "프랑스",
        "team_color": "#FFFFFF",
        "image": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Kylian_Mbapp%C3%A9_2022.jpg",
        "stats": {"스피드":96,"드리블":90,"슈팅":91,"패스":80,"수비":40},
        "season": {"골":26,"도움":18,"경기":33},
        "career": [
            "전속 스피드형 스트라이커",
            "모나코·PSG에서 두각, 레알 이적",
            "월드컵 우승 경험 보유"
        ]
    },
    "네이마르": {
        "club": "산투스",
        "nation": "브라질",
        "team_color": "#00AEEF",
        "image": "https://upload.wikimedia.org/wikipedia/commons/3/37/Neymar_2018.jpg",
        "stats": {"스피드":91,"드리블":94,"슈팅":86,"패스":87,"수비":30},
        "season": {"골":22,"도움":19,"경기":30},
        "career": [
            "기술·창의성의 아이콘",
            "바르셀로나 시절 MSN 트리오",
            "국가대표 핵심 자원"
        ]
    },
    "케빈 더 브라위너": {
        "club": "맨체스터 시티",
        "nation": "벨기에",
        "team_color": "#00AEEF",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Kevin_De_Bruyne_2018.jpg",
        "stats": {"스피드":79,"드리블":85,"슈팅":88,"패스":94,"수비":50},
        "season": {"골":12,"도움":21,"경기":34},
        "career": [
            "시야·패스 능력 최상급",
            "맨시티의 핵심 플레이메이커",
            "셋피스와 어시스트 능력"
        ]
    },
    "모하메드 살라": {
        "club": "리버풀",
        "nation": "이집트",
        "team_color": "#C8102E",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0c/Mohamed_Salah_2018.jpg",
        "stats": {"스피드":92,"드리블":91,"슈팅":90,"패스":80,"수비":35},
        "season": {"골":27,"도움":13,"경기":33},
        "career": [
            "프리미어리그 득점왕 경험",
            "양발 + 스피드의 조합",
            "클럽 및 대표팀에서 핵심"
        ]
    },
    "로베르트 레반도프스키": {
        "club": "FC 바르셀로나",
        "nation": "폴란드",
        "team_color": "#A50044",
        "image": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Robert_Lewandowski_2021.jpg",
        "stats": {"스피드":76,"드리블":82,"슈팅":95,"패스":78,"수비":40},
        "season": {"골":34,"도움":9,"경기":36},
        "career": [
            "역사적인 골게터",
            "바이에른 뮌헨 시절 최정상 득점력",
            "포지셔닝과 마무리 능력 탁월"
        ]
    },
    "버질 반 다이크": {
        "club": "리버풀",
        "nation": "네덜란드",
        "team_color": "#C8102E",
        "image": "https://upload.wikimedia.org/wikipedia/commons/1/12/Virgil_van_Dijk_2019.jpg",
        "stats": {"스피드":70,"드리블":60,"슈팅":65,"패스":82,"수비":94},
        "season": {"골":5,"도움":3,"경기":32},
        "career": [
            "현대 축구의 대표적인 센터백",
            "리버풀 리빌딩 핵심",
            "공중볼과 수비 지휘 능력"
        ]
    },
    "이강인": {
        "club": "마요르카",
        "nation": "대한민국",
        "team_color": "#0033A0",
        "image": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Lee_Gang-in_2021.jpg",
        "stats": {"스피드":87,"드리블":88,"슈팅":80,"패스":90,"수비":45},
        "season": {"골":10,"도움":8,"경기":30},
        "career": [
            "유스 시절부터 기술 우수",
            "유럽 무대에서 성장 중",
            "창의적 패스·프리킥 가능"
        ]
    },
    "해리 케인": {
        "club":"바이에른 뮌헨","nation":"잉글랜드","team_color":"#CC0000",
        "image":"https://upload.wikimedia.org/wikipedia/commons/0/0c/Harry_Kane_2018.jpg",
        "stats":{"스피드":80,"드리블":75,"슈팅":93,"패스":86,"수비":42},
        "season":{"골":33,"도움":10,"경기":34},
        "career":["전술적 스트라이커","포스트 플레이 우수","골 결정력 탁월"]
    },
    "카림 벤제마": {
        "club":"알 이티하드","nation":"프랑스","team_color":"#F4E242",
        "image":"https://upload.wikimedia.org/wikipedia/commons/9/91/Karim_Benzema_2022.jpg",
        "stats":{"스피드":78,"드리블":86,"슈팅":91,"패스":83,"수비":38},
        "season":{"골":25,"도움":7,"경기":33},
        "career":["레알 마드리드 핵심 공격수","발롱도르 수상","포스트 플레이 강자"]
    },
    "크바라츠헬리아": {
        "club":"나폴리","nation":"조지아","team_color":"#1B4CA1",
        "image":"https://upload.wikimedia.org/wikipedia/commons/7/72/Khvicha_Kvaratskhelia_2022.jpg",
        "stats":{"스피드":90,"드리블":94,"슈팅":84,"패스":76,"수비":30},
        "season":{"골":14,"도움":11,"경기":32},
        "career":["나폴리 핵심 윙어","드리블과 순간 돌파력"]
    },
    "라파엘 레앙": {
        "club":"AC 밀란","nation":"포르투갈","team_color":"#B00000",
        "image":"https://upload.wikimedia.org/wikipedia/commons/2/2d/Rafael_Le%C3%A3o_2022.jpg",
        "stats":{"스피드":94,"드리블":92,"슈팅":88,"패스":82,"수비":36},
        "season":{"골":13,"도움":9,"경기":28},
        "career":["AC 밀란 핵심 공격 자원","스피드+드리블 장점"]
    },
    "주드 벨링엄": {
        "club":"레알 마드리드","nation":"잉글랜드","team_color":"#111111",
        "image":"https://upload.wikimedia.org/wikipedia/commons/c/ce/Jude_Bellingham_2022.jpg",
        "stats":{"스피드":88,"드리블":88,"슈팅":89,"패스":92,"수비":70},
        "season":{"골":20,"도움":12,"경기":29},
        "career":["중원 장악형 미드필더","젊은 핵심 자원","다재다능한 전술 이해도"]
    }
}

# ---------------------------
# 도움 함수들
# ---------------------------
def get_player_list():
    return list(PLAYERS.keys())

@lru_cache(maxsize=128)
def load_image_url(url):
    # 단순 캐싱용; 실제로는 URL을 그대로 사용 (Streamlit이 내부 처리)
    return url

def stat_badge_class(value):
    # 배지 분류: 90+ Legend, 80-89 WorldClass, 70-79 Good
    if value >= 90:
        return "stat-badge legend-badge"
    elif value >= 80:
        return "stat-badge worldclass-badge"
    else:
        return "stat-badge good-badge"

def elo_probability(score_a, score_b):
    # 간단한 ELO 유사 확률: logistic function
    diff = score_a - score_b
    prob = 1 / (1 + math.exp(-diff/10))  # /10 으로 스케일 조정
    return prob

def automatic_commentary(p1_name, p2_name, p1_stats, p2_stats):
    # 간단한 규칙 기반 코멘트 생성
    p1_total = sum(p1_stats.values())
    p2_total = sum(p2_stats.values())
    lines = []
    lines.append(f"비교: **{p1_name} vs {p2_name}**")
    if p1_total > p2_total:
        lines.append(f"총합 기준으로는 **{p1_name}**가 우세합니다. (합계: {p1_total} vs {p2_total})")
    elif p2_total > p1_total:
        lines.append(f"총합 기준으로는 **{p2_name}**가 우세합니다. (합계: {p2_total} vs {p1_total})")
    else:
        lines.append("총합이 같습니다 — 세부 항목에서 차이를 보세요.")
    # 포인트별 언급
    for k in p1_stats.keys():
        a = p1_stats[k]; b = p2_stats[k]
        if abs(a-b) >= 12:
            stronger = p1_name if a>b else p2_name
            lines.append(f"- **{k}** 항목에서 확연한 차이: {stronger} 우세 ({a} vs {b})")
        elif abs(a-b) >= 5:
            stronger = p1_name if a>b else p2_name
            lines.append(f"- {k} 항목에서 약간 우세: {stronger} ({a} vs {b})")
    # 플레이스타일 요약
    p1_role = "공격형" if p1_stats["슈팅"]+p1_stats["드리블"] > p1_stats["패스"]+p1_stats["수비"] else "조율형"
    p2_role = "공격형" if p2_stats["슈팅"]+p2_stats["드리블"] > p2_stats["패스"]+p2_stats["수비"] else "조율형"
    lines.append(f"- 플레이스타일 분석: {p1_name} = {p1_role}, {p2_name} = {p2_role}.")
    return "\n".join(lines)

def badge_label(v):
    if v >= 90:
        return "Legend"
    elif v >= 80:
        return "World Class"
    elif v >= 70:
        return "Good"
    else:
        return "Solid"

# ---------------------------
# 사이드바: 검색 / 자동완성 / 필터
# ---------------------------
st.sidebar.header("🔎 선수 찾기 / 설정")
search_text = st.sidebar.text_input("선수 검색 (자동완성):", "")
# autocomplete-like: show players containing substring
matched = [p for p in get_player_list() if search_text.lower() in p.lower()]
if not matched:
    matched = get_player_list()

# 기본 선택 (2명)
default_sel = [matched[0], matched[1]] if len(matched) >= 2 else get_player_list()[:2]

selected = st.sidebar.multiselect("비교할 선수 선택", matched, default=default_sel)

if len(selected) < 2:
    st.sidebar.warning("선수를 최소 2명 선택하세요 (사이드바에서 선택).")

# 옵션: 슬라이드형 비교 보기 토글
slide_mode = st.sidebar.checkbox("슬라이드형 비교 보기 (Next/Prev)", value=False)
# 옵션: 능력치 슬라이더 활성화
enable_sliders = st.sidebar.checkbox("능력치 슬라이더 활성화", value=True)
# 옵션: 우승 확률 시뮬레이션 토글
enable_ucl_sim = st.sidebar.checkbox("우승 확률(간단 시뮬레이션) 표시", value=True)

# ---------------------------
# 메인 컨테이너
# ---------------------------
st.markdown('<div class="app-container">', unsafe_allow_html=True)

# 선택 선수 데이터
compare_list = [p for p in selected if p in PLAYERS]
if len(compare_list) < 2:
    st.info("사이드바에서 비교할 선수 2명 이상 선택해주세요.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------------------------
# 능력치 슬라이더 (사용자 조정 가능)
# ---------------------------
st.header("1) 능력치 비교 & 커스터마이즈")
colA, colB = st.columns(2)
p1_name = compare_list[0]
p2_name = compare_list[1]
p1 = PLAYERS[p1_name]
p2 = PLAYERS[p2_name]

# 초기 stats (복사)
p1_stats = p1["stats"].copy()
p2_stats = p2["stats"].copy()

if enable_sliders:
    with colA:
        st.subheader(p1_name)
        st.image(load_image_url(p1["image"]), width=180)
        st.write(f"클럽: {p1['club']}  |  국적: {p1['nation']}")
        st.markdown("---")
        for k,v in p1_stats.items():
            p1_stats[k] = st.slider(f"{p1_name} - {k}", 0, 100, int(v))
    with colB:
        st.subheader(p2_name)
        st.image(load_image_url(p2["image"]), width=180)
        st.write(f"클럽: {p2['club']}  |  국적: {p2['nation']}")
        st.markdown("---")
        for k,v in p2_stats.items():
            p2_stats[k] = st.slider(f"{p2_name} - {k}", 0, 100, int(v))
else:
    with colA:
        st.subheader(p1_name)
        st.image(load_image_url(p1["image"]), width=180)
        st.write(f"클럽: {p1['club']}  |  국적: {p1['nation']}")
        st.markdown("---")
        for k,v in p1_stats.items():
            st.write(f"{k}: {v}")
    with colB:
        st.subheader(p2_name)
        st.image(load_image_url(p2["image"]), width=180)
        st.write(f"클럽: {p2['club']}  |  국적: {p2['nation']}")
        st.markdown("---")
        for k,v in p2_stats.items():
            st.write(f"{k}: {v}")

# ---------------------------
# 레이더 차트 (변경된 능력치 사용)
# ---------------------------
st.subheader("능력치 레이더 차트")
categories = list(p1_stats.keys())
fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=list(p1_stats.values()), theta=categories, fill='toself', name=p1_name))
fig.add_trace(go.Scatterpolar(r=list(p2_stats.values()), theta=categories, fill='toself', name=p2_name))
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=True)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 자동 분석 코멘트 & 배지
# ---------------------------
st.subheader("전문가 코멘트 (자동 생성)")
comment = automatic_commentary(p1_name, p2_name, p1_stats, p2_stats)
st.markdown(comment)

st.markdown("**능력치 배지**")
cols = st.columns(2)
with cols[0]:
    st.markdown(f"**{p1_name}**")
    for k,v in p1_stats.items():
        cls = stat_badge_class(v)
        st.markdown(f"<span class='{cls}'>{k}: {v} ({badge_label(v)})</span>", unsafe_allow_html=True)
with cols[1]:
    st.markdown(f"**{p2_name}**")
    for k,v in p2_stats.items():
        cls = stat_badge_class(v)
        st.markdown(f"<span class='{cls}'>{k}: {v} ({badge_label(v)})</span>", unsafe_allow_html=True)

# ---------------------------
# 시즌 기록 막대그래프 (그룹형, 팀컬러 적용)
# ---------------------------
st.subheader("시즌 기록 비교 (골/도움/경기)")
season_metrics = ["골","도움","경기"]
fig_bar = go.Figure()
for name in [p1_name, p2_name]:
    row = PLAYERS[name]
    fig_bar.add_trace(go.Bar(
        x=season_metrics,
        y=[row["season"][m] for m in season_metrics],
        name=name,
        marker_color=row["team_color"]
    ))
fig_bar.update_layout(barmode='group', template="plotly_white")
st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------
# 우승 확률 시뮬레이션 (간단)
# ---------------------------
if enable_ucl_sim:
    st.subheader("우승 확률(간단 시뮬레이션)")
    p1_score = sum(p1_stats.values())
    p2_score = sum(p2_stats.values())
    prob1 = elo_probability(p1_score, p2_score)
    prob2 = 1 - prob1
    st.write(f"**{p1_name}** 우승(가상) 확률: {prob1*100:.1f}%")
    st.write(f"**{p2_name}** 우승(가상) 확률: {prob2*100:.1f}%")

# ---------------------------
# 선수 카드 목록 (애니메이션 적용된 그리드)
# ---------------------------
st.header("전체 선수 카드 (클릭하면 상세)")
cards = st.columns(5)
names = list(PLAYERS.keys())
for i,name in enumerate(names):
    col = cards[i%5]
    info = PLAYERS[name]
    with col:
        # 카드 HTML (팀컬러 배경 + 반투명 오버레이으로 가독성 확보)
        st.markdown(
            f"""
            <div class="player-card" style="background:{info['team_color']};">
                <div class="player-overlay">
                    <img src="{info['image']}" width="160" style="border-radius:10px; display:block; margin: 6px auto;">
                    <div style="font-weight:800; font-size:16px; color:white; text-shadow:1px 1px 3px rgba(0,0,0,0.7);">{name}</div>
                    <div style="color:#fff; opacity:0.9; font-size:13px;">{info['club']} · {info['nation']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------
# 상세 커리어 영역 (아래에서 펼쳐짐)
# ---------------------------
st.header("선수 커리어 & 수상 상세 (선택한 선수)")
for name in compare_list:
    info = PLAYERS[name]
    with st.expander(f"{name} - 상세 커리어 / 수상"):
        st.image(info["image"], width=220)
        st.write(f"클럽: {info['club']}  |  국적: {info['nation']}")
        st.write("**시즌 기록**")
        st.write(info["season"])
        st.write("**능력치**")
        st.write(info["stats"])
        st.write("**수상 / 주요 커리어**")
        for item in info["career"]:
            st.markdown(f"- {item}")

# ---------------------------
# 슬라이드형 비교 뷰 (Next/Prev) — 선택 옵션일 때 동작
# ---------------------------
if slide_mode:
    st.header("슬라이드형 비교 뷰")
    # 슬라이드 인덱스 보존 (세션 상태)
    if "slide_idx" not in st.session_state:
        st.session_state["slide_idx"] = 0
    total = len(compare_list)
    c1, c2, c3 = st.columns([1,2,1])
    with c1:
        if st.button("◀ 이전"):
            st.session_state["slide_idx"] = (st.session_state["slide_idx"] - 1) % total
    with c3:
        if st.button("다음 ▶"):
            st.session_state["slide_idx"] = (st.session_state["slide_idx"] + 1) % total
    idx = st.session_state["slide_idx"]
    current_name = compare_list[idx]
    info = PLAYERS[current_name]
    st.subheader(f"▶ 현재 슬라이드: {current_name}")
    st.image(info["image"], width=320)
    st.write(f"클럽: {info['club']}  |  국적: {info['nation']}")
    st.write("커리어 하이라이트:")
    for it in info["career"]:
        st.markdown(f"- {it}")

# ---------------------------
# 오늘의 추천 (종합)
# ---------------------------
st.markdown("---")
st.header("오늘의 추천")
if st.button("🎯 추천받기"):
    # 추천 기준: 시즌 골+도움 + 능력치 총합 (단순 가중)
    scored = []
    for name in PLAYERS:
        info = PLAYERS[name]
        stat_sum = sum(info["stats"].values())
        form = info["season"]["골"] * 3 + info["season"]["도움"] * 2
        score = stat_sum + form
        scored.append((name, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[0][0]
    tinfo = PLAYERS[top]
    st.success(f"오늘의 추천 선수: **{top}**")
    st.image(tinfo["image"], width=260)
    st.write(f"클럽: {tinfo['club']}, 국적: {tinfo['nation']}")
    st.write("주요 커리어:")
    for it in tinfo["career"]:
        st.markdown(f"- {it}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# 끝: 추가 안내
# ---------------------------
st.caption("앱: 능력치 슬라이더로 수치 바꿔가며 시뮬레이션, 슬라이드 모드로 발표용 UI, 상세 커리어는 expander 확인하세요.")
