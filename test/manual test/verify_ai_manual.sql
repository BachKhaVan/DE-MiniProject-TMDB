-- ============================================================================
-- MANUAL TEST SQL: ĐỐI CHIẾU SỐ LIỆU WEB AI (ai_assistant) VỚI POSTGRESQL DDS
-- Cách chạy: Get-Content .\ai_assistant\verify_ai_manual.sql | docker compose exec -T postgres psql -U labuser -d warehouse
-- ============================================================================

-- ----------------------------------------------------------------------------
-- [TEST 1 — TAB 1] KPI TOÀN CẦU (KHÔNG LỌC GÌ)
-- Đối chiếu: Valid Revenue $391.49bn | Movies 4,803 | Valid 3,229 | Profit $260.22bn | Median ROI 130.0% | Pct Over Budget 75.5%
-- ----------------------------------------------------------------------------
SELECT
    COUNT(*) AS movies,
    COUNT(*) FILTER (WHERE is_finance_valid = 1) AS valid_movies,
    ROUND((SUM(revenue) FILTER (WHERE is_finance_valid = 1) / 1e9)::numeric, 2) AS valid_revenue_bn,
    ROUND((SUM(profit)  FILTER (WHERE is_finance_valid = 1) / 1e9)::numeric, 2) AS profit_bn,
    ROUND(((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY roi)
        FILTER (WHERE is_finance_valid = 1))::numeric) * 100, 1) AS median_roi_pct,
    ROUND(100.0 * SUM(is_revenue_over_budget) FILTER (WHERE is_finance_valid = 1)
        / NULLIF(COUNT(*) FILTER (WHERE is_finance_valid = 1), 0), 1) AS pct_over_budget
FROM dds.fact_movie;

-- Top 5 phim lợi nhuận cao nhất toàn cầu (Tab 1)
SELECT m.title, d.year AS release_year, f.revenue, f.profit, ROUND((f.roi * 100)::numeric, 1) AS roi_pct, f.vote_average
FROM dds.fact_movie f
JOIN dds.dim_movie m ON m.movie_sk = f.movie_sk
LEFT JOIN dds.dim_date d ON d.date_sk = f.date_sk
WHERE f.is_finance_valid = 1
ORDER BY f.profit DESC NULLS LAST, m.title ASC
LIMIT 5;

-- ----------------------------------------------------------------------------
-- [TEST 2 — TAB 1] LỌC ĐA CHỌN (MULTI-SELECT) — KIỂM TRA KHÔNG NHÂN ĐÔI PHIM
-- Trên Web AI chọn: Country = [United States of America], Year = [2014, 2015], Genre = [Action, Adventure]
-- ----------------------------------------------------------------------------
WITH filtered AS (
    SELECT f.*
    FROM dds.fact_movie f
    WHERE EXISTS (SELECT 1 FROM dds.dim_date d WHERE d.date_sk = f.date_sk AND d.year IN (2014, 2015))
      AND EXISTS (
          SELECT 1 FROM dds.bridge_movie_country bc
          JOIN dds.dim_country c ON c.country_sk = bc.country_sk
          WHERE bc.movie_sk = f.movie_sk AND c.country_name = 'United States of America'
      )
      AND EXISTS (
          SELECT 1 FROM dds.bridge_movie_genre bg
          JOIN dds.dim_genre g ON g.genre_sk = bg.genre_sk
          WHERE bg.movie_sk = f.movie_sk AND g.genre_name IN ('Action', 'Adventure')
      )
)
SELECT
    COUNT(*) AS movies,
    COUNT(*) FILTER (WHERE is_finance_valid = 1) AS valid_movies,
    ROUND((SUM(revenue) FILTER (WHERE is_finance_valid = 1) / 1e9)::numeric, 2) AS valid_revenue_bn,
    ROUND((SUM(profit)  FILTER (WHERE is_finance_valid = 1) / 1e9)::numeric, 2) AS profit_bn,
    ROUND(((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY roi)
        FILTER (WHERE is_finance_valid = 1))::numeric) * 100, 1) AS median_roi_pct,
    ROUND(100.0 * SUM(is_revenue_over_budget) FILTER (WHERE is_finance_valid = 1)
        / NULLIF(COUNT(*) FILTER (WHERE is_finance_valid = 1), 0), 1) AS pct_over_budget
FROM filtered;

-- ----------------------------------------------------------------------------
-- [TEST 3 — TAB 2] OVERVIEW: Profit by Genre (Top 10) — SO SÁNH WEIGHTED VS FULL
-- Trên Web AI tick: "Profit by Genre (Top 10)", đổi qua lại Weighted / Full ở Sidebar
-- ----------------------------------------------------------------------------
SELECT
    g.genre_name,
    COUNT(DISTINCT f.movie_sk) AS valid_movies,
    ROUND((SUM(f.profit * bg.weight_factor) / 1e9)::numeric, 2) AS weighted_profit_bn,
    ROUND((SUM(f.profit) / 1e9)::numeric, 2) AS full_profit_bn
FROM dds.fact_movie f
JOIN dds.bridge_movie_genre bg ON bg.movie_sk = f.movie_sk
JOIN dds.dim_genre g ON g.genre_sk = bg.genre_sk
WHERE f.is_finance_valid = 1 AND g.genre_sk <> -1
GROUP BY g.genre_sk, g.genre_name
ORDER BY weighted_profit_bn DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- [TEST 4 — TAB 2] COMPANIES & COUNTRIES: Top 10 Companies (>= 5 phim hợp lệ)
-- Trên Web AI tick: "Top 10 Companies by Profit"
-- ----------------------------------------------------------------------------
SELECT
    c.company_name,
    COUNT(DISTINCT f.movie_sk) AS valid_movies,
    ROUND((SUM(f.profit * bc.weight_factor) / 1e9)::numeric, 2) AS weighted_profit_bn,
    ROUND((SUM(f.profit) / 1e9)::numeric, 2) AS full_profit_bn
