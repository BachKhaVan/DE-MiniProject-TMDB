"""Parameterized, read-only analytics queries for the TMDB DDS."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

import pandas as pd

try:
    from db import run_query
except ImportError:
    from ai_assistant.db import run_query


BUSINESS_QUESTIONS = {
    "Q1": "Thời lượng và điểm đánh giá theo nhóm thời lượng và thể loại",
    "Q2": "Độ phổ biến và điểm đánh giá theo ngôn ngữ gốc và thể loại",
    "Q3": "Doanh thu và lợi nhuận theo năm, thập niên và thể loại",
    "Q4": "Hiệu quả tài chính theo 5 nhóm ngân sách",
    "Q5": "Top 10 hãng sản xuất: so sánh Weighted và Full",
    "Q6": "Hiệu quả tài chính theo tháng phát hành và thập niên",
    "Q7": "Hiệu quả tài chính theo quốc gia, hợp tác và ngôn ngữ",
    "Q8": "So sánh nhóm chủ đề: Sequel, Adaptation, Superhero và Other",
}

_RUNTIME_ORDER = """CASE fm.runtime_band
    WHEN 'Dưới 90 phút' THEN 1
    WHEN '90–119 phút' THEN 2
    WHEN '120–149 phút' THEN 3
    WHEN 'Từ 150 phút trở lên' THEN 4
    ELSE 5
END"""

_BUDGET_ORDER = """CASE fm.budget_band
    WHEN 'Dưới 1 triệu USD' THEN 1
    WHEN '1–10 triệu' THEN 2
    WHEN '10–50 triệu' THEN 3
    WHEN '50–100 triệu' THEN 4
    WHEN 'Từ 100 triệu trở lên' THEN 5
    ELSE 6
END"""


def _values(value: Any, *, integer: bool = False) -> list:
    if value is None:
        return []
    if isinstance(value, str):
        source = [value]
    elif isinstance(value, Iterable):
        source = list(value)
    else:
        source = [value]

    result = []
    for item in source:
        if item is None:
            continue
        if isinstance(item, str) and item.strip().lower() in {"", "tất cả", "all"}:
            continue
        normalized = int(item) if integer else str(item).strip()
        if normalized not in result:
            result.append(normalized)
    return result


def _normalize_filters(
    years=None,
    genres=None,
    countries=None,
    language_groups=None,
) -> tuple[list[int], list[str], list[str], list[str]]:
    return (
        _values(years, integer=True),
        _values(genres),
        _values(countries),
        _values(language_groups),
    )


def _filter_sql(
    years: list[int],
    genres: list[str],
    countries: list[str],
    language_groups: list[str],
    fact_alias: str = "f",
) -> tuple[str, list[list]]:
    clauses: list[str] = []
    params: list[list] = []
    if years:
        clauses.append(
            f"""EXISTS (
                SELECT 1
                FROM dds.dim_date AS fd
                WHERE fd.date_sk = {fact_alias}.date_sk
                  AND fd.year = ANY(%s)
            )"""
        )
        params.append(years)
    if genres:
        clauses.append(
            f"""EXISTS (
                SELECT 1
                FROM dds.bridge_movie_genre AS fbg
                INNER JOIN dds.dim_genre AS fg ON fg.genre_sk = fbg.genre_sk
                WHERE fbg.movie_sk = {fact_alias}.movie_sk
                  AND fg.genre_sk <> -1
                  AND fg.genre_name = ANY(%s)
            )"""
        )
        params.append(genres)
    if countries:
        clauses.append(
            f"""EXISTS (
                SELECT 1
                FROM dds.bridge_movie_country AS fbc
                INNER JOIN dds.dim_country AS fc ON fc.country_sk = fbc.country_sk
                WHERE fbc.movie_sk = {fact_alias}.movie_sk
                  AND fc.country_sk <> -1
                  AND fc.country_name = ANY(%s)
            )"""
        )
        params.append(countries)
    if language_groups:
        clauses.append(
            f"""EXISTS (
                SELECT 1
                FROM dds.dim_language AS fl
                WHERE fl.language_sk = {fact_alias}.language_sk
                  AND fl.language_sk <> -1
                  AND fl.language_group = ANY(%s)
            )"""
        )
        params.append(language_groups)
    return (" AND\n      ".join(clauses) if clauses else "TRUE"), params


def _filtered_movies_cte(filters: tuple[list, list, list, list]) -> tuple[str, list[list]]:
    years, genres, countries, language_groups = filters
    where_sql, params = _filter_sql(years, genres, countries, language_groups)
    sql = f"""WITH filtered_movies AS (
    SELECT
        f.movie_sk,
        f.date_sk,
        f.language_sk,
        f.budget,
        f.revenue,
        f.profit,
        f.roi,
        f.runtime,
        f.popularity,
        f.vote_average,
        f.vote_count,
        f.is_finance_valid,
        f.is_revenue_over_budget,
        d.year AS release_year,
        d.decade,
        d.month AS month_num,
        d.month_name,
        m.runtime_band,
        m.budget_band,
        m.country_type,
        l.language_name,
        l.language_group
    FROM dds.fact_movie AS f
    LEFT JOIN dds.dim_date AS d ON d.date_sk = f.date_sk
    INNER JOIN dds.dim_movie AS m ON m.movie_sk = f.movie_sk
    LEFT JOIN dds.dim_language AS l ON l.language_sk = f.language_sk
    WHERE {where_sql}
)"""
    return sql, params


def _dimension_filter(alias: str, column: str, values: list[str]) -> tuple[str, list[list]]:
    if not values:
        return "", []
    return f" AND {alias}.{column} = ANY(%s)", [values]


def _run_tables(
    cte: str,
    base_params: list[list],
    queries: list[tuple[str, str, list[list]]],
) -> dict[str, pd.DataFrame]:
    tables = {}
    for name, body, extra_params in queries:
        tables[name] = run_query(
            f"{cte}\n{body}",
            [*base_params, *extra_params],
        )
    return tables


def get_filter_options() -> dict:
    """Fetch selectable years and non-Unknown genre, country and language groups."""
    years_df = run_query(
        """SELECT DISTINCT d.year
           FROM dds.dim_date AS d
           INNER JOIN dds.fact_movie AS f ON f.date_sk = d.date_sk
           WHERE d.date_sk <> -1 AND d.year IS NOT NULL AND d.year > 0
           ORDER BY d.year DESC"""
    )
    genres_df = run_query(
        """SELECT g.genre_name
           FROM dds.dim_genre AS g
           WHERE g.genre_sk <> -1 AND g.genre_name IS NOT NULL
             AND LOWER(g.genre_name) <> 'unknown'
           ORDER BY g.genre_name ASC"""
    )
    countries_df = run_query(
        """SELECT c.country_name
           FROM dds.dim_country AS c
           WHERE c.country_sk <> -1 AND c.country_name IS NOT NULL
             AND LOWER(c.country_name) <> 'unknown'
           ORDER BY c.country_name ASC"""
    )
    language_df = run_query(
        """SELECT DISTINCT l.language_group
           FROM dds.dim_language AS l
           WHERE l.language_sk <> -1 AND l.language_group IS NOT NULL
             AND LOWER(l.language_group) <> 'unknown'
           ORDER BY l.language_group ASC"""
    )
    return {
        "years": [int(year) for year in years_df["year"].tolist()],
        "genres": [str(genre) for genre in genres_df["genre_name"].tolist()],
        "countries": [str(country) for country in countries_df["country_name"].tolist()],
        "language_groups": [str(group) for group in language_df["language_group"].tolist()],
    }


def get_kpi_summary(
    years: list[int] | None = None,
    genres: list[str] | None = None,
    countries: list[str] | None = None,
    language_groups: list[str] | None = None,
    allocation_mode: str = "full",
) -> dict:
    """Return Power BI Overview measures and the top five profitable movies.

    The Overview financial measures stay unweighted, matching the Power BI cards;
    allocation mode affects diagnostics that group by a multi-valued dimension.
    """
    filters = _normalize_filters(years, genres, countries, language_groups)
    cte, params = _filtered_movies_cte(filters)
    kpi_sql = f"""{cte}
