-- =============================================================================
-- SCRIPT KIỂM TRA & NGHIỆM THU DATA WAREHOUSE (SCHEMA: dds)
-- Phụ trách: Thịnh (Phần 3.3 – Data Warehouse)
-- Cách chạy:
--   docker compose exec -T postgres psql -U labuser -d warehouse -f /home/src/postgres/verify_dds_dw.sql
--   hoặc:
--   Get-Content .\postgres\verify_dds_dw.sql | docker compose exec -T postgres psql -U labuser -d warehouse
-- =============================================================================

\echo '========================================================================='
\echo '1. KIEM TRA DANH SACH 12 BANG DDS VA SO LUONG BAN GHI (ROW COUNTS)'
\echo '========================================================================='
SELECT table_type_group, table_name, row_count
FROM (
    SELECT '1 - Fact' AS table_type_group, 'dds.fact_movie' AS table_name, COUNT(*) AS row_count FROM dds.fact_movie
    UNION ALL SELECT '2 - Dimension (Single)', 'dds.dim_movie', COUNT(*) FROM dds.dim_movie
    UNION ALL SELECT '2 - Dimension (Single)', 'dds.dim_date', COUNT(*) FROM dds.dim_date
    UNION ALL SELECT '2 - Dimension (Single)', 'dds.dim_language', COUNT(*) FROM dds.dim_language
    UNION ALL SELECT '3 - Dimension (Multi)',  'dds.dim_genre', COUNT(*) FROM dds.dim_genre
    UNION ALL SELECT '3 - Dimension (Multi)',  'dds.dim_company', COUNT(*) FROM dds.dim_company
    UNION ALL SELECT '3 - Dimension (Multi)',  'dds.dim_country', COUNT(*) FROM dds.dim_country
    UNION ALL SELECT '3 - Dimension (Multi)',  'dds.dim_keyword', COUNT(*) FROM dds.dim_keyword
    UNION ALL SELECT '4 - Bridge',             'dds.bridge_movie_genre', COUNT(*) FROM dds.bridge_movie_genre
    UNION ALL SELECT '4 - Bridge',             'dds.bridge_movie_company', COUNT(*) FROM dds.bridge_movie_company
    UNION ALL SELECT '4 - Bridge',             'dds.bridge_movie_country', COUNT(*) FROM dds.bridge_movie_country
    UNION ALL SELECT '4 - Bridge',             'dds.bridge_movie_keyword', COUNT(*) FROM dds.bridge_movie_keyword
) t
ORDER BY table_type_group, table_name;

\echo '========================================================================='
\echo '2. KIEM TRA GRAIN CUA FACT_MOVIE VA TOAN VEN THAM CHIEU (FK LOGIC)'
\echo '========================================================================='
SELECT
    COUNT(*) AS total_fact_rows,
    COUNT(DISTINCT f.movie_sk) AS distinct_movie_sk,
    (SELECT COUNT(*) FROM dds.dim_movie) AS total_dim_movie_rows,
    COUNT(*) FILTER (WHERE m.movie_sk IS NULL) AS orphan_movie_fk,
    COUNT(*) FILTER (WHERE d.date_sk IS NULL) AS orphan_date_fk,
    COUNT(*) FILTER (WHERE l.language_sk IS NULL) AS orphan_language_fk
FROM dds.fact_movie f
LEFT JOIN dds.dim_movie m ON f.movie_sk = m.movie_sk
LEFT JOIN dds.dim_date d ON f.date_sk = d.date_sk
LEFT JOIN dds.dim_language l ON f.language_sk = l.language_sk;

\echo '========================================================================='
\echo '3. KIEM TRA RANG BUOC KHOA CHINH, UNIQUE VA 11 KHOA NGOAI VAT LY (DDL)'
\echo '========================================================================='
SELECT
    conrelid::regclass AS child_table,
    conname AS constraint_name,
    confrelid::regclass AS referenced_table,
    pg_get_constraintdef(oid) AS constraint_definition
FROM pg_constraint
WHERE contype = 'f'
  AND connamespace = 'dds'::regnamespace
ORDER BY 1, 2;

SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'dds'
  AND table_name = 'fact_movie'
  AND column_name = 'vote_count';

\echo '========================================================================='
\echo '4. KIEM TRA DONG DU LIEU MAC DINH UNKNOWN (SK = -1)'
\echo '========================================================================='
SELECT 'dim_date' AS dimension_table, date_sk AS sk, decade AS natural_key_or_group, month_name AS display_name FROM dds.dim_date WHERE date_sk = -1
UNION ALL
SELECT 'dim_language', language_sk, language_nk, language_name || ' (' || language_group || ')' FROM dds.dim_language WHERE language_sk = -1
UNION ALL
SELECT 'dim_genre', genre_sk, genre_nk::text, genre_name FROM dds.dim_genre WHERE genre_sk = -1
UNION ALL
SELECT 'dim_company', company_sk, company_nk::text, company_name FROM dds.dim_company WHERE company_sk = -1
UNION ALL
SELECT 'dim_country', country_sk, country_code, country_name || ' (' || region || ')' FROM dds.dim_country WHERE country_sk = -1
UNION ALL
SELECT 'dim_keyword', keyword_sk, keyword_nk::text, keyword_name || ' (' || theme_group || ')' FROM dds.dim_keyword WHERE keyword_sk = -1;