FROM dds.fact_movie f
JOIN dds.bridge_movie_company bc ON bc.movie_sk = f.movie_sk
JOIN dds.dim_company c ON c.company_sk = bc.company_sk
WHERE f.is_finance_valid = 1 AND c.company_sk <> -1
GROUP BY c.company_sk, c.company_name
HAVING COUNT(DISTINCT f.movie_sk) >= 5
ORDER BY weighted_profit_bn DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- [TEST 5 — TAB 2] FINANCIAL DRIVERS & AUDIENCE
-- 5A: ROI & Over-Budget Rate by Budget Band
-- ----------------------------------------------------------------------------
SELECT
    m.budget_band,
    COUNT(*) AS valid_movies,
    ROUND(((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.roi))::numeric) * 100, 1) AS roi_median_pct,
    ROUND(100.0 * SUM(f.is_revenue_over_budget) / NULLIF(COUNT(*), 0), 1) AS pct_over_budget
FROM dds.fact_movie f
JOIN dds.dim_movie m ON m.movie_sk = f.movie_sk
WHERE f.is_finance_valid = 1 AND m.budget_band IS NOT NULL AND m.budget_band <> 'Không rõ'
GROUP BY m.budget_band
ORDER BY MIN(f.budget);

-- 5B: Median Rating by Runtime Band (vote_count >= 100, >= 5 phim)
SELECT
    m.runtime_band,
    COUNT(DISTINCT f.movie_sk) AS rated_movies,
    ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.vote_average))::numeric, 2) AS median_rating
FROM dds.fact_movie f
JOIN dds.dim_movie m ON m.movie_sk = f.movie_sk
WHERE f.vote_count >= 100 AND f.vote_average IS NOT NULL
  AND m.runtime_band IS NOT NULL AND m.runtime_band <> 'Không rõ'
GROUP BY m.runtime_band
HAVING COUNT(DISTINCT f.movie_sk) >= 5
ORDER BY MIN(f.runtime);

-- ----------------------------------------------------------------------------
-- [TEST 6 — TAB 3] ĐỐI CHIẾU CÁC CÂU HỎI TEXT-TO-SQL TRỌNG TÂM
-- ----------------------------------------------------------------------------
-- 6A: "top 7 theo lợi nhuận của Nhật"
SELECT m.title, d.year AS release_year, f.profit
FROM dds.fact_movie f
JOIN dds.dim_movie m ON m.movie_sk = f.movie_sk
LEFT JOIN dds.dim_date d ON d.date_sk = f.date_sk
WHERE f.is_finance_valid = 1
  AND EXISTS (
      SELECT 1 FROM dds.bridge_movie_country bc
      JOIN dds.dim_country c ON c.country_sk = bc.country_sk
      WHERE bc.movie_sk = f.movie_sk AND c.country_code = 'JP'
  )
ORDER BY f.profit DESC
LIMIT 7;

-- 6B: "Top 7 theo lợi nhuận của phim do Mỹ và Nhật cùng sản xuất"
SELECT m.title, d.year AS release_year, f.profit
FROM dds.fact_movie f
JOIN dds.dim_movie m ON m.movie_sk = f.movie_sk
LEFT JOIN dds.dim_date d ON d.date_sk = f.date_sk
WHERE f.is_finance_valid = 1
  AND EXISTS (
      SELECT 1 FROM dds.bridge_movie_country bc
      JOIN dds.dim_country c ON c.country_sk = bc.country_sk
      WHERE bc.movie_sk = f.movie_sk AND c.country_code = 'US'
  )
  AND EXISTS (
      SELECT 1 FROM dds.bridge_movie_country bc
      JOIN dds.dim_country c ON c.country_sk = bc.country_sk
      WHERE bc.movie_sk = f.movie_sk AND c.country_code = 'JP'
  )
ORDER BY f.profit DESC
LIMIT 7;

-- 6C: "So sánh ROI trung vị giữa phim Sequel và Adaptation?"
WITH movie_theme AS (
    SELECT DISTINCT bk.movie_sk, k.theme_group
    FROM dds.bridge_movie_keyword bk
    JOIN dds.dim_keyword k ON k.keyword_sk = bk.keyword_sk
    WHERE k.theme_group IN ('Sequel', 'Adaptation')
)
SELECT
    mt.theme_group,
    COUNT(*) AS valid_movies,
    ROUND(((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.roi))::numeric) * 100, 1) AS median_roi_pct
FROM movie_theme mt
JOIN dds.fact_movie f ON f.movie_sk = mt.movie_sk
WHERE f.is_finance_valid = 1
GROUP BY mt.theme_group
ORDER BY mt.theme_group;

-- 6D: "Doanh thu phim năm 2026 là bao nhiêu?" (Phải trả 0 phim / NULL, AI không được bịa số)
SELECT COUNT(*) AS movies, SUM(f.revenue) AS total_revenue
FROM dds.fact_movie f
JOIN dds.dim_date d ON d.date_sk = f.date_sk
WHERE d.year = 2026 AND f.is_finance_valid = 1;