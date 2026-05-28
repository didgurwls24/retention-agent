import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

st.set_page_config(
    page_title="이탈 원인 분석 리텐션 Agent",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS — Streamlit 기본 건드리지 않고 최소한만
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif !important; }

.hdr {
    background: #0F172A;
    border-radius: 12px;
    padding: 24px 28px 20px;
    margin-bottom: 24px;
}
.hdr h1 { font-size: 18px; font-weight: 700; color: #F1F5F9; margin: 0 0 4px; }
.hdr p  { font-size: 12px; color: #64748B; margin: 0 0 12px; }
.hdr-tag {
    display: inline-block;
    font-size: 10.5px; font-weight: 600; color: #94A3B8;
    border: 1px solid #334155; border-radius: 20px;
    padding: 2px 10px; margin: 0 4px 4px 0;
}

.sec-tag  { font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: .1em; text-transform: uppercase; margin: 0 0 2px; }
.sec-head { font-size: 15px; font-weight: 700; color: #0F172A; margin: 0 0 12px; }

.card {
    background: #fff;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
}
.card-hl  { border-left: 4px solid #EF4444; }
.card-mid { border-left: 4px solid #F59E0B; }

.kpi-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
.kpi {
    flex: 1; min-width: 100px;
    background: #F8FAFC; border: 1px solid #E2E8F0;
    border-radius: 8px; padding: 12px 14px;
}
.kpi-v { font-size: 22px; font-weight: 700; color: #0F172A; line-height: 1; margin-bottom: 3px; }
.kpi-v.r { color: #DC2626; }
.kpi-v.a { color: #D97706; }
.kpi-l { font-size: 11px; color: #64748B; }

.type-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
.type-box {
    flex: 1; min-width: 100px;
    background: #F8FAFC; border: 1px solid #E2E8F0;
    border-radius: 8px; padding: 12px 10px; text-align: center;
}
.type-box .ico  { font-size: 16px; margin-bottom: 4px; }
.type-box .nm   { font-size: 11px; font-weight: 600; color: #374151; }
.type-box .cnt  { font-size: 20px; font-weight: 700; color: #0F172A; }
.type-box .str  { font-size: 9.5px; color: #94A3B8; margin-top: 2px; line-height: 1.3; }

.pill {
    display: inline-block; font-size: 11px; font-weight: 600;
    border-radius: 20px; padding: 2px 9px;
}
.p-신판 { color:#1D4ED8; background:#EFF6FF; border:1px solid #BFDBFE; }
.p-타사 { color:#7C3AED; background:#F5F3FF; border:1px solid #DDD6FE; }
.p-포인트{ color:#059669; background:#ECFDF5; border:1px solid #A7F3D0; }
.p-불만 { color:#DC2626; background:#FEF2F2; border:1px solid #FECACA; }
.p-카드 { color:#B45309; background:#FFFBEB; border:1px solid #FDE68A; }
.p-디지털{ color:#0E7490; background:#ECFEFF; border:1px solid #A5F3FC; }
.p-신규 { color:#9A3412; background:#FFF7ED; border:1px solid #FED7AA; }

.score-chip {
    font-size: 18px; font-weight: 700;
    padding: 2px 10px; border-radius: 6px;
}
.sc-r { color: #DC2626; background: #FEF2F2; }
.sc-a { color: #D97706; background: #FFFBEB; }

.bar-wrap  { margin: 5px 0; }
.bar-top   { display: flex; justify-content: space-between; font-size: 11.5px; color: #374151; margin-bottom: 2px; }
.bar-bg    { background: #F1F5F9; border-radius: 3px; height: 6px; overflow: hidden; }
.bar-fill  { background: #3B82F6; border-radius: 3px; height: 6px; }

.cause-box {
    background: #F8FAFC; border: 1px solid #E2E8F0;
    border-radius: 6px; padding: 7px 11px; margin-bottom: 10px;
    font-size: 11.5px; color: #374151;
}

.offer-chip {
    display: inline-block; font-size: 11.5px; font-weight: 600;
    color: #1D4ED8; background: #EFF6FF;
    border: 1px solid #BFDBFE; border-radius: 20px;
    padding: 3px 11px; margin-right: 6px;
}
.offer-desc { font-size: 11px; color: #64748B; }

.alert-box {
    background: #FFFBEB; border: 1px solid #FDE68A;
    border-left: 3px solid #F59E0B;
    border-radius: 8px; padding: 12px 16px; margin: 12px 0;
}
.alert-ttl { font-size: 12.5px; font-weight: 700; color: #92400E; margin-bottom: 4px; }
.alert-txt { font-size: 11.5px; color: #78350F; }

.result-box {
    background: #0F172A; border-radius: 10px;
    padding: 20px 24px; margin-top: 12px;
}
.result-row { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 12px; }
.ri-v { font-size: 24px; font-weight: 700; color: #60A5FA; line-height: 1; margin-bottom: 2px; }
.ri-l { font-size: 11px; color: #94A3B8; }
.result-ft { font-size: 11px; color: #475569; margin-top: 14px; padding-top: 12px; border-top: 1px solid #1E293B; }

.quote-box {
    background: #EFF6FF; border-left: 3px solid #3B82F6;
    border-radius: 0 8px 8px 0; padding: 12px 18px; margin-top: 12px;
    font-size: 12.5px; color: #1E40AF; font-style: italic; line-height: 1.8;
}
</style>
""", unsafe_allow_html=True)

# ══ 온톨로지 ══
ONTOLOGY = {
    "Var1":  {"name":"최근일주일내이용건수",         "type":"신판이용",  "dir":"LOW"},
    "Var2":  {"name":"한달전대비이용금액증감률",      "type":"신판이용",  "dir":"LOW"},
    "Var3":  {"name":"일주일전대비이용금액증감률",    "type":"신판이용",  "dir":"LOW"},
    "Var4":  {"name":"타사카드신규개설여부",          "type":"타사이용",  "dir":"HIGH"},
    "Var5":  {"name":"최근한달타사카드이용금액증감률","type":"타사이용",  "dir":"HIGH"},
    "Var6":  {"name":"최근한달타사대비당사이용비율",  "type":"타사이용",  "dir":"LOW"},
    "Var7":  {"name":"최근한달포인트사용량",          "type":"잔여포인트","dir":"HIGH"},
    "Var8":  {"name":"포인트잔여량",                  "type":"잔여포인트","dir":"LOW"},
    "Var9":  {"name":"최근포인트증가여부",            "type":"잔여포인트","dir":"LOW"},
    "Var10": {"name":"최근민원발생빈도",              "type":"고객불만",  "dir":"HIGH"},
    "Var11": {"name":"최근VOC발생빈도",               "type":"고객불만",  "dir":"HIGH"},
    "Var12": {"name":"최근온라인민원접수빈도",         "type":"고객불만",  "dir":"HIGH"},
    "Var13": {"name":"한달내만기대상카드존재여부",     "type":"카드보유",  "dir":"HIGH"},
    "Var14": {"name":"최근보유카드탈회수",             "type":"카드보유",  "dir":"HIGH"},
    "Var15": {"name":"최근카드분실신고여부",           "type":"카드보유",  "dir":"HIGH"},
    "Var16": {"name":"최근한달앱접속건수",             "type":"디지털이용","dir":"LOW"},
    "Var17": {"name":"디지털이용빈도증감률",           "type":"디지털이용","dir":"LOW"},
    "Var18": {"name":"마케팅Push개봉건수",             "type":"디지털이용","dir":"LOW"},
}
TYPE_STRATEGY = {
    "신판이용":   ("무이자할부 제공",               "당월 50만원 이상 이용 시 3개월 무이자할부"),
    "타사이용":   ("30만원 추가이용 시 캐시백",     "전월 대비 30만원 추가 이용 시 3만원 캐시백"),
    "잔여포인트": ("외식업종 포인트 2배",           "외식업종 이용 시 포인트 2배 적립"),
    "고객불만":   ("5천 포인트 제공",               "즉시 5,000 포인트 + VOC 전담 상담사 연결"),
    "카드보유":   ("추가 카드 연회비 할인",         "신규 카드 발급 시 첫 해 연회비 100% 면제"),
    "디지털이용": ("앱 접속 시 투썸 쿠폰",         "앱 로그인 시 투썸플레이스 아메리카노 쿠폰"),
}
TYPE_ICONS = {"신판이용":"💳","타사이용":"🔄","잔여포인트":"⭐","고객불만":"📞","카드보유":"🪪","디지털이용":"📱"}
TYPE_PILL  = {"신판이용":"p-신판","타사이용":"p-타사","잔여포인트":"p-포인트","고객불만":"p-불만","카드보유":"p-카드","디지털이용":"p-디지털"}
VAR_COLS = [f"Var{i}" for i in range(1, 19)]

def calc_contribs(row, avgs):
    c = {}
    for var, info in ONTOLOGY.items():
        v, a = float(row.get(var, 0.5)), float(avgs.get(var, 0.5))
        c[var] = max(0.0, a-v) if info["dir"]=="LOW" else max(0.0, v-a)
    t = sum(c.values()) or 1.0
    return {k: round(v/t*100,1) for k,v in c.items()}

def dominant_type(cb):
    ts = {}
    for var, pct in cb.items():
        tp = ONTOLOGY[var]["type"]
        ts[tp] = ts.get(tp, 0) + pct
    dom = max(ts, key=ts.get)
    top2 = sorted(ts.values(), reverse=True)[:2]
    is_new = (top2[0] + (top2[1] if len(top2)>1 else 0)) < 40
    return dom, ts, is_new

# ══ 헤더 ══
st.markdown("""
<div class="hdr">
  <h1>🎯 고객 이탈 원인 분석 및 초개인화 리텐션 Agent</h1>
  <p>XAI 기반 이탈 원인 진단 → 온톨로지 유형 분류 → 맞춤 리텐션 자동 실행</p>
  <span class="hdr-tag">XAI 기반</span>
  <span class="hdr-tag">온톨로지 분류</span>
  <span class="hdr-tag">Human-in-the-Loop</span>
  <span class="hdr-tag">초개인화 리텐션</span>
</div>
""", unsafe_allow_html=True)

# ══ STEP 1 ══
st.markdown('<p class="sec-tag">STEP 01</p><p class="sec-head">고객 데이터 업로드</p>', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "CSV 또는 Excel 업로드 (고객번호, Var1~Var18, Score)",
    type=["csv","xlsx"]
)
use_demo = st.button("🔍  더미 데이터로 시연하기")

st.divider()

df = None
if use_demo or "demo" in st.session_state:
    st.session_state["demo"] = True
    np.random.seed(99); n = 50
    demo = {"고객번호": [f"CL_{str(i).zfill(3)}" for i in range(1,n+1)]}
    for i in range(1,19):
        demo[f"Var{i}"] = np.random.uniform(0,1,n).round(4)
    df = pd.DataFrame(demo)
    W = {"Var1":-0.08,"Var2":-0.07,"Var3":-0.07,"Var4":0.09,"Var5":0.08,"Var6":-0.07,
         "Var7":0.06,"Var8":-0.05,"Var9":-0.05,"Var10":0.09,"Var11":0.08,"Var12":0.07,
         "Var13":0.06,"Var14":0.05,"Var15":0.04,"Var16":-0.05,"Var17":-0.04,"Var18":-0.04}
    df["Score"] = [round(sum((row[v]-0.5)*w*2 for v,w in W.items()), 6) for _,row in df.iterrows()]
    st.success(f"✅  더미 데이터 {n}명 로드 완료")
elif uploaded:
    try:
        df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        df.columns = [c.strip() for c in df.columns]
        st.success(f"✅  업로드 완료 — 총 {len(df)}명")
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")

# ══ 미리보기 ══
if df is not None:
    id_col = "고객번호" if "고객번호" in df.columns else df.columns[0]
    av = [v for v in VAR_COLS if v in df.columns]

    with st.expander("📋  데이터 미리보기 및 통계"):
        t1, t2, t3 = st.tabs(["미리보기", "변수 통계", "Score 분포"])
        with t1:
            show = [id_col]+av[:9]+(["Score"] if "Score" in df.columns else [])
            st.dataframe(df[show].head(20), use_container_width=True, height=260)
        with t2:
            stat = df[av].describe().T.round(4)
            stat["변수명"] = [ONTOLOGY[v]["name"] for v in stat.index]
            stat["유형"]  = [ONTOLOGY[v]["type"]  for v in stat.index]
            st.dataframe(
                stat[["변수명","유형","mean","std","min","max"]].rename(
                    columns={"mean":"평균","std":"표준편차","min":"최솟값","max":"최댓값"}),
                use_container_width=True, height=360)
        with t3:
            if "Score" in df.columns:
                c1,c2,c3,c4 = st.columns(4)
                c1.metric("평균", f"{df['Score'].mean():.4f}")
                c2.metric("최고", f"{df['Score'].max():.4f}")
                c3.metric("최저", f"{df['Score'].min():.4f}")
                c4.metric("표준편차", f"{df['Score'].std():.4f}")
                st.bar_chart(df.set_index(id_col)["Score"].sort_values(ascending=False))

    st.divider()

    # ══ STEP 2 ══
    st.markdown('<p class="sec-tag">STEP 02</p><p class="sec-head">분석 설정 및 실행</p>', unsafe_allow_html=True)
    threshold = st.slider("이탈 위험 임계값 (Score 기준)", 0.0, 0.5, 0.1, 0.01,
                          help="이 값 이상인 고객을 고위험으로 분류합니다")
    run = st.button("▶  이탈 원인 분석 실행", type="primary")
    st.divider()

    if run or "done" in st.session_state:
        st.session_state["done"] = True
        st.session_state["thr"] = threshold
        thr = st.session_state.get("thr", 0.1)

        with st.spinner("XAI 변수 기여도 분석 및 온톨로지 유형 분류 중..."):
            avgs = {v: float(df[v].mean()) for v in av}
            rows = []
            for _, row in df.iterrows():
                r = row.to_dict()
                sc = float(r.get("Score", 0))
                cb = calc_contribs(r, avgs)
                dom, ts, is_new = dominant_type(cb)
                strat, detail = TYPE_STRATEGY[dom]
                top3 = sorted(cb.items(), key=lambda x: x[1], reverse=True)[:3]
                rows.append({
                    "고객ID": r[id_col], "Score": sc, "주요유형": dom,
                    "type_scores": ts, "is_new": is_new, "기여도": cb,
                    "top3": top3, "전략": strat, "전략상세": detail,
                    "주요원인": ONTOLOGY[top3[0][0]]["name"],
                    "주요원인_pct": top3[0][1],
                })

        res  = pd.DataFrame(rows)
        high = res[res["Score"] >= thr].sort_values("Score", ascending=False)
        newp = res[(res["Score"] >= thr) & res["is_new"]]

        # ── STEP 3 ──
        st.markdown('<p class="sec-tag">STEP 03</p><p class="sec-head">분석 결과 — 이탈 원인 진단</p>', unsafe_allow_html=True)

        n_types = int(high["주요유형"].nunique()) if len(high) > 0 else 0
        st.markdown(
            f'<div class="kpi-row">'
            f'<div class="kpi"><div class="kpi-v">{len(df)}</div><div class="kpi-l">전체 분석 고객</div></div>'
            f'<div class="kpi"><div class="kpi-v r">{len(high)}</div><div class="kpi-l">고위험 고객 (Score ≥ {thr:.2f})</div></div>'
            f'<div class="kpi"><div class="kpi-v">{n_types}</div><div class="kpi-l">감지된 이탈 유형</div></div>'
            f'<div class="kpi"><div class="kpi-v a">{len(newp)}</div><div class="kpi-l">신규 복합 패턴</div></div>'
            f'</div>', unsafe_allow_html=True)

        if len(high) > 0:
            td = high["주요유형"].value_counts().to_dict()
            html = '<div class="type-row">'
            for tp, cnt in sorted(td.items(), key=lambda x: x[1], reverse=True):
                s,_ = TYPE_STRATEGY[tp]
                html += (f'<div class="type-box">'
                         f'<div class="ico">{TYPE_ICONS.get(tp,"")}</div>'
                         f'<div class="nm">{tp}</div>'
                         f'<div class="cnt">{cnt}명</div>'
                         f'<div class="str">{s}</div>'
                         f'</div>')
            st.markdown(html + '</div>', unsafe_allow_html=True)

        if len(newp) > 0:
            ids_str = ", ".join(str(x) for x in list(newp["고객ID"])[:5])
            st.markdown(
                f'<div class="alert-box">'
                f'<div class="alert-ttl">⚠ 신규 복합 이탈 패턴 Alert</div>'
                f'<div class="alert-txt">단일 유형으로 분류되지 않는 복합 패턴 고객 <b>{len(newp)}명</b> 감지.'
                f' 온톨로지 신규 유형 추가를 검토해 주세요.<br>'
                f'<span style="font-size:11px">대상: {ids_str} 등</span></div>'
                f'</div>', unsafe_allow_html=True)

        if len(high) > 0:
            st.markdown("##### 고위험 이탈 고객 상세 분석")
            for _, r in high.head(10).iterrows():
                sc_val   = float(r["Score"])
                card_cls = "card card-hl" if sc_val >= 0.3 else "card card-mid"
                chip_cls = "score-chip sc-r" if sc_val >= 0.3 else "score-chip sc-a"
                tp       = str(r["주요유형"])
                pc       = TYPE_PILL.get(tp, "p-신규") if not r["is_new"] else "p-신규"
                tp_lbl   = tp + (" ·신규패턴" if r["is_new"] else "")

                bars = ""
                for v, p in r["top3"]:
                    bars += (
                        f'<div class="bar-wrap">'
                        f'<div class="bar-top">'
                        f'<span>{ONTOLOGY[v]["name"]}'
                        f'<span style="font-size:10px;color:#94A3B8;margin-left:4px">({ONTOLOGY[v]["type"]})</span></span>'
                        f'<span style="color:#2563EB;font-weight:600">{p}%</span>'
                        f'</div>'
                        f'<div class="bar-bg"><div class="bar-fill" style="width:{p}%"></div></div>'
                        f'</div>'
                    )
                ts_html = ""
                for t, s in sorted(r["type_scores"].items(), key=lambda x: x[1], reverse=True)[:3]:
                    ts_html += f'<span style="font-size:11px;color:#64748B;margin-right:10px">{TYPE_ICONS.get(t,"")} {t} <b style="color:#374151">{round(s,1)}%</b></span>'

                st.markdown(
                    f'<div class="{card_cls}">'
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:6px">'
                    f'<div style="display:flex;align-items:center;gap:8px">'
                    f'<span style="font-size:14px;font-weight:700;color:#0F172A">{r["고객ID"]}</span>'
                    f'<span class="pill {pc}">{TYPE_ICONS.get(r["주요유형"],"")} {tp_lbl}</span>'
                    f'</div>'
                    f'<span class="{chip_cls}">{round(sc_val,4)}</span>'
                    f'</div>'
                    f'<div style="font-size:11px;color:#94A3B8;margin-bottom:8px">{ts_html}</div>'
                    f'<div class="cause-box">주요 이탈 원인: <span style="color:#1D4ED8;font-weight:600">{r["주요원인"]} ({r["주요원인_pct"]}%)</span></div>'
                    f'{bars}'
                    f'<div style="margin-top:10px;padding-top:10px;border-top:1px solid #F1F5F9;display:flex;align-items:center;gap:8px;flex-wrap:wrap">'
                    f'<span style="font-size:11px;color:#94A3B8;font-weight:600">추천 리텐션</span>'
                    f'<span class="offer-chip">{r["전략"]}</span>'
                    f'<span class="offer-desc">{r["전략상세"]}</span>'
                    f'</div></div>',
                    unsafe_allow_html=True)
        else:
            st.info(f"임계값 {thr:.2f} 이상인 고위험 고객이 없습니다. 슬라이더를 낮춰보세요.")

        st.divider()

        # ── STEP 4 ──
        st.markdown('<p class="sec-tag">STEP 04 · Human-in-the-Loop</p><p class="sec-head">현업 검토 및 캠페인 승인</p>', unsafe_allow_html=True)
        st.caption("Agent가 분석한 리텐션 전략을 검토하고 실행을 승인해 주세요.")
        ca, cb_, cc = st.columns(3)
        with ca: approve = st.button("✅  전체 승인 후 캠페인 실행", use_container_width=True, type="primary")
        with cb_: st.button("✏️  일부 수정 후 실행", use_container_width=True)
        with cc:  st.button("⏸  보류", use_container_width=True)
        st.divider()

        # ── STEP 5 ──
        if approve or "camp" in st.session_state:
            st.session_state["camp"] = True
            st.markdown('<p class="sec-tag">STEP 05</p><p class="sec-head">리텐션 캠페인 실행 완료</p>', unsafe_allow_html=True)
            st.success(f"✅  {len(high)}명 대상 초개인화 리텐션 캠페인이 실행되었습니다.")

            tc = high["주요유형"].value_counts().to_dict()
            ri = "".join(f'<div><div class="ri-v">{cnt}</div><div class="ri-l">{TYPE_ICONS.get(tp,"")} {tp}</div></div>' for tp,cnt in tc.items())
            now = datetime.now().strftime('%Y-%m-%d %H:%M')
            st.markdown(
                f'<div class="result-box">'
                f'<div style="font-size:11px;color:#475569">{now} · 캠페인 실행 현황</div>'
                f'<div class="result-row">'
                f'<div><div class="ri-v">{len(high)}</div><div class="ri-l">총 발송 대상</div></div>'
                f'{ri}</div>'
                f'<div class="result-ft">Push / LMS / 카카오톡 채널 자동 선택 완료 · 성과 데이터는 24시간 후 자동 수집됩니다</div>'
                f'</div>', unsafe_allow_html=True)
            st.divider()

            # ── STEP 6 ──
            st.markdown('<p class="sec-tag">STEP 06 · 성과 리포트</p><p class="sec-head">캠페인 성과 리포트 (시뮬레이션)</p>', unsafe_allow_html=True)
            sim = round(random.uniform(28,44),1)
            m1,m2,m3 = st.columns(3)
            m1.metric("예상 리텐션 전환율", f"{sim}%", f"+{round(sim-18,1)}%p vs 기존 일괄 오퍼")
            m2.metric("이탈 방어 예상 고객", f"{int(len(high)*sim/100)}명")
            m3.metric("오퍼 비용 효율", "↑ 개선", "유형별 맞춤 오퍼 적용")
            st.markdown(
                '<div class="quote-box">'
                '"이제 마케터의 역할은 데이터를 찾는 것이 아니라,<br>'
                'Agent가 발견한 인사이트를 바탕으로 더 나은 마케팅 방식을 고민하는 것으로 전환됩니다."'
                '</div>', unsafe_allow_html=True)

st.markdown('<div style="text-align:center;padding:32px 0 8px;color:#CBD5E1;font-size:11px">고객 이탈 원인 분석 및 초개인화 리텐션 Agent (XAI 기반)</div>', unsafe_allow_html=True)
