WITH scenarios (case_order, case_id, country_name, release_year, genre_name) AS (
    VALUES
    (1, '01_ALL', NULL, NULL, NULL),
    (2, '02_USA_2014_ACTION', 'United States of America', 2014, 'Action'),
    (3, '03_USA_2014_ALL_GENRES', 'United States of America', 2014, NULL),
    (4, '04_ALL_COUNTRIES_2014_ACTION', NULL, 2014, 'Action'),
    (5, '05_USA_2014_COMEDY', 'United States of America', 2014, 'Comedy'),
    (6, '06_USA_2010_ACTION', 'United States of America', 2010, 'Action'),
    (7, '07_JAPAN_ALL_YEARS_ACTION', 'Japan', NULL, 'Action')
),
selected_movies AS (
    SELECT s.case_order, s.case_id, f.movie_sk, f.is_finance_valid,
           f.is_revenue_over_budget, f.revenue, f.profit, f.roi
    FROM scenarios s
    CROSS JOIN dds.fact_movie f
    WHERE (s.release_year IS NULL OR EXISTS (
        SELECT 1 FROM dds.dim_date d
        WHERE d.date_sk = f.date_sk AND d.year = s.release_year
    ))
      AND (s.country_name IS NULL OR EXISTS (
        SELECT 1
        FROM dds.bridge_movie_country bc
        JOIN dds.dim_country c ON c.country_sk = bc.country_sk
        WHERE bc.movie_sk = f.movie_sk AND c.country_name = s.country_name
    ))
      AND (s.genre_name IS NULL OR EXISTS (
        SELECT 1
        FROM dds.bridge_movie_genre bg
        JOIN dds.dim_genre g ON g.genre_sk = bg.genre_sk
        WHERE bg.movie_sk = f.movie_sk AND g.genre_name = s.genre_name
    ))
)
SELECT s.case_id,
       COUNT(m.movie_sk) AS movies,
       COUNT(m.movie_sk) FILTER (WHERE m.is_finance_valid = 1) AS valid_movies,
       ROUND((SUM(m.revenue) FILTER (WHERE m.is_finance_valid = 1)) / 1e9, 2)
           AS revenue_bn,
       ROUND((SUM(m.profit) FILTER (WHERE m.is_finance_valid = 1)) / 1e9, 2)
           AS profit_bn,
       ROUND((PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY m.roi)
           FILTER (WHERE m.is_finance_valid = 1))::numeric * 100, 1)
           AS median_roi_pct,
       ROUND(100.0 * SUM(m.is_revenue_over_budget)
           / NULLIF(COUNT(m.movie_sk) FILTER (WHERE m.is_finance_valid = 1), 0), 1)
           AS over_budget_pct
FROM scenarios s
LEFT JOIN selected_movies m ON m.case_order = s.case_order
GROUP BY s.case_order, s.case_id
ORDER BY s.case_order;
