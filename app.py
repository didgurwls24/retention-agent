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
html,body,[class*="css"],.stApp{font-family:'Noto Sans KR',sans-serif!important;background-color:#EDF1F8!important;}
.block-container{max-width:1080px!important;padding:1.5rem 2rem!important;margin:0 auto!important;}
.main-header{background:linear-gradient(135deg,#071430 0%,#0B1F4E 55%,#1A3A8F 100%);padding:32px 40px 26px;border-radius:16px;margin-bottom:24px;border-top:5px solid #1565E8;box-shadow:0 6px 24px rgba(7,20,48,0.2);}
.main-title{font-size:21px;font-weight:900;color:#fff;margin:0 0 5px;letter-spacing:-0.3px;line-height:1.3;}
.main-sub{font-size:12px;color:rgba(255,255,255,0.5);margin:0 0 14px;}
.badge{display:inline-block;background:rgba(0,70,173,0.4);border:1px solid rgba(0,100,210,0.35);color:#90C4FF;font-size:10.5px;font-weight:700;padding:3px 11px;border-radius:20px;margin:0 5px 5px 0;}
.sec-label{font-size:10px;font-weight:800;color:#0046AD;letter-spacing:0.14em;text-transform:uppercase;margin-bottom:2px;}
.sec-title{font-size:15px;font-weight:700;color:#0B1F4E;margin-bottom:14px;}
.kpi-row{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap;}
.kpi-box{flex:1;min-width:120px;background:linear-gradient(135deg,#F4F7FF,#EEF3FF);border:1.5px solid #D0DCFF;border-radius:12px;padding:16px 14px;text-align:center;}
.kpi-n{font-size:26px;font-weight:900;color:#0046AD;line-height:1;margin-bottom:4px;}
.kpi-n.red{color:#E53935;}.kpi-n.amber{color:#F57C00;}
.kpi-l{font-size:11px;color:#6680AA;line-height:1.4;}
.rc{background:#fff;border-radius:12px;padding:16px 18px;margin-bottom:10px;border:1.5px solid #D8E4FF;border-left:5px solid #E53935;}
.rc.mid{border-left-color:#FB8C00;}
.bw{margin:6px 0;}.bl{display:flex;justify-content:space-between;font-size:11.5px;color:#555;margin-bottom:2px;}
.bb{background:#EEF3FF;border-radius:5px;height:7px;width:100%;overflow:hidden;}
.bf{background:linear-gradient(90deg,#0046AD,#1565E8);border-radius:5px;height:7px;}
.type-신판이용{background:#E3F2FD;color:#1565C0;border:1px solid #BBDEFB;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700;}
.type-타사이용{background:#FCE4EC;color:#880E4F;border:1px solid #F8BBD0;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700;}
.type-잔여포인트{background:#F3E5F5;color:#6A1B9A;border:1px solid #E1BEE7;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700;}
.type-고객불만{background:#FFEBEE;color:#B71C1C;border:1px solid #FFCDD2;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700;}
.type-카드보유{background:#FFF8E1;color:#F57F17;border:1px solid #FFECB3;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700;}
.type-디지털이용{background:#E8F5E9;color:#1B5E20;border:1px solid #C8E6C9;padding:2px 10px;border-radius:20px;font-size:11px;font-weight:700;}
.ob{display:inline-block;background:#EEF3FF;border:1.5px solid #C8D8FF;color:#0046AD;font-size:11.5px;font-weight:700;padding:3px 12px;border-radius:20px;margin-right:6px;}
.alert{background:#FFF8E1;border:1.5px solid #FFB74D;border-left:5px solid #FF8F00;border-radius:10px;padding:14px 18px;margin:14px 0;}
.at{font-size:13px;font-weight:700;color:#E65100;margin-bottom:4px;}
.rsbox{background:linear-gradient(135deg,#071430,#0B1F4E,#0046AD);border-radius:14px;padding:24px 28px;margin-top:16px;box-shadow:0 6px 20px rgba(0,30,100,0.2);}
.sg{display:flex;gap:16px;flex-wrap:wrap;margin-top:14px;}
.si{flex:1;min-width:80px;}
.sn{font-size:26px;font-weight:900;color:#7AADFF;line-height:1;margin-bottom:3px;}
.sl{font-size:11px;color:rgba(255,255,255,0.5);}
.qb{background:#F4F7FF;border-left:4px solid #0046AD;border-radius:0 10px 10px 0;padding:14px 20px;margin-top:14px;font-size:12.5px;color:#0B1F4E;font-style:italic;line-height:1.8;}
.stButton>button{background:linear-gradient(135deg,#0046AD,#1565E8)!important;color:#fff!important;border:none!important;border-radius:9px!important;font-weight:700!important;font-family:'Noto Sans KR',sans-serif!important;padding:10px 22px!important;font-size:13.5px!important;box-shadow:0 2px 8px rgba(0,70,173,0.2)!important;}
.stButton>button:hover{background:linear-gradient(135deg,#003A8C,#0046AD)!important;box-shadow:0 5px 14px rgba(0,70,173,0.3)!important;transform:translateY(-1px)!important;}
[data-testid="metric-container"]{background:#F4F7FF!important;border:1.5px solid #D0DCFF!important;border-radius:12px!important;padding:12px 14px!important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# 온톨로지 정의 (엑셀 기반)
# ══════════════════════════════════════
ONTOLOGY = {
    "Var1":  {"name":"최근일주일내이용건수",        "type":"신판이용",   "direction":"LOW"},
    "Var2":  {"name":"한달전대비이용금액증감률",      "type":"신판이용",   "direction":"LOW"},
    "Var3":  {"name":"일주일전대비이용금액증감률",    "type":"신판이용",   "direction":"LOW"},
    "Var4":  {"name":"타사카드신규개설여부",          "type":"타사이용",   "direction":"HIGH"},
    "Var5":  {"name":"최근한달타사카드이용금액증감률", "type":"타사이용",   "direction":"HIGH"},
    "Var6":  {"name":"최근한달타사대비당사이용비율",  "type":"타사이용",   "direction":"LOW"},
    "Var7":  {"name":"최근한달포인트사용량",          "type":"잔여포인트", "direction":"HIGH"},
    "Var8":  {"name":"포인트잔여량",                 "type":"잔여포인트", "direction":"LOW"},
    "Var9":  {"name":"최근포인트증가여부",            "type":"잔여포인트", "direction":"LOW"},
    "Var10": {"name":"최근민원발생빈도",              "type":"고객불만",   "direction":"HIGH"},
    "Var11": {"name":"최근VOC발생빈도",               "type":"고객불만",   "direction":"HIGH"},
    "Var12": {"name":"최근온라인민원접수빈도",         "type":"고객불만",   "direction":"HIGH"},
    "Var13": {"name":"한달내만기대상카드존재여부",     "type":"카드보유",   "direction":"HIGH"},
    "Var14": {"name":"최근보유카드탈회수",             "type":"카드보유",   "direction":"HIGH"},
    "Var15": {"name":"최근카드분실신고여부",           "type":"카드보유",   "direction":"HIGH"},
    "Var16": {"name":"최근한달앱접속건수",             "type":"디지털이용", "direction":"LOW"},
    "Var17": {"name":"디지털이용빈도증감률",           "type":"디지털이용", "direction":"LOW"},
    "Var18": {"name":"마케팅Push개봉건수",             "type":"디지털이용", "direction":"LOW"},
}

TYPE_STRATEGY = {
    "신판이용":   {"strategy":"무이자할부 제공",              "detail":"당월 50만원 이상 이용 시 3개월 무이자할부 제공"},
    "타사이용":   {"strategy":"신판 30만원 추가 이용 시 캐시백","detail":"전월 대비 30만원 추가 이용 시 3만원 캐시백"},
    "잔여포인트": {"strategy":"외식업종 포인트 2배",           "detail":"외식업종 이용 시 포인트 2배 적립"},
    "고객불만":   {"strategy":"5천 포인트 제공",               "detail":"즉시 5,000 포인트 지급 + VOC 전담 상담사 연결"},
    "카드보유":   {"strategy":"추가 카드 발급 시 연회비 할인",  "detail":"신규 카드 발급 시 첫 해 연회비 100% 면제"},
    "디지털이용": {"strategy":"앱 접속 시 투썸 쿠폰 제공",     "detail":"앱 로그인 시 투썸플레이스 아메리카노 쿠폰 즉시 발송"},
}

TYPE_ICONS = {
    "신판이용":"💳","타사이용":"🔄","잔여포인트":"⭐",
    "고객불만":"📞","카드보유":"🪪","디지털이용":"📱"
}

VAR_COLS = [f"Var{i}" for i in range(1, 19)]

def compute_churn_contribution(row, avg_dict):
    """
    온톨로지 방향성 기반 기여도 계산
    LOW_INCREASES_CHURN: 평균보다 낮을수록 위험 → 기여도 = max(0, avg - val)
    HIGH_INCREASES_CHURN: 평균보다 높을수록 위험 → 기여도 = max(0, val - avg)
    """
    contribs = {}
    for var, info in ONTOLOGY.items():
        val = row.get(var, 0.5)
        avg = avg_dict.get(var, 0.5)
        if info["direction"] == "LOW":
            contribs[var] = max(0, avg - val)
        else:
            contribs[var] = max(0, val - avg)
    total = sum(contribs.values()) or 1
    return {k: round(v/total*100, 1) for k, v in contribs.items()}

def get_dominant_type(contribs_pct):
    """기여도 합산으로 지배적 이탈 유형 결정"""
    type_scores = {}
    for var, pct in contribs_pct.items():
        t = ONTOLOGY[var]["type"]
        type_scores[t] = type_scores.get(t, 0) + pct
    return max(type_scores, key=type_scores.get), type_scores

def is_new_pattern(type_scores):
    """상위 2개 유형의 합이 50% 미만이면 신규 복합 패턴"""
    sorted_scores = sorted(type_scores.values(), reverse=True)
    return (sorted_scores[0] + (sorted_scores[1] if len(sorted_scores)>1 else 0)) < 40

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

# ══ STEP 1: 데이터 업로드 ══
st.markdown('<div class="sec-label">STEP 01</div><div class="sec-title">📂 고객 데이터 업로드</div>', unsafe_allow_html=True)
col_u, col_d = st.columns([3, 1])
with col_u:
    uploaded = st.file_uploader("CSV 또는 Excel 업로드", type=["csv","xlsx"], label_visibility="collapsed")
    st.caption("필수 컬럼: 고객번호, Var1~Var18 (스케일링된 값), Score")
with col_d:
    use_demo = st.button("🔍 더미 데이터\n시연하기", use_container_width=True)
st.divider()

df = None
if use_demo or "demo" in st.session_state:
    st.session_state["demo"] = True
    # 엑셀 더미 데이터 그대로 사용
    demo_data = {
        "고객번호": [f"CL_{i}" for i in range(1, 29)],
        "Var1":  [0.218,0.082,0.506,0.437,0.211,0.740,0.335,0.752,0.575,0.834,0.537,0.758,0.803,0.178,0.093,0.238,0.144,0.861,0.276,0.942,0.382,0.584,0.959,0.995,0.833,0.941,0.130,0.522],
        "Var2":  [0.391,0.467,0.237,0.082,0.801,0.391,0.996,0.942,0.244,0.011,0.327,0.914,0.746,0.302,0.160,0.454,0.896,0.875,0.969,0.014,0.832,0.703,0.983,0.157,0.495,0.061,0.255,0.801],
        "Var3":  [0.705,0.009,0.889,0.051,0.683,0.339,0.028,0.464,0.287,0.347,0.400,0.298,0.361,0.941,0.555,0.201,0.279,0.611,0.227,0.080,0.988,0.497,0.599,0.366,0.581,0.344,0.668,0.722],
        "Var4":  [0.726,0.449,0.269,0.295,0.059,0.788,0.819,0.988,0.004,0.393,0.279,0.864,0.351,0.710,0.352,0.716,0.304,0.094,0.496,0.047,0.662,0.841,0.859,0.186,0.255,0.128,0.897,0.021],
        "Var5":  [0.728,0.038,0.023,0.907,0.334,0.395,0.328,0.600,0.398,0.500,0.116,0.708,0.750,0.948,0.681,0.028,0.521,0.655,0.579,0.305,0.324,0.887,0.373,0.426,0.087,0.550,0.689,0.760],
        "Var6":  [0.430,0.276,0.266,0.419,0.804,0.844,0.559,0.472,0.320,0.306,0.380,0.734,0.553,0.769,0.989,0.638,0.391,0.186,0.061,0.796,0.424,0.626,0.911,0.317,0.214,0.472,0.460,0.626],
        "Var7":  [0.260,0.690,0.434,0.530,0.398,0.818,0.455,0.546,0.908,0.614,0.746,0.032,0.587,0.361,0.408,0.511,0.621,0.668,0.372,0.695,0.184,0.230,0.371,0.072,0.290,0.434,0.553,0.638],
        "Var8":  [0.588,0.870,0.622,0.274,0.465,0.776,0.728,0.522,0.035,0.199,0.674,0.022,0.340,0.210,0.400,0.679,0.346,0.771,0.113,0.692,0.156,0.005,0.869,0.966,0.153,0.459,0.918,0.028],
        "Var9":  [0.705,0.615,0.596,0.531,0.418,0.356,0.121,0.613,0.882,0.294,0.198,0.866,0.312,0.878,0.950,0.440,0.468,0.990,0.332,0.847,0.773,0.281,0.828,0.380,0.601,0.863,0.964,0.637],
        "Var10": [0.299,0.083,0.854,0.571,0.606,0.029,0.790,0.631,0.811,0.091,0.659,0.020,0.144,0.373,0.797,0.848,0.632,0.022,0.743,0.947,0.863,0.531,0.232,0.433,0.916,0.939,0.695,0.672],
        "Var11": [0.984,0.394,0.471,0.172,0.075,0.965,0.908,0.053,0.536,0.716,0.554,0.187,0.045,0.005,0.674,0.786,0.157,0.696,0.380,0.220,0.428,0.454,0.800,0.090,0.667,0.609,0.818,0.162],
        "Var12": [0.853,0.095,0.091,0.560,0.851,0.853,0.244,0.748,0.106,0.687,0.373,0.233,0.145,0.993,0.250,0.557,0.851,0.937,0.895,0.141,0.155,0.665,0.534,0.753,0.007,0.849,0.267,0.894],
        "Var13": [0.224,0.423,0.221,0.209,0.101,0.667,0.293,0.077,0.459,0.893,0.123,0.933,0.156,0.878,0.342,0.489,0.941,0.812,0.691,0.948,0.944,0.009,0.133,0.522,0.025,0.817,0.656,0.044],
        "Var14": [0.646,0.180,0.055,0.205,0.955,0.077,0.630,0.062,0.268,0.644,0.407,0.698,0.210,0.103,0.146,0.617,0.350,0.780,0.191,0.280,0.288,0.359,0.914,0.410,0.804,0.268,0.331,0.105],
        "Var15": [0.858,0.492,0.287,0.570,0.934,0.415,0.441,0.274,0.482,0.304,0.186,0.646,0.965,0.849,0.539,0.992,0.342,0.799,0.998,0.191,0.642,0.072,0.319,0.858,0.661,0.910,0.196,0.083],
        "Var16": [0.712,0.567,0.863,0.574,0.773,0.741,0.683,0.997,0.371,0.462,0.937,0.594,0.008,0.445,0.116,0.686,0.963,0.949,0.219,0.514,0.867,0.063,0.717,0.982,0.534,0.941,0.125,0.230],
        "Var17": [0.146,0.929,0.318,0.685,0.029,0.697,0.082,0.148,0.973,0.497,0.652,0.732,0.207,0.368,0.394,0.989,0.938,0.678,0.134,0.329,0.596,0.706,0.070,0.966,0.760,0.031,0.648,0.930],
        "Var18": [0.052,0.404,0.253,0.369,0.187,0.424,0.083,0.257,0.729,0.773,0.115,0.854,0.064,0.990,0.627,0.731,0.542,0.760,0.367,0.947,0.757,0.492,0.074,0.010,0.424,0.496,0.737,0.583],
        "Score": [0.381,-.081,-.154,0.222,0.121,0.084,0.329,-.052,0.062,0.302,0.011,-.093,0.125,0.152,0.116,0.206,0.092,-.057,0.538,-.083,-.067,0.144,-.097,-.083,-.005,0.268,0.161,-.131],
    }
    df = pd.DataFrame(demo_data)
    st.success(f"✅ 더미 데이터 로드 완료 — 고객 {len(df)}명")

elif uploaded:
    try:
        if uploaded.name.endswith('.csv'):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        # 컬럼명 정리
        df.columns = [c.strip() for c in df.columns]
        st.success(f"✅ 업로드 완료 — 고객 {len(df)}명 / 컬럼 {len(df.columns)}개")
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")

# ══ STEP 2: 분석 ══
if df is not None:
    # 고객번호 컬럼 자동 감지
    id_col = "고객번호" if "고객번호" in df.columns else df.columns[0]
    score_col = "Score" if "Score" in df.columns else None

    # 사용 가능한 변수 필터
    available_vars = [v for v in VAR_COLS if v in df.columns]

    st.markdown('<div class="sec-label">STEP 02</div><div class="sec-title">🤖 Agent 분석 실행</div>', unsafe_allow_html=True)
    
    threshold = st.slider("이탈 위험 임계값 (Score 기준)", 0.0, 0.5, 0.1, 0.05,
                          help="Score가 임계값 이상인 고객을 고위험으로 분류합니다")
    run = st.button("▶ 이탈 원인 분석 시작")
    st.divider()

    if run or "done" in st.session_state:
        st.session_state["done"] = True
        st.session_state["threshold"] = threshold

        thr = st.session_state.get("threshold", 0.1)

        with st.spinner("온톨로지 기반 XAI 변수 기여도 분석 중..."):
            # 각 변수 평균 계산 (기여도 기준점)
            avg_dict = {v: df[v].mean() for v in available_vars}

            results = []
            for _, row in df.iterrows():
                r = row.to_dict()
                sc = float(r.get("Score", 0))
                cb = compute_churn_contribution(r, avg_dict)
                dom_type, type_scores = get_dominant_type(cb)
                new_pat = is_new_pattern(type_scores)

                strat = TYPE_STRATEGY[dom_type]
                top3_vars = sorted(cb.items(), key=lambda x: x[1], reverse=True)[:3]

                results.append({
                    "고객ID": r[id_col],
                    "Score": sc,
                    "주요유형": dom_type,
                    "type_scores": type_scores,
                    "is_new": new_pat,
                    "기여도": cb,
                    "top3": top3_vars,
                    "전략": strat["strategy"],
                    "전략상세": strat["detail"],
                    "주요원인": f"{ONTOLOGY[top3_vars[0][0]]['name']} ({top3_vars[0][1]}%)"
                })

        res = pd.DataFrame(results)
        high = res[res["Score"] >= thr].sort_values("Score", ascending=False)
        new_pats = res[(res["Score"] >= thr) & (res["is_new"] == True)]

        # ── STEP 3 ──
        st.markdown('<div class="sec-label">STEP 03</div><div class="sec-title">📊 분석 결과 — 이탈 원인 진단</div>', unsafe_allow_html=True)

        type_dist = high["주요유형"].value_counts().to_dict() if len(high) > 0 else {}
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-box"><div class="kpi-n">{len(df)}<span style="font-size:15px">명</span></div><div class="kpi-l">전체 분석 고객</div></div>
            <div class="kpi-box"><div class="kpi-n red">{len(high)}<span style="font-size:15px">명</span></div><div class="kpi-l">고위험 고객<br>(Score ≥ {thr})</div></div>
            <div class="kpi-box"><div class="kpi-n">{len(type_dist)}<span style="font-size:15px">종</span></div><div class="kpi-l">감지된 이탈 유형</div></div>
            <div class="kpi-box"><div class="kpi-n amber">{len(new_pats)}<span style="font-size:15px">명</span></div><div class="kpi-l">신규 복합 패턴</div></div>
        </div>
        """, unsafe_allow_html=True)

        # 유형별 분포
        if type_dist:
            st.markdown("**이탈 유형별 분포**")
            cols_t = st.columns(len(type_dist))
            for i, (tp, cnt) in enumerate(sorted(type_dist.items(), key=lambda x: x[1], reverse=True)):
                icon = TYPE_ICONS.get(tp, "")
                strat = TYPE_STRATEGY[tp]["strategy"]
                with cols_t[i]:
                    st.markdown(f"""
                    <div style="background:#fff;border:1.5px solid #D0DCFF;border-radius:10px;padding:12px;text-align:center;">
                        <div style="font-size:20px">{icon}</div>
                        <div style="font-size:12px;font-weight:700;color:#0B1F4E;margin:4px 0">{tp}</div>
                        <div style="font-size:20px;font-weight:900;color:#0046AD">{cnt}명</div>
                        <div style="font-size:10px;color:#888;margin-top:4px">{strat}</div>
                    </div>
                    """, unsafe_allow_html=True)

        if len(new_pats) > 0:
            ids = list(new_pats["고객ID"])[:5]
            st.markdown(f"""
            <div class="alert"><div class="at">⚠️ 신규 복합 이탈 패턴 Alert</div>
            단일 유형으로 분류되지 않는 복합 이탈 패턴 고객 <b>{len(new_pats)}명</b> 감지.<br>
            온톨로지 신규 유형 추가를 검토해 주세요.
            <br><span style="font-size:11px;color:#aaa">대상: {', '.join(str(i) for i in ids)} 등</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>**🔴 고위험 이탈 고객 상세 분석**", unsafe_allow_html=True)

        for _, r in high.head(10).iterrows():
            sc_val = r["Score"]
            sc_cls = "rc" if sc_val >= 0.3 else "rc mid"
            sc_col = "#E53935" if sc_val >= 0.3 else "#FB8C00"
            tp = r["주요유형"]
            type_cls = f"type-{tp}"
            icon = TYPE_ICONS.get(tp, "")

            # 기여도 바
            bars = "".join([
                f'<div class="bw"><div class="bl">'
                f'<span>{ONTOLOGY[v]["name"]}<span style="font-size:10px;color:#999;margin-left:4px">({ONTOLOGY[v]["type"]})</span></span>'
                f'<span style="font-weight:700;color:#0046AD">{p}%</span></div>'
                f'<div class="bb"><div class="bf" style="width:{p}%"></div></div></div>'
                for v, p in r["top3"]
            ])

            # 유형별 점수 미니 차트
            type_bars = "".join([
                f'<span style="font-size:11px;color:#555;margin-right:12px">'
                f'{TYPE_ICONS.get(t,"")} {t} <b style="color:#0046AD">{round(s,1)}%</b></span>'
                for t, s in sorted(r["type_scores"].items(), key=lambda x: x[1], reverse=True)[:3]
            ])

            new_badge = '<span style="background:#FFF3E0;color:#E65100;border:1px solid #FFE0B2;padding:1px 8px;border-radius:10px;font-size:10px;font-weight:700;margin-left:6px">신규패턴</span>' if r["is_new"] else ""

            st.markdown(f"""
            <div class="{sc_cls}">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:6px;">
                <div style="display:flex;align-items:center;gap:8px;">
                  <span style="font-size:15px;font-weight:900;color:#0B1F4E">{r['고객ID']}</span>
                  <span class="{type_cls}">{icon} {tp}</span>
                  {new_badge}
                </div>
                <div><span style="font-size:11px;color:#aaa">이탈 Score</span>
                  <span style="font-size:24px;font-weight:900;color:{sc_col};margin-left:6px">{round(sc_val,3)}</span>
                </div>
              </div>
              <div style="font-size:11px;color:#888;margin-bottom:8px">{type_bars}</div>
              <div style="font-size:11.5px;color:#666;background:#F8FAFF;border-radius:7px;padding:7px 11px;margin-bottom:10px;">
                📌 주요 이탈 원인: <b style="color:#0046AD">{r['주요원인']}</b>
              </div>
              {bars}
              <div style="margin-top:12px;padding-top:10px;border-top:1px solid #EEF3FF;display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                <span style="font-size:11px;color:#aaa;font-weight:600">추천 리텐션</span>
                <span class="ob">{r['전략']}</span>
                <span style="font-size:11px;color:#777">{r['전략상세']}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ── STEP 4: Human-in-the-Loop ──
        st.markdown('<div class="sec-label">STEP 04 · Human-in-the-Loop</div><div class="sec-title">✅ 현업 검토 및 캠페인 승인</div>', unsafe_allow_html=True)
        st.caption("Agent가 분석한 리텐션 전략을 검토하고 실행을 승인해 주세요.")
        ca, cb_, cc = st.columns(3)
        with ca: approve = st.button("✅ 전체 승인 후 캠페인 실행", use_container_width=True)
        with cb_: st.button("✏️ 일부 수정 후 실행", use_container_width=True)
        with cc:  st.button("⏸ 보류", use_container_width=True)
        st.divider()

        # ── STEP 5: 실행 ──
        if approve or "camp" in st.session_state:
            st.session_state["camp"] = True
            st.markdown('<div class="sec-label">STEP 05</div><div class="sec-title">🚀 리텐션 캠페인 실행 완료</div>', unsafe_allow_html=True)
            st.success(f"✅ {len(high)}명 대상 초개인화 리텐션 캠페인이 실행되었습니다.")

            type_counts = high["주요유형"].value_counts().to_dict()
            boxes = "".join([
                f'<div class="si"><div class="sn">{cnt}</div><div class="sl">{TYPE_ICONS.get(tp,"")} {tp}</div></div>'
                for tp, cnt in type_counts.items()
            ])

            st.markdown(f"""
            <div class="rsbox">
              <div style="font-size:11.5px;color:rgba(255,255,255,0.45);margin-bottom:4px">
                {datetime.now().strftime('%Y-%m-%d %H:%M')} · 캠페인 실행 현황
              </div>
              <div class="sg">
                <div class="si"><div class="sn">{len(high)}</div><div class="sl">총 발송 대상</div></div>
                {boxes}
              </div>
              <div style="margin-top:18px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.1);font-size:11.5px;color:rgba(255,255,255,0.4)">
                Push / LMS / 카카오톡 채널 자동 선택 완료 · 성과 데이터는 24시간 후 자동 수집됩니다
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.divider()

            # ── STEP 6: 성과 리포트 ──
            st.markdown('<div class="sec-label">STEP 06 · 성과 리포트</div><div class="sec-title">📈 캠페인 성과 리포트 (시뮬레이션)</div>', unsafe_allow_html=True)
            sim = round(random.uniform(28, 44), 1)
            sim_s = int(len(high) * sim / 100)
            m1, m2, m3 = st.columns(3)
            m1.metric("예상 리텐션 전환율", f"{sim}%", f"+{round(sim-18,1)}%p vs 기존 일괄 오퍼")
            m2.metric("이탈 방어 예상 고객", f"{sim_s}명")
            m3.metric("오퍼 비용 효율", "↑ 개선", "유형별 맞춤 오퍼 적용")
            st.markdown("""
            <div class="qb">
              "이제 마케터의 역할은 데이터를 찾는 것이 아니라,<br>
              Agent가 발견한 인사이트를 바탕으로 더 나은 마케팅 방식을 고민하는 것으로 전환됩니다."
            </div>
            """, unsafe_allow_html=True)

# ── 푸터 ──
st.markdown("""
<div style="text-align:center;padding:32px 0 8px;color:#BBC8DD;font-size:11px;letter-spacing:0.04em;">
    고객 이탈 원인 분석 및 초개인화 리텐션 Agent (XAI 기반)
</div>
""", unsafe_allow_html=True)