SELECT
    COUNT(*) AS total_movies,
    COUNT(*) FILTER (WHERE is_finance_valid = 1) AS valid_movies,
    SUM(revenue) FILTER (WHERE is_finance_valid = 1) AS total_revenue,
    SUM(profit) FILTER (WHERE is_finance_valid = 1) AS total_profit,
    (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY roi)
        FILTER (WHERE is_finance_valid = 1))::numeric AS roi_median,
    ROUND(
        100.0 * SUM(is_revenue_over_budget) FILTER (WHERE is_finance_valid = 1)
        / NULLIF(COUNT(*) FILTER (WHERE is_finance_valid = 1), 0), 2
    ) AS pct_over_budget,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY vote_average)
            FILTER (WHERE vote_count > 0))::numeric, 2
    ) AS median_rating
FROM filtered_movies"""
    top_sql = f"""{cte}
SELECT
    m.title,
    fm.release_year,
    fm.revenue,
    fm.profit,
    fm.roi,
    fm.vote_average
FROM filtered_movies AS fm
INNER JOIN dds.dim_movie AS m ON m.movie_sk = fm.movie_sk
WHERE fm.is_finance_valid = 1
ORDER BY fm.profit DESC NULLS LAST, m.title ASC
LIMIT 5"""
    return {
        "sql": (kpi_sql, top_sql),
        "kpi_df": run_query(kpi_sql, params),
        "top_movies_df": run_query(top_sql, params),
    }


def _question_1(cte: str, params: list[list], filters: tuple[list, list, list, list]) -> dict:
    genres = filters[1]
    genre_filter, genre_params = _dimension_filter("g", "genre_name", genres)
    tables = _run_tables(
        cte,
        params,
        [
            (
                "Theo nhóm thời lượng",
                f"""SELECT
    fm.runtime_band,
    COUNT(DISTINCT fm.movie_sk) AS rated_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.vote_average))::numeric, 2) AS median_rating
FROM filtered_movies AS fm
WHERE fm.vote_count >= 100
  AND fm.runtime_band IS NOT NULL
  AND fm.runtime_band <> 'Không rõ'
GROUP BY fm.runtime_band
ORDER BY {_RUNTIME_ORDER}""",
                [],
            ),
            (
                "Theo thể loại",
                f"""SELECT
    g.genre_name,
    COUNT(DISTINCT fm.movie_sk) AS rated_movies,
    ROUND(AVG(fm.runtime)::numeric, 1) AS avg_runtime,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.vote_average))::numeric, 2) AS median_rating,
    SUM(fm.vote_count) AS total_votes
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_genre AS bg ON bg.movie_sk = fm.movie_sk
INNER JOIN dds.dim_genre AS g ON g.genre_sk = bg.genre_sk
WHERE fm.vote_count >= 100
  AND g.genre_sk <> -1
  {genre_filter}
