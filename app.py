import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

st.set_page_config(
    page_title="고객 이탈 원인 분석 및 초개인화 리텐션 Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif !important;
    box-sizing: border-box;
}

/* ── 전체 배경 ── */
.stApp { background: #EDF1F8; }
.block-container {
    max-width: 1100px !important;
    padding: 2rem 1.5rem !important;
    margin: 0 auto;
}

/* ── 반응형 ── */
@media (max-width: 768px) {
    .block-container { padding: 1rem 0.75rem !important; }
    .main-title { font-size: 18px !important; }
    .main-header { padding: 24px 20px 20px !important; }
    .kpi-grid { grid-template-columns: repeat(2, 1fr) !important; }
    .summary-grid { grid-template-columns: repeat(2, 1fr) !important; }
    .step-card { padding: 16px !important; }
}
@media (max-width: 480px) {
    .main-title { font-size: 15px !important; }
    .kpi-grid { grid-template-columns: 1fr 1fr !important; }
    .summary-grid { grid-template-columns: 1fr 1fr !important; }
}

/* ── 헤더 ── */
.main-header {
    background: linear-gradient(135deg, #071430 0%, #0B1F4E 55%, #1A3A8F 100%);
    padding: 36px 44px 30px;
    border-radius: 18px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(7,20,48,0.22);
}
.main-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 5px;
    background: linear-gradient(90deg, #0046AD, #1565E8, #4A90D9);
}
.main-header::after {
    content: '';
    position: absolute;
    right: -60px; top: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(21,101,232,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.main-title {
    font-size: 22px;
    font-weight: 900;
    color: #fff;
    margin: 0 0 6px;
    letter-spacing: -0.5px;
    line-height: 1.3;
}
.main-sub {
    font-size: 12.5px;
    color: rgba(255,255,255,0.5);
    margin: 0 0 14px;
}
.badge-row { display: flex; gap: 8px; flex-wrap: wrap; }
.badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(0,70,173,0.35);
    border: 1px solid rgba(0,100,210,0.35);
    color: #90C4FF;
    font-size: 11px; font-weight: 700;
    padding: 4px 12px; border-radius: 20px;
    letter-spacing: 0.05em;
}

/* ── 단계 카드 ── */
.step-card {
    background: #fff;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 18px;
    border: 1.5px solid #E0E8F5;
    box-shadow: 0 2px 12px rgba(0,30,100,0.06);
    transition: box-shadow 0.2s;
}
.step-card:hover { box-shadow: 0 4px 20px rgba(0,30,100,0.10); }
.step-label {
    font-size: 10.5px; font-weight: 800;
    color: #0046AD; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 4px;
}
.step-title {
    font-size: 16px; font-weight: 700;
    color: #0B1F4E; margin-bottom: 14px;
}

/* ── KPI 그리드 ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 20px;
}
.kpi-card {
    background: linear-gradient(135deg, #F8FAFF, #EEF3FF);
    border: 1.5px solid #D0DCFF;
    border-radius: 12px;
    padding: 16px 18px;
    text-align: center;
}
.kpi-num {
    font-size: 28px; font-weight: 900;
    color: #0046AD; line-height: 1.1;
    margin-bottom: 4px;
}
.kpi-label {
    font-size: 11px; color: #6680AA;
    font-weight: 500; line-height: 1.4;
}

/* ── 결과 카드 ── */
.result-card {
    background: #fff;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    border: 1.5px solid #D8E4FF;
    transition: box-shadow 0.2s, transform 0.2s;
}
.result-card:hover {
    box-shadow: 0 4px 16px rgba(0,70,173,0.10);
    transform: translateY(-1px);
}
.score-high { border-left: 5px solid #E53935; }
.score-mid  { border-left: 5px solid #FB8C00; }

/* ── 유형 뱃지 ── */
.type-cl1 { background:#FFEBEE; color:#C62828; border:1px solid #FFCDD2; padding:3px 11px; border-radius:20px; font-size:11.5px; font-weight:700; }
.type-cl2 { background:#E3F2FD; color:#1565C0; border:1px solid #BBDEFB; padding:3px 11px; border-radius:20px; font-size:11.5px; font-weight:700; }
.type-cl3 { background:#E8F5E9; color:#2E7D32; border:1px solid #C8E6C9; padding:3px 11px; border-radius:20px; font-size:11.5px; font-weight:700; }
.type-new { background:#FFF3E0; color:#E65100; border:1px solid #FFE0B2; padding:3px 11px; border-radius:20px; font-size:11.5px; font-weight:700; }

/* ── 오퍼 뱃지 ── */
.offer-badge {
    display: inline-block;
    background: #EEF3FF; border: 1.5px solid #C8D8FF;
    color: #0046AD; font-size: 12px; font-weight: 700;
    padding: 4px 14px; border-radius: 20px; margin: 4px 4px 4px 0;
}

/* ── 기여도 바 ── */
.bar-wrap { margin: 7px 0; }
.bar-label {
    display: flex; justify-content: space-between;
    font-size: 12px; color: #555; margin-bottom: 3px;
}
.bar-bg {
    background: #EEF3FF; border-radius: 6px;
    height: 8px; width: 100%; overflow: hidden;
}
.bar-fill {
    background: linear-gradient(90deg, #0046AD, #1565E8);
    border-radius: 6px; height: 8px;
    transition: width 0.6s ease;
}

/* ── Alert ── */
.alert-box {
    background: linear-gradient(135deg, #FFF8E1, #FFF3E0);
    border: 1.5px solid #FFB74D;
    border-left: 5px solid #FF8F00;
    border-radius: 12px;
    padding: 16px 20px; margin: 16px 0;
}
.alert-title {
    font-size: 14px; font-weight: 700;
    color: #E65100; margin-bottom: 6px;
}

/* ── 성과 요약 ── */
.result-summary {
    background: linear-gradient(135deg, #071430, #0B1F4E, #0046AD);
    border-radius: 14px;
    padding: 28px 32px;
    color: #fff; margin-top: 20px;
    box-shadow: 0 8px 24px rgba(0,30,100,0.22);
    position: relative; overflow: hidden;
}
.result-summary::after {
    content: '';
    position: absolute; right: -40px; bottom: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.summary-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px; margin-top: 16px;
}
.summary-num {
    font-size: 30px; font-weight: 900;
    color: #7AADFF; line-height: 1;
    margin-bottom: 4px;
}
.summary-label {
    font-size: 11.5px;
    color: rgba(255,255,255,0.55);
}

/* ── 버튼 ── */
.stButton > button {
    background: linear-gradient(135deg, #0046AD, #1565E8) !important;
    color: #fff !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    padding: 12px 24px !important; font-size: 14px !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(0,70,173,0.2) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #003A8C, #0046AD) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(0,70,173,0.3) !important;
}

/* ── 인용 박스 ── */
.quote-box {
    background: linear-gradient(135deg, #EEF3FF, #F8FAFF);
    border-left: 5px solid #0046AD;
    border-radius: 0 12px 12px 0;
    padding: 16px 22px; margin-top: 16px;
    font-size: 13px; color: #0B1F4E;
    font-style: italic; line-height: 1.8;
}

/* ── 구분선 ── */
.divider { height: 1px; background: #E8EFF8; margin: 20px 0; }

/* ── 업로드 영역 ── */
.upload-hint {
    background: #F8FAFF; border: 2px dashed #C8D8FF;
    border-radius: 12px; padding: 20px;
    text-align: center; color: #6680AA;
    font-size: 13px; margin-top: 8px;
}

/* streamlit metric 카드 스타일 덮어쓰기 */
[data-testid="metric-container"] {
    background: #F8FAFF !important;
    border: 1.5px solid #D0DCFF !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
}
</style>
""", unsafe_allow_html=True)


# ── 온톨로지 & 전략 ──
ONTOLOGY = {
    "CL_1": {"name":"고객불만 발생형","condition":lambda r:r["민원발생횟수"]>=2,
              "offer":"카페 할인쿠폰 제공","offer_detail":"제휴 카페 20% 할인 쿠폰 즉시 발송","color":"type-cl1","icon":"🔴"},
    "CL_2": {"name":"이용감소형","condition":lambda r:r["이용빈도변화율"]<=-30 and r["민원발생횟수"]<2,
              "offer":"외식업종 30% 할인","offer_detail":"외식업종 결제 시 30% 즉시 할인 (월 3회)","color":"type-cl2","icon":"🟠"},
    "CL_3": {"name":"이용비중 감소형","condition":lambda r:r["이용금액변화율"]<=-40 and r["이용빈도변화율"]>-30,
              "offer":"캐시백 오퍼","offer_detail":"전월 대비 30만원 추가 이용 시 5만원 캐시백","color":"type-cl3","icon":"🟡"},
}
VARIABLES = ["이용빈도변화율","이용금액변화율","민원발생횟수","해지문의여부","포인트소멸예정금액"]
VAR_KR = {"이용빈도변화율":"이용빈도 감소","이용금액변화율":"이용금액 감소",
           "민원발생횟수":"고객불만 발생","해지문의여부":"해지 문의 이력","포인트소멸예정금액":"포인트 소멸 예정"}


def compute_score(r):
    s = 0.3
    if r["이용빈도변화율"] <= -30: s += 0.25
    elif r["이용빈도변화율"] <= -15: s += 0.12
    if r["이용금액변화율"] <= -40: s += 0.22
    elif r["이용금액변화율"] <= -20: s += 0.10
    if r["민원발생횟수"] >= 3: s += 0.18
    elif r["민원발생횟수"] >= 1: s += 0.08
    if r["해지문의여부"] == 1: s += 0.15
    if r["포인트소멸예정금액"] >= 50000: s += 0.05
    return min(round(s, 2), 0.99)


def compute_contributions(r, base):
    c = {}
    for v in VARIABLES:
        t = r.copy(); t[v] = 0
        c[v] = max(round(base - compute_score(t), 3), 0)
    total = sum(c.values()) or 1
    return {k: round(v/total*100,1) for k,v in c.items()}


def classify_type(r):
    for cl, info in ONTOLOGY.items():
        if info["condition"](r): return cl
    return "NEW"


def detect_new_patterns(df):
    out = []
    for _, row in df.iterrows():
        r = row.to_dict()
        if compute_score(r) >= 0.7 and classify_type(r) == "NEW":
            out.append(r["고객ID"])
    return out


# ══════════════════════════════════════
# 헤더
# ══════════════════════════════════════
st.markdown("""
<div class="main-header">
    <div class="main-title">🎯 고객 이탈 원인 분석 및 초개인화 리텐션 Agent</div>
    <div class="main-sub">XAI 기반 이탈 원인 진단 → 처방 → 자동 실행</div>
    <div class="badge-row">
        <span class="badge">XAI 기반</span>
        <span class="badge">온톨로지 분류</span>
        <span class="badge">Human-in-the-Loop</span>
        <span class="badge">초개인화 리텐션</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════
# STEP 1 — 데이터 업로드
# ══════════════════════════════════════
st.markdown('<div class="step-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">STEP 01</div><div class="step-title">📂 고객 데이터 업로드</div>', unsafe_allow_html=True)

col_up, col_demo = st.columns([3, 1])
with col_up:
    uploaded = st.file_uploader(
        "고객 데이터 CSV 파일을 업로드하세요",
        type=["csv"], label_visibility="collapsed"
    )
    st.markdown("""<div class="upload-hint">
        CSV 컬럼: 고객ID · 이용빈도변화율 · 이용금액변화율 · 민원발생횟수 · 해지문의여부 · 포인트소멸예정금액
    </div>""", unsafe_allow_html=True)
with col_demo:
    st.markdown("<br>", unsafe_allow_html=True)
    use_demo = st.button("🔍 더미 데이터\n시연하기", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

df = None
if use_demo or "demo" in st.session_state:
    st.session_state["demo"] = True
    np.random.seed(42)
    n = 30
    df = pd.DataFrame({
        "고객ID": [f"C{str(i).zfill(4)}" for i in range(1, n+1)],
        "이용빈도변화율": np.random.choice([-55,-40,-30,-20,-10,0,5,10], n),
        "이용금액변화율": np.random.choice([-60,-45,-35,-20,-10,0,5], n),
        "민원발생횟수": np.random.choice([0,0,0,1,2,3], n),
        "해지문의여부": np.random.choice([0,0,0,1], n),
        "포인트소멸예정금액": np.random.choice([0,0,10000,30000,70000], n),
    })
    st.success(f"✅ 더미 데이터 로드 완료 — 고객 {n}명")
elif uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"✅ 업로드 완료 — 고객 {len(df)}명")


# ══════════════════════════════════════
# STEP 2 — 분석 실행
# ══════════════════════════════════════
if df is not None:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-label">STEP 02</div><div class="step-title">🤖 Agent 분석 실행</div>', unsafe_allow_html=True)
    run = st.button("▶ 이탈 원인 분석 시작", use_container_width=False)
    st.markdown('</div>', unsafe_allow_html=True)

    if run or "done" in st.session_state:
        st.session_state["done"] = True

        with st.spinner("XAI 변수 기여도 분석 및 온톨로지 유형 분류 중..."):
            results = []
            for _, row in df.iterrows():
                r = row.to_dict()
                score = compute_score(r)
                contribs = compute_contributions(r, score)
                cl = classify_type(r)
                if cl != "NEW":
                    info = ONTOLOGY[cl]
                    results.append({"고객ID":r["고객ID"],"이탈점수":score,"이탈유형":cl,
                        "유형명":info["name"],"color":info["color"],"icon":info["icon"],
                        "기여도":contribs,"추천오퍼":info["offer"],"오퍼상세":info["offer_detail"],
                        "주요원인":f"{VAR_KR.get(max(contribs,key=contribs.get))} ({max(contribs.values())}%)"})
                else:
                    results.append({"고객ID":r["고객ID"],"이탈점수":score,"이탈유형":"NEW",
                        "유형명":"신규 패턴","color":"type-new","icon":"⚪",
                        "기여도":contribs,"추천오퍼":"신규 패턴 — 검토 필요","오퍼상세":"기존 유형에 해당하지 않는 패턴",
                        "주요원인":f"{VAR_KR.get(max(contribs,key=contribs.get))} ({max(contribs.values())}%)"})

        res_df = pd.DataFrame(results)
        high = res_df[res_df["이탈점수"] >= 0.7].sort_values("이탈점수", ascending=False)
        new_pts = detect_new_patterns(df)

        # ── STEP 3: 분석 결과 ──
        st.markdown('<div class="step-card">', unsafe_allow_html=True)
        st.markdown('<div class="step-label">STEP 03</div><div class="step-title">📊 분석 결과 — 이탈 원인 진단</div>', unsafe_allow_html=True)

        n_types = res_df[res_df["이탈유형"]!="NEW"]["이탈유형"].nunique()
        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-num">{len(df)}<span style="font-size:16px">명</span></div>
                <div class="kpi-label">전체 분석 고객</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-num" style="color:#E53935">{len(high)}<span style="font-size:16px">명</span></div>
                <div class="kpi-label">고위험 고객<br>(이탈점수 0.7↑)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-num">{n_types}<span style="font-size:16px">종</span></div>
                <div class="kpi-label">이탈 유형 분류</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-num" style="color:#FF8F00">{len(new_pts)}<span style="font-size:16px">명</span></div>
                <div class="kpi-label">신규 패턴 감지</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if len(new_pts) >= 3:
            st.markdown(f"""
            <div class="alert-box">
                <div class="alert-title">⚠️ 신규 이탈 패턴 감지 Alert</div>
                기존 CL_1/2/3에 해당하지 않는 고위험 고객 <b>{len(new_pts)}명</b>이 감지되었습니다.
                새로운 이탈 유형 추가를 검토해 주세요.<br>
                <span style="font-size:12px;color:#999">대상: {', '.join(new_pts[:5])} 외 {max(0,len(new_pts)-5)}명</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("**🔴 고위험 이탈 고객 상세 분석**")

        for _, r in high.head(9).iterrows():
            sc = "score-high" if r["이탈점수"] >= 0.8 else "score-mid"
            top3 = sorted(r["기여도"].items(), key=lambda x:x[1], reverse=True)[:3]
            bars = "".join([
                f'<div class="bar-wrap">'
                f'<div class="bar-label"><span>{VAR_KR.get(v,v)}</span><span style="font-weight:700;color:#0046AD">{p}%</span></div>'
                f'<div class="bar-bg"><div class="bar-fill" style="width:{p}%"></div></div>'
                f'</div>' for v,p in top3
            ])
            score_color = "#E53935" if r["이탈점수"] >= 0.8 else "#FB8C00"
            st.markdown(f"""
            <div class="result-card {sc}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px;">
                    <div style="display:flex;align-items:center;gap:10px;">
                        <span style="font-size:16px;font-weight:900;color:#0B1F4E;">{r['고객ID']}</span>
                        <span class="{r['color']}">{r['icon']} {r['유형명']}</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;">
                        <span style="font-size:12px;color:#888;">이탈 점수</span>
                        <span style="font-size:26px;font-weight:900;color:{score_color};">{r['이탈점수']}</span>
                    </div>
                </div>
                <div style="font-size:12px;color:#666;margin-bottom:12px;padding:8px 12px;background:#F8FAFF;border-radius:8px;">
                    📌 주요 이탈 원인: <b style="color:#0046AD">{r['주요원인']}</b>
                </div>
                {bars}
                <div style="margin-top:14px;padding-top:12px;border-top:1px solid #EEF3FF;display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                    <span style="font-size:11.5px;color:#888;font-weight:600;">추천 오퍼</span>
                    <span class="offer-badge">{r['추천오퍼']}</span>
                    <span style="font-size:11px;color:#777;">{r['오퍼상세']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── STEP 4: Human-in-the-Loop ──
        st.markdown('<div class="step-card">', unsafe_allow_html=True)
        st.markdown('<div class="step-label">STEP 04 · Human-in-the-Loop</div><div class="step-title">✅ 현업 검토 및 캠페인 승인</div>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:13px;color:#555;margin-bottom:16px;">'
            'Agent가 제안한 리텐션 오퍼를 검토하고 실행을 승인해 주세요.</p>',
            unsafe_allow_html=True
        )
        c1, c2, c3 = st.columns(3)
        with c1: approve = st.button("✅ 전체 승인 후 캠페인 실행", use_container_width=True)
        with c2: st.button("✏️ 일부 수정 후 실행", use_container_width=True)
        with c3: st.button("⏸ 보류", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── STEP 5: 캠페인 실행 ──
        if approve or "camp" in st.session_state:
            st.session_state["camp"] = True

            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown('<div class="step-label">STEP 05</div><div class="step-title">🚀 리텐션 캠페인 실행 완료</div>', unsafe_allow_html=True)
            st.success(f"✅ {len(high)}명 대상 초개인화 리텐션 캠페인이 실행되었습니다.")

            cl1 = len(high[high["이탈유형"]=="CL_1"])
            cl2 = len(high[high["이탈유형"]=="CL_2"])
            cl3 = len(high[high["이탈유형"]=="CL_3"])

            st.markdown(f"""
            <div class="result-summary">
                <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-bottom:4px;">
                    {datetime.now().strftime('%Y-%m-%d %H:%M')} · 캠페인 실행 현황
                </div>
                <div class="summary-grid">
                    <div>
                        <div class="summary-num">{len(high)}</div>
                        <div class="summary-label">총 발송 대상</div>
                    </div>
                    <div>
                        <div class="summary-num">{cl1}</div>
                        <div class="summary-label">CL_1 카페쿠폰</div>
                    </div>
                    <div>
                        <div class="summary-num">{cl2}</div>
                        <div class="summary-label">CL_2 외식할인</div>
                    </div>
                    <div>
                        <div class="summary-num">{cl3}</div>
                        <div class="summary-label">CL_3 캐시백</div>
                    </div>
                </div>
                <div style="margin-top:20px;padding-top:14px;border-top:1px solid rgba(255,255,255,0.12);
                            font-size:12px;color:rgba(255,255,255,0.45);">
                    Push / LMS / 카카오톡 채널 자동 선택 완료 · 성과 데이터는 24시간 후 자동 수집됩니다
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── STEP 6: 성과 리포트 ──
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.markdown('<div class="step-label">STEP 06 · 성과 리포트</div><div class="step-title">📈 캠페인 성과 리포트 (시뮬레이션)</div>', unsafe_allow_html=True)

            sim_rate = round(random.uniform(28, 42), 1)
            sim_save = int(len(high) * sim_rate / 100)

            m1, m2, m3 = st.columns(3)
            m1.metric("예상 리텐션 전환율", f"{sim_rate}%", f"+{round(sim_rate-18,1)}%p vs 기존 일괄 오퍼")
            m2.metric("이탈 방어 예상 고객", f"{sim_save}명")
            m3.metric("오퍼 비용 효율", "↑ 개선", "원인별 맞춤 오퍼 적용")

            st.markdown("""
            <div class="quote-box">
                "이제 마케터의 역할은 데이터를 찾는 것이 아니라,<br>
                Agent가 발견한 인사이트를 바탕으로 더 나은 마케팅 방식을 고민하는 것으로 전환됩니다."
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ── 푸터 ──
st.markdown("""
<div style="text-align:center;padding:28px 0 8px;color:#BBC8DD;font-size:11.5px;letter-spacing:0.04em;">
    고객 이탈 원인 분석 및 초개인화 리텐션 Agent (XAI 기반)
</div>
""", unsafe_allow_html=True)
