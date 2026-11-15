-- QUERY 1. Baseline: Country = All, Year = All, Genre = All.
-- Expected display: Movies 4803, Valid Movies 3229, Revenue 391.49bn,
-- Profit 260.22bn, Median ROI 130.0%, Pct Over Budget 75.5%.
SELECT
    COUNT(*) AS movies,
    COUNT(*) FILTER (WHERE f.is_finance_valid = 1) AS valid_movies,
    ROUND((SUM(f.revenue) FILTER (WHERE f.is_finance_valid = 1)) / 1000000000.0, 2)
        AS valid_revenue_bn,
    ROUND((SUM(f.profit) FILTER (WHERE f.is_finance_valid = 1)) / 1000000000.0, 2)
        AS profit_bn,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.roi)
            FILTER (WHERE f.is_finance_valid = 1))::numeric * 100, 1
    ) AS median_roi_pct,
    ROUND(
        100.0 * (SUM(f.is_revenue_over_budget) FILTER (WHERE f.is_finance_valid = 1))
        / NULLIF(COUNT(*) FILTER (WHERE f.is_finance_valid = 1), 0), 1
    ) AS pct_over_budget
FROM dds.fact_movie AS f;

-- QUERY 2. Independent check of the Power BI slicers:
-- Country = United States of America; Year = 2014; Genre = Action;
-- Allocation mode = Weighted (the standard Overview KPIs below remain UNWEIGHTED).
-- EXISTS prevents duplicate movies when filtering through the many-to-many Bridges.
-- Expected display from the Power BI screenshot in the report:
-- Movies = 47; Valid Movies = 41; Revenue ~ 13.84bn; Profit ~ 9.87bn;
-- Median ROI ~ 216.4%; Pct Over Budget ~ 87.8%.
WITH selected_movies AS (
    SELECT f.movie_sk, f.is_finance_valid, f.is_revenue_over_budget,
           f.revenue, f.profit, f.roi
    FROM dds.fact_movie AS f
    INNER JOIN dds.dim_date AS d
        ON d.date_sk = f.date_sk
    WHERE d.year = 2014
      AND EXISTS (
          SELECT 1
          FROM dds.bridge_movie_country AS bc
          INNER JOIN dds.dim_country AS c
              ON c.country_sk = bc.country_sk
          WHERE bc.movie_sk = f.movie_sk
            AND c.country_name = 'United States of America'
      )
      AND EXISTS (
          SELECT 1
          FROM dds.bridge_movie_genre AS bg
          INNER JOIN dds.dim_genre AS g
              ON g.genre_sk = bg.genre_sk
          WHERE bg.movie_sk = f.movie_sk
            AND g.genre_name = 'Action'
      )
)
SELECT
    COUNT(*) AS movies,
    COUNT(*) FILTER (WHERE is_finance_valid = 1) AS valid_movies,
    ROUND((SUM(revenue) FILTER (WHERE is_finance_valid = 1)) / 1000000000.0, 2)
        AS valid_revenue_bn,
    ROUND((SUM(profit) FILTER (WHERE is_finance_valid = 1)) / 1000000000.0, 2)
        AS profit_bn,
    ROUND(
        (PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY roi)
            FILTER (WHERE is_finance_valid = 1))::numeric * 100, 1
    ) AS median_roi_pct,
    ROUND(
        100.0 * (SUM(is_revenue_over_budget) FILTER (WHERE is_finance_valid = 1))
        / NULLIF(COUNT(*) FILTER (WHERE is_finance_valid = 1), 0), 1
    ) AS pct_over_budget
FROM selected_movies;

-- QUERY 3 (OPTIONAL). Weighted Profit ATTRIBUTED TO ACTION.
-- This is a genre-level allocation, NOT the Overview Profit KPI above.
-- If a movie has k genres, Action gets that movie's profit / k.
-- Do not compare this result with Overview Profit = 9.87bn.
SELECT
    ROUND((SUM(f.profit * bg.weight_factor)
        FILTER (WHERE f.is_finance_valid = 1)) / 1000000000.0, 2)
        AS action_weighted_profit_bn
FROM dds.fact_movie AS f
INNER JOIN dds.dim_date AS d
    ON d.date_sk = f.date_sk
INNER JOIN dds.bridge_movie_genre AS bg
    ON bg.movie_sk = f.movie_sk
INNER JOIN dds.dim_genre AS g
    ON g.genre_sk = bg.genre_sk
WHERE d.year = 2014
  AND g.genre_name = 'Action'
  AND EXISTS (
      SELECT 1
      FROM dds.bridge_movie_country AS bc
      INNER JOIN dds.dim_country AS c
          ON c.country_sk = bc.country_sk
      WHERE bc.movie_sk = f.movie_sk
        AND c.country_name = 'United States of America'
  );

-- Troubleshooting if numbers differ:
-- (1) Confirm the database and schema match the snapshot that Power BI refreshed.
-- (2) Confirm country_name and genre_name are exactly as shown (including capitalization).
-- (3) Ensure all other slicers/visual cross-filters are cleared.
-- (4) Check whether the slicer Country uses production country (dim_country),
--     rather than original language, and Year uses release year (dim_date.year).
-- (5) Do not SUM joined Fact rows directly across 2 bridges: it may duplicate movies.
-- (6) ROI Median uses median(movie-level ROI), NOT SUM(profit) / SUM(budget).