GROUP BY g.genre_sk, g.genre_name
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY median_rating DESC NULLS LAST, g.genre_name ASC
LIMIT 50""",
                genre_params,
            ),
        ],
    )
    return {
        "title": BUSINESS_QUESTIONS["Q1"],
        "description": "Các nhóm chỉ xét phim có ít nhất 100 lượt bình chọn; thể loại cần tối thiểu 5 phim.",
        "tables": tables,
    }


def _question_2(cte: str, params: list[list], filters: tuple[list, list, list, list]) -> dict:
    genres = filters[1]
    genre_filter, genre_params = _dimension_filter("g", "genre_name", genres)
    tables = _run_tables(
        cte,
        params,
        [
            (
                "Top ngôn ngữ theo tổng lượt bình chọn",
                """SELECT
    l.language_name,
    l.language_group,
    COUNT(DISTINCT fm.movie_sk) AS rated_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.popularity))::numeric, 2) AS median_popularity,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.vote_average))::numeric, 2) AS median_rating,
    SUM(fm.vote_count) AS total_votes
FROM filtered_movies AS fm
INNER JOIN dds.dim_language AS l ON l.language_sk = fm.language_sk
WHERE fm.vote_count >= 100
  AND l.language_sk <> -1
  AND l.language_name IS NOT NULL
GROUP BY l.language_sk, l.language_name, l.language_group
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY total_votes DESC, l.language_name ASC
LIMIT 15""",
                [],
            ),
            (
                "Xếp hạng điểm đánh giá theo thể loại",
                f"""SELECT
    g.genre_name,
    COUNT(DISTINCT fm.movie_sk) AS rated_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.vote_average))::numeric, 2) AS median_rating,
    SUM(fm.vote_count) AS total_votes
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_genre AS bg ON bg.movie_sk = fm.movie_sk
INNER JOIN dds.dim_genre AS g ON g.genre_sk = bg.genre_sk
WHERE fm.vote_count >= 100
  AND g.genre_sk <> -1
  {genre_filter}
GROUP BY g.genre_sk, g.genre_name
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY median_rating DESC NULLS LAST, g.genre_name ASC
LIMIT 50""",
                genre_params,
            ),
        ],
    )
    return {
        "title": BUSINESS_QUESTIONS["Q2"],
        "description": "Chỉ xét phim có ít nhất 100 lượt bình chọn; mỗi ngôn ngữ/thể loại cần tối thiểu 5 phim.",
        "tables": tables,
    }


def _question_3(
    cte: str,
    params: list[list],
    filters: tuple[list, list, list, list],
    mode: str,
) -> dict:
    genres = filters[1]
    genre_filter, genre_params = _dimension_filter("g", "genre_name", genres)
    profit_expr = "fm.profit * bg.weight_factor" if mode == "weighted" else "fm.profit"
    revenue_expr = "fm.revenue * bg.weight_factor" if mode == "weighted" else "fm.revenue"
    if mode == "weighted" and genres:
        decade_profit = """SUM(fm.profit * COALESCE((
            SELECT SUM(fbg.weight_factor)
            FROM dds.bridge_movie_genre AS fbg
            INNER JOIN dds.dim_genre AS fg ON fg.genre_sk = fbg.genre_sk
            WHERE fbg.movie_sk = fm.movie_sk
              AND fg.genre_sk <> -1
              AND fg.genre_name = ANY(%s)
        ), 0))"""
        decade_revenue = """SUM(fm.revenue * COALESCE((
            SELECT SUM(fbg.weight_factor)
            FROM dds.bridge_movie_genre AS fbg
            INNER JOIN dds.dim_genre AS fg ON fg.genre_sk = fbg.genre_sk
            WHERE fbg.movie_sk = fm.movie_sk
              AND fg.genre_sk <> -1
              AND fg.genre_name = ANY(%s)
        ), 0))"""
        decade_params = [genres, genres]
    else:
        decade_profit = "SUM(fm.profit)"
        decade_revenue = "SUM(fm.revenue)"
        decade_params = []

    tables = _run_tables(
        cte,
        params,
        [
            (
                "Top 10 thể loại",
                f"""SELECT
    g.genre_name,
    COUNT(DISTINCT fm.movie_sk) AS valid_movies,
    SUM({revenue_expr}) AS total_revenue,
    SUM({profit_expr}) AS total_profit,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_genre AS bg ON bg.movie_sk = fm.movie_sk
INNER JOIN dds.dim_genre AS g ON g.genre_sk = bg.genre_sk
WHERE fm.is_finance_valid = 1
  AND g.genre_sk <> -1
  {genre_filter}
GROUP BY g.genre_sk, g.genre_name
ORDER BY total_profit DESC NULLS LAST, g.genre_name ASC
LIMIT 10""",
                genre_params,
            ),
            (
                "Tổng hợp theo thập niên",
                f"""SELECT
    fm.decade,
    COUNT(*) AS valid_movies,
    {decade_revenue} AS total_revenue,
    {decade_profit} AS total_profit,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
WHERE fm.is_finance_valid = 1
  AND fm.date_sk <> -1
  AND fm.decade IS NOT NULL
GROUP BY fm.decade
ORDER BY fm.decade ASC
LIMIT 50""",
                decade_params,
            ),
        ],
    )
    return {
        "title": BUSINESS_QUESTIONS["Q3"],
        "description": f"Phân bổ thể loại đang chọn: {mode.title()}. ROI trung vị được tính trên ROI phim, không nhân trọng số.",
        "tables": tables,
    }


def _question_4(cte: str, params: list[list]) -> dict:
    table = (
        "Theo nhóm ngân sách",
        f"""SELECT
    fm.budget_band,
    COUNT(*) AS valid_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct,
    ROUND(100.0 * SUM(fm.is_revenue_over_budget) / NULLIF(COUNT(*), 0), 1) AS pct_over_budget,
    SUM(fm.profit) AS total_profit