\echo '========================================================================='
\echo '5. KIEM TRA TRONG SO PHAN BO WEIGHT_FACTOR TREN 4 BANG BRIDGE'
\echo '========================================================================='
SELECT
    'bridge_movie_genre' AS bridge_table,
    COUNT(DISTINCT movie_sk) AS distinct_movies_covered,
    COUNT(*) FILTER (WHERE genre_sk = -1) AS unknown_fallback_links,
    (SELECT COUNT(*) FROM (
        SELECT movie_sk FROM dds.bridge_movie_genre GROUP BY movie_sk HAVING ABS(SUM(weight_factor) - 1.0) > 0.0000001
    ) q) AS invalid_weight_sum_movies
FROM dds.bridge_movie_genre
UNION ALL
SELECT
    'bridge_movie_company',
    COUNT(DISTINCT movie_sk),
    COUNT(*) FILTER (WHERE company_sk = -1),
    (SELECT COUNT(*) FROM (
        SELECT movie_sk FROM dds.bridge_movie_company GROUP BY movie_sk HAVING ABS(SUM(weight_factor) - 1.0) > 0.0000001
    ) q)
FROM dds.bridge_movie_company
UNION ALL
SELECT
    'bridge_movie_country',
    COUNT(DISTINCT movie_sk),
    COUNT(*) FILTER (WHERE country_sk = -1),
    (SELECT COUNT(*) FROM (
        SELECT movie_sk FROM dds.bridge_movie_country GROUP BY movie_sk HAVING ABS(SUM(weight_factor) - 1.0) > 0.0000001
    ) q)
FROM dds.bridge_movie_country;

-- Xác nhận bridge_movie_keyword không có cột weight_factor
SELECT
    COUNT(*) AS bridge_keyword_weight_factor_columns
FROM information_schema.columns
WHERE table_schema = 'dds'
  AND table_name = 'bridge_movie_keyword'
  AND column_name = 'weight_factor';

\echo '========================================================================='
\echo '6. KIEM TRA QUY TAC NGHIEP VU CAC CHI SO TAI CHINH & KHAN GIA (FACT_MOVIE)'
\echo '========================================================================='
SELECT
    COUNT(*) FILTER (WHERE budget IS NOT NULL AND budget <= 0) AS invalid_zero_or_neg_budget,
    COUNT(*) FILTER (WHERE revenue IS NOT NULL AND revenue <= 0) AS invalid_zero_or_neg_revenue,
    COUNT(*) FILTER (
        WHERE (is_finance_valid = 1 AND (budget IS NULL OR revenue IS NULL OR profit IS NULL OR roi IS NULL))
           OR (is_finance_valid = 0 AND (profit IS NOT NULL OR roi IS NOT NULL))
    ) AS invalid_finance_flag_or_nulls,
    COUNT(*) FILTER (
        WHERE is_finance_valid = 1 AND profit <> (revenue - budget)
    ) AS invalid_profit_formula,
    COUNT(*) FILTER (
        WHERE is_finance_valid = 1 AND ABS(roi - ROUND((revenue - budget) / budget, 4)) > 0.0001
    ) AS invalid_roi_formula,
    COUNT(*) FILTER (
        WHERE is_revenue_over_budget NOT IN (0, 1)
           OR (is_revenue_over_budget = 1 AND NOT (is_finance_valid = 1 AND revenue > budget))
           OR (is_revenue_over_budget = 0 AND (is_finance_valid = 1 AND revenue > budget))
    ) AS invalid_over_budget_flag,
    COUNT(*) FILTER (
        WHERE (vote_count = 0 AND vote_average IS NOT NULL)
           OR (vote_count < 0)
    ) AS invalid_vote_rules,
    COUNT(*) FILTER (WHERE movie_count <> 1) AS invalid_movie_count
FROM dds.fact_movie;

\echo '========================================================================='
\echo '7. THONG KE TONG QUAN CAC CHI SO TRONG FACT_MOVIE (PHUC VU DOI CHIEU BI)'
\echo '========================================================================='
SELECT
    COUNT(*) AS total_movies,
    SUM(is_finance_valid) AS finance_valid_movies,
    SUM(is_revenue_over_budget) AS movies_over_budget,
    ROUND(100.0 * SUM(is_revenue_over_budget) / NULLIF(SUM(is_finance_valid), 0), 2) AS pct_over_budget_valid,
    SUM(budget) FILTER (WHERE is_finance_valid = 1) AS total_valid_budget_usd,
    SUM(revenue) FILTER (WHERE is_finance_valid = 1) AS total_valid_revenue_usd,
    SUM(profit) AS total_valid_profit_usd,
    ROUND(SUM(profit) / NULLIF(SUM(budget) FILTER (WHERE is_finance_valid = 1), 0), 4) AS aggregate_roi_ratio
FROM dds.fact_movie;

