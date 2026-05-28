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

/* 중앙 정렬 최대 너비 */
.block-container {
    max-width: 1080px !important;
    padding: 1.5rem 2rem !important;
    margin: 0 auto !important;
}

/* 헤더 */
.main-header {
    background: linear-gradient(135deg, #071430 0%, #0B1F4E 55%, #1A3A8F 100%);
    padding: 32px 40px 26px;
    border-radius: 16px;
    margin-bottom: 24px;
    border-top: 5px solid #1565E8;
    box-shadow: 0 6px 24px rgba(7,20,48,0.2);
}
.main-title {
    font-size: 21px; font-weight: 900; color: #fff;
    margin: 0 0 5px; letter-spacing: -0.3px; line-height: 1.3;
}
.main-sub { font-size: 12px; color: rgba(255,255,255,0.5); margin: 0 0 14px; }
.badge {
    display: inline-block;
    background: rgba(0,70,173,0.4); border: 1px solid rgba(0,100,210,0.35);
    color: #90C4FF; font-size: 10.5px; font-weight: 700;
    padding: 3px 11px; border-radius: 20px; margin: 0 5px 5px 0;
}

/* 섹션 헤더 */
.sec-label {
    font-size: 10px; font-weight: 800; color: #0046AD;
    letter-spacing: 0.14em; text-transform: uppercase;
    margin-bottom: 2px;
}
.sec-title {
    font-size: 15px; font-weight: 700; color: #0B1F4E;
    margin-bottom: 14px;
}

/* KPI 그리드 */
.kpi-row { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.kpi-box {
    flex: 1; min-width: 120px;
    background: linear-gradient(135deg, #F4F7FF, #EEF3FF);
    border: 1.5px solid #D0DCFF; border-radius: 12px;
    padding: 16px 14px; text-align: center;
}
.kpi-n { font-size: 26px; font-weight: 900; color: #0046AD; line-height: 1; margin-bottom: 4px; }
.kpi-n.red { color: #E53935; }
.kpi-n.amber { color: #F57C00; }
.kpi-l { font-size: 11px; color: #6680AA; line-height: 1.4; }

/* 결과 카드 */
.rc {
    background: #fff; border-radius: 12px;
    padding: 16px 18px; margin-bottom: 10px;
    border: 1.5px solid #D8E4FF;
    border-left: 5px solid #E53935;
}
.rc.mid { border-left-color: #FB8C00; }

/* 기여도 바 */
.bw { margin: 6px 0; }
.bl { display:flex; justify-content:space-between; font-size:11.5px; color:#555; margin-bottom:2px; }
.bb { background:#EEF3FF; border-radius:5px; height:7px; width:100%; overflow:hidden; }
.bf { background:linear-gradient(90deg,#0046AD,#1565E8); border-radius:5px; height:7px; }

/* 유형 뱃지 */
.t1 { background:#FFEBEE; color:#C62828; border:1px solid #FFCDD2; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.t2 { background:#E3F2FD; color:#1565C0; border:1px solid #BBDEFB; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.t3 { background:#E8F5E9; color:#2E7D32; border:1px solid #C8E6C9; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }
.tn { background:#FFF3E0; color:#E65100; border:1px solid #FFE0B2; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:700; }

/* 오퍼 뱃지 */
.ob { display:inline-block; background:#EEF3FF; border:1.5px solid #C8D8FF; color:#0046AD; font-size:11.5px; font-weight:700; padding:3px 12px; border-radius:20px; margin-right:6px; }

/* Alert */
.alert {
    background:#FFF8E1; border:1.5px solid #FFB74D;
    border-left:5px solid #FF8F00; border-radius:10px;
    padding:14px 18px; margin:14px 0;
}
.at { font-size:13px; font-weight:700; color:#E65100; margin-bottom:4px; }

/* 성과 박스 */
.rsbox {
    background: linear-gradient(135deg, #071430, #0B1F4E, #0046AD);
    border-radius: 14px; padding: 24px 28px; margin-top: 16px;
    box-shadow: 0 6px 20px rgba(0,30,100,0.2);
}
.sg { display:flex; gap:20px; flex-wrap:wrap; margin-top:14px; }
.si { flex:1; min-width:100px; }
.sn { font-size:28px; font-weight:900; color:#7AADFF; line-height:1; margin-bottom:3px; }
.sl { font-size:11px; color:rgba(255,255,255,0.5); }

/* 인용 */
.qb {
    background:#F4F7FF; border-left:4px solid #0046AD;
    border-radius:0 10px 10px 0; padding:14px 20px; margin-top:14px;
    font-size:12.5px; color:#0B1F4E; font-style:italic; line-height:1.8;
}

/* 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #0046AD, #1565E8) !important;
    color: #fff !important; border: none !important;
    border-radius: 9px !important; font-weight: 700 !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    padding: 10px 22px !important; font-size: 13.5px !important;
    box-shadow: 0 2px 8px rgba(0,70,173,0.2) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #003A8C, #0046AD) !important;
    box-shadow: 0 5px 14px rgba(0,70,173,0.3) !important;
    transform: translateY(-1px) !important;
}

/* 구분선 */
hr { border: none; border-top: 1px solid #E0E8F5; margin: 18px 0; }

/* metric 카드 */
[data-testid="metric-container"] {
    background: #F4F7FF !important;
    border: 1.5px solid #D0DCFF !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
}

/* 파일 업로더 배경 수정 */
[data-testid="stFileUploader"] {
    background: #fff !important;
    border: 2px dashed #C8D8FF !important;
    border-radius: 12px !important;
    padding: 12px !important;
}
section[data-testid="stFileUploadDropzone"] {
    background: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# ── 온톨로지 ──
ONTOLOGY = {
    "CL_1": {"name":"고객불만 발생형","cond":lambda r:r["민원발생횟수"]>=2,
              "offer":"카페 할인쿠폰 제공","detail":"제휴 카페 20% 할인 쿠폰 즉시 발송","cls":"t1","icon":"🔴"},
    "CL_2": {"name":"이용감소형","cond":lambda r:r["이용빈도변화율"]<=-30 and r["민원발생횟수"]<2,
              "offer":"외식업종 30% 할인","detail":"외식업종 결제 시 30% 즉시 할인 (월 3회)","cls":"t2","icon":"🟠"},
    "CL_3": {"name":"이용비중 감소형","cond":lambda r:r["이용금액변화율"]<=-40 and r["이용빈도변화율"]>-30,
              "offer":"캐시백 오퍼","detail":"전월 대비 30만원 추가 이용 시 5만원 캐시백","cls":"t3","icon":"🟡"},
}
VARS = ["이용빈도변화율","이용금액변화율","민원발생횟수","해지문의여부","포인트소멸예정금액"]
VKR  = {"이용빈도변화율":"이용빈도 감소","이용금액변화율":"이용금액 감소",
        "민원발생횟수":"고객불만 발생","해지문의여부":"해지 문의 이력","포인트소멸예정금액":"포인트 소멸 예정"}

def score(r):
    s=0.3
    if r["이용빈도변화율"]<=-30: s+=0.25
    elif r["이용빈도변화율"]<=-15: s+=0.12
    if r["이용금액변화율"]<=-40: s+=0.22
    elif r["이용금액변화율"]<=-20: s+=0.10
    if r["민원발생횟수"]>=3: s+=0.18
    elif r["민원발생횟수"]>=1: s+=0.08
    if r["해지문의여부"]==1: s+=0.15
    if r["포인트소멸예정금액"]>=50000: s+=0.05
    return min(round(s,2),0.99)

def contribs(r,base):
    c={}
    for v in VARS:
        t=r.copy(); t[v]=0
        c[v]=max(round(base-score(t),3),0)
    tot=sum(c.values()) or 1
    return {k:round(v/tot*100,1) for k,v in c.items()}

def ctype(r):
    for cl,info in ONTOLOGY.items():
        if info["cond"](r): return cl
    return "NEW"

def new_pts(df):
    out=[]
    for _,row in df.iterrows():
        r=row.to_dict()
        if score(r)>=0.7 and ctype(r)=="NEW": out.append(r["고객ID"])
    return out

# ══ 헤더 ══
st.markdown("""
<div class="main-header">
    <div class="main-title">🎯 고객 이탈 원인 분석 및 초개인화 리텐션 Agent</div>
    <div class="main-sub">XAI 기반 이탈 원인 진단 → 처방 → 자동 실행</div>
    <span class="badge">XAI 기반</span>
    <span class="badge">온톨로지 분류</span>
    <span class="badge">Human-in-the-Loop</span>
    <span class="badge">초개인화 리텐션</span>
</div>
""", unsafe_allow_html=True)

# ══ STEP 1 ══
st.markdown('<div class="sec-label">STEP 01</div><div class="sec-title">📂 고객 데이터 업로드</div>', unsafe_allow_html=True)
col_u, col_d = st.columns([3,1])
with col_u:
    uploaded = st.file_uploader("CSV 업로드", type=["csv"], label_visibility="collapsed")
    st.caption("CSV 컬럼: 고객ID · 이용빈도변화율 · 이용금액변화율 · 민원발생횟수 · 해지문의여부 · 포인트소멸예정금액")
with col_d:
    use_demo = st.button("🔍 더미 데이터로\n시연하기", use_container_width=True)

st.divider()

df = None
if use_demo or "demo" in st.session_state:
    st.session_state["demo"] = True
    np.random.seed(42); n=30
    df = pd.DataFrame({
        "고객ID":[f"C{str(i).zfill(4)}" for i in range(1,n+1)],
        "이용빈도변화율":np.random.choice([-55,-40,-30,-20,-10,0,5,10],n),
        "이용금액변화율":np.random.choice([-60,-45,-35,-20,-10,0,5],n),
        "민원발생횟수":np.random.choice([0,0,0,1,2,3],n),
        "해지문의여부":np.random.choice([0,0,0,1],n),
        "포인트소멸예정금액":np.random.choice([0,0,10000,30000,70000],n),
    })
    st.success(f"✅ 더미 데이터 로드 완료 — 고객 {n}명")
elif uploaded:
    df=pd.read_csv(uploaded)
    st.success(f"✅ 업로드 완료 — 고객 {len(df)}명")

# ══ STEP 2 ══
if df is not None:
    st.markdown('<div class="sec-label">STEP 02</div><div class="sec-title">🤖 Agent 분석 실행</div>', unsafe_allow_html=True)
    run = st.button("▶ 이탈 원인 분석 시작")
    st.divider()

    if run or "done" in st.session_state:
        st.session_state["done"] = True

        with st.spinner("XAI 변수 기여도 분석 및 온톨로지 유형 분류 중..."):
            rows=[]
            for _,row in df.iterrows():
                r=row.to_dict(); sc=score(r); cb=contribs(r,sc); cl=ctype(r)
                if cl!="NEW":
                    inf=ONTOLOGY[cl]
                    rows.append({"고객ID":r["고객ID"],"점수":sc,"유형":cl,"유형명":inf["name"],
                        "cls":inf["cls"],"icon":inf["icon"],"기여도":cb,
                        "오퍼":inf["offer"],"상세":inf["detail"],
                        "원인":f"{VKR.get(max(cb,key=cb.get))} ({max(cb.values())}%)"})
                else:
                    rows.append({"고객ID":r["고객ID"],"점수":sc,"유형":"NEW","유형명":"신규 패턴",
                        "cls":"tn","icon":"⚪","기여도":cb,
                        "오퍼":"신규 패턴 — 검토 필요","상세":"기존 유형에 해당하지 않는 패턴",
                        "원인":f"{VKR.get(max(cb,key=cb.get))} ({max(cb.values())}%)"})

        res=pd.DataFrame(rows)
        high=res[res["점수"]>=0.7].sort_values("점수",ascending=False)
        np_=new_pts(df)

        # ── STEP 3 ──
        st.markdown('<div class="sec-label">STEP 03</div><div class="sec-title">📊 분석 결과 — 이탈 원인 진단</div>', unsafe_allow_html=True)
        n_cl=res[res["유형"]!="NEW"]["유형"].nunique()
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-box"><div class="kpi-n">{len(df)}<span style="font-size:15px">명</span></div><div class="kpi-l">전체 분석 고객</div></div>
            <div class="kpi-box"><div class="kpi-n red">{len(high)}<span style="font-size:15px">명</span></div><div class="kpi-l">고위험 고객<br>(점수 0.7↑)</div></div>
            <div class="kpi-box"><div class="kpi-n">{n_cl}<span style="font-size:15px">종</span></div><div class="kpi-l">이탈 유형 분류</div></div>
            <div class="kpi-box"><div class="kpi-n amber">{len(np_)}<span style="font-size:15px">명</span></div><div class="kpi-l">신규 패턴 감지</div></div>
        </div>
        """, unsafe_allow_html=True)

        if len(np_)>=3:
            st.markdown(f"""
            <div class="alert"><div class="at">⚠️ 신규 이탈 패턴 감지 Alert</div>
            기존 CL_1/2/3에 해당하지 않는 고위험 고객 <b>{len(np_)}명</b>이 감지되었습니다.
            새로운 이탈 유형 추가를 검토해 주세요.<br>
            <span style="font-size:11.5px;color:#aaa">대상: {', '.join(np_[:5])} 외 {max(0,len(np_)-5)}명</span></div>
            """, unsafe_allow_html=True)

        st.markdown("**🔴 고위험 이탈 고객 상세 분석**")
        for _,r in high.head(9).iterrows():
            cls_="rc" if r["점수"]>=0.8 else "rc mid"
            top3=sorted(r["기여도"].items(),key=lambda x:x[1],reverse=True)[:3]
            bars="".join([
                f'<div class="bw"><div class="bl"><span>{VKR.get(v,v)}</span>'
                f'<span style="font-weight:700;color:#0046AD">{p}%</span></div>'
                f'<div class="bb"><div class="bf" style="width:{p}%"></div></div></div>'
                for v,p in top3])
            sc_col="#E53935" if r["점수"]>=0.8 else "#FB8C00"
            st.markdown(f"""
            <div class="{cls_}">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;flex-wrap:wrap;gap:6px;">
                <div style="display:flex;align-items:center;gap:8px;">
                  <span style="font-size:15px;font-weight:900;color:#0B1F4E">{r['고객ID']}</span>
                  <span class="{r['cls']}">{r['icon']} {r['유형명']}</span>
                </div>
                <div><span style="font-size:11px;color:#aaa">이탈 점수</span>
                  <span style="font-size:24px;font-weight:900;color:{sc_col};margin-left:6px">{r['점수']}</span>
                </div>
              </div>
              <div style="font-size:11.5px;color:#666;background:#F8FAFF;border-radius:7px;padding:7px 11px;margin-bottom:10px;">
                📌 주요 원인: <b style="color:#0046AD">{r['원인']}</b>
              </div>
              {bars}
              <div style="margin-top:12px;padding-top:10px;border-top:1px solid #EEF3FF;display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                <span style="font-size:11px;color:#aaa;font-weight:600">추천 오퍼</span>
                <span class="ob">{r['오퍼']}</span>
                <span style="font-size:11px;color:#777">{r['상세']}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ── STEP 4 ──
        st.markdown('<div class="sec-label">STEP 04 · Human-in-the-Loop</div><div class="sec-title">✅ 현업 검토 및 캠페인 승인</div>', unsafe_allow_html=True)
        st.caption("Agent가 제안한 리텐션 오퍼를 검토하고 실행을 승인해 주세요.")
        ca,cb_,cc=st.columns(3)
        with ca: approve=st.button("✅ 전체 승인 후 캠페인 실행",use_container_width=True)
        with cb_: st.button("✏️ 일부 수정 후 실행",use_container_width=True)
        with cc:  st.button("⏸ 보류",use_container_width=True)
        st.divider()

        # ── STEP 5 ──
        if approve or "camp" in st.session_state:
            st.session_state["camp"]=True
            st.markdown('<div class="sec-label">STEP 05</div><div class="sec-title">🚀 리텐션 캠페인 실행 완료</div>', unsafe_allow_html=True)
            st.success(f"✅ {len(high)}명 대상 초개인화 리텐션 캠페인이 실행되었습니다.")

            c1=len(high[high["유형"]=="CL_1"])
            c2=len(high[high["유형"]=="CL_2"])
            c3=len(high[high["유형"]=="CL_3"])

            st.markdown(f"""
            <div class="rsbox">
              <div style="font-size:11.5px;color:rgba(255,255,255,0.45);margin-bottom:4px">
                {datetime.now().strftime('%Y-%m-%d %H:%M')} · 캠페인 실행 현황
              </div>
              <div class="sg">
                <div class="si"><div class="sn">{len(high)}</div><div class="sl">총 발송 대상</div></div>
                <div class="si"><div class="sn">{c1}</div><div class="sl">CL_1 카페쿠폰</div></div>
                <div class="si"><div class="sn">{c2}</div><div class="sl">CL_2 외식할인</div></div>
                <div class="si"><div class="sn">{c3}</div><div class="sl">CL_3 캐시백</div></div>
              </div>
              <div style="margin-top:18px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.1);
                          font-size:11.5px;color:rgba(255,255,255,0.4)">
                Push / LMS / 카카오톡 채널 자동 선택 완료 · 성과 데이터는 24시간 후 자동 수집됩니다
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.divider()

            # ── STEP 6 ──
            st.markdown('<div class="sec-label">STEP 06 · 성과 리포트</div><div class="sec-title">📈 캠페인 성과 리포트 (시뮬레이션)</div>', unsafe_allow_html=True)
            sim=round(random.uniform(28,42),1)
            sim_s=int(len(high)*sim/100)
            m1,m2,m3=st.columns(3)
            m1.metric("예상 리텐션 전환율",f"{sim}%",f"+{round(sim-18,1)}%p vs 기존 일괄 오퍼")
            m2.metric("이탈 방어 예상 고객",f"{sim_s}명")
            m3.metric("오퍼 비용 효율","↑ 개선","원인별 맞춤 오퍼 적용")

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