FROM filtered_movies AS fm
WHERE fm.is_finance_valid = 1
  AND fm.budget_band IS NOT NULL
  AND fm.budget_band <> 'Không rõ'
GROUP BY fm.budget_band
ORDER BY {_BUDGET_ORDER}
LIMIT 5""",
        [],
    )
    return {
        "title": BUSINESS_QUESTIONS["Q4"],
        "description": "Chỉ tính phim hợp lệ tài chính; ROI là trung vị theo phim và không cộng dồn.",
        "tables": _run_tables(cte, params, [table]),
    }


def _question_5(
    cte: str,
    params: list[list],
    mode: str,
) -> dict:
    ordering = "weighted_profit" if mode == "weighted" else "full_profit"
    table = (
        "So sánh thứ hạng hãng phim",
        f""", company_totals AS (
    SELECT
        c.company_sk,
        c.company_name,
        COUNT(DISTINCT fm.movie_sk) AS valid_movies,
        SUM(fm.profit * bc.weight_factor) AS weighted_profit,
        SUM(fm.profit) AS full_profit
    FROM filtered_movies AS fm
    INNER JOIN dds.bridge_movie_company AS bc ON bc.movie_sk = fm.movie_sk
    INNER JOIN dds.dim_company AS c ON c.company_sk = bc.company_sk
    WHERE fm.is_finance_valid = 1
      AND c.company_sk <> -1
      AND c.company_name IS NOT NULL
    GROUP BY c.company_sk, c.company_name
    HAVING COUNT(DISTINCT fm.movie_sk) >= 5
), ranked_companies AS (
    SELECT
        company_name,
        valid_movies,
        weighted_profit,
        RANK() OVER (ORDER BY weighted_profit DESC) AS weighted_rank,
        full_profit,
        RANK() OVER (ORDER BY full_profit DESC) AS full_rank
    FROM company_totals
)
SELECT company_name, weighted_profit, weighted_rank, full_profit, full_rank, valid_movies
FROM ranked_companies
ORDER BY {ordering} DESC, company_name ASC
LIMIT 10""",
        [],
    )
    return {
        "title": BUSINESS_QUESTIONS["Q5"],
        "description": "Chỉ xếp hạng hãng có ít nhất 5 phim hợp lệ; lợi nhuận là giá trị quy thuộc, không phải lợi nhuận kế toán.",
        "tables": _run_tables(cte, params, [table]),
    }


def _question_6(
    cte: str,
    params: list[list],
    filters: tuple[list, list, list, list],
    mode: str,
) -> dict:
    genres = filters[1]
    if mode == "weighted" and genres:
        profit_expr = """SUM(fm.profit * COALESCE((
            SELECT SUM(fbg.weight_factor)
            FROM dds.bridge_movie_genre AS fbg
            INNER JOIN dds.dim_genre AS fg ON fg.genre_sk = fbg.genre_sk
            WHERE fbg.movie_sk = fm.movie_sk
              AND fg.genre_sk <> -1
              AND fg.genre_name = ANY(%s)
        ), 0))"""
        extra_params = [genres]
    else:
        profit_expr = "SUM(fm.profit)"
        extra_params = []
    tables = _run_tables(
        cte,
        params,
        [
            (
                "Theo tháng phát hành",
                f"""SELECT
    fm.month_num,
    fm.month_name,
    COUNT(*) AS valid_movies,
    {profit_expr} AS total_profit,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
WHERE fm.is_finance_valid = 1
  AND fm.date_sk <> -1
  AND fm.month_num BETWEEN 1 AND 12
GROUP BY fm.month_num, fm.month_name
ORDER BY fm.month_num
LIMIT 12""",
                extra_params,
            ),
            (
                "Theo thập niên",
                f"""SELECT
    fm.decade,
    COUNT(*) AS valid_movies,
    {profit_expr} AS total_profit,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
WHERE fm.is_finance_valid = 1
  AND fm.date_sk <> -1
  AND fm.decade IS NOT NULL
GROUP BY fm.decade
ORDER BY fm.decade
LIMIT 50""",
                extra_params,
            ),
        ],
    )
    return {
        "title": BUSINESS_QUESTIONS["Q6"],
        "description": f"Lợi nhuận theo ngữ cảnh lọc; chế độ phân bổ thể loại: {mode.title()}.",
        "tables": tables,
    }


def _question_7(
    cte: str,
    params: list[list],
    filters: tuple[list, list, list, list],
    mode: str,
) -> dict:
    countries = filters[2]
    country_filter, country_params = _dimension_filter("c", "country_name", countries)
    profit_expr = "fm.profit * bc.weight_factor" if mode == "weighted" else "fm.profit"
    tables = _run_tables(
        cte,
        params,
        [
            (
                "Top 15 quốc gia theo ROI trung vị",
                f"""SELECT
    c.country_name,
    COUNT(DISTINCT fm.movie_sk) AS valid_movies,
    SUM({profit_expr}) AS total_profit,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_country AS bc ON bc.movie_sk = fm.movie_sk
INNER JOIN dds.dim_country AS c ON c.country_sk = bc.country_sk
WHERE fm.is_finance_valid = 1
  AND c.country_sk <> -1
  {country_filter}
GROUP BY c.country_sk, c.country_name
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY roi_median_pct DESC NULLS LAST, c.country_name ASC
LIMIT 15""",
                country_params,
            ),
            (
                "CountryType và LanguageGroup",
                """SELECT
    fm.country_type,
    fm.language_group,
    COUNT(*) AS valid_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
