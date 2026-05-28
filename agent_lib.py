"""
agent_lib.py — 메인 페이지와 관리자 페이지가 공유하는 코어 모듈
- 온톨로지 / 전략 매핑 / 페르소나 / 합성 데이터 생성
- ChurnAgent (학습·예측·설명·분류·피드백·재학습)
- 공통 CSS (APP_CSS)
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_absolute_error


# ═══════════════════════════════════════════════════════════════
# 공통 CSS
# ═══════════════════════════════════════════════════════════════
APP_CSS = """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css');

:root {
  --primary: #0046FF;
  --primary-d: #0036CC;
  --primary-l: #E8EFFF;
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
  --good: #16A34A;
  --good-l: #DCFCE7;
}

html, body, [class*="css"], .stApp, .stMarkdown, button, input, textarea, select {
  font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Noto Sans KR', sans-serif !important;
  letter-spacing: -0.01em;
}
.stApp { background: var(--bg); }
.block-container { padding-top: 0 !important; padding-bottom: 4rem; max-width: 880px; }
header[data-testid="stHeader"] { background: transparent; height: 0; }
#MainMenu, footer { visibility: hidden; }

.page-header { padding: 28px 0 26px; margin-bottom: 8px; border-bottom: 1px solid var(--line); }
.page-title { font-size: 24px; font-weight: 700; color: var(--ink); letter-spacing: -0.03em; line-height: 1.35; margin: 0 0 8px; }
.page-desc { font-size: 13.5px; color: var(--sub); line-height: 1.6; margin: 0; }

