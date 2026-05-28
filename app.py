import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

# ── 페이지 설정 ──
st.set_page_config(
    page_title="고객 이탈 원인 분석 및 초개인화 리텐션 Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 전체 배경 */
.stApp { background: #F0F4FA; }

/* 헤더 */
.main-header {
    background: linear-gradient(135deg, #071430 0%, #0B1F4E 60%, #1A3A8F 100%);
    padding: 36px 40px 28px;
    border-radius: 16px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #0046AD, #1565E8, #4A90D9);
}
.main-title {
    font-size: 26px;
    font-weight: 900;
    color: #fff;
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.main-subtitle {
    font-size: 13px;
    color: rgba(255,255,255,0.55);
    margin: 0;
}
.main-badge {
    display: inline-block;
    background: rgba(0,70,173,0.4);
    border: 1px solid rgba(0,100,210,0.4);
    color: #7AADFF;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 10px;
    letter-spacing: 0.06em;
}

/* 단계 카드 */
.step-card {
    background: #fff;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    border: 1.5px solid #E0E8F5;
    box-shadow: 0 2px 8px rgba(0,30,100,0.06);
}
.step-label {
    font-size: 11px;
    font-weight: 700;
    color: #0046AD;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}
.step-title {
    font-size: 16px;
    font-weight: 700;
    color: #0B1F4E;
    margin-bottom: 12px;
}

/* 결과 카드 */
.result-card {
    background: #fff;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    border: 1.5px solid #C8D8FF;
}
.score-high { border-left: 4px solid #E53935; }
.score-mid  { border-left: 4px solid #FB8C00; }
.score-low  { border-left: 4px solid #43A047; }

/* 오퍼 뱃지 */
.offer-badge {
    display: inline-block;
    background: #EEF3FF;
    border: 1px solid #C8D8FF;
    color: #0046AD;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 4px 4px 4px 0;
}

/* Alert 박스 */
.alert-box {
    background: #FFF3E0;
    border: 1.5px solid #FFB74D;
    border-left: 4px solid #FF8F00;
    border-radius: 10px;
    padding: 16px 20px;
    margin: 16px 0;
}
.alert-title {
    font-size: 14px;
    font-weight: 700;
    color: #E65100;
    margin-bottom: 6px;
}

/* 성과 박스 */
.result-summary {
    background: linear-gradient(135deg, #0B1F4E, #0046AD);
    border-radius: 12px;
    padding: 24px 28px;
    color: #fff;
    margin-top: 20px;
}
.summary-num {
    font-size: 32px;
    font-weight: 900;
    color: #7AADFF;
}
.summary-label {
    font-size: 12px;
    color: rgba(255,255,255,0.6);
    margin-top: 2px;
}

/* 기여도 바 */
.contrib-bar-wrap {
    margin: 6px 0;
}
.contrib-label {
    font-size: 12px;
    color: #444;
    margin-bottom: 2px;
}
.contrib-bar-bg {
    background: #EEF3FF;
    border-radius: 4px;
    height: 10px;
    width: 100%;
}
.contrib-bar-fill {
    background: linear-gradient(90deg, #0046AD, #1565E8);
    border-radius: 4px;
    height: 10px;
}

/* 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #0046AD, #1565E8) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    padding: 10px 24px !important;
    font-size: 14px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #003A8C, #0046AD) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,70,173,0.3) !important;
}

/* 구분선 */
.divider {
    height: 1px;
    background: #E0E8F5;
    margin: 20px 0;
}

/* 온톨로지 유형 뱃지 */
.type-cl1 { background:#FFEBEE; color:#C62828; border:1px solid #FFCDD2; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:700; }
.type-cl2 { background:#E3F2FD; color:#1565C0; border:1px solid #BBDEFB; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:700; }
.type-cl3 { background:#E8F5E9; color:#2E7D32; border:1px solid #C8E6C9; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:700; }
.type-new { background:#FFF3E0; color:#E65100; border:1px solid #FFE0B2; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:700; }
</style>
""", unsafe_allow_html=True)


# ── 온톨로지 & 전략 정의 ──
ONTOLOGY = {
    "CL_1": {
        "name": "고객불만 발생형",
        "condition": lambda r: r["민원발생횟수"] >= 2,
        "offer": "카페 할인쿠폰 제공",
        "offer_detail": "제휴 카페 20% 할인 쿠폰 즉시 발송",
        "color": "type-cl1"
    },
    "CL_2": {
        "name": "이용감소형",
        "condition": lambda r: r["이용빈도변화율"] <= -30 and r["민원발생횟수"] < 2,
        "offer": "외식업종 30% 할인",
        "offer_detail": "외식업종 결제 시 30% 즉시 할인 (월 3회)",
        "color": "type-cl2"
    },
    "CL_3": {
        "name": "이용비중 감소형",
        "condition": lambda r: r["이용금액변화율"] <= -40 and r["이용빈도변화율"] > -30,
        "offer": "캐시백 오퍼",
        "offer_detail": "전월 대비 30만원 추가 이용 시 5만원 캐시백",
        "color": "type-cl3"
    }
}

VARIABLES = ["이용빈도변화율", "이용금액변화율", "민원발생횟수", "해지문의여부", "포인트소멸예정금액"]


def compute_score(row):
    """이탈 스코어 계산 (규칙 기반)"""
    score = 0.3
    if row["이용빈도변화율"] <= -30: score += 0.25
    elif row["이용빈도변화율"] <= -15: score += 0.12
    if row["이용금액변화율"] <= -40: score += 0.22
    elif row["이용금액변화율"] <= -20: score += 0.10
    if row["민원발생횟수"] >= 3: score += 0.18
    elif row["민원발생횟수"] >= 1: score += 0.08
    if row["해지문의여부"] == 1: score += 0.15
    if row["포인트소멸예정금액"] >= 50000: score += 0.05
    return min(round(score, 2), 0.99)


def compute_contributions(row, base_score):
    """변수별 기여도 계산 — 각 변수 제외 시 점수 변화량 역산"""
    contribs = {}
    for var in VARIABLES:
        temp = row.copy()
        # 해당 변수를 평균값(중립)으로 대체
        if var == "이용빈도변화율": temp[var] = 0
        elif var == "이용금액변화율": temp[var] = 0
        elif var == "민원발생횟수": temp[var] = 0
        elif var == "해지문의여부": temp[var] = 0
        elif var == "포인트소멸예정금액": temp[var] = 0
        score_without = compute_score(temp)
        contribs[var] = max(round(base_score - score_without, 3), 0)
    total = sum(contribs.values()) or 1
    return {k: round(v/total*100, 1) for k, v in contribs.items()}


def classify_type(row):
    """온톨로지 유형 분류"""
    for cl, info in ONTOLOGY.items():
        if info["condition"](row):
            return cl
    return "NEW"


def detect_new_pattern(df):
    """신규 패턴 감지 — 기존 CL에 해당하지 않는 고위험 고객"""
    new_patterns = []
    for _, row in df.iterrows():
        score = compute_score(row)
        cl = classify_type(row)
        if score >= 0.7 and cl == "NEW":
            new_patterns.append(row["고객ID"])
    return new_patterns


# ── 메인 UI ──
st.markdown("""
<div class="main-header">
    <div class="main-title">🎯 고객 이탈 원인 분석 및 초개인화 리텐션 Agent</div>
    <div class="main-subtitle">XAI 기반 이탈 원인 진단 → 처방 → 자동 실행</div>
    <span class="main-badge">XAI 기반 · 온톨로지 분류 · Human-in-the-Loop</span>
</div>
""", unsafe_allow_html=True)

# ── STEP 1: 데이터 업로드 ──
st.markdown('<div class="step-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">STEP 1</div>', unsafe_allow_html=True)
st.markdown('<div class="step-title">📂 고객 데이터 업로드</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    uploaded = st.file_uploader(
        "고객 데이터 CSV 파일을 업로드하세요",
        type=["csv"],
        help="컬럼: 고객ID, 이용빈도변화율, 이용금액변화율, 민원발생횟수, 해지문의여부, 포인트소멸예정금액"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    use_demo = st.button("🔍 더미 데이터로 시연하기", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# 데이터 로드
df = None
if use_demo or "demo_loaded" in st.session_state:
    st.session_state["demo_loaded"] = True
    np.random.seed(42)
    n = 30
    df = pd.DataFrame({
        "고객ID": [f"C{str(i).zfill(4)}" for i in range(1, n+1)],
        "이용빈도변화율": np.random.choice([-55, -40, -30, -20, -10, 0, 5, 10], n),
        "이용금액변화율": np.random.choice([-60, -45, -35, -20, -10, 0, 5], n),
        "민원발생횟수": np.random.choice([0, 0, 0, 1, 2, 3], n),
        "해지문의여부": np.random.choice([0, 0, 0, 1], n),
        "포인트소멸예정금액": np.random.choice([0, 0, 10000, 30000, 70000], n),
    })
    st.success(f"✅ 더미 데이터 로드 완료 — 고객 {n}명")

elif uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"✅ 업로드 완료 — 고객 {len(df)}명")

# ── STEP 2: Agent 분석 실행 ──
if df is not None:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-label">STEP 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="step-title">🤖 Agent 분석 실행</div>', unsafe_allow_html=True)

    run_btn = st.button("▶ 이탈 원인 분석 시작", use_container_width=False)

    if run_btn or "analysis_done" in st.session_state:
        st.session_state["analysis_done"] = True

        with st.spinner("이탈 스코어 계산 및 XAI 변수 기여도 분석 중..."):
            results = []
            for _, row in df.iterrows():
                r = row.to_dict()
                score = compute_score(r)
                contribs = compute_contributions(r, score)
                cl = classify_type(r)
                if cl != "NEW":
                    offer = ONTOLOGY[cl]["offer"]
                    offer_detail = ONTOLOGY[cl]["offer_detail"]
                    type_name = ONTOLOGY[cl]["name"]
                    type_class = ONTOLOGY[cl]["color"]
                else:
                    offer = "신규 패턴 — 검토 필요"
                    offer_detail = "기존 유형에 해당하지 않는 패턴입니다"
                    type_name = "신규 패턴"
                    type_class = "type-new"

                top_var = max(contribs, key=contribs.get)
                top_pct = contribs[top_var]
                var_name_map = {
                    "이용빈도변화율": "이용빈도 감소",
                    "이용금액변화율": "이용금액 감소",
                    "민원발생횟수": "고객불만 발생",
                    "해지문의여부": "해지 문의 이력",
                    "포인트소멸예정금액": "포인트 소멸 예정"
                }
                reason = f"{var_name_map.get(top_var, top_var)} ({top_pct}%)"

                results.append({
                    "고객ID": r["고객ID"],
                    "이탈점수": score,
                    "이탈유형": cl,
                    "유형명": type_name,
                    "type_class": type_class,
                    "주요원인": reason,
                    "기여도": contribs,
                    "추천오퍼": offer,
                    "오퍼상세": offer_detail,
                })

        res_df = pd.DataFrame(results)
        high_risk = res_df[res_df["이탈점수"] >= 0.7].sort_values("이탈점수", ascending=False)
        new_patterns = detect_new_pattern(df)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── STEP 3: 분석 결과 ──
        st.markdown('<div class="step-card">', unsafe_allow_html=True)
        st.markdown('<div class="step-label">STEP 3</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-title">📊 분석 결과 — 이탈 원인 진단</div>', unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("전체 분석 고객", f"{len(df)}명")
        m2.metric("고위험 고객 (0.7↑)", f"{len(high_risk)}명")
        m3.metric("이탈 유형 분류", f"{res_df['이탈유형'].nunique() - (1 if 'NEW' in res_df['이탈유형'].values else 0)}종")
        m4.metric("신규 패턴 감지", f"{len(new_patterns)}명")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # 신규 패턴 Alert
        if len(new_patterns) >= 3:
            st.markdown(f"""
            <div class="alert-box">
                <div class="alert-title">⚠️ 신규 이탈 패턴 감지 Alert</div>
                기존 CL_1/2/3에 해당하지 않는 고위험 고객이 <b>{len(new_patterns)}명</b> 감지되었습니다.<br>
                새로운 이탈 유형 추가를 검토해 주세요. (대상: {', '.join(new_patterns[:5])} 등)
            </div>
            """, unsafe_allow_html=True)

        # 고위험 고객 카드
        st.markdown("**🔴 고위험 이탈 고객 상세 분석**")
        for _, r in high_risk.head(8).iterrows():
            score_class = "score-high" if r["이탈점수"] >= 0.8 else "score-mid"
            contribs = r["기여도"]
            top2 = sorted(contribs.items(), key=lambda x: x[1], reverse=True)[:3]
            var_map = {
                "이용빈도변화율": "이용빈도 감소",
                "이용금액변화율": "이용금액 감소",
                "민원발생횟수": "고객불만",
                "해지문의여부": "해지 문의",
                "포인트소멸예정금액": "포인트 소멸"
            }
            bars = "".join([
                f'<div class="contrib-bar-wrap">'
                f'<div class="contrib-label">{var_map.get(v,v)} {p}%</div>'
                f'<div class="contrib-bar-bg"><div class="contrib-bar-fill" style="width:{p}%"></div></div>'
                f'</div>' for v, p in top2
            ])
            st.markdown(f"""
            <div class="result-card {score_class}">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                    <div>
                        <span style="font-size:15px;font-weight:700;color:#0B1F4E;">{r['고객ID']}</span>
                        &nbsp;&nbsp;<span class="{r['type_class']}">{r['유형명']}</span>
                    </div>
                    <div style="font-size:22px;font-weight:900;color:{'#E53935' if r['이탈점수']>=0.8 else '#FB8C00'}">
                        {r['이탈점수']}
                    </div>
                </div>
                <div style="font-size:12px;color:#555;margin-bottom:10px;">
                    주요 이탈 원인: <b style="color:#0046AD">{r['주요원인']}</b>
                </div>
                {bars}
                <div style="margin-top:10px;">
                    <span style="font-size:12px;color:#888;">추천 오퍼</span><br>
                    <span class="offer-badge">{r['추천오퍼']}</span>
                    <span style="font-size:11px;color:#666;">{r['오퍼상세']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── STEP 4: Human-in-the-Loop 승인 ──
        st.markdown('<div class="step-card">', unsafe_allow_html=True)
        st.markdown('<div class="step-label">STEP 4 · Human-in-the-Loop</div>', unsafe_allow_html=True)
        st.markdown('<div class="step-title">✅ 현업 검토 및 캠페인 승인</div>', unsafe_allow_html=True)
        st.markdown("Agent가 제안한 리텐션 오퍼를 검토하고 실행을 승인해 주세요.")

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            approve = st.button("✅ 전체 승인 후 캠페인 실행", use_container_width=True)
        with col_b:
            st.button("✏️ 일부 수정 후 실행", use_container_width=True)
        with col_c:
            st.button("⏸ 보류", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── STEP 5: 캠페인 실행 결과 ──
        if approve or "campaign_done" in st.session_state:
            st.session_state["campaign_done"] = True

            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown('<div class="step-label">STEP 5</div>', unsafe_allow_html=True)
            st.markdown('<div class="step-title">🚀 리텐션 캠페인 실행 완료</div>', unsafe_allow_html=True)

            st.success(f"✅ {len(high_risk)}명 대상 초개인화 리텐션 캠페인이 실행되었습니다.")

            cl1 = len(high_risk[high_risk["이탈유형"]=="CL_1"])
            cl2 = len(high_risk[high_risk["이탈유형"]=="CL_2"])
            cl3 = len(high_risk[high_risk["이탈유형"]=="CL_3"])

            st.markdown(f"""
            <div class="result-summary">
                <div style="font-size:13px;color:rgba(255,255,255,0.6);margin-bottom:16px;">
                    {datetime.now().strftime('%Y-%m-%d %H:%M')} 기준 캠페인 실행 현황
                </div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:20px;">
                    <div>
                        <div class="summary-num">{len(high_risk)}</div>
                        <div class="summary-label">총 발송 대상</div>
                    </div>
                    <div>
                        <div class="summary-num">{cl1}</div>
                        <div class="summary-label">CL_1 카페쿠폰 발송</div>
                    </div>
                    <div>
                        <div class="summary-num">{cl2}</div>
                        <div class="summary-label">CL_2 외식할인 발송</div>
                    </div>
                    <div>
                        <div class="summary-num">{cl3}</div>
                        <div class="summary-label">CL_3 캐시백 발송</div>
                    </div>
                </div>
                <div style="margin-top:20px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.15);
                            font-size:13px;color:rgba(255,255,255,0.55);">
                    Push/LMS/카카오톡 채널 자동 선택 완료 · 성과 데이터는 24시간 후 자동 수집됩니다
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # 성과 리포트 (시뮬레이션)
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown('<div class="step-label">STEP 6 · 성과 리포트</div>', unsafe_allow_html=True)
            st.markdown('<div class="step-title">📈 캠페인 성과 리포트 (시뮬레이션)</div>', unsafe_allow_html=True)

            sim_rate = round(random.uniform(28, 42), 1)
            sim_save = int(len(high_risk) * sim_rate / 100)

            r1, r2, r3 = st.columns(3)
            r1.metric("예상 리텐션 전환율", f"{sim_rate}%", f"+{round(sim_rate-18,1)}%p (기존 일괄 오퍼 대비)")
            r2.metric("이탈 방어 예상 고객", f"{sim_save}명")
            r3.metric("오퍼 비용 효율", "↑ 개선", "원인별 맞춤 오퍼 적용")

            st.markdown("""
            <div style="background:#EEF3FF;border-radius:10px;padding:14px 18px;margin-top:12px;
                        border-left:4px solid #0046AD;font-size:13px;color:#0B1F4E;font-style:italic;">
                "이제 마케터의 역할은 데이터를 찾는 것이 아니라,<br>
                Agent가 발견한 인사이트를 바탕으로 더 나은 마케팅 방식을 고민하는 것으로 전환됩니다."
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown('</div>', unsafe_allow_html=True)

# ── 푸터 ──
st.markdown("""
<div style="text-align:center;padding:24px;color:#aaa;font-size:12px;margin-top:20px;">
고객 이탈 원인 분석 및 초개인화 리텐션 Agent (XAI 기반)
</div>
""", unsafe_allow_html=True)