WHERE fm.is_finance_valid = 1
  AND fm.country_type IS NOT NULL
  AND fm.country_type <> 'Unknown'
  AND fm.language_group IS NOT NULL
  AND fm.language_group <> 'Unknown'
GROUP BY fm.country_type, fm.language_group
ORDER BY fm.country_type, fm.language_group
LIMIT 50""",
                [],
            ),
        ],
    )
    return {
        "title": BUSINESS_QUESTIONS["Q7"],
        "description": f"Quốc gia xếp theo ROI trung vị; lợi nhuận quy thuộc dùng chế độ {mode.title()}.",
        "tables": tables,
    }


def _question_8(cte: str, params: list[list]) -> dict:
    table = (
        "Theo nhóm chủ đề",
        """ , movie_theme AS (
    SELECT DISTINCT bk.movie_sk, k.theme_group
    FROM dds.bridge_movie_keyword AS bk
    INNER JOIN dds.dim_keyword AS k ON k.keyword_sk = bk.keyword_sk
    WHERE k.theme_group IN ('Sequel', 'Adaptation', 'Superhero', 'Other')
)
SELECT
    mt.theme_group,
    COUNT(DISTINCT mt.movie_sk) AS movies,
    COUNT(DISTINCT fm.movie_sk) FILTER (WHERE fm.is_finance_valid = 1) AS valid_movies,
    SUM(fm.profit) FILTER (WHERE fm.is_finance_valid = 1) AS total_profit,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi)
            FILTER (WHERE fm.is_finance_valid = 1))::numeric * 100, 1
    ) AS roi_median_pct
FROM movie_theme AS mt
INNER JOIN filtered_movies AS fm ON fm.movie_sk = mt.movie_sk
GROUP BY mt.theme_group
ORDER BY mt.theme_group
LIMIT 4""",
        [],
    )
    return {
        "title": BUSINESS_QUESTIONS["Q8"],
        "description": (
            "Một phim có thể thuộc nhiều nhóm chủ đề; bridge_movie_keyword không có weight_factor. "
            "Vì vậy các dòng chồng lấn và không được cộng trực tiếp thành tổng."
        ),
        "tables": _run_tables(cte, params, [table]),
    }


def get_business_diagnostic(
    question_id: str,
    years: list[int] | None = None,
    genres: list[str] | None = None,
    countries: list[str] | None = None,
    language_groups: list[str] | None = None,
    allocation_mode: str = "full",
) -> dict:
    """Run one of the eight business diagnostics under the active multi-select filters."""
    question_id = str(question_id).strip().upper()
    if question_id not in BUSINESS_QUESTIONS:
        raise ValueError(f"Câu hỏi nghiệp vụ không hợp lệ: {question_id}")
    filters = _normalize_filters(years, genres, countries, language_groups)
    cte, params = _filtered_movies_cte(filters)
    mode = "weighted" if str(allocation_mode).strip().lower().startswith("weight") else "full"
    builders = {
        "Q1": lambda: _question_1(cte, params, filters),
        "Q2": lambda: _question_2(cte, params, filters),
        "Q3": lambda: _question_3(cte, params, filters, mode),
        "Q4": lambda: _question_4(cte, params),
        "Q5": lambda: _question_5(cte, params, mode),
        "Q6": lambda: _question_6(cte, params, filters, mode),
        "Q7": lambda: _question_7(cte, params, filters, mode),
        "Q8": lambda: _question_8(cte, params),
    }
    return {
        "question_id": question_id,
        "title": BUSINESS_QUESTIONS[question_id],
        **builders[question_id](),
    }


ChartQuery = Callable[[str, list[list], tuple[list, list, list, list], str], pd.DataFrame]


def _run_chart_query(
    cte: str,
    params: list[list],
    sql: str,
    extra_params: list[list] | None = None,
) -> pd.DataFrame:
    return run_query(f"{cte}\n{sql}", [*params, *(extra_params or [])])


def _chart_filter(alias: str, column: str, values: list[str]) -> tuple[str, list[list]]:
    return _dimension_filter(alias, column, values)


def _chart_revenue_profit_by_year(cte, params, filters, mode):
    return _run_chart_query(
        cte,
        params,
        """SELECT
    fm.release_year,
    COUNT(*) AS movies,
    COUNT(*) FILTER (WHERE fm.is_finance_valid = 1) AS valid_movies,
    SUM(fm.revenue) FILTER (WHERE fm.is_finance_valid = 1) AS valid_revenue,
    SUM(fm.profit) FILTER (WHERE fm.is_finance_valid = 1) AS total_profit
FROM filtered_movies AS fm
WHERE fm.release_year IS NOT NULL AND fm.date_sk <> -1
GROUP BY fm.release_year
ORDER BY fm.release_year
LIMIT 100""",
    )


def _chart_profit_by_genre(cte, params, filters, mode):
    genre_filter, genre_params = _chart_filter("g", "genre_name", filters[1])
    profit = "SUM(fm.profit * bg.weight_factor)" if mode == "weighted" else "SUM(fm.profit)"
    return _run_chart_query(
        cte,
        params,
        f"""SELECT
    g.genre_name,
    COUNT(DISTINCT fm.movie_sk) AS valid_movies,
    {profit} AS total_profit
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_genre AS bg ON bg.movie_sk = fm.movie_sk
INNER JOIN dds.dim_genre AS g ON g.genre_sk = bg.genre_sk
WHERE fm.is_finance_valid = 1 AND g.genre_sk <> -1
  {genre_filter}