.agent-board { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 18px 20px; margin: 20px 0 8px; }
.ab-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.ab-cell { border-right: 1px solid var(--line); padding-right: 16px; }
.ab-cell:last-child { border-right: none; padding-right: 0; }
.ab-label { font-size: 11.5px; color: var(--sub); font-weight: 500; margin-bottom: 6px; letter-spacing: -0.005em; }
.ab-value { font-size: 22px; font-weight: 700; color: var(--ink); letter-spacing: -0.025em; line-height: 1.1; font-variant-numeric: tabular-nums; }
.ab-unit { font-size: 12px; font-weight: 500; color: var(--sub); margin-left: 3px; }
.ab-accent { color: var(--primary); }
.ab-hint { margin-top: 14px; padding-top: 14px; border-top: 1px solid #F3F4F6; font-size: 11.5px; color: var(--sub); line-height: 1.5; }
.ab-hint b { color: var(--ink); font-weight: 600; }
@media (max-width: 640px) {
  .ab-row { grid-template-columns: repeat(2, 1fr); }
  .ab-cell { border-right: none; padding-right: 0; }
  .ab-cell:nth-child(odd) { border-right: 1px solid var(--line); padding-right: 12px; }
}

.section-block { margin: 32px 0 16px; }
.section-num { font-size: 11.5px; font-weight: 700; color: var(--primary); letter-spacing: 0.06em; margin-bottom: 6px; }
.section-title { font-size: 20px; font-weight: 700; color: var(--ink); letter-spacing: -0.025em; margin: 0 0 4px; }
.section-desc { font-size: 13.5px; color: var(--sub); margin: 0 0 12px; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
.kpi-cell { background: #FFFFFF; border: 1px solid var(--line); border-radius: 10px; padding: 16px 14px; }
.kpi-label { font-size: 12px; color: var(--sub); font-weight: 500; margin-bottom: 6px; line-height: 1.4; }
.kpi-value { font-size: 26px; font-weight: 700; color: var(--ink); letter-spacing: -0.03em; line-height: 1; }
.kpi-value.accent { color: var(--primary); }
.kpi-value.warn { color: var(--warn); }
.kpi-value.gold { color: #B8860B; }
.kpi-unit { font-size: 13px; font-weight: 500; color: var(--sub); margin-left: 2px; }
@media (max-width: 640px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }

.type-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 16px; }
.type-cell { background: #FFFFFF; border: 1px solid var(--line); border-radius: 10px; padding: 14px 14px 12px; }
.type-head { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.type-icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px; background: var(--primary-l); color: var(--primary); }
.type-name { font-size: 13px; font-weight: 600; color: var(--ink); }
.type-count { font-size: 22px; font-weight: 700; color: var(--ink); letter-spacing: -0.02em; }
.type-pct { font-size: 12px; color: var(--sub); font-weight: 500; margin-left: 4px; }
.type-meta { font-size: 11.5px; color: var(--sub); margin-top: 6px; padding-top: 6px; border-top: 1px solid #F3F4F6; line-height: 1.5; }
.type-meta b { color: var(--ink); font-weight: 600; }
.type-strat { font-size: 11.5px; color: var(--primary); margin-top: 4px; font-weight: 500; line-height: 1.4; }
@media (max-width: 640px) { .type-grid { grid-template-columns: repeat(2, 1fr); } }

/* ── 점수 분포 차트 ── */
.dist-block { background: #FFFFFF; border: 1px solid var(--line); border-radius: 10px; padding: 16px 18px 14px; margin-bottom: 16px; }
.dist-title { font-size: 13px; font-weight: 700; color: var(--ink); letter-spacing: -0.02em; margin-bottom: 12px; }
.dist-row { display: grid; grid-template-columns: 100px 1fr 90px; align-items: center; gap: 12px; margin-bottom: 6px; }
.dist-label { font-size: 11.5px; color: var(--body); font-weight: 500; font-variant-numeric: tabular-nums; }
.dist-track { height: 18px; background: #F1F3F5; border-radius: 4px; overflow: hidden; position: relative; }
.dist-fill { height: 100%; background: var(--primary); border-radius: 4px; transition: width 0.3s; }
.dist-fill.high { background: var(--warn); }
.dist-fill.mid  { background: var(--gold); }
.dist-meta { font-size: 11.5px; color: var(--body); text-align: right; font-variant-numeric: tabular-nums; }
.dist-meta b { color: var(--ink); font-weight: 700; }
.dist-note { margin-top: 8px; padding-top: 8px; border-top: 1px solid #F3F4F6; font-size: 11.5px; color: var(--sub); line-height: 1.5; }
.dist-note b { color: var(--ink); font-weight: 600; }

/* ── 요약 라인 ── */
.summary-line { background: #FAFBFC; border: 1px solid var(--line); border-radius: 10px; padding: 12px 16px; margin-bottom: 12px; font-size: 12.5px; color: var(--body); line-height: 1.6; }
.summary-line b { color: var(--ink); font-weight: 700; }
.summary-line .acc { color: var(--primary); font-weight: 700; }
.summary-line .warn-t { color: var(--warn); font-weight: 700; }

/* ── 미리보기 헤더 ── */
.preview-head { display: flex; justify-content: space-between; align-items: baseline; margin: 24px 0 8px; flex-wrap: wrap; gap: 6px; }
.preview-title { font-size: 14px; font-weight: 700; color: var(--ink); letter-spacing: -0.02em; }
.preview-sub { font-size: 11.5px; color: var(--sub); }

.cust-card { background: #FFFFFF; border: 1px solid var(--line); border-radius: 12px; padding: 18px 20px; margin-bottom: 10px; }
.cust-card.high { border-left: 3px solid var(--warn); }
.cust-card.mid  { border-left: 3px solid var(--gold); }
.cust-head { display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; }
.cust-id-area { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.cust-id { font-size: 15px; font-weight: 700; color: var(--ink); letter-spacing: -0.02em; }
.cust-pill { display: inline-flex; align-items: center; gap: 4px; font-size: 11.5px; font-weight: 600; padding: 3px 9px; border-radius: 4px; }
.p-신판   { color:#0046FF; background:#E8EFFF; }
.p-타사   { color:#6B21A8; background:#F3E8FF; }
.p-포인트 { color:#047857; background:#D1FAE5; }
.p-불만   { color:#B91C1C; background:#FEE2E2; }
.p-카드   { color:#92400E; background:#FEF3C7; }
.p-디지털 { color:#0E7490; background:#CFFAFE; }
.p-신규   { color:#9A3412; background:#FFEDD5; }

.score-chip { font-size: 16px; font-weight: 700; padding: 4px 12px; border-radius: 6px; letter-spacing: -0.01em; font-variant-numeric: tabular-nums; }
.sc-r { color: var(--warn); background: var(--warn-l); }
.sc-a { color: #B8860B; background: var(--gold-l); }

.type-mini { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #F3F4F6; }
.type-mini span { font-size: 11.5px; color: var(--sub); }
.type-mini b { color: var(--body); font-weight: 600; margin-left: 2px; }

.cause-line { font-size: 12.5px; color: var(--body); margin-bottom: 14px; padding: 10px 14px; background: #FAFBFC; border-radius: 8px; border-left: 2px solid var(--primary); }
.cause-line b { color: var(--primary); font-weight: 700; }

.bar-item { margin-bottom: 8px; }
.bar-row { display: flex; justify-content: space-between; font-size: 12px; color: var(--body); margin-bottom: 4px; }
.bar-row .vname { font-weight: 500; }
.bar-row .vtype { font-size: 10.5px; color: #9CA3AF; margin-left: 4px; }
.bar-row .vpct { color: var(--primary); font-weight: 700; font-variant-numeric: tabular-nums; }
.bar-track { height: 5px; background: #F1F3F5; border-radius: 3px; overflow: hidden; }
.bar-fill { height: 5px; background: var(--primary); border-radius: 3px; }

.offer-row { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; margin-top: 14px; padding-top: 14px; border-top: 1px solid #F3F4F6; }
.offer-label { font-size: 11px; font-weight: 600; color: var(--sub); letter-spacing: 0.04em; }
.offer-name { font-size: 13px; font-weight: 600; color: var(--primary); padding: 4px 10px; background: var(--primary-l); border-radius: 4px; }
.offer-detail { font-size: 12px; color: var(--sub); }

.alert-warn { background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; padding: 14px 18px; margin: 12px 0; border-left: 3px solid var(--gold); }
.alert-warn-title { font-size: 13px; font-weight: 700; color: #92400E; margin-bottom: 4px; }
.alert-warn-body { font-size: 12.5px; color: #78350F; line-height: 1.5; }

.alert-new { background: #FFFFFF; border: 1px solid var(--line); border-left: 3px solid var(--primary); border-radius: 10px; padding: 16px 20px; margin: 14px 0; }
.alert-new-title { font-size: 14px; font-weight: 700; color: var(--ink); margin-bottom: 4px; letter-spacing: -0.02em; }
.alert-new-desc { font-size: 12.5px; color: var(--sub); margin-bottom: 12px; line-height: 1.5; }
.alert-new-item { display: flex; justify-content: space-between; align-items: center; gap: 10px; padding: 10px 0; border-top: 1px solid #F3F4F6; font-size: 12.5px; color: var(--body); }
.alert-new-item:first-of-type { border-top: none; padding-top: 4px; }
.alert-new-item .combo b { color: var(--ink); font-weight: 600; }
.alert-new-item .combo .ttype { font-size: 10.5px; color: var(--sub); margin-left: 4px; }
.alert-new-item .meta { font-size: 11.5px; color: var(--primary); font-weight: 600; white-space: nowrap; }

.result-box { background: var(--ink); border-radius: 12px; padding: 24px 26px; margin-top: 8px; color: #fff; }
.result-time { font-size: 12px; color: #94A3B8; margin-bottom: 16px; }
.result-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 18px; }
.result-cell .rv { font-size: 24px; font-weight: 700; color: #fff; line-height: 1; margin-bottom: 4px; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
.result-cell .rl { font-size: 11.5px; color: #94A3B8; font-weight: 500; }
.result-foot { margin-top: 18px; padding-top: 14px; border-top: 1px solid #1E293B; font-size: 11.5px; color: #94A3B8; line-height: 1.6; }

.callout { background: var(--primary-l); border-radius: 10px; padding: 18px 22px; margin-top: 16px; border-left: 3px solid var(--primary); }
.callout-text { font-size: 13.5px; color: var(--ink); line-height: 1.7; font-weight: 500; letter-spacing: -0.015em; }

.retrain-box { background: var(--primary-l); border: 1px solid #BFD2FF; border-radius: 12px; padding: 18px 20px; margin: 16px 0; }
.retrain-title { font-size: 14px; font-weight: 700; color: var(--ink); margin-bottom: 4px; }
.retrain-desc { font-size: 12.5px; color: var(--body); line-height: 1.5; margin-bottom: 12px; }
.delta-up { color: var(--good); font-weight: 700; }
.delta-down { color: var(--warn); font-weight: 700; }

.stButton > button {
  border-radius: 8px !important; font-weight: 600 !important; font-size: 13.5px !important;
  height: 44px !important; letter-spacing: -0.01em !important;
  border: 1px solid var(--line) !important; background: #FFFFFF !important;
  color: var(--ink) !important; box-shadow: none !important; transition: all 0.15s !important;
}
.stButton > button:hover { background: #FAFBFC !important; border-color: #D1D5DB !important; }
.stButton > button[kind="primary"] { background: var(--primary) !important; border-color: var(--primary) !important; color: #FFFFFF !important; }
.stButton > button[kind="primary"]:hover { background: var(--primary-d) !important; border-color: var(--primary-d) !important; }

[data-testid="stFileUploader"] section {
  border: 1.5px dashed #CBD5E1 !important; background: #FAFBFC !important;
  border-radius: 10px !important; padding: 22px !important;
}
[data-testid="stFileUploader"] section:hover { border-color: var(--primary) !important; }
[data-testid="stFileUploader"] small { color: var(--sub) !important; }

.stSlider > div > div > div > div { background: var(--primary) !important; }
.stSlider [data-baseweb="slider"] > div:nth-child(3) { background: var(--primary) !important; }

[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 700 !important; color: var(--ink) !important; letter-spacing: -0.025em !important; }
[data-testid="stMetricLabel"] { font-size: 12px !important; color: var(--sub) !important; font-weight: 500 !important; }
[data-testid="stMetricDelta"] { font-size: 12px !important; }

hr { border-color: var(--line) !important; margin: 24px 0 !important; }
[data-testid="stAlert"] { border-radius: 10px !important; }
label, .stCheckbox label, .stSelectbox label, .stSlider label {
  color: var(--body) !important; font-size: 13px !important; font-weight: 500 !important;
}

.site-footer { margin-top: 48px; padding: 24px 0 8px; border-top: 1px solid var(--line); text-align: center; }
.site-footer-text { font-size: 11.5px; color: var(--sub); line-height: 1.6; }

/* 사이드바 페이지 네비게이션 — 'app' 라벨을 '리텐션 Agent'로 치환 */
[data-testid="stSidebarNav"] ul { padding-top: 8px; }
[data-testid="stSidebarNav"] a { font-weight: 500 !important; font-size: 13.5px !important; }
[data-testid="stSidebarNav"] span[label="app"] { font-size: 0 !important; }
[data-testid="stSidebarNav"] span[label="app"]::before {
  content: "리텐션 Agent" !important;
  font-size: 13.5px !important;
  font-weight: 600 !important;
  color: var(--ink) !important;
}
</style>
"""


# ═══════════════════════════════════════════════════════════════
# 온톨로지 · 전략 정의
# ═══════════════════════════════════════════════════════════════
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


# ═══════════════════════════════════════════════════════════════
# 합성 데이터 생성
# ═══════════════════════════════════════════════════════════════
PERSONAS = [
    {"name":"신판이용감소형",   "types":["신판이용"],              "intensity":0.85, "noise":0.05, "weight":0.04},
    {"name":"타사이용증가형",   "types":["타사이용"],              "intensity":0.85, "noise":0.05, "weight":0.04},
    {"name":"포인트소진형",     "types":["잔여포인트"],            "intensity":0.85, "noise":0.05, "weight":0.04},
    {"name":"민원증가형",       "types":["고객불만"],              "intensity":0.85, "noise":0.05, "weight":0.04},
    {"name":"카드해지위험형",   "types":["카드보유"],              "intensity":0.80, "noise":0.05, "weight":0.04},
    {"name":"디지털이탈형",     "types":["디지털이용"],            "intensity":0.85, "noise":0.05, "weight":0.04},
    {"name":"복합_신판타사",    "types":["신판이용","타사이용"],   "intensity":0.65, "noise":0.08, "weight":0.02},
    {"name":"복합_불만디지털",  "types":["고객불만","디지털이용"], "intensity":0.65, "noise":0.08, "weight":0.02},
    {"name":"복합_포인트신판",  "types":["잔여포인트","신판이용"], "intensity":0.65, "noise":0.08, "weight":0.02},
    {"name":"경계고객",         "types":["신판이용"],              "intensity":0.45, "noise":0.10, "weight":0.18},
    {"name":"안정고객",         "types":[],                        "intensity":0.0,  "noise":0.12, "weight":0.52},
]


def gen_customer(idx, persona, rng):
    """페르소나 기반 단일 고객 생성"""
    row = {"고객번호": f"CL_{idx:04d}"}
    active = set(persona["types"])
    for var, info in ONTOLOGY.items():
        if info["type"] in active:
            if info["dir"] == "LOW":
                center = 0.5 - 0.5 * persona["intensity"]
            else:
                center = 0.5 + 0.5 * persona["intensity"]
            val = rng.normal(center, persona["noise"])
        else:
            val = rng.normal(0.5, 0.13)
        row[var] = round(float(np.clip(val, 0.0, 1.0)), 4)
    base = 0.0
    for var, info in ONTOLOGY.items():
        sign = -1.0 if info["dir"] == "LOW" else 1.0
        var_active = info["type"] in active
        w = 0.18 if var_active else 0.025
        base += sign * (row[var] - 0.5) * w
    if len(active) >= 2:
        base += 0.06
    base += rng.normal(0, 0.025)
    row["Score"] = round(float(base), 6)
    return row


def generate_synthetic_customers(n=300, seed=42, start_idx=1):
    rng = np.random.default_rng(seed)
    weights = np.array([p["weight"] for p in PERSONAS])
    weights = weights / weights.sum()
    rows = []
    for k in range(n):
        i = rng.choice(len(PERSONAS), p=weights)
        rows.append(gen_customer(start_idx + k, PERSONAS[i], rng))
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════
# ChurnAgent
# ═══════════════════════════════════════════════════════════════
class ChurnAgent:
    def __init__(self):
        self.model = None
        self.version = 0
        self.training_size = 0
        self.last_trained = None
        self.r2 = 0.0
        self.mae = 0.0
        self.feature_importance = {}
        self.feature_means = {}
        self.feedback_log = []
        self.history = []
        self.training_df = None

    def train(self, df, note="초기 학습"):
        X = df[VAR_COLS].values
        y = df["Score"].values
        params = dict(n_estimators=140, max_depth=4, learning_rate=0.07,
                      subsample=0.9, random_state=42)
        model = GradientBoostingRegressor(**params)
        model.fit(X, y)
        cv = cross_val_score(GradientBoostingRegressor(**params), X, y,
                             cv=KFold(n_splits=5, shuffle=True, random_state=7),
                             scoring="r2")
        mae = mean_absolute_error(y, model.predict(X))

        self.model = model
        self.version += 1
        self.training_size = len(df)
        self.last_trained = datetime.now()
        self.r2 = float(cv.mean())
        self.mae = float(mae)
        self.feature_importance = {v: float(imp) for v, imp in zip(VAR_COLS, model.feature_importances_)}
        self.feature_means = {v: float(df[v].mean()) for v in VAR_COLS}
        self.training_df = df.copy()
        self.history.append({
            "version": self.version, "time": self.last_trained,
            "size": self.training_size, "r2": self.r2, "mae": self.mae, "note": note,
        })

    def predict(self, X):
        return self.model.predict(X)

    def explain(self, row):
        contribs = {}
        for var, info in ONTOLOGY.items():
            v = float(row.get(var, 0.5))
            mean = self.feature_means.get(var, 0.5)
            imp = self.feature_importance.get(var, 1.0 / len(VAR_COLS))
            dev = v - mean
            signed = max(0.0, -dev) if info["dir"] == "LOW" else max(0.0, dev)
            contribs[var] = imp * signed
        total = sum(contribs.values()) or 1.0
        return {k: round(v / total * 100, 1) for k, v in contribs.items()}

    def classify(self, contribs):
        ts = {}
        for var, pct in contribs.items():
            tp = ONTOLOGY[var]["type"]
            ts[tp] = ts.get(tp, 0) + pct
        dom = max(ts, key=ts.get)
        top2 = sorted(ts.values(), reverse=True)[:2]
        is_new = (top2[0] + (top2[1] if len(top2) > 1 else 0)) < 40
        return dom, ts, is_new

    def recommend(self, type_):
        return TYPE_STRATEGY.get(type_, ("오퍼 미적용", "해당 유형 미정의"))

    def detect_new_combos(self, results, threshold=3):
        combos = {}
        examples = {}
        for r in results:
            top2 = tuple(sorted([v for v, _ in r["top3"][:2]]))
            combos[top2] = combos.get(top2, 0) + 1
            examples.setdefault(top2, []).append(r["고객ID"])
        new_combos = {k: v for k, v in combos.items() if v >= threshold}
        return new_combos, examples

    def add_feedback(self, customer_id, dominant_type, original_offer, final_offer, excluded):
        self.feedback_log.append({
            "time": datetime.now(),
            "customer_id": customer_id,
            "type": dominant_type,
            "original_offer": original_offer,
            "final_offer": final_offer,
            "excluded": excluded,
        })

    def retrain_with_feedback(self, extra_df=None):
        if self.training_df is None:
            return None
        feedback_count = len(self.feedback_log)
        extra_n = max(20, feedback_count * 3)
        rng = np.random.default_rng(seed=2000 + self.version)
        new_rows = []
        nums = self.training_df["고객번호"].apply(lambda s: int(str(s).split("_")[-1]))
        start = int(nums.max()) + 1
        weights = np.array([p["weight"] for p in PERSONAS])
        weights = weights / weights.sum()
        for k in range(extra_n):
            i = rng.choice(len(PERSONAS), p=weights)
            new_rows.append(gen_customer(start + k, PERSONAS[i], rng))
        new_df = pd.DataFrame(new_rows)
        if extra_df is not None and len(extra_df):
            new_df = pd.concat([new_df, extra_df], ignore_index=True)
        merged = pd.concat([self.training_df, new_df], ignore_index=True)
        prev_r2 = self.r2
        prev_size = self.training_size
        note = f"재학습 · 신규 {len(new_df)}건 추가 · 피드백 {feedback_count}건 반영"
        self.train(merged, note=note)
        return {
            "prev_r2": prev_r2, "new_r2": self.r2,
            "prev_size": prev_size, "new_size": self.training_size,
            "added": len(new_df), "feedback": feedback_count,
        }


# ═══════════════════════════════════════════════════════════════
# Agent 싱글톤 (세션 캐시) — 모든 페이지에서 호출
# ═══════════════════════════════════════════════════════════════
def get_agent():
    if "agent" not in st.session_state:
        with st.spinner("Agent 초기 학습 중 (합성 데이터 300건 기준 모델 적합)..."):
            agent = ChurnAgent()
            baseline = generate_synthetic_customers(n=300, seed=42)
            agent.train(baseline, note="초기 학습 · 합성 데이터 300건")
            st.session_state.agent = agent
    return st.session_state.agent
