import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

st.set_page_config(
    page_title="고객 이탈 원인 분석 리텐션 Agent",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');

:root {
  --shinhan: #0046FF;
  --shinhan-d: #0036CC;
  --shinhan-l: #E8EFFF;
  --ink: #0F1A33;
  --body: #374151;
  --sub: #6B7280;
  --line: #E5E7EB;
  --bg: #F5F6F8;
  --card: #FFFFFF;
  --warn: #E84B4B;
  --warn-l: #FEF2F2;
  --gold: #FFB800;
  --gold-l: #FFF8E1;
}

html, body, [class*="css"], .stApp, .stMarkdown, button, input, textarea, select {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Noto Sans KR', sans-serif !important;
  letter-spacing: -0.01em;
}

.stApp { background: var(--bg); }
.block-container { padding-top: 0 !important; padding-bottom: 4rem; max-width: 880px; }
header[data-testid="stHeader"] { background: transparent; height: 0; }
#MainMenu, footer { visibility: hidden; }

/* ── 페이지 헤더 ── */
.page-header {
  padding: 28px 0 26px;
  margin-bottom: 8px;
  border-bottom: 1px solid var(--line);
}
.page-title {
  font-size: 24px; font-weight: 700; color: var(--ink);
  letter-spacing: -0.03em; line-height: 1.35;
  margin: 0 0 8px;
}
.page-desc {
  font-size: 13.5px; color: var(--sub); line-height: 1.6;
  margin: 0;
}

/* ── 섹션 헤더 ── */
.section-block { margin: 32px 0 16px; }
.section-num {
  font-size: 11.5px; font-weight: 700; color: var(--shinhan);
  letter-spacing: 0.06em; margin-bottom: 6px;
}
.section-title {
  font-size: 20px; font-weight: 700; color: var(--ink);
  letter-spacing: -0.025em; margin: 0 0 4px;
}
.section-desc {
  font-size: 13.5px; color: var(--sub); margin: 0 0 12px;
}

/* ── 카드 공통 ── */
.s-card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 20px 22px;
  margin-bottom: 12px;
  box-shadow: 0 1px 3px rgba(15,26,51,0.03);
}