GROUP BY g.genre_sk, g.genre_name
ORDER BY total_profit DESC NULLS LAST, g.genre_name
LIMIT 10""",
        genre_params,
    )


def _chart_profit_roi_by_decade(cte, params, filters, mode):
    return _run_chart_query(
        cte,
        params,
        """SELECT
    fm.decade,
    COUNT(*) AS valid_movies,
    SUM(fm.profit) AS total_profit,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
WHERE fm.is_finance_valid = 1 AND fm.date_sk <> -1 AND fm.decade IS NOT NULL
GROUP BY fm.decade
ORDER BY fm.decade
LIMIT 50""",
    )


def _chart_genre_profit_ranking_by_decade(cte, params, filters, mode):
    genre_filter, genre_params = _chart_filter("g", "genre_name", filters[1])
    profit = "SUM(fm.profit * bg.weight_factor)" if mode == "weighted" else "SUM(fm.profit)"
    return _run_chart_query(
        cte,
        params,
        f""", genre_decade AS (
    SELECT
        fm.decade,
        g.genre_name,
        COUNT(DISTINCT fm.movie_sk) AS valid_movies,
        {profit} AS total_profit
    FROM filtered_movies AS fm
    INNER JOIN dds.bridge_movie_genre AS bg ON bg.movie_sk = fm.movie_sk
    INNER JOIN dds.dim_genre AS g ON g.genre_sk = bg.genre_sk
    WHERE fm.is_finance_valid = 1 AND fm.decade IS NOT NULL AND g.genre_sk <> -1
      {genre_filter}
    GROUP BY fm.decade, g.genre_sk, g.genre_name
    HAVING COUNT(DISTINCT fm.movie_sk) >= 5
)
SELECT
    decade,
    genre_name,
    valid_movies,
    total_profit,
    RANK() OVER (PARTITION BY decade ORDER BY total_profit DESC) AS profit_rank
FROM genre_decade
ORDER BY decade, profit_rank, genre_name
LIMIT 50""",
        genre_params,
    )


def _chart_genre_portfolio(cte, params, filters, mode):
    genre_filter, genre_params = _chart_filter("g", "genre_name", filters[1])
    return _run_chart_query(
        cte,
        params,
        f"""SELECT
    g.genre_name,
    COUNT(DISTINCT fm.movie_sk) AS valid_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_genre AS bg ON bg.movie_sk = fm.movie_sk
INNER JOIN dds.dim_genre AS g ON g.genre_sk = bg.genre_sk
WHERE fm.is_finance_valid = 1 AND g.genre_sk <> -1
  {genre_filter}
GROUP BY g.genre_sk, g.genre_name
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY valid_movies DESC, g.genre_name
LIMIT 50""",
        genre_params,
    )


def _chart_seasonality(cte, params, filters, mode):
    return _run_chart_query(
        cte,
        params,
        """SELECT
    fm.month_num,
    fm.month_name,
    COUNT(*) AS valid_movies,
    SUM(fm.profit) AS total_profit,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
WHERE fm.is_finance_valid = 1 AND fm.date_sk <> -1 AND fm.month_num BETWEEN 1 AND 12
GROUP BY fm.month_num, fm.month_name
ORDER BY fm.month_num
LIMIT 12""",
    )


def _chart_budget_roi_over_budget(cte, params, filters, mode):
    return _run_chart_query(
        cte,
        params,
        f"""SELECT
    fm.budget_band,
    COUNT(*) AS valid_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct,
    ROUND(100.0 * SUM(fm.is_revenue_over_budget) / NULLIF(COUNT(*), 0), 1) AS pct_over_budget
FROM filtered_movies AS fm
WHERE fm.is_finance_valid = 1
  AND fm.budget_band IS NOT NULL AND fm.budget_band <> 'Không rõ'
GROUP BY fm.budget_band
ORDER BY {_BUDGET_ORDER}
LIMIT 5""",
    )


def _chart_countries_by_roi(cte, params, filters, mode):
    country_filter, country_params = _chart_filter("c", "country_name", filters[2])
    return _run_chart_query(
        cte,
        params,
        f"""SELECT
    c.country_name,
    COUNT(DISTINCT fm.movie_sk) AS valid_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_country AS bc ON bc.movie_sk = fm.movie_sk
INNER JOIN dds.dim_country AS c ON c.country_sk = bc.country_sk
WHERE fm.is_finance_valid = 1 AND c.country_sk <> -1
  {country_filter}
GROUP BY c.country_sk, c.country_name
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY roi_median_pct DESC NULLS LAST, c.country_name
LIMIT 15""",
        country_params,
    )


def _chart_country_type_language_roi(cte, params, filters, mode):
    return _run_chart_query(
        cte,
        params,
        """SELECT
    fm.country_type,
    fm.language_group,
    COUNT(*) AS valid_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi))::numeric * 100, 1) AS roi_median_pct
FROM filtered_movies AS fm
WHERE fm.is_finance_valid = 1
  AND fm.country_type IS NOT NULL AND fm.country_type <> 'Unknown'
  AND fm.language_group IS NOT NULL AND fm.language_group <> 'Unknown'
