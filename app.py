import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

st.set_page_config(
    page_title="이탈 원인 분석 리텐션 Agent",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+KR:wght@400;500;700&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Noto Sans KR', 'Inter', sans-serif !important;
}
.stApp { background: #F7F8FA !important; }
.block-container { max-width: 1060px !important; padding: 2rem 2rem 4rem !important; margin: 0 auto !important; }

/* ─── 헤더 ─── */
.hdr {
    background: #111827;
    border-radius: 14px;
    padding: 28px 36px;
    margin-bottom: 28px;
}
.hdr-title { font-size: 20px; font-weight: 700; color: #F9FAFB; margin: 0 0 4px; letter-spacing: -0.3px; }
.hdr-sub   { font-size: 12.5px; color: #6B7280; margin: 0 0 14px; }
.hdr-tags  { display: flex; gap: 8px; flex-wrap: wrap; }
.tag {
    font-size: 11px; font-weight: 600; color: #9CA3AF;
    border: 1px solid #374151; border-radius: 20px;
    padding: 3px 11px; letter-spacing: 0.03em;
}

/* ─── 섹션 ─── */
.step-tag  { font-size: 10.5px; font-weight: 700; color: #6B7280; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 3px; }
.step-head { font-size: 15px; font-weight: 700; color: #111827; margin-bottom: 14px; }

/* ─── KPI ─── */
.kpi-row { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
.kpi {
    flex: 1; min-width: 110px;
    background: #fff; border: 1px solid #E5E7EB;
    border-radius: 10px; padding: 14px 16px;
    text-align: left;
}
.kpi-val  { font-size: 24px; font-weight: 700; color: #111827; line-height: 1; margin-bottom: 3px; }
.kpi-val.r{ color: #DC2626; }
.kpi-val.a{ color: #D97706; }
.kpi-lbl  { font-size: 11px; color: #6B7280; line-height: 1.4; }

/* ─── 유형 분포 카드 ─── */
.type-dist { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 20px; }
.td-card {
    flex: 1; min-width: 120px;
    background: #fff; border: 1px solid #E5E7EB;
    border-radius: 10px; padding: 14px 14px;
    text-align: center;
}
.td-icon  { font-size: 18px; margin-bottom: 6px; }
.td-name  { font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 4px; }
.td-count { font-size: 22px; font-weight: 700; color: #111827; }
.td-strat { font-size: 10px; color: #9CA3AF; margin-top: 3px; line-height: 1.3; }

/* ─── 고객 결과 카드 ─── */
.cust-card {
    background: #fff; border: 1px solid #E5E7EB;
    border-radius: 12px; padding: 18px 20px;
    margin-bottom: 10px;
    border-left: 4px solid #DC2626;
}
.cust-card.mid { border-left-color: #D97706; }
.cust-card.low { border-left-color: #059669; }

.cust-top {
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: 10px;
    flex-wrap: wrap; gap: 8px;
}
.cust-id   { font-size: 15px; font-weight: 700; color: #111827; }
.score-chip {
    font-size: 18px; font-weight: 700;
    padding: 3px 12px; border-radius: 8px;
}
.score-h { color: #DC2626; background: #FEF2F2; }
.score-m { color: #D97706; background: #FFFBEB; }

.type-pill {
    font-size: 11px; font-weight: 600;
    border-radius: 20px; padding: 2px 10px;
    display: inline-block;
}
.p-신판이용   { color: #1D4ED8; background: #EFF6FF; border: 1px solid #BFDBFE; }
.p-타사이용   { color: #6D28D9; background: #F5F3FF; border: 1px solid #DDD6FE; }
.p-잔여포인트 { color: #047857; background: #ECFDF5; border: 1px solid #A7F3D0; }
.p-고객불만   { color: #B91C1C; background: #FEF2F2; border: 1px solid #FECACA; }
.p-카드보유   { color: #B45309; background: #FFFBEB; border: 1px solid #FDE68A; }
.p-디지털이용 { color: #0E7490; background: #ECFEFF; border: 1px solid #A5F3FC; }
.p-new        { color: #9A3412; background: #FFF7ED; border: 1px solid #FED7AA; }

/* ─── 기여도 바 ─── */
.bar-wrap  { margin: 5px 0; }
.bar-label { display: flex; justify-content: space-between; font-size: 11.5px; color: #374151; margin-bottom: 2px; }
.bar-track { background: #F3F4F6; border-radius: 4px; height: 6px; width: 100%; overflow: hidden; }
.bar-fill  { background: #3B82F6; border-radius: 4px; height: 6px; }

/* ─── 원인 하이라이트 ─── */
.cause-box {
    background: #F9FAFB; border: 1px solid #E5E7EB;
    border-radius: 8px; padding: 8px 12px;
    font-size: 11.5px; color: #374151; margin-bottom: 10px;
}

/* ─── 오퍼 ─── */
.offer-pill {
    display: inline-block;
    font-size: 11.5px; font-weight: 600;
    color: #1D4ED8; background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 20px; padding: 3px 12px; margin-right: 6px;
}
.offer-detail { font-size: 11px; color: #6B7280; }

/* ─── Alert ─── */
.alert-box {
    background: #FFFBEB; border: 1px solid #FDE68A;
    border-left: 4px solid #F59E0B;
    border-radius: 10px; padding: 14px 18px; margin: 14px 0;
}
.alert-ttl { font-size: 13px; font-weight: 700; color: #92400E; margin-bottom: 4px; }
.alert-txt { font-size: 12px; color: #78350F; }

/* ─── 승인 박스 ─── */
.approve-box {
    background: #fff; border: 1px solid #E5E7EB;
    border-radius: 12px; padding: 20px 24px; margin-bottom: 16px;
}
.approve-label { font-size: 12px; color: #6B7280; margin-bottom: 10px; }

/* ─── 성과 박스 ─── */
.result-box {
    background: #111827; border-radius: 12px;
    padding: 24px 28px; margin-top: 16px;
}
.result-row { display: flex; gap: 24px; flex-wrap: wrap; margin-top: 14px; }
.result-item { flex: 1; min-width: 80px; }
.result-num { font-size: 26px; font-weight: 700; color: #60A5FA; line-height: 1; margin-bottom: 3px; }
.result-lbl { font-size: 11px; color: #9CA3AF; }
.result-footer { font-size: 11px; color: #4B5563; margin-top: 16px; padding-top: 14px; border-top: 1px solid #1F2937; }

/* ─── 인용 ─── */
.quote-box {
    background: #EFF6FF; border-left: 4px solid #3B82F6;
    border-radius: 0 10px 10px 0; padding: 14px 20px; margin-top: 14px;
    font-size: 12.5px; color: #1E40AF; font-style: italic; line-height: 1.8;
}

/* ─── 버튼 ─── */
.stButton > button {
    background: #111827 !important; color: #F9FAFB !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; font-family: 'Noto Sans KR', sans-serif !important;
    padding: 10px 20px !important; font-size: 13px !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: #1F2937 !important; }

/* ─── 미리보기 ─── */
[data-testid="stExpander"] { background: #fff !important; border: 1px solid #E5E7EB !important; border-radius: 10px !important; }
[data-testid="metric-container"] {
    background: #fff !important; border: 1px solid #E5E7EB !important;
    border-radius: 10px !important; padding: 12px 16px !important;
}
[data-testid="stMetricValue"] > div { color: #111827 !important; }
[data-testid="stMetricLabel"] > div { color: #6B7280 !important; }
[data-testid="stMetricDelta"] > div { font-size: 12px !important; }

div[data-testid="stDataFrame"] { border: 1px solid #E5E7EB !important; border-radius: 8px !important; }
.stSlider > div > div > div { color: #111827 !important; }
label[data-testid="stWidgetLabel"] > div > p { color: #374151 !important; font-size: 13px !important; }
.stCaption > div > p { color: #9CA3AF !important; }
.stSuccess { background: #ECFDF5 !important; color: #065F46 !important; border: 1px solid #A7F3D0 !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ══ 온톨로지 ══
ONTOLOGY = {
    "Var1":  {"name":"최근일주일내이용건수",        "type":"신판이용",   "dir":"LOW"},
    "Var2":  {"name":"한달전대비이용금액증감률",     "type":"신판이용",   "dir":"LOW"},
    "Var3":  {"name":"일주일전대비이용금액증감률",   "type":"신판이용",   "dir":"LOW"},
    "Var4":  {"name":"타사카드신규개설여부",         "type":"타사이용",   "dir":"HIGH"},
    "Var5":  {"name":"최근한달타사카드이용금액증감률","type":"타사이용",   "dir":"HIGH"},
    "Var6":  {"name":"최근한달타사대비당사이용비율", "type":"타사이용",   "dir":"LOW"},
    "Var7":  {"name":"최근한달포인트사용량",         "type":"잔여포인트", "dir":"HIGH"},
    "Var8":  {"name":"포인트잔여량",                "type":"잔여포인트", "dir":"LOW"},
    "Var9":  {"name":"최근포인트증가여부",           "type":"잔여포인트", "dir":"LOW"},
    "Var10": {"name":"최근민원발생빈도",             "type":"고객불만",   "dir":"HIGH"},
    "Var11": {"name":"최근VOC발생빈도",              "type":"고객불만",   "dir":"HIGH"},
    "Var12": {"name":"최근온라인민원접수빈도",        "type":"고객불만",   "dir":"HIGH"},
    "Var13": {"name":"한달내만기대상카드존재여부",   "type":"카드보유",   "dir":"HIGH"},
    "Var14": {"name":"최근보유카드탈회수",           "type":"카드보유",   "dir":"HIGH"},
    "Var15": {"name":"최근카드분실신고여부",         "type":"카드보유",   "dir":"HIGH"},
    "Var16": {"name":"최근한달앱접속건수",           "type":"디지털이용", "dir":"LOW"},
    "Var17": {"name":"디지털이용빈도증감률",         "type":"디지털이용", "dir":"LOW"},
    "Var18": {"name":"마케팅Push개봉건수",           "type":"디지털이용", "dir":"LOW"},
}
TYPE_STRATEGY = {
    "신판이용":   ("무이자할부 제공",                "당월 50만원 이상 이용 시 3개월 무이자할부"),
    "타사이용":   ("신판 30만원 추가이용 시 캐시백", "전월 대비 30만원 추가 이용 시 3만원 캐시백"),
    "잔여포인트": ("외식업종 포인트 2배",            "외식업종 이용 시 포인트 2배 적립"),
    "고객불만":   ("5천 포인트 제공",                "즉시 5,000 포인트 + VOC 전담 상담사 연결"),
    "카드보유":   ("추가 카드 발급 시 연회비 할인",  "신규 카드 발급 시 첫 해 연회비 100% 면제"),
    "디지털이용": ("앱 접속 시 투썸 쿠폰",           "앱 로그인 시 투썸플레이스 아메리카노 쿠폰 발송"),
}
TYPE_ICONS = {"신판이용":"💳","타사이용":"🔄","잔여포인트":"⭐","고객불만":"📞","카드보유":"🪪","디지털이용":"📱"}
VAR_COLS = [f"Var{i}" for i in range(1, 19)]

def calc_contribs(row, avgs):
    c = {}
    for var, info in ONTOLOGY.items():
        v = float(row.get(var, 0.5))
        a = float(avgs.get(var, 0.5))
        c[var] = max(0.0, a - v) if info["dir"] == "LOW" else max(0.0, v - a)
    total = sum(c.values()) or 1.0
    return {k: round(v / total * 100, 1) for k, v in c.items()}

def dominant_type(cb):
    ts = {}
    for var, pct in cb.items():
        t = ONTOLOGY[var]["type"]
        ts[t] = ts.get(t, 0) + pct
    dom = max(ts, key=ts.get)
    top2 = sorted(ts.values(), reverse=True)[:2]
    is_new = (top2[0] + (top2[1] if len(top2) > 1 else 0)) < 40
    return dom, ts, is_new

# ══ 헤더 ══
st.markdown("""
<div class="hdr">
  <div class="hdr-title">고객 이탈 원인 분석 및 초개인화 리텐션 Agent</div>
  <div class="hdr-sub">XAI 기반 이탈 원인 진단 → 온톨로지 유형 분류 → 맞춤 리텐션 자동 실행</div>
  <div class="hdr-tags">
    <span class="tag">XAI 기반</span>
    <span class="tag">온톨로지 분류</span>
    <span class="tag">Human-in-the-Loop</span>
    <span class="tag">초개인화 리텐션</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══ STEP 1 ══
st.markdown('<div class="step-tag">STEP 01</div><div class="step-head">고객 데이터 업로드</div>', unsafe_allow_html=True)

col_u, col_d = st.columns([3, 1])
with col_u:
    uploaded = st.file_uploader("CSV 또는 Excel 업로드", type=["csv","xlsx"], label_visibility="collapsed")
    st.caption("필수 컬럼: 고객번호, Var1~Var18 (0~1 스케일링 값), Score")
with col_d:
    st.markdown("<br>", unsafe_allow_html=True)
    use_demo = st.button("더미 데이터 시연", use_container_width=True)

st.divider()

df = None
if use_demo or "demo" in st.session_state:
    st.session_state["demo"] = True
    np.random.seed(99); n = 50
    demo = {"고객번호": [f"CL_{str(i).zfill(3)}" for i in range(1, n+1)]}
    for i in range(1, 19):
        demo[f"Var{i}"] = np.random.uniform(0, 1, n).round(4)
    df = pd.DataFrame(demo)
    weights = {"Var1":-0.08,"Var2":-0.07,"Var3":-0.07,"Var4":0.09,"Var5":0.08,"Var6":-0.07,
               "Var7":0.06,"Var8":-0.05,"Var9":-0.05,"Var10":0.09,"Var11":0.08,"Var12":0.07,
               "Var13":0.06,"Var14":0.05,"Var15":0.04,"Var16":-0.05,"Var17":-0.04,"Var18":-0.04}
    scores = []
    for _, row in df.iterrows():
        r = row.to_dict()
        s = sum((r[v] - 0.5) * w * 2 for v, w in weights.items())
        scores.append(round(s, 6))
    df["Score"] = scores
    st.success(f"더미 데이터 {n}명 로드 완료")

elif uploaded:
    try:
        df = pd.read_csv(uploaded) if uploaded.name.endswith('.csv') else pd.read_excel(uploaded)
        df.columns = [c.strip() for c in df.columns]
        st.success(f"업로드 완료 — 총 {len(df)}명")
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")

# ══ 미리보기 ══
if df is not None:
    id_col = "고객번호" if "고객번호" in df.columns else df.columns[0]
    avail_vars = [v for v in VAR_COLS if v in df.columns]

    with st.expander("데이터 미리보기 및 통계", expanded=False):
        t1, t2, t3 = st.tabs(["데이터 미리보기", "변수 통계", "Score 분포"])
        with t1:
            show = [id_col] + avail_vars[:9] + (["Score"] if "Score" in df.columns else [])
            st.dataframe(df[show].head(20), use_container_width=True, height=280)
        with t2:
            stat = df[avail_vars].describe().T.round(4)
            stat["변수명"] = [ONTOLOGY[v]["name"] for v in stat.index]
            stat["유형"]  = [ONTOLOGY[v]["type"]  for v in stat.index]
            st.dataframe(
                stat[["변수명","유형","mean","std","min","max"]].rename(
                    columns={"mean":"평균","std":"표준편차","min":"최솟값","max":"최댓값"}),
                use_container_width=True, height=380)
        with t3:
            if "Score" in df.columns:
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("평균", f"{df['Score'].mean():.4f}")
                c2.metric("최고", f"{df['Score'].max():.4f}")
                c3.metric("최저", f"{df['Score'].min():.4f}")
                c4.metric("표준편차", f"{df['Score'].std():.4f}")
                st.bar_chart(df.set_index(id_col)["Score"].sort_values(ascending=False))
            else:
                st.info("Score 컬럼이 없습니다.")

    st.divider()

    # ══ STEP 2 ══
    st.markdown('<div class="step-tag">STEP 02</div><div class="step-head">분석 설정 및 실행</div>', unsafe_allow_html=True)
    col_sl, col_btn = st.columns([4, 1])
    with col_sl:
        threshold = st.slider(
            "이탈 위험 임계값 (Score 기준 — 이 값 이상인 고객을 고위험으로 분류)",
            0.0, 0.5, 0.1, 0.01
        )
    with col_btn:
        st.markdown("<br><br>", unsafe_allow_html=True)
        run = st.button("분석 실행", use_container_width=True)
    st.divider()

    if run or "done" in st.session_state:
        st.session_state["done"] = True
        st.session_state["thr"] = threshold
        thr = st.session_state.get("thr", 0.1)

        with st.spinner("XAI 변수 기여도 분석 및 온톨로지 유형 분류 중..."):
            avgs = {v: float(df[v].mean()) for v in avail_vars}
            rows = []
            for _, row in df.iterrows():
                r = row.to_dict()
                sc = float(r.get("Score", 0))
                cb = calc_contribs(r, avgs)
                dom, ts, is_new = dominant_type(cb)
                strat, detail = TYPE_STRATEGY[dom]
                top3 = sorted(cb.items(), key=lambda x: x[1], reverse=True)[:3]
                rows.append({
                    "고객ID": r[id_col], "Score": sc,
                    "주요유형": dom, "type_scores": ts, "is_new": is_new,
                    "기여도": cb, "top3": top3,
                    "전략": strat, "전략상세": detail,
                    "주요원인": ONTOLOGY[top3[0][0]]["name"],
                    "주요원인_pct": top3[0][1],
                })

        res = pd.DataFrame(rows)
        high = res[res["Score"] >= thr].sort_values("Score", ascending=False)
        new_pats = res[(res["Score"] >= thr) & res["is_new"]]

        # ── STEP 3 ──
        st.markdown('<div class="step-tag">STEP 03</div><div class="step-head">분석 결과 — 이탈 원인 진단</div>', unsafe_allow_html=True)

        n_types = int(high["주요유형"].nunique()) if len(high) > 0 else 0
        st.markdown(
            f'<div class="kpi-row">'
            f'<div class="kpi"><div class="kpi-val">{len(df)}</div><div class="kpi-lbl">전체 분석 고객</div></div>'
            f'<div class="kpi"><div class="kpi-val r">{len(high)}</div><div class="kpi-lbl">고위험 고객<br>(Score ≥ {thr:.2f})</div></div>'
            f'<div class="kpi"><div class="kpi-val">{n_types}</div><div class="kpi-lbl">감지된 이탈 유형</div></div>'
            f'<div class="kpi"><div class="kpi-val a">{len(new_pats)}</div><div class="kpi-lbl">신규 복합 패턴</div></div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # 유형별 분포
        if len(high) > 0:
            type_dist = high["주요유형"].value_counts().to_dict()
            td_html = '<div class="type-dist">'
            for tp, cnt in sorted(type_dist.items(), key=lambda x: x[1], reverse=True):
                icon = TYPE_ICONS.get(tp, "")
                strat, _ = TYPE_STRATEGY[tp]
                td_html += (
                    f'<div class="td-card">'
                    f'<div class="td-icon">{icon}</div>'
                    f'<div class="td-name">{tp}</div>'
                    f'<div class="td-count">{cnt}명</div>'
                    f'<div class="td-strat">{strat}</div>'
                    f'</div>'
                )
            td_html += '</div>'
            st.markdown(td_html, unsafe_allow_html=True)

        if len(new_pats) > 0:
            ids_str = ", ".join(str(x) for x in list(new_pats["고객ID"])[:5])
            st.markdown(
                f'<div class="alert-box">'
                f'<div class="alert-ttl">⚠ 신규 복합 이탈 패턴 Alert</div>'
                f'<div class="alert-txt">단일 유형으로 분류되지 않는 복합 패턴 고객 <b>{len(new_pats)}명</b> 감지.'
                f' 온톨로지 신규 유형 추가를 검토해 주세요.<br>'
                f'<span style="font-size:11px;color:#92400E">대상: {ids_str} 등</span></div>'
                f'</div>',
                unsafe_allow_html=True
            )

        if len(high) > 0:
            st.markdown(
                '<p style="font-size:13px;font-weight:700;color:#111827;margin:16px 0 10px">고위험 이탈 고객 상세 분석</p>',
                unsafe_allow_html=True
            )
            for _, r in high.head(10).iterrows():
                sc_val = float(r["Score"])
                card_cls = "cust-card" if sc_val >= 0.3 else "cust-card mid"
                chip_cls = "score-chip score-h" if sc_val >= 0.3 else "score-chip score-m"
                tp = str(r["주요유형"])
                pill_cls = f"type-pill p-{tp}"
                if r["is_new"]:
                    pill_cls = "type-pill p-new"
                    tp_label = f"{tp} (신규패턴)"
                else:
                    tp_label = tp

                # 기여도 바
                bars = ""
                for v, p in r["top3"]:
                    vname = ONTOLOGY[v]["name"]
                    vtype = ONTOLOGY[v]["type"]
                    bars += (
                        f'<div class="bar-wrap">'
                        f'<div class="bar-label">'
                        f'<span style="color:#374151">{vname}'
                        f'<span style="font-size:10px;color:#9CA3AF;margin-left:4px">({vtype})</span></span>'
                        f'<span style="color:#1D4ED8;font-weight:600">{p}%</span>'
                        f'</div>'
                        f'<div class="bar-track"><div class="bar-fill" style="width:{p}%"></div></div>'
                        f'</div>'
                    )

                # 유형 분포 미니
                type_row = ""
                for t, s in sorted(r["type_scores"].items(), key=lambda x: x[1], reverse=True)[:3]:
                    type_row += (
                        f'<span style="font-size:11px;color:#6B7280;margin-right:12px">'
                        f'{TYPE_ICONS.get(t,"")} {t} '
                        f'<span style="font-weight:600;color:#374151">{round(s,1)}%</span></span>'
                    )

                st.markdown(
                    f'<div class="{card_cls}">'
                    f'<div class="cust-top">'
                    f'<div style="display:flex;align-items:center;gap:8px">'
                    f'<span class="cust-id">{r["고객ID"]}</span>'
                    f'<span class="{pill_cls}">{TYPE_ICONS.get(r["주요유형"],"")} {tp_label}</span>'
                    f'</div>'
                    f'<span class="{chip_cls}">{round(sc_val, 4)}</span>'
                    f'</div>'
                    f'<div style="font-size:11px;color:#6B7280;margin-bottom:8px">{type_row}</div>'
                    f'<div class="cause-box">'
                    f'주요 이탈 원인: <span style="color:#1D4ED8;font-weight:600">'
                    f'{r["주요원인"]} ({r["주요원인_pct"]}%)</span>'
                    f'</div>'
                    f'{bars}'
                    f'<div style="margin-top:12px;padding-top:10px;border-top:1px solid #F3F4F6;'
                    f'display:flex;align-items:center;gap:8px;flex-wrap:wrap">'
                    f'<span style="font-size:11px;color:#9CA3AF;font-weight:600">추천 리텐션</span>'
                    f'<span class="offer-pill">{r["전략"]}</span>'
                    f'<span class="offer-detail">{r["전략상세"]}</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info(f"임계값 {thr:.2f} 이상인 고위험 고객이 없습니다. 슬라이더를 낮춰보세요.")

        st.divider()

        # ── STEP 4 ──
        st.markdown('<div class="step-tag">STEP 04 · Human-in-the-Loop</div><div class="step-head">현업 검토 및 캠페인 승인</div>', unsafe_allow_html=True)
        st.markdown(
            '<p style="font-size:12.5px;color:#6B7280;margin-bottom:14px">'
            'Agent가 분석한 리텐션 전략을 검토하고 실행을 승인해 주세요.</p>',
            unsafe_allow_html=True
        )
        ca, cb_, cc = st.columns(3)
        with ca: approve = st.button("전체 승인 후 캠페인 실행", use_container_width=True)
        with cb_: st.button("일부 수정 후 실행", use_container_width=True)
        with cc:  st.button("보류", use_container_width=True)
        st.divider()

        # ── STEP 5 ──
        if approve or "camp" in st.session_state:
            st.session_state["camp"] = True
            st.markdown('<div class="step-tag">STEP 05</div><div class="step-head">리텐션 캠페인 실행 완료</div>', unsafe_allow_html=True)
            st.success(f"{len(high)}명 대상 초개인화 리텐션 캠페인이 실행되었습니다.")

            type_counts = high["주요유형"].value_counts().to_dict()
            items_html = "".join(
                f'<div class="result-item">'
                f'<div class="result-num">{cnt}</div>'
                f'<div class="result-lbl">{TYPE_ICONS.get(tp,"")} {tp}</div>'
                f'</div>'
                for tp, cnt in type_counts.items()
            )
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            st.markdown(
                f'<div class="result-box">'
                f'<div style="font-size:11px;color:#6B7280;margin-bottom:2px">{now_str} · 캠페인 실행 현황</div>'
                f'<div class="result-row">'
                f'<div class="result-item"><div class="result-num">{len(high)}</div><div class="result-lbl">총 발송 대상</div></div>'
                f'{items_html}'
                f'</div>'
                f'<div class="result-footer">Push / LMS / 카카오톡 채널 자동 선택 완료 · 성과 데이터는 24시간 후 자동 수집됩니다</div>'
                f'</div>',
                unsafe_allow_html=True
            )
            st.divider()

            # ── STEP 6 ──
            st.markdown('<div class="step-tag">STEP 06 · 성과 리포트</div><div class="step-head">캠페인 성과 리포트 (시뮬레이션)</div>', unsafe_allow_html=True)
            sim = round(random.uniform(28, 44), 1)
            sim_s = int(len(high) * sim / 100)
            m1, m2, m3 = st.columns(3)
            m1.metric("예상 리텐션 전환율", f"{sim}%", f"+{round(sim-18,1)}%p vs 기존 일괄 오퍼")
            m2.metric("이탈 방어 예상 고객", f"{sim_s}명")
            m3.metric("오퍼 비용 효율", "↑ 개선", "유형별 맞춤 오퍼 적용")
            st.markdown(
                '<div class="quote-box">'
                '"이제 마케터의 역할은 데이터를 찾는 것이 아니라,<br>'
                'Agent가 발견한 인사이트를 바탕으로 더 나은 마케팅 방식을 고민하는 것으로 전환됩니다."'
                '</div>',
                unsafe_allow_html=True
            )

st.markdown(
    '<div style="text-align:center;padding:36px 0 8px;color:#D1D5DB;font-size:11px">'
    '고객 이탈 원인 분석 및 초개인화 리텐션 Agent (XAI 기반)'
    '</div>',
    unsafe_allow_html=True
)
