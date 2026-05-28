"""
관리자.py — Agent 운영 대시보드
- Agent 버전 / 학습 데이터 / 모델 성능 / 누적 피드백
- 학습 이력 테이블 + 변수 중요도 차트
- 피드백 로그
- Agent 재학습 (피드백 + 신규 합성데이터 추가)
"""

import streamlit as st
import pandas as pd

from agent_lib import APP_CSS, VAR_COLS, ONTOLOGY, get_agent


st.set_page_config(
    page_title="Agent 관리자 · 고객 이탈 리텐션",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="auto",
)
st.markdown(APP_CSS, unsafe_allow_html=True)

agent = get_agent()


# ── 헤더 ──
st.markdown(
    '<div class="page-header">'
    '<h1 class="page-title">Agent 관리자</h1>'
    '<p class="page-desc">학습된 Agent의 운영 상태를 점검하고 누적 피드백을 활용한 재학습을 진행합니다.</p>'
    '</div>', unsafe_allow_html=True)


# ── 상태 대시보드 ──
fb_cnt = len(agent.feedback_log)
last_str = agent.last_trained.strftime("%Y-%m-%d %H:%M") if agent.last_trained else "—"
st.markdown(
    f'<div class="agent-board">'
    f'<div class="ab-row">'
    f'<div class="ab-cell"><div class="ab-label">Agent 버전</div>'
    f'<div class="ab-value ab-accent">v{agent.version}.0</div></div>'
    f'<div class="ab-cell"><div class="ab-label">학습 데이터</div>'
    f'<div class="ab-value">{agent.training_size:,}<span class="ab-unit">건</span></div></div>'
    f'<div class="ab-cell"><div class="ab-label">모델 성능 · R²</div>'
    f'<div class="ab-value">{agent.r2:.3f}</div></div>'
    f'<div class="ab-cell"><div class="ab-label">누적 피드백</div>'
    f'<div class="ab-value">{fb_cnt:,}<span class="ab-unit">건</span></div></div>'
    f'</div>'
    f'<div class="ab-hint">최근 학습 · <b>{last_str}</b> · MAE {agent.mae:.4f} · '
    f'모델 GradientBoosting (140 trees, depth 4)</div>'
    f'</div>',
    unsafe_allow_html=True)


# ── 학습 이력 ──
st.markdown(
    '<div class="section-block">'
    '<div class="section-num">TRAINING LOG</div>'
    '<div class="section-title">학습 이력</div>'
    '<div class="section-desc">Agent가 학습된 시점·데이터 규모·성능 변화를 기록합니다.</div>'
    '</div>', unsafe_allow_html=True)

hist_df = pd.DataFrame([
    {"버전": f"v{h['version']}.0",
     "시각": h["time"].strftime("%Y-%m-%d %H:%M:%S"),
     "학습데이터": h["size"],
     "R²": round(h["r2"], 4),
     "MAE": round(h["mae"], 4),
     "비고": h["note"]}
    for h in agent.history
])
st.dataframe(hist_df, use_container_width=True, hide_index=True)


# ── 변수 중요도 ──
st.markdown(
    '<div class="section-block">'
    '<div class="section-num">FEATURE IMPORTANCE</div>'
    '<div class="section-title">모델이 학습한 변수 중요도</div>'
    '<div class="section-desc">GradientBoosting 모델이 이탈 예측에 사용한 변수별 비중입니다.</div>'
    '</div>', unsafe_allow_html=True)

fi_df = pd.DataFrame({
    "변수": [ONTOLOGY[v]["name"] for v in VAR_COLS],
    "유형": [ONTOLOGY[v]["type"] for v in VAR_COLS],
    "중요도": [agent.feature_importance.get(v, 0) for v in VAR_COLS],
}).sort_values("중요도", ascending=False)

st.bar_chart(fi_df.set_index("변수")["중요도"])

with st.expander("변수별 중요도 표"):
    st.dataframe(fi_df.assign(중요도=fi_df["중요도"].round(4)),
                 use_container_width=True, hide_index=True)


# ── 피드백 로그 ──
st.markdown(
    '<div class="section-block">'
    '<div class="section-num">FEEDBACK</div>'
    '<div class="section-title">캠페인 피드백 로그</div>'
    '<div class="section-desc">메인 페이지의 캠페인 실행 결과가 자동으로 누적됩니다.</div>'
    '</div>', unsafe_allow_html=True)

if agent.feedback_log:
    fb_df = pd.DataFrame([
        {"시각": f["time"].strftime("%Y-%m-%d %H:%M:%S"),
         "고객ID": f["customer_id"],
         "유형": f["type"],
         "원래 오퍼": f["original_offer"],
         "최종 오퍼": f["final_offer"] if not f["excluded"] else "(제외)",
         "변경/제외": "제외" if f["excluded"] else ("수정" if f["final_offer"] != f["original_offer"] else "")}
        for f in agent.feedback_log
    ])
    st.dataframe(fb_df, use_container_width=True, hide_index=True, height=320)

    type_summary = (
        pd.DataFrame(agent.feedback_log)
          .groupby("type")
          .size()
          .reset_index(name="건수")
          .rename(columns={"type": "유형"})
          .sort_values("건수", ascending=False)
    )
    st.markdown("**유형별 피드백 분포**")
    st.bar_chart(type_summary.set_index("유형")["건수"])
else:
    st.info("아직 누적된 피드백이 없습니다. 메인 페이지에서 캠페인을 실행하면 자동으로 기록됩니다.")


# ── 재학습 ──
st.markdown(
    '<div class="section-block">'
    '<div class="section-num">RETRAIN</div>'
    '<div class="section-title">Agent 재학습</div>'
    '<div class="section-desc">누적된 피드백을 학습 신호로 활용해 신규 데이터와 함께 모델을 재적합합니다.</div>'
    '</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="retrain-box">'
    f'<div class="retrain-title">현재 상태</div>'
    f'<div class="retrain-desc">v{agent.version}.0 · 학습데이터 {agent.training_size:,}건 · '
    f'누적 피드백 {len(agent.feedback_log)}건<br>'
    f'재학습 시 신규 합성 데이터가 추가되고 Agent 버전이 증가합니다.</div>'
    f'</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([1, 3])
with col_a:
    retrain_btn = st.button("Agent 재학습 실행", type="primary", use_container_width=True)

if retrain_btn:
    with st.spinner("피드백 반영 + 신규 학습 데이터 추가 + 모델 재적합 중..."):
        delta = agent.retrain_with_feedback()
    if delta:
        d_r2 = delta["new_r2"] - delta["prev_r2"]
        d_sz = delta["new_size"] - delta["prev_size"]
        sign = "+" if d_r2 >= 0 else ""
        st.success(
            f"재학습 완료 · v{agent.version}.0 → 학습데이터 {delta['prev_size']:,} → "
            f"{delta['new_size']:,} (+{d_sz}) · R² {delta['prev_r2']:.3f} → "
            f"{delta['new_r2']:.3f} ({sign}{d_r2:+.3f})"
        )
        # 메인 페이지가 새 피드백을 다시 기록할 수 있도록 플래그 초기화
        st.session_state["feedback_logged"] = False
        st.rerun()


# ── 푸터 ──
st.markdown(
    '<div class="site-footer">'
    '<div class="site-footer-text">고객 이탈 원인 분석 및 초개인화 리텐션 Agent · 관리자</div>'
    '</div>', unsafe_allow_html=True)