GROUP BY fm.country_type, fm.language_group
HAVING COUNT(*) >= 5
ORDER BY fm.country_type, fm.language_group
LIMIT 50""",
    )


def _chart_themes_keywords(cte, params, filters, mode):
    return _run_chart_query(
        cte,
        params,
        """, movie_theme AS (
    SELECT DISTINCT bk.movie_sk, k.theme_group
    FROM dds.bridge_movie_keyword AS bk
    INNER JOIN dds.dim_keyword AS k ON k.keyword_sk = bk.keyword_sk
    WHERE k.theme_group IN ('Adaptation', 'Sequel', 'Superhero', 'Other')
)
SELECT
    mt.theme_group,
    COUNT(DISTINCT fm.movie_sk) AS movies,
    COUNT(DISTINCT fm.movie_sk) FILTER (WHERE fm.is_finance_valid = 1) AS valid_movies,
    SUM(fm.profit) FILTER (WHERE fm.is_finance_valid = 1) AS total_profit,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.roi)
        FILTER (WHERE fm.is_finance_valid = 1))::numeric * 100, 1) AS roi_median_pct
FROM movie_theme AS mt
INNER JOIN filtered_movies AS fm ON fm.movie_sk = mt.movie_sk
GROUP BY mt.theme_group
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY mt.theme_group
LIMIT 4""",
    )


def _chart_companies_by_profit(cte, params, filters, mode):
    profit = "SUM(fm.profit * bc.weight_factor)" if mode == "weighted" else "SUM(fm.profit)"
    return _run_chart_query(
        cte,
        params,
        f"""SELECT
    c.company_name,
    COUNT(DISTINCT fm.movie_sk) AS valid_movies,
    {profit} AS total_profit
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_company AS bc ON bc.movie_sk = fm.movie_sk
INNER JOIN dds.dim_company AS c ON c.company_sk = bc.company_sk
WHERE fm.is_finance_valid = 1
  AND c.company_sk <> -1 AND c.company_name IS NOT NULL
GROUP BY c.company_sk, c.company_name
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY total_profit DESC NULLS LAST, c.company_name
LIMIT 10""",
    )


def _chart_runtime_rating_by_genre(cte, params, filters, mode):
    genre_filter, genre_params = _chart_filter("g", "genre_name", filters[1])
    return _run_chart_query(
        cte,
        params,
        f"""SELECT
    g.genre_name,
    COUNT(DISTINCT fm.movie_sk) AS rated_movies,
    ROUND(AVG(fm.runtime)::numeric, 1) AS avg_runtime,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.vote_average))::numeric, 2) AS median_rating
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_genre AS bg ON bg.movie_sk = fm.movie_sk
INNER JOIN dds.dim_genre AS g ON g.genre_sk = bg.genre_sk
WHERE fm.vote_count >= 100 AND fm.vote_average IS NOT NULL AND fm.runtime IS NOT NULL
  AND g.genre_sk <> -1
  {genre_filter}
GROUP BY g.genre_sk, g.genre_name
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY median_rating DESC NULLS LAST, g.genre_name
LIMIT 50""",
        genre_params,
    )


def _chart_median_rating_by_genre(cte, params, filters, mode):
    genre_filter, genre_params = _chart_filter("g", "genre_name", filters[1])
    return _run_chart_query(
        cte,
        params,
        f"""SELECT
    g.genre_name,
    COUNT(DISTINCT fm.movie_sk) AS rated_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.vote_average))::numeric, 2) AS median_rating
FROM filtered_movies AS fm
INNER JOIN dds.bridge_movie_genre AS bg ON bg.movie_sk = fm.movie_sk
INNER JOIN dds.dim_genre AS g ON g.genre_sk = bg.genre_sk
WHERE fm.vote_count >= 100 AND fm.vote_average IS NOT NULL AND g.genre_sk <> -1
  {genre_filter}
GROUP BY g.genre_sk, g.genre_name
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY median_rating DESC NULLS LAST, g.genre_name
LIMIT 50""",
        genre_params,
    )


def _chart_median_rating_by_runtime(cte, params, filters, mode):
    return _run_chart_query(
        cte,
        params,
        f"""SELECT
    fm.runtime_band,
    COUNT(DISTINCT fm.movie_sk) AS rated_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.vote_average))::numeric, 2) AS median_rating
FROM filtered_movies AS fm
WHERE fm.vote_count >= 100 AND fm.vote_average IS NOT NULL
  AND fm.runtime_band IS NOT NULL AND fm.runtime_band <> 'Không rõ'
GROUP BY fm.runtime_band
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY {_RUNTIME_ORDER}
LIMIT 10""",
    )


def _chart_popularity_rating_by_language(cte, params, filters, mode):
    return _run_chart_query(
        cte,
        params,
        """SELECT
    fm.language_name,
    COUNT(DISTINCT fm.movie_sk) AS rated_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.popularity))::numeric, 2) AS median_popularity,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY fm.vote_average))::numeric, 2) AS median_rating
FROM filtered_movies AS fm
WHERE fm.vote_count >= 100 AND fm.vote_average IS NOT NULL
  AND fm.popularity IS NOT NULL AND fm.language_sk <> -1
  AND fm.language_name IS NOT NULL AND LOWER(fm.language_name) <> 'unknown'
