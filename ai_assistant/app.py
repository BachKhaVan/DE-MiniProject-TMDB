"""TMDB financial analytics companion, backed by read-only PostgreSQL queries."""

from __future__ import annotations

import html
import math
import uuid
from collections.abc import Mapping

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="TMDB 5000 — Tài chính Điện ảnh",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
:root {
  --navy: #09152B;
  --navy-2: #0D1F3C;
  --navy-3: #152B4A;
  --gold: #C9A227;
  --gold-light: #D4AF37;
  --canvas: #F8F9FB;
  --card: #FFFFFF;
  --ink: #111827;
  --muted: #475569;
  --line: #E5E7EB;
  --shadow: 0 12px 30px rgba(9,21,43,.07);
}
.stApp {
  background:
    radial-gradient(ellipse at 7% 0%, rgba(201,162,39,.10), transparent 31rem),
    radial-gradient(ellipse at 96% 8%, rgba(14,116,144,.08), transparent 34rem),
    var(--canvas);
  color: var(--ink);
}
.block-container {max-width: 1480px; padding-top: 1.55rem; padding-bottom: 3rem;}
[data-testid="stSidebar"] {
  background: linear-gradient(165deg, #09152B 0%, #0D1F3C 62%, #12294A 100%);
  border-right: 1px solid rgba(212,175,55,.32);
  box-shadow: 8px 0 30px rgba(9,21,43,.08);
}
[data-testid="stSidebar"] * {color: #FFFFFF;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] label {color: #E2E8F0;}
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="tag"] {
  background: rgba(255,255,255,.07);
  border-color: rgba(226,232,240,.22);
  border-radius: 8px;
}
[data-testid="stSidebar"] [data-baseweb="tag"] * {color: #FFFFFF;}
[data-testid="stSidebar"] input {color: var(--ink);}
[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
  border-color: var(--gold-light);
  box-shadow: 0 0 0 1px var(--gold-light);
}
[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,255,255,.05);
  color: #FFFFFF;
  border: 1px solid rgba(212,175,55,.55);
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(201,162,39,.16);
  border-color: var(--gold-light);
  transform: translateY(-1px);
}
[data-testid="stSidebar"] .section-heading {color:#FFFFFF;}
[data-testid="stSidebar"] .section-heading .ui-icon {color:#FFFFFF;}
.hero {
  position:relative;
  overflow:hidden;
  display:flex; align-items:center; justify-content:space-between; gap:1rem;
  background:
    radial-gradient(circle at 84% 8%, rgba(201,162,39,.21), transparent 17rem),
    linear-gradient(118deg, #09152B 0%, #102848 62%, #123A50 100%);
  border:1px solid rgba(212,175,55,.38);
  border-bottom:3px solid var(--gold);
  border-radius:18px;
  padding:1.45rem 1.75rem;
  margin-bottom:1.5rem;
  box-shadow:0 16px 38px rgba(9,21,43,.17);
}
.hero::after {
  content:"";
  position:absolute;
  width:19rem;
  height:19rem;
  right:13%;
  top:-15rem;
  border:1px solid rgba(255,255,255,.10);
  border-radius:50%;
  box-shadow:0 0 0 2.4rem rgba(255,255,255,.025), 0 0 0 5rem rgba(255,255,255,.02);
  pointer-events:none;
}
.hero-copy {position:relative; z-index:1;}
.hero-eyebrow {
  color:#E9CC74;
  font-size:.68rem;
  font-weight:750;
  letter-spacing:.19em;
  text-transform:uppercase;
  margin:0 0 .45rem .1rem;
}
.hero .hero-title, .hero .hero-title span {
  display:flex; align-items:center; gap:.7rem; margin:0; color:#FFFFFF !important;
  font-size:clamp(1.2rem, 2vw, 1.7rem);
  font-weight:760;
  letter-spacing:-.025em;
}
.hero .ui-icon {color:#FFFFFF;}
.model-name {
  position:relative;
  z-index:1;
  display:inline-flex;
  align-items:center;
  gap:.5rem;
  max-width:32%;
  color:#F8FAFC;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  border:1px solid rgba(233,204,116,.42);
  border-radius:999px;
  padding:.55rem .85rem;
  background:rgba(4,13,28,.32);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06);
  font-size:.77rem;
  font-weight:650;
}
.model-dot {
  width:7px;
  height:7px;
  flex:none;
  border-radius:50%;
  background:#50D890;
  box-shadow:0 0 0 4px rgba(80,216,144,.12);
}
.ui-icon {width:20px; height:20px; flex:none; vertical-align:middle;}
.ui-icon .accent {stroke:var(--gold-light);}
.section-heading {
  display:flex;
  align-items:center;
  gap:.62rem;
  color:var(--navy);
  font-size:1.12rem;
  font-weight:740;
  letter-spacing:-.015em;
  margin:.9rem 0 .9rem;
}
.section-heading .ui-icon {color:var(--ink);}
.section-heading .ui-icon .accent {stroke:var(--gold);}
.sidebar-title {
  color:#FFFFFF;
  font-size:1.02rem;
  font-weight:740;
  letter-spacing:.01em;
  margin:.15rem 0 .9rem;
  padding-bottom:.85rem;
  border-bottom:1px solid rgba(212,175,55,.27);
}
.data-status {display:flex; align-items:center; gap:.55rem; font-size:.9rem; font-weight:650; margin:.3rem 0 .65rem;}
.status-dot {height:9px; width:9px; border-radius:50%; display:inline-block; background:#22C55E; box-shadow:0 0 0 3px rgba(34,197,94,.16);}
.status-dot.offline {background:#F87171; box-shadow:0 0 0 3px rgba(248,113,113,.16);}
[data-testid="stMetric"] {
  position:relative;
  overflow:hidden;
  background:linear-gradient(145deg,#FFFFFF 0%,#FCFCFD 100%);
  border:1px solid #E4E8EF;
  border-top:2px solid rgba(201,162,39,.75);
  border-radius:14px;
  padding:.9rem 1rem;
  box-shadow:0 5px 16px rgba(15,23,42,.045);
  transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
[data-testid="stMetric"]:hover {
  transform:translateY(-2px);
  border-color:rgba(201,162,39,.55);
  box-shadow:0 12px 24px rgba(15,23,42,.09);
}
.stMetric label {color:var(--muted);}
[data-testid="stMetricLabel"] p {color:var(--muted); font-size:.78rem; font-weight:680; letter-spacing:.01em;}
[data-testid="stMetricValue"] {color:var(--navy); font-weight:780; font-size:1.52rem; letter-spacing:-.035em;}
.stTabs [data-baseweb="tab-list"] {
  gap:.42rem;
  padding:.34rem;
  border:1px solid #E7EAF0;
  border-radius:13px;
  background:rgba(255,255,255,.78);
  box-shadow:0 4px 14px rgba(15,23,42,.035);
}
.stTabs [data-baseweb="tab"] {
  height:2.7rem;
  border-radius:9px;
  color:var(--muted);
  font-weight:680;
  transition:background .16s ease,color .16s ease;
}
.stTabs [data-baseweb="tab"]:hover {color:var(--navy); background:#F3F5F8;}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
  color:var(--navy);
  background:#F4F0E4;
}
.stTabs [data-baseweb="tab-highlight"] {background:var(--gold); height:3px;}
.stButton > button {
  min-height:2.45rem;
  border:1px solid #D6DCE5;
  border-radius:9px;
  color:var(--navy);
  background:linear-gradient(180deg,#FFFFFF,#F9FAFC);
  box-shadow:0 2px 5px rgba(9,21,43,.035);
  font-weight:680;
  transition:transform .16s ease, box-shadow .16s ease, border-color .16s ease;
}
.stButton > button:hover {
  transform:translateY(-1px);
  border-color:rgba(201,162,39,.8);
  color:var(--navy);
  background:#FFFCF5;
  box-shadow:0 6px 14px rgba(9,21,43,.08);
}
.stButton > button[kind="primary"] {
  background:linear-gradient(115deg,#09152B,#153052);
  border-color:#102644;
  color:#FFFFFF;
  box-shadow:0 5px 13px rgba(9,21,43,.18);
}
.stButton > button[kind="primary"]:hover {
  background:linear-gradient(115deg,#102644,#1B3B60);
  border-color:var(--gold);
  color:#FFFFFF;
}
.ai-card, [class*="st-key-aicard"] {
  background:linear-gradient(135deg,#FFFFFF 0%,#F7FAFC 100%);
  border:1px solid #DCE5ED;
  border-left:4px solid var(--gold);
  border-radius:12px;
  padding:1rem 1.25rem;
  margin:.8rem 0 1.1rem;
  box-shadow:0 7px 20px rgba(9,21,43,.055);
  line-height:1.72;
}
[data-testid="stVerticalBlockBorderWrapper"] {
  border-color:#E2E7EE !important;
  border-radius:13px !important;
  background:rgba(255,255,255,.76);
  box-shadow:0 5px 16px rgba(9,21,43,.035);
}
[data-testid="stExpander"] {
  border:1px solid #E1E6ED;
  border-radius:11px;
  background:rgba(255,255,255,.86);
  box-shadow:0 3px 10px rgba(9,21,43,.025);
}
[data-testid="stDataFrame"] {
  border:1px solid #E1E6ED;
  border-radius:11px;
  overflow:hidden;
  box-shadow:0 5px 16px rgba(9,21,43,.04);
}
[data-testid="stChatMessage"] {
  border:1px solid #E6EAF0;
  border-radius:13px;
  background:rgba(255,255,255,.78);
  box-shadow:0 4px 12px rgba(9,21,43,.035);
}
div[data-testid="stCaptionContainer"] p {color:var(--muted); font-size:.82rem;}
button:focus-visible, input:focus-visible {outline:2px solid var(--gold) !important; outline-offset:2px;}
@media (max-width: 760px) {
  .block-container {padding-top:1rem;}
  .hero {align-items:flex-start; flex-direction:column; padding:1.2rem;}
  .model-name {max-width:100%;}
  .stTabs [data-baseweb="tab"] {font-size:.78rem; padding-left:.55rem; padding-right:.55rem;}
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

try:
    try:
        import db
        import llm
        import queries
    except ImportError:
        from ai_assistant import db, llm, queries
except Exception:
    st.error("Không thể khởi tạo các thành phần dữ liệu. Kiểm tra cấu hình ứng dụng rồi tải lại.")
    st.stop()

BUSINESS_QUESTIONS = queries.BUSINESS_QUESTIONS
ALLOC_OPTIONS = {"Weighted": "weighted", "Full": "full"}
MAX_SELECTED_CHARTS = 4
CHART_PAGE_ORDER = (
    "Overview",
    "Financial drivers",
    "Companies & Countries",
    "Audience & Ratings",
)
SUGGESTED_QUESTIONS = (
    "Top 5 phim lợi nhuận cao nhất năm 2014?",
    "So sánh ROI trung vị giữa phim Sequel và Adaptation?",
    "Tháng phát hành nào có tổng lợi nhuận cao nhất?",
    "Top 5 hãng phim có lợi nhuận phân bổ Weighted cao nhất?",
    "Doanh thu phim năm 2026 là bao nhiêu?",
)

COLUMN_LABELS = {
    "title": "Title",
    "release_year": "Release year",
    "revenue": "Revenue",
    "profit": "Profit",
    "roi": "ROI",
    "vote_average": "Vote Average",
    "runtime_band": "Runtime band",
    "budget_band": "Budget band",
    "genre_name": "Genre",
    "language_name": "Language",
    "language_group": "Language group",
    "country_name": "Country",
    "country_type": "Country type",
    "theme_group": "Theme group",
    "month_num": "Month",
    "month_name": "Month name",
    "decade": "Decade",
    "rated_movies": "Rated Movies",
    "valid_movies": "Valid Movies",
    "total_movies": "Movies",
    "movies": "Movies",
    "avg_runtime": "Avg Runtime (min)",
    "median_rating": "Median Rating",
    "median_popularity": "Median Popularity",
    "total_votes": "Total Votes",
    "total_revenue": "Total Revenue",
    "total_profit": "Total Profit",
    "valid_revenue": "Valid Revenue",
    "roi_median_pct": "ROI Median (%)",
    "pct_over_budget": "Pct Over Budget (%)",
    "profit_rank": "Profit Rank",
    "weighted_profit": "Weighted Profit",
    "weighted_rank": "Weighted Rank",
    "full_profit": "Full Profit",
    "full_rank": "Full Rank",
}

_ICONS = {
    "film": '<rect x="3" y="4" width="18" height="16" rx="2"/><path class="accent" d="M3 9h18M8 4v5m8-5v5"/>',
    "overview": '<rect x="3" y="3" width="8" height="8" rx="1"/><rect x="13" y="3" width="8" height="5" rx="1"/><rect x="13" y="10" width="8" height="11" rx="1"/><rect class="accent" x="3" y="13" width="8" height="8" rx="1"/>',
    "diagnostic": '<path d="M3 3v18h18"/><path class="accent" d="m7 14 4-4 3 3 6-7"/><path d="M17 6h3v3"/>',
    "chat": '<path d="M21 11.5a8.5 8.5 0 0 1-12.8 7.3L3 20l1.2-4.1A8.5 8.5 0 1 1 21 11.5Z"/><path class="accent" d="M8 11h8m-8 4h5"/>',
    "database": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path class="accent" d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    "filter": '<path d="M4 6h16M7 12h10m-7 6h4"/><circle class="accent" cx="8" cy="6" r="1.5"/>',
    "refresh": '<path d="M20 7v5h-5M4 17v-5h5"/><path class="accent" d="M5.5 9A7 7 0 0 1 18 6l2 2M4 16l2 2a7 7 0 0 0 12.5-3"/>',
}


def icon_svg(name: str, *, dark: bool = False) -> str:
    stroke = "#FFFFFF" if dark else "#111827"
    return (
        f'<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="{stroke}" '
        f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'{_ICONS[name]}</svg>'
    )


def section_heading(title: str, icon: str) -> None:
    st.markdown(
        f'<div class="section-heading">{icon_svg(icon)}<span>{html.escape(title)}</span></div>',
        unsafe_allow_html=True,
    )


def _number(value, default=None):
    try:
        if value is None:
            return default
        number = float(value)
        return default if not math.isfinite(number) else number
    except (TypeError, ValueError):
        return default


def fmt_int(value) -> str:
    number = _number(value)
    return "—" if number is None else f"{int(round(number)):,}"


def fmt_money(value) -> str:
    number = _number(value)
    if number is None:
        return "—"
    absolute = abs(number)
    sign = "-" if number < 0 else ""
    if absolute >= 1_000_000_000:
        return f"{sign}${absolute / 1_000_000_000:,.2f} B"
    if absolute >= 1_000_000:
        return f"{sign}${absolute / 1_000_000:,.2f} M"
    return f"{sign}${absolute:,.0f}"


def fmt_billions(value) -> str:
    number = _number(value)
    return "—" if number is None else f"{number / 1_000_000_000:,.2f}"


def fmt_pct(value, scale: float = 1.0) -> str:
    number = _number(value)
    return "—" if number is None else f"{number * scale:,.1f}%"


def _format_cell(column: str, value):
    number = _number(value)
    if number is None:
        return "—" if value is None or pd.isna(value) else value
    name = column.lower()
    if any(token in name for token in ("revenue", "profit", "budget")):
        return fmt_money(number)
    if name.endswith("_pct") or "over_budget" in name:
        return fmt_pct(number)
    if "roi" in name:
        return fmt_pct(number, 100.0)
    if any(token in name for token in ("movies", "votes", "rank", "count")):
        return fmt_int(number)
    if "rating" in name or "popularity" in name:
        return f"{number:,.2f}"
    if "runtime" in name:
        return f"{number:,.1f}"
    return value


def pretty_df(frame: pd.DataFrame) -> pd.DataFrame:
    formatted = frame.copy()
    for column in formatted.columns:
        if pd.api.types.is_numeric_dtype(formatted[column]):
            formatted[column] = formatted[column].map(lambda value: _format_cell(column, value))
    return formatted.rename(columns={column: COLUMN_LABELS.get(column, column) for column in formatted.columns})


def show_df(frame: pd.DataFrame) -> None:
    formatted = pretty_df(frame)
    if _streamlit_version() >= (1, 50):
        st.dataframe(formatted, hide_index=True, width="stretch")
    else:
        st.dataframe(formatted, hide_index=True, use_container_width=True)


def _streamlit_version() -> tuple[int, int]:
    parts = st.__version__.split(".")
    try:
        return int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        return (0, 0)


def ai_card(text: str, key: str) -> None:
    with st.container(key=key):
        st.markdown(text)


def _option_list(options: dict, keys: tuple[str, ...]) -> list:
    for key in keys:
        value = options.get(key)
        if isinstance(value, (list, tuple)):
            return list(value)
    return []


def parse_options(options: dict) -> tuple[list[int], list[str], list[str]]:
    years = []
    for value in _option_list(options, ("years", "year", "year_options", "release_years")):
        number = _number(value)
        if number is not None:
            years.append(int(number))
    genres = [str(value) for value in _option_list(options, ("genres", "genre", "genre_names"))]
    countries = [str(value) for value in _option_list(options, ("countries", "country", "country_names"))]
    return years, genres, countries


@st.cache_data(ttl=60, show_spinner=False)
def cached_connection() -> dict:
    return db.test_connection()


@st.cache_data(ttl=600, show_spinner=False)
def cached_options() -> dict:
    return queries.get_filter_options()


@st.cache_data(ttl=300, show_spinner=False)
def cached_kpi(years, genres, countries, mode) -> dict:
    return queries.get_kpi_summary(
        years=list(years),
        genres=list(genres),
        countries=list(countries),
        language_groups=[],
        allocation_mode=mode,
    )


@st.cache_data(ttl=300, show_spinner=False)
def cached_business_diagnostic(question_id, years, genres, countries, mode) -> dict:
    return queries.get_business_diagnostic(
        question_id,
        years=list(years),
        genres=list(genres),
        countries=list(countries),
        language_groups=[],
        allocation_mode=mode,
    )


@st.cache_data(ttl=300, show_spinner=False)
def cached_selected_charts(chart_ids, years, genres, countries, mode) -> list[dict]:
    return queries.get_selected_charts_data(
        chart_ids=list(chart_ids),
        years=list(years),
        genres=list(genres),
        countries=list(countries),
        allocation_mode=mode,
    )


def _filter_values(values: list, label: str) -> str:
    return ", ".join(str(value) for value in values) if values else f"Tất cả {label}"


def filter_summary(years, genres, countries, mode_label) -> str:
    return (
        f"Năm: {_filter_values(years, 'năm')} · "
        f"Thể loại: {_filter_values(genres, 'thể loại')} · "
        f"Quốc gia: {_filter_values(countries, 'quốc gia')} · "
        f"Phân bổ: {mode_label}"
    )


def _filter_key(prefix: str, question_id: str = "") -> str:
    return "|".join(
        (
            prefix,
            question_id,
            repr(tuple(YEARS)),
            repr(tuple(GENRES)),
            repr(tuple(COUNTRIES)),
            MODE,
        )
    )


def _records(tables: Mapping[str, pd.DataFrame]) -> dict[str, list[dict]]:
    return {name: db.df_to_clean_records(frame) for name, frame in tables.items()}


st.session_state.setdefault("ai_summaries", {})
st.session_state.setdefault("ai_diagnostics", {})
st.session_state.setdefault("ai_chart_explanations", {})
st.session_state.setdefault("dashboard_chart_results", {})
st.session_state.setdefault("chat", [])


def _migrate_chat_history(history: list) -> list[dict]:
    if not history or all(
        isinstance(turn, dict) and {"id", "question", "result"}.issubset(turn)
        for turn in history
    ):
        return history

    turns = []
    pending = None
    for message in history:
        if not isinstance(message, dict):
            continue
        if message.get("role") == "user":
            pending = {
                "id": uuid.uuid4().hex,
                "question": str(message.get("content") or ""),
                "result": None,
            }
        elif message.get("role") == "assistant" and pending is not None:
            pending["result"] = message.get("result") or {
                "status": "error",
                "answer": "Câu trả lời cũ không còn dữ liệu để hiển thị.",
                "dataframe": None,
                "question": pending["question"],
            }
            turns.append(pending)
            pending = None
    if pending is not None:
        pending["result"] = {
            "status": "error",
            "answer": "Câu trả lời chưa được lưu hoàn tất.",
            "dataframe": None,
            "question": pending["question"],
        }
        turns.append(pending)
    return turns[-20:]


st.session_state["chat"] = _migrate_chat_history(st.session_state["chat"])

st.markdown(
    '<div class="hero"><div class="hero-copy">'
    '<div class="hero-eyebrow">TMDB 5000 · EXECUTIVE BI</div>'
    f'<h1 class="hero-title">{icon_svg("film", dark=True)}'
    '<span>AI phân tích hiệu quả tài chính điện ảnh</span></h1>'
    '</div>'
    f'<div class="model-name"><span class="model-dot"></span>{html.escape(llm.get_model_name())}</div></div>',
    unsafe_allow_html=True,
)


def render_sidebar() -> tuple[list[int], list[str], list[str], str, str]:
    with st.sidebar:
        st.markdown(
            f'<div class="sidebar-title">{icon_svg("overview", dark=True)} '
            "Tài chính Điện ảnh TMDB</div>",
            unsafe_allow_html=True,
        )
        try:
            connection = cached_connection()
            connected = bool(connection.get("connected"))
            movie_count = connection.get("fact_movie_rows")
        except Exception:
            connected, movie_count = False, None

        dot_class = "status-dot" if connected else "status-dot offline"
        status_text = f"Dữ liệu: {movie_count:,} phim" if connected and movie_count is not None else "Dữ liệu chưa sẵn sàng"
        st.markdown(
            f'<div class="data-status"><span class="{dot_class}"></span><span>{status_text}</span></div>',
            unsafe_allow_html=True,
        )

        if st.button("Làm mới", key="refresh_data"):
            st.cache_data.clear()
            st.session_state["ai_summaries"] = {}
            st.session_state["ai_diagnostics"] = {}
            st.session_state["ai_chart_explanations"] = {}
            st.session_state["dashboard_chart_results"] = {}
            st.rerun()

        st.markdown("---")
        section_heading("Bộ lọc", "filter")
        try:
            years, genres, countries = parse_options(cached_options())
        except Exception:
            years, genres, countries = [], [], []
            st.caption("Danh sách bộ lọc chưa tải được.")

        selected_countries = st.multiselect("Quốc gia", countries, key="flt_countries", placeholder="Tất cả")
        selected_years = st.multiselect("Năm phát hành", years, key="flt_years", placeholder="Tất cả")
        selected_genres = st.multiselect("Thể loại", genres, key="flt_genres", placeholder="Tất cả")
        allocation_label = st.radio("Chế độ phân bổ", list(ALLOC_OPTIONS), horizontal=True, key="flt_mode")

    return (
        selected_years,
        selected_genres,
        selected_countries,
        allocation_label,
        ALLOC_OPTIONS[allocation_label],
    )


YEARS, GENRES, COUNTRIES, MODE_LABEL, MODE = render_sidebar()


def _render_data_basis(scope: str, tables: Mapping[str, pd.DataFrame]) -> None:
    with st.expander("Căn cứ dữ liệu đối chiếu"):
        st.markdown(f"**Phạm vi lọc:** {html.escape(scope)}")
        if not tables:
            st.caption("Không có truy vấn dữ liệu để đối chiếu.")
        for title, frame in tables.items():
            st.markdown(f"**{html.escape(title)}**")
            if frame is None or frame.empty:
                st.caption("Không có dòng dữ liệu phù hợp.")
            else:
                show_df(frame)


def _kpi_basis(kpi: dict) -> pd.DataFrame:
    rating = _number(kpi.get("median_rating"))
    rows = [
        ("Valid Revenue ($bn)", fmt_billions(kpi.get("total_revenue"))),
        ("Movies", fmt_int(kpi.get("total_movies"))),
        ("Valid movies", fmt_int(kpi.get("valid_movies"))),
        ("Profit ($bn)", fmt_billions(kpi.get("total_profit"))),
        ("Median ROI (%)", fmt_pct(kpi.get("roi_median"), 100.0)),
        ("Pct Over Budget (%)", fmt_pct(kpi.get("pct_over_budget"))),
        ("Median rating (10-point scale)", "—" if rating is None else f"{rating:.2f}"),
    ]
    return pd.DataFrame(rows, columns=["Indicator", "Value"])


def render_kpi_tab() -> None:
    section_heading("Tóm tắt KPI", "overview")
    try:
        result = cached_kpi(tuple(YEARS), tuple(GENRES), tuple(COUNTRIES), MODE)
    except Exception:
        st.error("Không thể tải KPI. Hãy thử Làm mới hoặc kiểm tra kết nối dữ liệu.")
        return

    row = result["kpi_df"].iloc[0].to_dict()
    scope = filter_summary(YEARS, GENRES, COUNTRIES, MODE_LABEL)
    st.caption(scope)
    first_row = st.columns(3)
    first_row[0].metric("Valid Revenue ($bn)", fmt_billions(row.get("total_revenue")))
    first_row[1].metric("Movies", fmt_int(row.get("total_movies")))
    first_row[2].metric("Valid movies", fmt_int(row.get("valid_movies")))
    second_row = st.columns(3)
    second_row[0].metric("Profit ($bn)", fmt_billions(row.get("total_profit")))
    second_row[1].metric("Median ROI (%)", fmt_pct(row.get("roi_median"), 100.0))
    second_row[2].metric("Pct Over Budget (%)", fmt_pct(row.get("pct_over_budget")))

    section_heading("Top 5 phim theo lợi nhuận", "diagnostic")
    show_df(result["top_movies_df"])

    summary_key = _filter_key("kpi")
    if st.button(
        "Tạo tóm tắt",
        type="primary",
        disabled=not llm.is_configured(),
        key="generate_kpi_summary",
    ):
        filters = {
            "years": YEARS or "Tất cả",
            "genres": GENRES or "Tất cả",
            "countries": COUNTRIES or "Tất cả",
            "allocation": MODE_LABEL,
        }
        try:
            with st.container(key="aicard-kpi"):
                with st.spinner("Đang tổng hợp tóm tắt, vui lòng chờ giây lát..."):
                    st.session_state["ai_summaries"][summary_key] = st.write_stream(
                        llm.stream_kpi_summary(
                            filters,
                            db.df_to_clean_records(result["kpi_df"]),
                            db.df_to_clean_records(result["top_movies_df"]),
                        )
                    )
        except Exception:
            st.error("Chưa thể tạo tóm tắt lúc này. Vui lòng thử lại sau.")
    elif summary_key in st.session_state["ai_summaries"]:
        ai_card(st.session_state["ai_summaries"][summary_key], "aicard-kpi")

    _render_data_basis(
        scope,
        {
            "Power BI Overview KPIs": _kpi_basis(row),
            "Top 5 movies (valid financial records)": result["top_movies_df"],
        },
    )


def render_business_diagnostics() -> None:
    section_heading("Chọn biểu đồ Power BI để phân tích", "diagnostic")
    charts_by_page = {
        page: [chart for chart in queries.DASHBOARD_CHARTS if chart["page"] == page]
        for page in CHART_PAGE_ORDER
    }

    if st.button("Bỏ chọn tất cả", key="clear_chart_selection"):
        for chart in queries.DASHBOARD_CHARTS:
            st.session_state.pop(f"chart_select_{chart['chart_id']}", None)
        st.rerun()

    selected_ids = [
        chart["chart_id"]
        for chart in queries.DASHBOARD_CHARTS
        if st.session_state.get(f"chart_select_{chart['chart_id']}", False)
    ]
    page_columns = st.columns(4)
    for column, page in zip(page_columns, CHART_PAGE_ORDER):
        with column:
            with st.container(border=True):
                st.markdown(f"**{page}**")
                for chart in charts_by_page[page]:
                    chart_id = chart["chart_id"]
                    key = f"chart_select_{chart_id}"
                    checked = st.checkbox(
                        chart["title"],
                        key=key,
                        disabled=len(selected_ids) >= MAX_SELECTED_CHARTS
                        and not st.session_state.get(key, False),
                    )
                    if checked and chart_id not in selected_ids:
                        selected_ids.append(chart_id)
                    elif not checked and chart_id in selected_ids:
                        selected_ids.remove(chart_id)
                    st.caption(chart["short_desc"])

    st.caption(f"Đang chọn {len(selected_ids)}/{MAX_SELECTED_CHARTS} biểu đồ")
    user_focus = st.text_input(
        "Vấn đề hoặc biến động cụ thể bạn muốn tập trung làm rõ (không bắt buộc)",
        placeholder="Vì sao ROI thập niên 1910s–1920s cao bất thường?",
        key="dashboard_chart_focus",
    )
    scope = filter_summary(YEARS, GENRES, COUNTRIES, MODE_LABEL)
    chart_ids = tuple(
        chart["chart_id"]
        for chart in queries.DASHBOARD_CHARTS
        if chart["chart_id"] in selected_ids
    )
    analysis_key = (
        tuple(YEARS),
        tuple(GENRES),
        tuple(COUNTRIES),
        MODE,
        chart_ids,
        user_focus.strip(),
    )

    if st.button(
        "Phân tích biểu đồ đã chọn",
        type="primary",
        key="analyze_selected_charts",
        disabled=not chart_ids or not llm.is_configured(),
    ):
        try:
            with st.spinner("Đang truy vấn dữ liệu và phân tích biểu đồ..."):
                chart_results = cached_selected_charts(
                    chart_ids,
                    tuple(YEARS),
                    tuple(GENRES),
                    tuple(COUNTRIES),
                    MODE,
                )
            st.session_state["dashboard_chart_results"][analysis_key] = chart_results
            with st.container(key="aicard-dashboard-charts"):
                st.session_state["ai_chart_explanations"][analysis_key] = st.write_stream(
                    llm.stream_dashboard_charts_explanation(
                        scope,
                        MODE,
                        chart_results,
                        user_focus,
                    )
                )
        except Exception:
            st.error("Chưa thể hoàn tất phân tích. Hãy kiểm tra kết nối dữ liệu/AI rồi thử lại.")
    elif analysis_key in st.session_state["ai_chart_explanations"]:
        ai_card(st.session_state["ai_chart_explanations"][analysis_key], "aicard-dashboard-charts")

    chart_results = st.session_state["dashboard_chart_results"].get(analysis_key)
    if chart_results:
        _render_data_basis(
            scope,
            {
                f"{chart['page']} · {chart['title']}": chart["df"]
                for chart in chart_results
            },
        )


def _render_assistant_result(result: dict, *, show_answer: bool = True) -> None:
    status = result.get("status")
    if status == "out_of_scope":
        st.caption("Ngoài phạm vi dữ liệu TMDB")
    elif status == "blocked":
        st.caption("Yêu cầu không được thực hiện")
    elif status == "ok":
        st.caption("Kết quả truy vấn dữ liệu")
    answer = result.get("answer", "")
    if answer and show_answer:
        st.markdown(answer)
    frame = result.get("dataframe")
    with st.expander("Căn cứ dữ liệu"):
        st.markdown(f"**Câu hỏi:** {html.escape(result.get('question', ''))}")
        if isinstance(frame, pd.DataFrame) and not frame.empty:
            show_df(frame)
        else:
            st.caption("Không có bảng kết quả cho câu hỏi này.")


def _run_chat_question(question: str) -> str:
    turn_id = uuid.uuid4().hex
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Đang tìm câu trả lời, vui lòng chờ giây lát..."):
                result = llm.prepare_text_to_sql(question)
        except Exception:
            result = {
                "status": "error",
                "sql": None,
                "dataframe": None,
                "answer": "Chưa thể tìm câu trả lời lúc này. Vui lòng thử lại sau.",
                "error": "query_preparation_failed",
            }
        result["question"] = question
        frame = result.get("dataframe")
        answer_streamed = False
        if result.get("status") == "ok" and isinstance(frame, pd.DataFrame) and not frame.empty:
            try:
                result["answer"] = st.write_stream(
                    llm.stream_text_to_sql_answer(question, result.get("sql") or "", frame)
                )
                answer_streamed = True
            except Exception:
                result["answer"] = (
                    "Đã có dữ liệu đối chiếu, nhưng phần diễn giải chưa hoàn tất. "
                    "Bạn vẫn có thể xem bảng kết quả bên dưới."
                )
        if answer_streamed:
            _render_assistant_result(result, show_answer=False)
        else:
            _render_assistant_result(result)
    st.session_state["chat"].append(
        {"id": turn_id, "question": question, "result": result}
    )
    st.session_state["chat"] = st.session_state["chat"][-20:]
    return turn_id


def _render_chat_turn(turn: dict) -> None:
    with st.container(border=True):
        delete_column, _ = st.columns([1, 8])
        if delete_column.button(
            "Xóa đoạn này",
            key=f"delete_chat_{turn['id']}",
            help="Xóa riêng cuộc hội thoại này",
        ):
            st.session_state["chat"] = [
                current
                for current in st.session_state["chat"]
                if current["id"] != turn["id"]
            ]
            st.rerun()
        with st.chat_message("user"):
            st.write(turn["question"])
        with st.chat_message("assistant"):
            _render_assistant_result(turn["result"])


def render_chat_tab() -> None:
    section_heading("Hỏi đáp dữ liệu", "chat")
    sample_columns = st.columns(len(SUGGESTED_QUESTIONS))
    selected_question = None
    for index, sample in enumerate(SUGGESTED_QUESTIONS):
        if sample_columns[index].button(sample, key=f"sample_question_{index}"):
            selected_question = sample

    typed_question = st.chat_input("Nhập câu hỏi về dữ liệu TMDB")
    question = selected_question or typed_question
    newest_turn_id = None
    if question:
        newest_turn_id = _run_chat_question(question)

    for turn in reversed(st.session_state["chat"]):
        if turn["id"] != newest_turn_id:
            _render_chat_turn(turn)


tabs = st.tabs(["Tóm tắt KPI", "Giải thích xu hướng", "Hỏi đáp dữ liệu"])
with tabs[0]:
    render_kpi_tab()
with tabs[1]:
    render_business_diagnostics()
with tabs[2]:
    render_chat_tab()
