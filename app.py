"""
app.py — 메인 (현업) 페이지
고객 데이터를 업로드해 이탈 원인을 진단하고 맞춤 리텐션 캠페인을 실행합니다.
Agent 관리 정보(버전·학습이력·재학습)는 사이드바의 [관리자] 페이지에서 확인할 수 있습니다.
"""

import random
from datetime import datetime

import streamlit as st
import pandas as pd

from agent_lib import (
    APP_CSS,
    ONTOLOGY, TYPE_STRATEGY, ALL_STRATEGIES, TYPE_ICONS, TYPE_PILL, VAR_COLS,
    generate_synthetic_customers, get_agent,
)


# ═══════════════════════════════════════════════════════════════
# 페이지 설정 · CSS
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="고객 이탈 원인 분석 리텐션 Agent",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(APP_CSS, unsafe_allow_html=True)

agent = get_agent()


# ═══════════════════════════════════════════════════════════════
# 고객 카드 렌더링
# ═══════════════════════════════════════════════════════════════
def render_customer_card(r, edit_mode=False, idx=0):
    sc_val   = float(r["Score"])
    card_cls = "cust-card high" if sc_val >= 0.20 else "cust-card mid"
    chip_cls = "score-chip sc-r" if sc_val >= 0.20 else "score-chip sc-a"
    tp       = str(r["주요유형"])
    pc       = TYPE_PILL.get(tp, "p-신규") if not r["is_new"] else "p-신규"
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
    for t, s in sorted(r["type_scores"].items(), key=lambda x: x[1], reverse=True)[:3]:
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
        col_s, col_exc = st.columns([3, 1])
        key_s   = f"edit_strat_{idx}"
        key_exc = f"edit_exc_{idx}"
        cur_str = r["전략"]
        options = list(ALL_STRATEGIES.keys())
        with col_s:
            sel = st.selectbox(
                f"오퍼 변경 — {r['고객ID']}", options,
                index=options.index(cur_str) if cur_str in options else 0,
                key=key_s, label_visibility="collapsed"
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


# ═══════════════════════════════════════════════════════════════
# 헤더
# ═══════════════════════════════════════════════════════════════
st.markdown(
    '<div class="page-header">'
    '<h1 class="page-title">고객 이탈 원인 분석 및 초개인화 리텐션 Agent</h1>'
    '<p class="page-desc">이탈 위험 고객을 진단하고 원인에 맞는 맞춤 리텐션 캠페인을 자동 실행합니다.</p>'
    '</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# STEP 01 · 데이터 업로드
# ═══════════════════════════════════════════════════════════════
st.markdown(
    '<div class="section-block">'
    '<div class="section-num">STEP 01</div>'
    '<div class="section-title">고객 데이터 업로드</div>'
    '<div class="section-desc">분석할 고객 데이터를 업로드하거나, 더미 데이터로 바로 시연할 수 있습니다.</div>'
    '</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("CSV 또는 Excel · 컬럼: 고객번호, Var1~Var18, (선택) Score", type=["csv", "xlsx"])
use_demo = st.button("내장 더미 데이터로 시연하기")

df = None
if use_demo or "demo" in st.session_state:
    st.session_state["demo"] = True
    df = generate_synthetic_customers(n=80, seed=2025, start_idx=1)
    st.success(f"내장 더미 데이터 {len(df)}명 로드 완료")
elif uploaded:
    try:
        df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
        df.columns = [c.strip() for c in df.columns]
        st.success(f"업로드 완료 · 총 {len(df)}명")
    except Exception as e:
        st.error(f"파일 읽기 오류 · {e}")

if df is not None:
    id_col = "고객번호" if "고객번호" in df.columns else df.columns[0]
    av = [v for v in VAR_COLS if v in df.columns]

    if "Score" not in df.columns and len(av) == 18:
        df["Score"] = agent.predict(df[VAR_COLS].values).round(6)
        st.info("Score 컬럼이 없어 Agent 모델이 자동으로 예측했습니다.")

    with st.expander("데이터 미리보기 및 통계 확인"):
        t1, t2, t3 = st.tabs(["미리보기", "변수 통계", "Score 분포"])
        with t1:
            show = [id_col] + av[:9] + (["Score"] if "Score" in df.columns else [])
            st.dataframe(df[show].head(20), use_container_width=True, height=260)
        with t2:
            stat = df[av].describe().T.round(4)
            stat["변수명"] = [ONTOLOGY[v]["name"] for v in stat.index]
            stat["유형"]   = [ONTOLOGY[v]["type"] for v in stat.index]
            st.dataframe(
                stat[["변수명", "유형", "mean", "std", "min", "max"]].rename(
                    columns={"mean": "평균", "std": "표준편차", "min": "최솟값", "max": "최댓값"}),
                use_container_width=True, height=360)
        with t3:
            if "Score" in df.columns:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("평균", f"{df['Score'].mean():.4f}")
                c2.metric("최고", f"{df['Score'].max():.4f}")
                c3.metric("최저", f"{df['Score'].min():.4f}")
                c4.metric("표준편차", f"{df['Score'].std():.4f}")
                st.bar_chart(df.set_index(id_col)["Score"].sort_values(ascending=False))

    # ═══════════════════════════════════════════════════════════════
    # STEP 02
    # ═══════════════════════════════════════════════════════════════
    st.markdown(
        '<div class="section-block">'
        '<div class="section-num">STEP 02</div>'
        '<div class="section-title">분석 설정 및 실행</div>'
        '<div class="section-desc">이탈 위험 임계값과 신규 패턴 Alert 기준을 설정합니다.</div>'
        '</div>', unsafe_allow_html=True)

    col_sl, col_btn = st.columns([4, 1])
    with col_sl:
        threshold = st.slider(
            "이탈 위험 임계값 — Score가 이 값 이상이면 고위험으로 분류",
            min_value=0.0, max_value=1.0, value=0.10, step=0.01, format="%.2f")
        alert_min = st.slider(
            "신규 변수 조합 Alert 기준 — 동일 조합이 N건 이상 누적되면 Alert 발송",
            min_value=1, max_value=20, value=3, step=1)
    with col_btn:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        run = st.button("분석 실행", use_container_width=True, type="primary")

    if run or "done" in st.session_state:
        st.session_state["done"] = True
        st.session_state["thr"] = threshold
        st.session_state["alert_min"] = alert_min
        thr = st.session_state.get("thr", 0.1)
        alert_min = st.session_state.get("alert_min", 3)

        with st.spinner("Agent가 변수 기여도 분석 및 온톨로지 유형 분류 중..."):
            rows = []
            for _, row in df.iterrows():
                r = row.to_dict()
                contribs = agent.explain(r)
                dom, ts, is_new = agent.classify(contribs)
                strat, detail = agent.recommend(dom)
                top3 = sorted(contribs.items(), key=lambda x: x[1], reverse=True)[:3]
                rows.append({
                    "고객ID": r[id_col], "Score": float(r.get("Score", 0)),
                    "주요유형": dom, "type_scores": ts, "is_new": is_new,
                    "기여도": contribs, "top3": top3,
                    "전략": strat, "전략상세": detail,
                    "주요원인": ONTOLOGY[top3[0][0]]["name"],
                    "주요원인_pct": top3[0][1],
                })

        res = pd.DataFrame(rows)
        high = res[res["Score"] >= thr].sort_values("Score", ascending=False)
        newp = res[(res["Score"] >= thr) & res["is_new"]]
        st.session_state["high_rows"] = high.to_dict("records")

        # ── STEP 03 ──
        st.markdown(
            '<div class="section-block">'
            '<div class="section-num">STEP 03</div>'
            '<div class="section-title">분석 결과 — 이탈 원인 진단</div>'
            '<div class="section-desc">변수 기여도와 온톨로지 매핑을 통해 고객별 이탈 원인을 진단합니다.</div>'
            '</div>', unsafe_allow_html=True)

        n_types = int(high["주요유형"].nunique()) if len(high) > 0 else 0
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

        if len(high) > 0:
            td = high["주요유형"].value_counts().to_dict()
            html = '<div class="type-grid">'
            for tp, cnt in sorted(td.items(), key=lambda x: x[1], reverse=True):
                s, _ = TYPE_STRATEGY[tp]
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
            st.markdown(html + '</div>', unsafe_allow_html=True)

        if len(newp) > 0:
            ids_str = ", ".join(str(x) for x in list(newp["고객ID"])[:5])
            st.markdown(
                f'<div class="alert-warn">'
                f'<div class="alert-warn-title">신규 복합 이탈 패턴 감지</div>'
                f'<div class="alert-warn-body">단일 유형으로 분류되지 않는 복합 패턴 고객 <b>{len(newp)}명</b>이 감지되었습니다. '
                f'온톨로지 신규 유형 추가를 검토해 주세요.<br>'
                f'<span style="font-size:11.5px;color:#9A6B00">대상 · {ids_str} 등</span>'
                f'</div></div>',
                unsafe_allow_html=True)

        if len(high) > 0:
            new_combos, combo_examples = agent.detect_new_combos(
                high.to_dict("records"), threshold=alert_min)
            if new_combos:
                combo_rows = ""
                for combo, cnt in sorted(new_combos.items(), key=lambda x: x[1], reverse=True):
                    v1_name = ONTOLOGY[combo[0]]["name"]
                    v2_name = ONTOLOGY[combo[1]]["name"]
                    v1_type = ONTOLOGY[combo[0]]["type"]
                    v2_type = ONTOLOGY[combo[1]]["type"]
                    ex_ids = ", ".join(str(x) for x in combo_examples[combo][:3])
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
                    f'</div>', unsafe_allow_html=True)

        if len(high) > 0:
            st.markdown(
                '<div style="margin:24px 0 12px;font-size:14px;font-weight:700;color:var(--ink);letter-spacing:-0.02em">'
                '고위험 이탈 고객 상세 분석</div>', unsafe_allow_html=True)
            edit_mode = st.session_state.get("edit_mode", False)
            for i, (_, r) in enumerate(high.head(10).iterrows()):
                render_customer_card(r, edit_mode=edit_mode, idx=i)
        else:
            st.info(f"임계값 {thr:.2f} 이상인 고위험 고객이 없습니다. 슬라이더 값을 낮춰보세요.")

        # ── STEP 04 ──
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
            st.info("수정 모드 · 각 고객 카드에서 오퍼를 변경하거나 캠페인에서 제외할 수 있습니다.")
            if st.button("수정 완료 및 실행", type="primary"):
                st.session_state["edit_mode"] = False
                st.session_state["camp"] = True
                st.rerun()

        # ── STEP 05 ──
        if approve or "camp" in st.session_state:
            st.session_state["camp"] = True
            st.markdown(
                '<div class="section-block">'
                '<div class="section-num">STEP 05</div>'
                '<div class="section-title">리텐션 캠페인 실행 완료</div>'
                '<div class="section-desc">선정된 고객에게 채널별 맞춤 오퍼가 발송되었습니다.</div>'
                '</div>', unsafe_allow_html=True)

            final_high = high.head(10).copy()
            excluded, modified = [], []
            for _, r in final_high.iterrows():
                cid = r["고객ID"]
                key = f"final_strat_{cid}"
                if key in st.session_state:
                    chosen = st.session_state[key]
                    if chosen is None:
                        excluded.append(cid)
                    elif chosen != r["전략"]:
                        modified.append((cid, r["전략"], chosen))

            if not st.session_state.get("feedback_logged", False):
                for _, r in final_high.iterrows():
                    cid = r["고객ID"]
                    chosen = st.session_state.get(f"final_strat_{cid}", r["전략"])
                    agent.add_feedback(
                        customer_id=cid,
                        dominant_type=r["주요유형"],
                        original_offer=r["전략"],
                        final_offer=chosen,
                        excluded=(chosen is None),
                    )
                st.session_state["feedback_logged"] = True

            target_cnt = len(final_high) - len(excluded)
            st.success(f"{target_cnt}명 대상 초개인화 리텐션 캠페인이 실행되었습니다."
                       + (f" · {len(excluded)}명 제외" if excluded else "")
                       + (f" · {len(modified)}건 오퍼 수정" if modified else ""))

            tc = high.head(10)[~high.head(10)["고객ID"].isin(excluded)]["주요유형"].value_counts().to_dict()
            ri = "".join(
                f'<div class="result-cell"><div class="rv">{cnt}</div><div class="rl">{TYPE_ICONS.get(tp,"")} {tp}</div></div>'
                for tp, cnt in tc.items()
            )
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            st.markdown(
                f'<div class="result-box">'
                f'<div class="result-time">{now} · 캠페인 실행 현황</div>'
                f'<div class="result-grid">'
                f'<div class="result-cell"><div class="rv">{target_cnt}</div><div class="rl">총 발송 대상</div></div>'
                f'{ri}</div>'
                f'<div class="result-foot">Push · LMS · 카카오톡 채널 자동 선택 완료 · 성과 데이터는 24시간 후 자동 수집됩니다</div>'
                f'</div>', unsafe_allow_html=True)

            # ── STEP 06 · 성과 (재학습 UI는 관리자 페이지로 분리) ──
            st.markdown(
                '<div class="section-block">'
                '<div class="section-num">STEP 06</div>'
                '<div class="section-title">캠페인 성과 리포트</div>'
                '<div class="section-desc">발송 결과를 시뮬레이션한 예상 성과입니다.</div>'
                '</div>', unsafe_allow_html=True)

            sim = round(random.uniform(28, 44), 1)
            m1, m2, m3 = st.columns(3)
            m1.metric("예상 리텐션 전환율", f"{sim}%", f"+{round(sim-18,1)}%p vs 기존 일괄 오퍼")
            m2.metric("이탈 방어 예상 고객", f"{int(target_cnt*sim/100)}명")
            m3.metric("오퍼 비용 효율", "개선", "유형별 맞춤 오퍼 적용")

            st.markdown(
                '<div class="callout">'
                '<div class="callout-text">"이제 현업의 역할은 데이터를 찾는 것이 아니라,<br>'
                'Agent가 발견한 인사이트를 바탕으로 더 나은 마케팅 방식을 고민하는 것으로 전환됩니다."</div>'
                '</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# 푸터
# ═══════════════════════════════════════════════════════════════
st.markdown(
    '<div class="site-footer">'
    '<div class="site-footer-text">고객 이탈 원인 분석 및 초개인화 리텐션 Agent</div>'
    '</div>', unsafe_allow_html=True)