GROUP BY fm.language_sk, fm.language_name
HAVING COUNT(DISTINCT fm.movie_sk) >= 5
ORDER BY median_popularity DESC NULLS LAST, fm.language_name
LIMIT 50""",
    )


DASHBOARD_CHARTS = [
    {
        "chart_id": "overview_revenue_profit_by_year",
        "page": "Overview",
        "title": "Revenue & Profit by Release Year",
        "short_desc": "Doanh thu và lợi nhuận hợp lệ theo năm phát hành.",
        "query": _chart_revenue_profit_by_year,
    },
    {
        "chart_id": "overview_profit_by_genre",
        "page": "Overview",
        "title": "Profit by Genre (Top 10)",
        "short_desc": "Top 10 thể loại theo lợi nhuận, theo chế độ phân bổ.",
        "query": _chart_profit_by_genre,
    },
    {
        "chart_id": "overview_profit_roi_by_decade",
        "page": "Overview",
        "title": "Profit & Median ROI by Decade",
        "short_desc": "Lợi nhuận hợp lệ và ROI trung vị theo thập niên.",
        "query": _chart_profit_roi_by_decade,
    },
    {
        "chart_id": "financial_genre_profit_ranking_by_decade",
        "page": "Financial drivers",
        "title": "Genre Profit Ranking by Decade",
        "short_desc": "Thứ hạng lợi nhuận thể loại qua các thập niên (tối thiểu 5 phim).",
        "query": _chart_genre_profit_ranking_by_decade,
    },
    {
        "chart_id": "financial_genre_portfolio",
        "page": "Financial drivers",
        "title": "Genre Portfolio: Valid Volume vs Median ROI",
        "short_desc": "Số phim tài chính hợp lệ và ROI trung vị theo thể loại.",
        "query": _chart_genre_portfolio,
    },
    {
        "chart_id": "financial_seasonality_by_month",
        "page": "Financial drivers",
        "title": "Seasonality: Profit & Median ROI by Month",
        "short_desc": "Lợi nhuận hợp lệ và ROI trung vị theo tháng phát hành.",
        "query": _chart_seasonality,
    },
    {
        "chart_id": "financial_roi_over_budget_by_band",
        "page": "Financial drivers",
        "title": "ROI & Over-Budget Rate by Budget Band",
        "short_desc": "ROI trung vị và tỷ lệ doanh thu vượt ngân sách theo nhóm vốn.",
        "query": _chart_budget_roi_over_budget,
    },
    {
        "chart_id": "companies_top_countries_by_roi",
        "page": "Companies & Countries",
        "title": "Top 15 Countries by Median ROI",
        "short_desc": "Top 15 quốc gia theo ROI trung vị, tối thiểu 5 phim hợp lệ.",
        "query": _chart_countries_by_roi,
    },
    {
        "chart_id": "companies_roi_by_country_type_language",
        "page": "Companies & Countries",
        "title": "Median ROI by Country Type & Language",
        "short_desc": "ROI trung vị theo loại hợp tác quốc gia và nhóm ngôn ngữ.",
        "query": _chart_country_type_language_roi,
    },
    {
        "chart_id": "companies_themes_keywords",
        "page": "Companies & Countries",
        "title": "Themes & Keywords",
        "short_desc": "Phim, lợi nhuận và ROI theo nhóm chủ đề keyword; nhóm có thể chồng lấp.",
        "query": _chart_themes_keywords,
    },
    {
        "chart_id": "companies_top_companies_by_profit",
        "page": "Companies & Countries",
        "title": "Top 10 Companies by Profit",
        "short_desc": "Top 10 hãng theo lợi nhuận phân bổ, tối thiểu 5 phim hợp lệ.",
        "query": _chart_companies_by_profit,
    },
    {
        "chart_id": "audience_runtime_rating_by_genre",
        "page": "Audience & Ratings",
        "title": "Runtime vs Rating by Genre",
        "short_desc": "Thời lượng trung bình và rating trung vị; phim có ít nhất 100 votes.",
        "query": _chart_runtime_rating_by_genre,
    },
    {
        "chart_id": "audience_median_rating_by_genre",
        "page": "Audience & Ratings",
        "title": "Median Rating by Genre",
        "short_desc": "Rating trung vị theo thể loại; tối thiểu 100 votes/phim và 5 phim/nhóm.",
        "query": _chart_median_rating_by_genre,
    },
    {
        "chart_id": "audience_median_rating_by_runtime",
        "page": "Audience & Ratings",
        "title": "Median Rating by Runtime Band",
        "short_desc": "Rating trung vị theo nhóm thời lượng; phim có ít nhất 100 votes.",
        "query": _chart_median_rating_by_runtime,
    },
    {
        "chart_id": "audience_popularity_rating_by_language",
        "page": "Audience & Ratings",
        "title": "Popularity vs Rating by Language",
        "short_desc": "Popularity và rating trung vị theo ngôn ngữ; phim có ít nhất 100 votes.",
        "query": _chart_popularity_rating_by_language,
    },
]


def get_selected_charts_data(
    chart_ids: list[str],
    years=None,
    genres=None,
    countries=None,
    allocation_mode: str = "weighted",
) -> list[dict]:
    """Run only selected Power BI chart queries under the current sidebar filters."""
    selected_ids = list(dict.fromkeys(chart_ids or []))
    if len(selected_ids) > 4:
        raise ValueError("Chọn tối đa 4 biểu đồ cho mỗi lượt phân tích.")

    chart_by_id = {chart["chart_id"]: chart for chart in DASHBOARD_CHARTS}
    unknown_ids = [chart_id for chart_id in selected_ids if chart_id not in chart_by_id]
    if unknown_ids:
        raise ValueError(f"Chart ID không hợp lệ: {', '.join(unknown_ids)}")
    if not selected_ids:
        return []

    filters = _normalize_filters(years, genres, countries, [])
    cte, params = _filtered_movies_cte(filters)
    mode = "weighted" if str(allocation_mode).strip().lower().startswith("weight") else "full"
    results = []
    for chart_id in selected_ids:
        chart = chart_by_id[chart_id]
        frame = chart["query"](cte, params, filters, mode)
        results.append(
            {
                "chart_id": chart_id,
                "page": chart["page"],
                "title": chart["title"],
                "description": chart["short_desc"],
                "df": frame,
            }
        )
    return results