/* ── KPI ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}
.kpi-cell {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 16px 14px;
}
.kpi-label {
  font-size: 12px; color: var(--sub); font-weight: 500;
  margin-bottom: 6px; line-height: 1.4;
}
.kpi-value {
  font-size: 26px; font-weight: 700; color: var(--ink);
  letter-spacing: -0.03em; line-height: 1;
}
.kpi-value.accent { color: var(--shinhan); }
.kpi-value.warn { color: var(--warn); }
.kpi-value.gold { color: #B8860B; }
.kpi-unit { font-size: 13px; font-weight: 500; color: var(--sub); margin-left: 2px; }
@media (max-width: 640px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}

/* ── 유형 분포 박스 ── */
.type-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 16px;
}
.type-cell {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 16px 14px;
}
.type-head { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.type-icon {
  width: 32px; height: 32px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; background: var(--shinhan-l); color: var(--shinhan);
}
.type-name { font-size: 13px; font-weight: 600; color: var(--ink); }
.type-count {
  font-size: 22px; font-weight: 700; color: var(--ink);
  letter-spacing: -0.02em; margin-bottom: 2px;
}
.type-strat { font-size: 11.5px; color: var(--sub); line-height: 1.4; }
@media (max-width: 640px) {
  .type-grid { grid-template-columns: repeat(2, 1fr); }
}

/* ── 고객 카드 ── */
.cust-card {
  background: #FFFFFF;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 10px;
  position: relative;
}
.cust-card.high { border-left: 3px solid var(--warn); }
.cust-card.mid  { border-left: 3px solid var(--gold); }
.cust-head {
  display: flex; justify-content: space-between; align-items: center;
  gap: 8px; flex-wrap: wrap; margin-bottom: 10px;
}
.cust-id-area { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.cust-id {
  font-size: 15px; font-weight: 700; color: var(--ink);
  letter-spacing: -0.02em;
}
.cust-pill {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 11.5px; font-weight: 600;
  padding: 3px 9px; border-radius: 4px;
}
.p-신판   { color:#0046FF; background:#E8EFFF; }
.p-타사   { color:#6B21A8; background:#F3E8FF; }
.p-포인트 { color:#047857; background:#D1FAE5; }
.p-불만   { color:#B91C1C; background:#FEE2E2; }
.p-카드   { color:#92400E; background:#FEF3C7; }
.p-디지털 { color:#0E7490; background:#CFFAFE; }
.p-신규   { color:#9A3412; background:#FFEDD5; }

.score-chip {
  font-size: 16px; font-weight: 700;
  padding: 4px 12px; border-radius: 6px;
  letter-spacing: -0.01em;
  font-variant-numeric: tabular-nums;
}
.sc-r { color: var(--warn); background: var(--warn-l); }
.sc-a { color: #B8860B; background: var(--gold-l); }

.type-mini {
  display: flex; gap: 14px; flex-wrap: wrap;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #F3F4F6;
}
.type-mini span { font-size: 11.5px; color: var(--sub); }
.type-mini b { color: var(--body); font-weight: 600; margin-left: 2px; }

.cause-line {
  font-size: 12.5px; color: var(--body);
  margin-bottom: 14px; padding: 10px 14px;
  background: #FAFBFC; border-radius: 8px;
  border-left: 2px solid var(--shinhan);
}
.cause-line b { color: var(--shinhan); font-weight: 700; }

.bar-item { margin-bottom: 8px; }
.bar-row {
  display: flex; justify-content: space-between;
  font-size: 12px; color: var(--body); margin-bottom: 4px;
}
.bar-row .vname { font-weight: 500; }
.bar-row .vtype { font-size: 10.5px; color: #9CA3AF; margin-left: 4px; }
.bar-row .vpct {
  color: var(--shinhan); font-weight: 700;
  font-variant-numeric: tabular-nums;
}
.bar-track { height: 5px; background: #F1F3F5; border-radius: 3px; overflow: hidden; }
.bar-fill { height: 5px; background: var(--shinhan); border-radius: 3px; }

.offer-row {
  display: flex; align-items: center; gap: 10px;
  flex-wrap: wrap; margin-top: 14px;
  padding-top: 14px; border-top: 1px solid #F3F4F6;
}
.offer-label {
  font-size: 11px; font-weight: 600; color: var(--sub);
  letter-spacing: 0.04em;
}
.offer-name {
  font-size: 13px; font-weight: 600; color: var(--shinhan);
  padding: 4px 10px; background: var(--shinhan-l); border-radius: 4px;
}
.offer-detail { font-size: 12px; color: var(--sub); }

/* ── Alert ── */
.alert-warn {
  background: #FFFBEB; border: 1px solid #FDE68A;
  border-radius: 10px; padding: 14px 18px;
  margin: 12px 0; border-left: 3px solid var(--gold);
}
.alert-warn-title {
  font-size: 13px; font-weight: 700; color: #92400E;
  margin-bottom: 4px;
}
.alert-warn-body { font-size: 12.5px; color: #78350F; line-height: 1.5; }

.alert-new {
  background: #FFFFFF; border: 1px solid var(--line);
  border-left: 3px solid var(--shinhan);
  border-radius: 10px; padding: 16px 20px; margin: 14px 0;
}
.alert-new-title {
  font-size: 14px; font-weight: 700; color: var(--ink);
  margin-bottom: 4px; letter-spacing: -0.02em;
}
.alert-new-desc {
  font-size: 12.5px; color: var(--sub); margin-bottom: 12px;
  line-height: 1.5;
}
.alert-new-item {
  display: flex; justify-content: space-between;
  align-items: center; gap: 10px;
  padding: 10px 0;
  border-top: 1px solid #F3F4F6;
  font-size: 12.5px; color: var(--body);
}
.alert-new-item:first-of-type { border-top: none; padding-top: 4px; }
.alert-new-item .combo b { color: var(--ink); font-weight: 600; }
.alert-new-item .combo .ttype { font-size: 10.5px; color: var(--sub); margin-left: 4px; }
.alert-new-item .meta {
  font-size: 11.5px; color: var(--shinhan); font-weight: 600;
  white-space: nowrap;
}

/* ── 결과 박스 ── */
.result-box {
  background: var(--ink); border-radius: 12px;
  padding: 24px 26px; margin-top: 8px; color: #fff;
}
.result-time { font-size: 12px; color: #94A3B8; margin-bottom: 16px; }
.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 18px;
}
.result-cell .rv {
  font-size: 24px; font-weight: 700; color: #fff;
  line-height: 1; margin-bottom: 4px; letter-spacing: -0.02em;
  font-variant-numeric: tabular-nums;
}
.result-cell .rl {
  font-size: 11.5px; color: #94A3B8; font-weight: 500;
}
.result-foot {
  margin-top: 18px; padding-top: 14px;
  border-top: 1px solid #1E293B;
  font-size: 11.5px; color: #94A3B8; line-height: 1.6;
}

/* ── 인용 ── */
.callout {
  background: var(--shinhan-l);
  border-radius: 10px;
  padding: 18px 22px; margin-top: 16px;
  border-left: 3px solid var(--shinhan);
}
.callout-text {
  font-size: 13.5px; color: var(--ink); line-height: 1.7;
  font-weight: 500; letter-spacing: -0.015em;
}

/* ── Streamlit 컴포넌트 오버라이드 ── */
.stButton > button {
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-size: 13.5px !important;
  height: 44px !important;
  letter-spacing: -0.01em !important;
  border: 1px solid var(--line) !important;
  background: #FFFFFF !important;
  color: var(--ink) !important;
  box-shadow: none !important;
  transition: all 0.15s !important;
}
.stButton > button:hover {
  background: #FAFBFC !important;
  border-color: #D1D5DB !important;
}
.stButton > button[kind="primary"] {
  background: var(--shinhan) !important;
  border-color: var(--shinhan) !important;
  color: #FFFFFF !important;
}
.stButton > button[kind="primary"]:hover {
  background: var(--shinhan-d) !important;
  border-color: var(--shinhan-d) !important;
}

[data-testid="stFileUploader"] section {
  border: 1.5px dashed #CBD5E1 !important;
  background: #FAFBFC !important;
  border-radius: 10px !important;
  padding: 22px !important;
}
[data-testid="stFileUploader"] section:hover { border-color: var(--shinhan) !important; }
[data-testid="stFileUploader"] small { color: var(--sub) !important; }

.stSlider > div > div > div > div { background: var(--shinhan) !important; }
.stSlider [data-baseweb="slider"] > div:nth-child(3) { background: var(--shinhan) !important; }

[data-testid="stMetricValue"] {
  font-size: 24px !important; font-weight: 700 !important;
  color: var(--ink) !important; letter-spacing: -0.025em !important;
}
[data-testid="stMetricLabel"] {
  font-size: 12px !important; color: var(--sub) !important;
  font-weight: 500 !important;
}
[data-testid="stMetricDelta"] { font-size: 12px !important; }

hr { border-color: var(--line) !important; margin: 24px 0 !important; }

[data-testid="stAlert"] { border-radius: 10px !important; }

/* 라벨 색상 */
label, .stCheckbox label, .stSelectbox label, .stSlider label {
  color: var(--body) !important; font-size: 13px !important;
  font-weight: 500 !important;
}

/* 푸터 */
.site-footer {
  margin-top: 48px; padding: 24px 0 8px;
  border-top: 1px solid var(--line);
  text-align: center;
}
.site-footer-text {
  font-size: 11.5px; color: var(--sub); line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ══ 온톨로지 ══
ONTOLOGY = {
    "Var1":  {"name":"최근일주일내이용건수",         "type":"신판이용",   "dir":"LOW"},
    "Var2":  {"name":"한달전대비이용금액증감률",      "type":"신판이용",   "dir":"LOW"},
    "Var3":  {"name":"일주일전대비이용금액증감률",    "type":"신판이용",   "dir":"LOW"},
    "Var4":  {"name":"타사카드신규개설여부",          "type":"타사이용",   "dir":"HIGH"},
    "Var5":  {"name":"최근한달타사카드이용금액증감률","type":"타사이용",   "dir":"HIGH"},
    "Var6":  {"name":"최근한달타사대비당사이용비율",  "type":"타사이용",   "dir":"LOW"},
    "Var7":  {"name":"최근한달포인트사용량",          "type":"잔여포인트", "dir":"HIGH"},
    "Var8":  {"name":"포인트잔여량",                  "type":"잔여포인트", "dir":"LOW"},
    "Var9":  {"name":"최근포인트증가여부",            "type":"잔여포인트", "dir":"LOW"},
    "Var10": {"name":"최근민원발생빈도",              "type":"고객불만",   "dir":"HIGH"},
    "Var11": {"name":"최근VOC발생빈도",               "type":"고객불만",   "dir":"HIGH"},
    "Var12": {"name":"최근온라인민원접수빈도",         "type":"고객불만",   "dir":"HIGH"},
    "Var13": {"name":"한달내만기대상카드존재여부",    "type":"카드보유",   "dir":"HIGH"},
    "Var14": {"name":"최근보유카드탈회수",             "type":"카드보유",   "dir":"HIGH"},
    "Var15": {"name":"최근카드분실신고여부",           "type":"카드보유",   "dir":"HIGH"},
    "Var16": {"name":"최근한달앱접속건수",             "type":"디지털이용", "dir":"LOW"},
    "Var17": {"name":"디지털이용빈도증감률",           "type":"디지털이용", "dir":"LOW"},
    "Var18": {"name":"마케팅Push개봉건수",             "type":"디지털이용", "dir":"LOW"},
}
TYPE_STRATEGY = {
    "신판이용":   ("무이자할부 제공",            "당월 50만원 이상 이용 시 3개월 무이자할부"),
    "타사이용":   ("30만원 추가이용 시 캐시백",  "전월 대비 30만원 추가 이용 시 3만원 캐시백"),
    "잔여포인트": ("외식업종 포인트 2배",        "외식업종 이용 시 포인트 2배 적립"),
    "고객불만":   ("5천 포인트 제공",            "즉시 5,000 포인트 + VOC 전담 상담사 연결"),
    "카드보유":   ("추가 카드 연회비 할인",      "신규 카드 발급 시 첫 해 연회비 100% 면제"),
    "디지털이용": ("앱 접속 시 투썸 쿠폰",      "앱 로그인 시 투썸플레이스 아메리카노 쿠폰"),
}
ALL_STRATEGIES = {
    "무이자할부 제공":          "당월 50만원 이상 이용 시 3개월 무이자할부",
    "30만원 추가이용 시 캐시백": "전월 대비 30만원 추가 이용 시 3만원 캐시백",
    "외식업종 포인트 2배":      "외식업종 이용 시 포인트 2배 적립",
    "5천 포인트 제공":          "즉시 5,000 포인트 + VOC 전담 상담사 연결",
    "추가 카드 연회비 할인":    "신규 카드 발급 시 첫 해 연회비 100% 면제",
    "앱 접속 시 투썸 쿠폰":     "앱 로그인 시 투썸플레이스 아메리카노 쿠폰",
    "오퍼 미적용":              "해당 고객 리텐션 캠페인 제외",
}
TYPE_ICONS = {"신판이용":"💳","타사이용":"🔄","잔여포인트":"⭐","고객불만":"💬","카드보유":"🪪","디지털이용":"📱"}
TYPE_PILL  = {"신판이용":"p-신판","타사이용":"p-타사","잔여포인트":"p-포인트","고객불만":"p-불만","카드보유":"p-카드","디지털이용":"p-디지털"}
VAR_COLS   = [f"Var{i}" for i in range(1,19)]

# ── 핵심 함수 ──
def calc_contribs(row, avgs):
    c = {}
    for var, info in ONTOLOGY.items():
        v, a = float(row.get(var,0.5)), float(avgs.get(var,0.5))
        c[var] = max(0.0, a-v) if info["dir"]=="LOW" else max(0.0, v-a)
    t = sum(c.values()) or 1.0
    return {k: round(v/t*100,1) for k,v in c.items()}

def dominant_type(cb):
    ts = {}
    for var, pct in cb.items():
        tp = ONTOLOGY[var]["type"]
        ts[tp] = ts.get(tp,0) + pct
    dom  = max(ts, key=ts.get)
    top2 = sorted(ts.values(), reverse=True)[:2]
    is_new = (top2[0] + (top2[1] if len(top2)>1 else 0)) < 40
    return dom, ts, is_new

def detect_new_combos(high_df, threshold=15):
    combo_counts = {}
    combo_examples = {}
    for _, r in high_df.iterrows():
        top2_vars = tuple(sorted([v for v,_ in r["top3"][:2]]))
        combo_counts[top2_vars] = combo_counts.get(top2_vars, 0) + 1
        if top2_vars not in combo_examples:
            combo_examples[top2_vars] = []
        combo_examples[top2_vars].append(r["고객ID"])
    new_combos = {k: v for k,v in combo_counts.items() if v >= threshold}
    return new_combos, combo_examples

def render_customer_card(r, edit_mode=False, idx=0):
    sc_val   = float(r["Score"])
    card_cls = "cust-card high" if sc_val >= 0.3 else "cust-card mid"
    chip_cls = "score-chip sc-r" if sc_val >= 0.3 else "score-chip sc-a"
    tp       = str(r["주요유형"])
    pc       = TYPE_PILL.get(tp,"p-신규") if not r["is_new"] else "p-신규"
    tp_lbl   = tp + (" · 신규패턴" if r["is_new"] else "")

    bars = ""
    for v, p in r["top3"]:
        bars += (
            f'<div class="bar-item">'
            f'<div class="bar-row">'
            f'<span><span class="vname">{ONTOLOGY[v]["name"]}</span>'
            f'<span class="vtype">({ONTOLOGY[v]["type"]})</span></span>'
            f'<span class="vpct">{p}%</span>'
            f'</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{p}%"></div></div>'
            f'</div>'
        )
    ts_html = ""
    for t, s in sorted(r["type_scores"].items(), key=lambda x:x[1], reverse=True)[:3]:
        ts_html += f'<span>{TYPE_ICONS.get(t,"")} {t} <b>{round(s,1)}%</b></span>'

    head_html = (
        f'<div class="{card_cls}">'
        f'<div class="cust-head">'
        f'<div class="cust-id-area">'
        f'<span class="cust-id">{r["고객ID"]}</span>'
        f'<span class="cust-pill {pc}">{TYPE_ICONS.get(r["주요유형"],"")} {tp_lbl}</span>'
        f'</div>'
        f'<span class="{chip_cls}">{round(sc_val,4)}</span>'
        f'</div>'
        f'<div class="type-mini">{ts_html}</div>'
        f'<div class="cause-line">주요 이탈 원인 · <b>{r["주요원인"]} ({r["주요원인_pct"]}%)</b></div>'
        f'{bars}'
    )

    if edit_mode:
        st.markdown(head_html + '</div>', unsafe_allow_html=True)
        with st.container():
            col_s, col_exc = st.columns([3,1])
            key_s   = f"edit_strat_{idx}"
            key_exc = f"edit_exc_{idx}"
            cur_str = r["전략"]
            options = list(ALL_STRATEGIES.keys())
            with col_s:
                sel = st.selectbox(
                    f"오퍼 변경 — {r['고객ID']}",
                    options,
                    index=options.index(cur_str) if cur_str in options else 0,
                    key=key_s,
                    label_visibility="collapsed"
                )
            with col_exc:
                exclude = st.checkbox("캠페인 제외", key=key_exc)
            if exclude:
                st.caption(f"{r['고객ID']} — 캠페인 제외 처리")
            else:
                st.caption(f"{r['고객ID']} → {sel} · {ALL_STRATEGIES[sel]}")
            st.session_state[f"final_strat_{r['고객ID']}"] = None if exclude else sel
    else:
        st.markdown(
            head_html
            + f'<div class="offer-row">'
              f'<span class="offer-label">추천 리텐션</span>'
              f'<span class="offer-name">{r["전략"]}</span>'
              f'<span class="offer-detail">{r["전략상세"]}</span>'
              f'</div>'
              f'</div>',
            unsafe_allow_html=True
        )

# ══ 페이지 헤더 ══
st.markdown(
    '<div class="page-header">'
    '<h1 class="page-title">고객 이탈 원인 분석 및 초개인화 리텐션 Agent</h1>'
    '<p class="page-desc">이탈 위험 고객을 진단하고 원인에 맞는 맞춤 리텐션 캠페인을 자동 실행합니다.</p>'
    '</div>', unsafe_allow_html=True)

# ══ STEP 1 ══
st.markdown(
    '<div class="section-block">'
    '<div class="section-num">STEP 01</div>'
    '<div class="section-title">고객 데이터 업로드</div>'
    '<div class="section-desc">분석할 고객 데이터를 업로드하거나, 더미 데이터로 바로 시연할 수 있습니다.</div>'
    '</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("CSV 또는 Excel · 컬럼: 고객번호, Var1~Var18, Score", type=["csv","xlsx"])
use_demo = st.button("더미 데이터로 시연하기")

df = None
if use_demo or "demo" in st.session_state:
    st.session_state["demo"] = True
    np.random.seed(99); n=50
    demo = {"고객번호":[f"CL_{str(i).zfill(3)}" for i in range(1,n+1)]}
    for i in range(1,19): demo[f"Var{i}"] = np.random.uniform(0,1,n).round(4)
    df = pd.DataFrame(demo)
    W = {"Var1":-0.08,"Var2":-0.07,"Var3":-0.07,"Var4":0.09,"Var5":0.08,"Var6":-0.07,
         "Var7":0.06,"Var8":-0.05,"Var9":-0.05,"Var10":0.09,"Var11":0.08,"Var12":0.07,
         "Var13":0.06,"Var14":0.05,"Var15":0.04,"Var16":-0.05,"Var17":-0.04,"Var18":-0.04}
    df["Score"] = [round(sum((row[v]-0.5)*w*2 for v,w in W.items()),6) for _,row in df.iterrows()]
    st.success(f"더미 데이터 {n}명 로드 완료")
elif uploaded:
    try:
        df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        df.columns = [c.strip() for c in df.columns]
        st.success(f"업로드 완료 · 총 {len(df)}명")
    except Exception as e:
        st.error(f"파일 읽기 오류 · {e}")

# ══ 미리보기 ══
if df is not None:
    id_col = "고객번호" if "고객번호" in df.columns else df.columns[0]
    av = [v for v in VAR_COLS if v in df.columns]

    with st.expander("데이터 미리보기 및 통계 확인"):
        t1,t2,t3 = st.tabs(["미리보기","변수 통계","Score 분포"])
        with t1:
            show = [id_col]+av[:9]+(["Score"] if "Score" in df.columns else [])
            st.dataframe(df[show].head(20), use_container_width=True, height=260)
        with t2:
            stat = df[av].describe().T.round(4)
            stat["변수명"] = [ONTOLOGY[v]["name"] for v in stat.index]
            stat["유형"]   = [ONTOLOGY[v]["type"]  for v in stat.index]
            st.dataframe(stat[["변수명","유형","mean","std","min","max"]].rename(
                columns={"mean":"평균","std":"표준편차","min":"최솟값","max":"최댓값"}),
                use_container_width=True, height=360)
        with t3:
            if "Score" in df.columns:
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("평균",f"{df['Score'].mean():.4f}")
                c2.metric("최고",f"{df['Score'].max():.4f}")
                c3.metric("최저",f"{df['Score'].min():.4f}")
                c4.metric("표준편차",f"{df['Score'].std():.4f}")
                st.bar_chart(df.set_index(id_col)["Score"].sort_values(ascending=False))

    # ══ STEP 2 ══
    st.markdown(
        '<div class="section-block">'
        '<div class="section-num">STEP 02</div>'
        '<div class="section-title">분석 설정 및 실행</div>'
        '<div class="section-desc">이탈 위험 임계값과 신규 패턴 Alert 기준을 설정합니다.</div>'
        '</div>', unsafe_allow_html=True)

    col_sl, col_btn = st.columns([4,1])
    with col_sl:
        threshold = st.slider(
            "이탈 위험 임계값 — Score가 이 값 이상이면 고위험으로 분류",
            min_value=0.0, max_value=1.0, value=0.1, step=0.01,
            format="%.2f"
        )
        alert_min = st.slider(
            "신규 변수 조합 Alert 기준 — 동일 조합이 N건 이상 누적되면 Alert 발송",
            min_value=1, max_value=20, value=3, step=1
        )
    with col_btn:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        run = st.button("분석 실행", use_container_width=True, type="primary")

    if run or "done" in st.session_state:
        st.session_state["done"] = True
        st.session_state["thr"] = threshold
        st.session_state["alert_min"] = alert_min
        thr       = st.session_state.get("thr", 0.1)
        alert_min = st.session_state.get("alert_min", 3)

        with st.spinner("XAI 변수 기여도 분석 및 온톨로지 유형 분류 중..."):
            avgs = {v: float(df[v].mean()) for v in av}
            rows = []
            for _, row in df.iterrows():
                r   = row.to_dict()
                sc  = float(r.get("Score",0))
                cb  = calc_contribs(r, avgs)
                dom, ts, is_new = dominant_type(cb)
                strat, detail   = TYPE_STRATEGY[dom]
                top3 = sorted(cb.items(), key=lambda x:x[1], reverse=True)[:3]
                rows.append({
                    "고객ID":r[id_col],"Score":sc,"주요유형":dom,
                    "type_scores":ts,"is_new":is_new,"기여도":cb,"top3":top3,
                    "전략":strat,"전략상세":detail,
                    "주요원인":ONTOLOGY[top3[0][0]]["name"],
                    "주요원인_pct":top3[0][1],
                })

        res  = pd.DataFrame(rows)
        high = res[res["Score"]>=thr].sort_values("Score",ascending=False)
        newp = res[(res["Score"]>=thr) & res["is_new"]]

        # ── STEP 3 ──
        st.markdown(
            '<div class="section-block">'
            '<div class="section-num">STEP 03</div>'
            '<div class="section-title">분석 결과 — 이탈 원인 진단</div>'
            '<div class="section-desc">XAI 기여도와 온톨로지 매핑을 통해 고객별 이탈 원인을 진단합니다.</div>'
            '</div>', unsafe_allow_html=True)

        n_types = int(high["주요유형"].nunique()) if len(high)>0 else 0
        st.markdown(
            f'<div class="kpi-grid">'
            f'<div class="kpi-cell"><div class="kpi-label">전체 분석 고객</div>'
            f'<div class="kpi-value">{len(df)}<span class="kpi-unit">명</span></div></div>'
            f'<div class="kpi-cell"><div class="kpi-label">고위험 고객 · Score ≥ {thr:.2f}</div>'
            f'<div class="kpi-value warn">{len(high)}<span class="kpi-unit">명</span></div></div>'
            f'<div class="kpi-cell"><div class="kpi-label">감지된 이탈 유형</div>'
            f'<div class="kpi-value accent">{n_types}<span class="kpi-unit">개</span></div></div>'
            f'<div class="kpi-cell"><div class="kpi-label">신규 복합 패턴</div>'
            f'<div class="kpi-value gold">{len(newp)}<span class="kpi-unit">명</span></div></div>'
            f'</div>', unsafe_allow_html=True)

        # 유형 분포
        if len(high)>0:
            td = high["주요유형"].value_counts().to_dict()
            html = '<div class="type-grid">'
            for tp,cnt in sorted(td.items(),key=lambda x:x[1],reverse=True):
                s,_ = TYPE_STRATEGY[tp]
                html += (
                    f'<div class="type-cell">'
                    f'<div class="type-head">'
                    f'<div class="type-icon">{TYPE_ICONS.get(tp,"")}</div>'
                    f'<div class="type-name">{tp}</div>'
                    f'</div>'
                    f'<div class="type-count">{cnt}<span class="kpi-unit">명</span></div>'
                    f'<div class="type-strat">{s}</div>'
                    f'</div>'
                )
            st.markdown(html+'</div>', unsafe_allow_html=True)

        # 기존 신규 복합 패턴 alert
        if len(newp)>0:
            ids_str = ", ".join(str(x) for x in list(newp["고객ID"])[:5])
            st.markdown(
                f'<div class="alert-warn">'
                f'<div class="alert-warn-title">신규 복합 이탈 패턴 감지</div>'
                f'<div class="alert-warn-body">단일 유형으로 분류되지 않는 복합 패턴 고객 <b>{len(newp)}명</b>이 감지되었습니다. '
                f'온톨로지 신규 유형 추가를 검토해 주세요.<br>'
                f'<span style="font-size:11.5px;color:#9A6B00">대상 · {ids_str} 등</span>'
                f'</div></div>',
                unsafe_allow_html=True)

        # ── 신규 변수 조합 Alert ──
        if len(high) > 0:
            new_combos, combo_examples = detect_new_combos(high, threshold=alert_min)
            if new_combos:
                combo_rows = ""
                for combo, cnt in sorted(new_combos.items(), key=lambda x:x[1], reverse=True):
                    v1_name = ONTOLOGY[combo[0]]["name"]
                    v2_name = ONTOLOGY[combo[1]]["name"]
                    v1_type = ONTOLOGY[combo[0]]["type"]
                    v2_type = ONTOLOGY[combo[1]]["type"]
                    ex_ids  = ", ".join(str(x) for x in combo_examples[combo][:3])
                    combo_rows += (
                        f'<div class="alert-new-item">'
                        f'<span class="combo"><b>{v1_name}</b><span class="ttype">{v1_type}</span>'
                        f' + <b>{v2_name}</b><span class="ttype">{v2_type}</span></span>'
                        f'<span class="meta">{cnt}건 · 예) {ex_ids}</span>'
                        f'</div>'
                    )
                st.markdown(
                    f'<div class="alert-new">'
                    f'<div class="alert-new-title">신규 변수 조합 패턴 — 온톨로지 업데이트 검토 필요</div>'
                    f'<div class="alert-new-desc">기존 온톨로지에 없는 변수 조합이 <b style="color:var(--ink)">{alert_min}건 이상</b> 반복 감지되었습니다. '
                    f'아래 조합을 검토 후 새로운 이탈 유형으로 등록해 주세요.</div>'
                    f'{combo_rows}'
                    f'</div>',
                    unsafe_allow_html=True)

        # 고위험 고객 카드
        if len(high) > 0:
            st.markdown(
                '<div style="margin:24px 0 12px;font-size:14px;font-weight:700;color:var(--ink);letter-spacing:-0.02em">'
                '고위험 이탈 고객 상세 분석</div>',
                unsafe_allow_html=True)
            edit_mode = st.session_state.get("edit_mode", False)
            for i, (_, r) in enumerate(high.head(10).iterrows()):
                render_customer_card(r, edit_mode=edit_mode, idx=i)
        else:
            st.info(f"임계값 {thr:.2f} 이상인 고위험 고객이 없습니다. 슬라이더 값을 낮춰보세요.")

        # ── STEP 4 ──
        st.markdown(
            '<div class="section-block">'
            '<div class="section-num">STEP 04</div>'
            '<div class="section-title">현업 검토 및 캠페인 승인</div>'
            '<div class="section-desc">Agent가 분석한 리텐션 전략을 검토하고 실행을 승인해 주세요.</div>'
            '</div>', unsafe_allow_html=True)

        ca, cb_, cc = st.columns(3)
        with ca:
            approve = st.button("전체 승인 후 실행", use_container_width=True, type="primary")
        with cb_:
            edit_btn = st.button("일부 수정 후 실행", use_container_width=True)
        with cc:
            hold_btn = st.button("보류", use_container_width=True)

        if edit_btn:
            st.session_state["edit_mode"] = True
            st.rerun()
        if hold_btn:
            st.session_state["edit_mode"] = False
            st.info("캠페인이 보류되었습니다.")

        if st.session_state.get("edit_mode", False):
            st.info("수정 모드 · 각 고객 카드에서 오퍼를 변경하거나 캠페인에서 제외할 수 있습니다. 완료 후 아래 버튼을 눌러주세요.")
            if st.button("수정 완료 및 실행", type="primary"):
                st.session_state["edit_mode"] = False
                st.session_state["camp"] = True
                st.rerun()

        # ── STEP 5 ──
        if approve or "camp" in st.session_state:
            st.session_state["camp"] = True
            st.markdown(
                '<div class="section-block">'
                '<div class="section-num">STEP 05</div>'
                '<div class="section-title">리텐션 캠페인 실행 완료</div>'
                '<div class="section-desc">선정된 고객에게 채널별 맞춤 오퍼가 발송되었습니다.</div>'
                '</div>', unsafe_allow_html=True)

            final_high = high.head(10).copy()
            excluded   = []
            for _, r in final_high.iterrows():
                cid = r["고객ID"]
                key = f"final_strat_{cid}"
                if key in st.session_state:
                    if st.session_state[key] is None:
                        excluded.append(cid)
            target_cnt = len(final_high) - len(excluded)

            st.success(f"{target_cnt}명 대상 초개인화 리텐션 캠페인이 실행되었습니다."
                       + (f" ({len(excluded)}명 제외)" if excluded else ""))

            tc = high.head(10)[~high.head(10)["고객ID"].isin(excluded)]["주요유형"].value_counts().to_dict()
            ri = "".join(
                f'<div class="result-cell"><div class="rv">{cnt}</div><div class="rl">{TYPE_ICONS.get(tp,"")} {tp}</div></div>'
                for tp,cnt in tc.items()
            )
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            st.markdown(
                f'<div class="result-box">'
                f'<div class="result-time">{now} · 캠페인 실행 현황</div>'
                f'<div class="result-grid">'
                f'<div class="result-cell"><div class="rv">{target_cnt}</div><div class="rl">총 발송 대상</div></div>'
                f'{ri}</div>'
                f'<div class="result-foot">Push · LMS · 카카오톡 채널 자동 선택 완료 · 성과 데이터는 24시간 후 자동 수집됩니다</div>'
                f'</div>', unsafe_allow_html=True)

            # ── STEP 6 ──
            st.markdown(
                '<div class="section-block">'
                '<div class="section-num">STEP 06</div>'
                '<div class="section-title">캠페인 성과 리포트</div>'
                '<div class="section-desc">발송 결과를 시뮬레이션한 예상 성과입니다.</div>'
                '</div>', unsafe_allow_html=True)
            sim = round(random.uniform(28,44),1)
            m1,m2,m3 = st.columns(3)
            m1.metric("예상 리텐션 전환율", f"{sim}%", f"+{round(sim-18,1)}%p vs 기존 일괄 오퍼")
            m2.metric("이탈 방어 예상 고객", f"{int(target_cnt*sim/100)}명")
            m3.metric("오퍼 비용 효율", "개선", "유형별 맞춤 오퍼 적용")
            st.markdown(
                '<div class="callout">'
                '<div class="callout-text">"이제 현업의 역할은 데이터를 찾는 것이 아니라,<br>'
                'Agent가 발견한 인사이트를 바탕으로 더 나은 마케팅 방식을 고민하는 것으로 전환됩니다."</div>'
                '</div>',
                unsafe_allow_html=True)

# ══ 푸터 ══
st.markdown(
    '<div class="site-footer">'
    '<div class="site-footer-text">고객 이탈 원인 분석 및 초개인화 리텐션 Agent</div>'
    '</div>', unsafe_allow_html=True)
