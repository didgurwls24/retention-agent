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
html, body, [class*="css"], .stApp {
    font-family: 'Noto Sans KR', sans-serif !important;
    background-color: #EDF1F8 !important;
}
.block-container {
    max-width: 1080px !important;
    padding: 1.5rem 2rem !important;
    margin: 0 auto !important;
}
.main-header {
    background: linear-gradient(135deg, #071430 0%, #0B1F4E 55%, #1A3A8F 100%);
    padding: 32px 40px 26px;
    border-radius: 16px;
    margin-bottom: 24px;
    border-top: 5px solid #1565E8;
    box-shadow: 0 6px 24px rgba(7,20,48,0.2);
}
.main-title { font-size:21px; font-weight:900; color:#fff; margin:0 0 5px; }
.main-sub   { font-size:12px; color:rgba(255,255,255,0.5); margin:0 0 14px; }
.badge {
    display:inline-block;
    background:rgba(0,70,173,0.4); border:1px solid rgba(0,100,210,0.35);
    color:#90C4FF; font-size:10.5px; font-weight:700;
    padding:3px 11px; border-radius:20px; margin:0 5px 5px 0;
}
.sec-label { font-size:10px; font-weight:800; color:#0046AD; letter-spacing:0.14em; text-transform:uppercase; margin-bottom:2px; }
.sec-title  { font-size:15px; font-weight:700; color:#0B1F4E; margin-bottom:14px; }
.kpi-row  { display:flex; gap:12px; margin-bottom:20px; flex-wrap:wrap; }
.kpi-box  {
    flex:1; min-width:120px;
    background:linear-gradient(135deg,#F4F7FF,#EEF3FF);
    border:1.5px solid #D0DCFF; border-radius:12px;
    padding:16px 14px; text-align:center;
}
.kpi-n      { font-size:26px; font-weight:900; color:#0046AD; line-height:1; margin-bottom:4px; }
.kpi-n.red  { color:#E53935; }
.kpi-n.amb  { color:#F57C00; }
.kpi-l      { font-size:11px; color:#6680AA; line-height:1.4; }
.rc     { background:#fff; border-radius:12px; padding:16px 18px; margin-bottom:10px; border:1.5px solid #D8E4FF; border-left:5px solid #E53935; }
.rc.mid { border-left-color:#FB8C00; }
.bw { margin:6px 0; }
.bl { display:flex; justify-content:space-between; font-size:11.5px; color:#444; margin-bottom:2px; }
.bb { background:#EEF3FF; border-radius:5px; height:7px; width:100%; overflow:hidden; }
.bf { background:linear-gradient(90deg,#0046AD,#1565E8); border-radius:5px; height:7px; }
.t-신판이용   { background:#E3F2FD; color:#1565C0; border:1px solid #BBDEFB; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.t-타사이용   { background:#FCE4EC; color:#880E4F; border:1px solid #F8BBD0; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.t-잔여포인트 { background:#F3E5F5; color:#6A1B9A; border:1px solid #E1BEE7; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.t-고객불만   { background:#FFEBEE; color:#B71C1C; border:1px solid #FFCDD2; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.t-카드보유   { background:#FFF8E1; color:#F57F17; border:1px solid #FFECB3; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.t-디지털이용 { background:#E8F5E9; color:#1B5E20; border:1px solid #C8E6C9; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.ob {
    display:inline-block; background:#EEF3FF; border:1.5px solid #C8D8FF;
    color:#0046AD; font-size:11.5px; font-weight:700;
    padding:3px 12px; border-radius:20px; margin-right:6px;
}
.alert { background:#FFF8E1; border:1.5px solid #FFB74D; border-left:5px solid #FF8F00; border-radius:10px; padding:14px 18px; margin:14px 0; }
.at    { font-size:13px; font-weight:700; color:#E65100; margin-bottom:4px; }
.rsbox {
    background:linear-gradient(135deg,#071430,#0B1F4E,#0046AD);
    border-radius:14px; padding:24px 28px; margin-top:16px;
    box-shadow:0 6px 20px rgba(0,30,100,0.2);
}
.sg { display:flex; gap:16px; flex-wrap:wrap; margin-top:14px; }
.si { flex:1; min-width:80px; }
.sn { font-size:26px; font-weight:900; color:#7AADFF; line-height:1; margin-bottom:3px; }
.sl { font-size:11px; color:rgba(255,255,255,0.5); }
.qb {
    background:#F4F7FF; border-left:4px solid #0046AD;
    border-radius:0 10px 10px 0; padding:14px 20px; margin-top:14px;
    font-size:12.5px; color:#0B1F4E; font-style:italic; line-height:1.8;
}
.score-chip {
    display:inline-block;
    font-size:22px; font-weight:900;
    padding:2px 10px; border-radius:8px;
}
.score-high { color:#E53935; background:#FFEBEE; }
.score-mid  { color:#FB8C00; background:#FFF3E0; }
.preview-box {
    background:#fff; border:1.5px solid #D0DCFF; border-radius:12px;
    padding:16px 20px; margin-bottom:16px;
}
.stButton > button {
    background:linear-gradient(135deg,#0046AD,#1565E8) !important;
    color:#fff !important; border:none !important;
    border-radius:9px !important; font-weight:700 !important;
    font-family:'Noto Sans KR',sans-serif !important;
    padding:10px 22px !important; font-size:13.5px !important;
    box-shadow:0 2px 8px rgba(0,70,173,0.2) !important;
}
.stButton > button:hover {
    background:linear-gradient(135deg,#003A8C,#0046AD) !important;
    box-shadow:0 5px 14px rgba(0,70,173,0.3) !important;
    transform:translateY(-1px) !important;
}
[data-testid="metric-container"] {
    background:#F4F7FF !important;
    border:1.5px solid #D0DCFF !important;
    border-radius:12px !important;
    padding:12px 14px !important;
}
</style>
""", unsafe_allow_html=True)

# ══ 온톨로지 ══
ONTOLOGY = {
    "Var1":  {"name":"최근일주일내이용건수",       "type":"신판이용",   "dir":"LOW"},
    "Var2":  {"name":"한달전대비이용금액증감률",    "type":"신판이용",   "dir":"LOW"},
    "Var3":  {"name":"일주일전대비이용금액증감률",  "type":"신판이용",   "dir":"LOW"},
    "Var4":  {"name":"타사카드신규개설여부",        "type":"타사이용",   "dir":"HIGH"},
    "Var5":  {"name":"최근한달타사카드이용금액증감률","type":"타사이용",  "dir":"HIGH"},
    "Var6":  {"name":"최근한달타사대비당사이용비율","type":"타사이용",   "dir":"LOW"},
    "Var7":  {"name":"최근한달포인트사용량",        "type":"잔여포인트", "dir":"HIGH"},
    "Var8":  {"name":"포인트잔여량",               "type":"잔여포인트", "dir":"LOW"},
    "Var9":  {"name":"최근포인트증가여부",          "type":"잔여포인트", "dir":"LOW"},
    "Var10": {"name":"최근민원발생빈도",            "type":"고객불만",   "dir":"HIGH"},
    "Var11": {"name":"최근VOC발생빈도",             "type":"고객불만",   "dir":"HIGH"},
    "Var12": {"name":"최근온라인민원접수빈도",       "type":"고객불만",   "dir":"HIGH"},
    "Var13": {"name":"한달내만기대상카드존재여부",  "type":"카드보유",   "dir":"HIGH"},
    "Var14": {"name":"최근보유카드탈회수",          "type":"카드보유",   "dir":"HIGH"},
    "Var15": {"name":"최근카드분실신고여부",        "type":"카드보유",   "dir":"HIGH"},
    "Var16": {"name":"최근한달앱접속건수",          "type":"디지털이용", "dir":"LOW"},
    "Var17": {"name":"디지털이용빈도증감률",        "type":"디지털이용", "dir":"LOW"},
    "Var18": {"name":"마케팅Push개봉건수",          "type":"디지털이용", "dir":"LOW"},
}
TYPE_STRATEGY = {
    "신판이용":   ("무이자할부 제공",              "당월 50만원 이상 이용 시 3개월 무이자할부"),
    "타사이용":   ("신판 30만원 추가이용 시 캐시백","전월 대비 30만원 추가 이용 시 3만원 캐시백"),
    "잔여포인트": ("외식업종 포인트 2배",           "외식업종 이용 시 포인트 2배 적립"),
    "고객불만":   ("5천 포인트 제공",               "즉시 5,000 포인트 + VOC 전담 상담사 연결"),
    "카드보유":   ("추가 카드 발급 시 연회비 할인", "신규 카드 발급 시 첫 해 연회비 100% 면제"),
    "디지털이용": ("앱 접속 시 투썸 쿠폰 제공",    "앱 로그인 시 투썸플레이스 아메리카노 쿠폰 발송"),
}
TYPE_ICONS = {"신판이용":"💳","타사이용":"🔄","잔여포인트":"⭐","고객불만":"📞","카드보유":"🪪","디지털이용":"📱"}
VAR_COLS = [f"Var{i}" for i in range(1, 19)]

def calc_contribs(row, avgs):
    c = {}
    for var, info in ONTOLOGY.items():
        v = row.get(var, 0.5)
        a = avgs.get(var, 0.5)
        c[var] = max(0, a - v) if info["dir"] == "LOW" else max(0, v - a)
    total = sum(c.values()) or 1
    return {k: round(v/total*100, 1) for k, v in c.items()}

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
<div class="main-header">
  <div class="main-title">🎯 고객 이탈 원인 분석 및 초개인화 리텐션 Agent</div>
  <div class="main-sub">XAI 기반 이탈 원인 진단 → 온톨로지 유형 분류 → 맞춤 리텐션 자동 실행</div>
  <span class="badge">XAI 기반</span>
  <span class="badge">온톨로지 분류</span>
  <span class="badge">Human-in-the-Loop</span>
  <span class="badge">초개인화 리텐션</span>
</div>
""", unsafe_allow_html=True)

# ══ STEP 1: 업로드 ══
st.markdown('<div class="sec-label">STEP 01</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">📂 고객 데이터 업로드</div>', unsafe_allow_html=True)

col_u, col_d = st.columns([3, 1])
with col_u:
    uploaded = st.file_uploader("CSV 또는 Excel 업로드", type=["csv","xlsx"], label_visibility="collapsed")
    st.caption("필수 컬럼: 고객번호, Var1~Var18 (0~1 스케일링 값), Score")
with col_d:
    use_demo = st.button("🔍 더미 데이터로\n시연하기", use_container_width=True)

st.divider()

df = None
if use_demo or "demo" in st.session_state:
    st.session_state["demo"] = True
    np.random.seed(99); n = 50
    demo = {"고객번호": [f"CL_{str(i).zfill(3)}" for i in range(1, n+1)]}
    for i in range(1, 19):
        demo[f"Var{i}"] = np.random.uniform(0, 1, n).round(4)
    df = pd.DataFrame(demo)
    avgs_d = {v: 0.5 for v in VAR_COLS}
    scores = []
    for _, row in df.iterrows():
        r = row.to_dict()
        s = 0
        weights = {"Var1":-0.08,"Var2":-0.07,"Var3":-0.07,"Var4":0.09,"Var5":0.08,"Var6":-0.07,
                   "Var7":0.06,"Var8":-0.05,"Var9":-0.05,"Var10":0.09,"Var11":0.08,"Var12":0.07,
                   "Var13":0.06,"Var14":0.05,"Var15":0.04,"Var16":-0.05,"Var17":-0.04,"Var18":-0.04}
        for v, w in weights.items():
            s += (r[v] - 0.5) * w * 2
        scores.append(round(s, 6))
    df["Score"] = scores
    st.success(f"✅ 더미 데이터 로드 완료 — 고객 {n}명")

elif uploaded:
    try:
        df = pd.read_csv(uploaded) if uploaded.name.endswith('.csv') else pd.read_excel(uploaded)
        df.columns = [c.strip() for c in df.columns]
        st.success(f"✅ 업로드 완료 — 고객 {len(df)}명")
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")

# ══ 데이터 미리보기 + 통계 ══
if df is not None:
    id_col = "고객번호" if "고객번호" in df.columns else df.columns[0]
    avail_vars = [v for v in VAR_COLS if v in df.columns]

    with st.expander("📋 데이터 미리보기 및 통계", expanded=True):
        tab1, tab2, tab3 = st.tabs(["🔢 데이터 미리보기", "📊 변수 통계", "📈 Score 분포"])

        with tab1:
            show_cols = [id_col] + avail_vars[:9] + (["Score"] if "Score" in df.columns else [])
            st.dataframe(
                df[show_cols].head(20).style.format({v: "{:.4f}" for v in avail_vars[:9]}),
                use_container_width=True, height=300
            )
            st.caption(f"전체 {len(df)}명 중 상위 20명 표시 / 변수 Var1~Var9 미리보기")

        with tab2:
            stat_df = df[avail_vars].describe().T.round(4)
            stat_df.index.name = "변수"
            stat_df["변수명"] = [ONTOLOGY[v]["name"] for v in stat_df.index]
            stat_df["유형"] = [ONTOLOGY[v]["type"] for v in stat_df.index]
            st.dataframe(
                stat_df[["변수명","유형","mean","std","min","max"]].rename(columns={"mean":"평균","std":"표준편차","min":"최솟값","max":"최댓값"}),
                use_container_width=True, height=400
            )

        with tab3:
            if "Score" in df.columns:
                col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                col_s1.metric("평균 Score", f"{df['Score'].mean():.4f}")
                col_s2.metric("최고 Score", f"{df['Score'].max():.4f}")
                col_s3.metric("최저 Score", f"{df['Score'].min():.4f}")
                col_s4.metric("표준편차", f"{df['Score'].std():.4f}")
                st.bar_chart(df.set_index(id_col)["Score"].sort_values(ascending=False))
            else:
                st.info("Score 컬럼이 없습니다. 온톨로지 기반으로 기여도만 계산합니다.")

    st.divider()

    # ══ STEP 2: 분석 설정 + 실행 ══
    st.markdown('<div class="sec-label">STEP 02</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">⚙️ 분석 설정</div>', unsafe_allow_html=True)

    col_t, col_btn = st.columns([3, 1])
    with col_t:
        threshold = st.slider(
            "이탈 위험 임계값 (Score 기준) — 이 값 이상인 고객을 고위험으로 분류",
            min_value=0.0, max_value=0.5, value=0.1, step=0.01
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        run = st.button("🔍 이탈 원인 분석 실행", use_container_width=True)

    st.divider()

    if run or "done" in st.session_state:
        st.session_state["done"] = True
        st.session_state["thr"] = threshold
        thr = st.session_state.get("thr", 0.1)

        with st.spinner("XAI 변수 기여도 분석 및 온톨로지 유형 분류 중..."):
            avgs = {v: df[v].mean() for v in avail_vars}
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
                    "주요원인": f"{ONTOLOGY[top3[0][0]]['name']} ({top3[0][1]}%)"
                })

        res = pd.DataFrame(rows)
        high = res[res["Score"] >= thr].sort_values("Score", ascending=False)
        new_pats = res[(res["Score"] >= thr) & res["is_new"]]

        # ── STEP 3: 결과 ──
        st.markdown('<div class="sec-label">STEP 03</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">📊 분석 결과 — 이탈 원인 진단</div>', unsafe_allow_html=True)

        n_types = high["주요유형"].nunique() if len(high) > 0 else 0
        st.markdown(f"""
        <div class="kpi-row">
          <div class="kpi-box"><div class="kpi-n">{len(df)}<span style="font-size:15px">명</span></div><div class="kpi-l">전체 분석 고객</div></div>
          <div class="kpi-box"><div class="kpi-n red">{len(high)}<span style="font-size:15px">명</span></div><div class="kpi-l">고위험 고객<br>(Score ≥ {thr})</div></div>
          <div class="kpi-box"><div class="kpi-n">{n_types}<span style="font-size:15px">종</span></div><div class="kpi-l">감지된 이탈 유형</div></div>
          <div class="kpi-box"><div class="kpi-n amb">{len(new_pats)}<span style="font-size:15px">명</span></div><div class="kpi-l">신규 복합 패턴</div></div>
        </div>
        """, unsafe_allow_html=True)

        # 유형별 분포
        if len(high) > 0:
            type_dist = high["주요유형"].value_counts().to_dict()
            cols_t = st.columns(len(type_dist))
            for i, (tp, cnt) in enumerate(sorted(type_dist.items(), key=lambda x: x[1], reverse=True)):
                icon = TYPE_ICONS.get(tp, "")
                strat, _ = TYPE_STRATEGY[tp]
                with cols_t[i]:
                    st.markdown(f"""
                    <div style="background:#fff;border:1.5px solid #D0DCFF;border-radius:10px;padding:12px;text-align:center;margin-bottom:16px;">
                      <div style="font-size:20px">{icon}</div>
                      <div style="font-size:12px;font-weight:700;color:#0B1F4E;margin:4px 0">{tp}</div>
                      <div style="font-size:20px;font-weight:900;color:#0046AD">{cnt}명</div>
                      <div style="font-size:10px;color:#777;margin-top:4px">{strat}</div>
                    </div>
                    """, unsafe_allow_html=True)

        if len(new_pats) > 0:
            ids_str = ', '.join(str(x) for x in list(new_pats["고객ID"])[:5])
            st.markdown(f"""
            <div class="alert">
              <div class="at">⚠️ 신규 복합 이탈 패턴 Alert</div>
              단일 유형으로 분류되지 않는 복합 이탈 패턴 고객 <b>{len(new_pats)}명</b> 감지.<br>
              온톨로지 신규 유형 추가를 검토해 주세요.<br>
              <span style="font-size:11px;color:#aaa">대상: {ids_str} 등</span>
            </div>
            """, unsafe_allow_html=True)

        # 고위험 고객 카드
        if len(high) > 0:
            st.markdown("**🔴 고위험 이탈 고객 상세 분석**")
            for _, r in high.head(10).iterrows():
                sc_val = float(r["Score"])
                sc_cls = "rc" if sc_val >= 0.3 else "rc mid"
                sc_color = "#E53935" if sc_val >= 0.3 else "#FB8C00"
                sc_bg    = "#FFEBEE" if sc_val >= 0.3 else "#FFF3E0"
                tp   = r["주요유형"]
                icon = TYPE_ICONS.get(tp, "")
                type_cls = f"t-{tp}"

                bars_html = ""
                for v, p in r["top3"]:
                    vname = ONTOLOGY[v]["name"]
                    vtype = ONTOLOGY[v]["type"]
                    bars_html += (
                        f'<div class="bw">'
                        f'<div class="bl">'
                        f'<span style="color:#333">{vname}'
                        f'<span style="font-size:10px;color:#999;margin-left:4px">({vtype})</span></span>'
                        f'<span style="font-weight:700;color:#0046AD">{p}%</span>'
                        f'</div>'
                        f'<div class="bb"><div class="bf" style="width:{p}%"></div></div>'
                        f'</div>'
                    )

                type_bars_html = ""
                for t, s in sorted(r["type_scores"].items(), key=lambda x: x[1], reverse=True)[:3]:
                    tico = TYPE_ICONS.get(t, "")
                    type_bars_html += f'<span style="font-size:11px;color:#444;margin-right:12px">{tico} {t} <b style="color:#0046AD">{round(s,1)}%</b></span>'

                new_badge_html = ""
                if r["is_new"]:
                    new_badge_html = '<span style="background:#FFF3E0;color:#E65100;border:1px solid #FFE0B2;padding:1px 8px;border-radius:10px;font-size:10px;font-weight:700;margin-left:6px">신규패턴</span>'

                st.markdown(
                    f'<div class="{sc_cls}">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:6px;">'
                    f'<div style="display:flex;align-items:center;gap:8px;">'
                    f'<span style="font-size:15px;font-weight:900;color:#0B1F4E">{r["고객ID"]}</span>'
                    f'<span class="{type_cls}">{icon} {tp}</span>'
                    f'{new_badge_html}'
                    f'</div>'
                    f'<div style="display:flex;align-items:center;gap:6px;">'
                    f'<span style="font-size:11px;color:#999">이탈 Score</span>'
                    f'<span style="font-size:22px;font-weight:900;color:{sc_color};background:{sc_bg};padding:2px 10px;border-radius:8px">{round(sc_val,4)}</span>'
                    f'</div>'
                    f'</div>'
                    f'<div style="font-size:11px;color:#888;margin-bottom:8px">{type_bars_html}</div>'
                    f'<div style="font-size:11.5px;color:#333;background:#F8FAFF;border-radius:7px;padding:7px 11px;margin-bottom:10px;">'
                    f'📌 주요 이탈 원인: <b style="color:#0046AD">{r["주요원인"]}</b>'
                    f'</div>'
                    f'{bars_html}'
                    f'<div style="margin-top:12px;padding-top:10px;border-top:1px solid #EEF3FF;display:flex;align-items:center;gap:8px;flex-wrap:wrap;">'
                    f'<span style="font-size:11px;color:#999;font-weight:600">추천 리텐션</span>'
                    f'<span class="ob">{r["전략"]}</span>'
                    f'<span style="font-size:11px;color:#555">{r["전략상세"]}</span>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info(f"임계값 {thr} 이상인 고위험 고객이 없습니다. 임계값을 낮춰보세요.")

        st.divider()

        # ── STEP 4: 승인 ──
        st.markdown('<div class="sec-label">STEP 04 · Human-in-the-Loop</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">✅ 현업 검토 및 캠페인 승인</div>', unsafe_allow_html=True)
        st.caption("Agent가 분석한 리텐션 전략을 검토하고 실행을 승인해 주세요.")
        ca, cb_, cc = st.columns(3)
        with ca: approve = st.button("✅ 전체 승인 후 캠페인 실행", use_container_width=True)
        with cb_: st.button("✏️ 일부 수정 후 실행", use_container_width=True)
        with cc:  st.button("⏸ 보류", use_container_width=True)
        st.divider()

        # ── STEP 5: 실행 ──
        if approve or "camp" in st.session_state:
            st.session_state["camp"] = True
            st.markdown('<div class="sec-label">STEP 05</div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-title">🚀 리텐션 캠페인 실행 완료</div>', unsafe_allow_html=True)
            st.success(f"✅ {len(high)}명 대상 초개인화 리텐션 캠페인이 실행되었습니다.")

            type_counts = high["주요유형"].value_counts().to_dict()
            si_html = "".join(
                f'<div class="si"><div class="sn">{cnt}</div><div class="sl">{TYPE_ICONS.get(tp,"")} {tp}</div></div>'
                for tp, cnt in type_counts.items()
            )
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
            st.markdown(
                f'<div class="rsbox">'
                f'<div style="font-size:11.5px;color:rgba(255,255,255,0.45);margin-bottom:4px">{now_str} · 캠페인 실행 현황</div>'
                f'<div class="sg">'
                f'<div class="si"><div class="sn">{len(high)}</div><div class="sl">총 발송 대상</div></div>'
                f'{si_html}'
                f'</div>'
                f'<div style="margin-top:18px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.1);font-size:11.5px;color:rgba(255,255,255,0.4)">'
                f'Push / LMS / 카카오톡 채널 자동 선택 완료 · 성과 데이터는 24시간 후 자동 수집됩니다'
                f'</div></div>',
                unsafe_allow_html=True
            )
            st.divider()

            # ── STEP 6: 성과 ──
            st.markdown('<div class="sec-label">STEP 06 · 성과 리포트</div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-title">📈 캠페인 성과 리포트 (시뮬레이션)</div>', unsafe_allow_html=True)
            sim = round(random.uniform(28, 44), 1)
            sim_s = int(len(high) * sim / 100)
            m1, m2, m3 = st.columns(3)
            m1.metric("예상 리텐션 전환율", f"{sim}%", f"+{round(sim-18,1)}%p vs 기존 일괄 오퍼")
            m2.metric("이탈 방어 예상 고객", f"{sim_s}명")
            m3.metric("오퍼 비용 효율", "↑ 개선", "유형별 맞춤 오퍼 적용")
            st.markdown(
                '<div class="qb">'
                '"이제 마케터의 역할은 데이터를 찾는 것이 아니라,<br>'
                'Agent가 발견한 인사이트를 바탕으로 더 나은 마케팅 방식을 고민하는 것으로 전환됩니다."'
                '</div>',
                unsafe_allow_html=True
            )

st.markdown(
    '<div style="text-align:center;padding:32px 0 8px;color:#BBC8DD;font-size:11px;letter-spacing:0.04em;">'
    '고객 이탈 원인 분석 및 초개인화 리텐션 Agent (XAI 기반)'
    '</div>',
    unsafe_allow_html=True
)
