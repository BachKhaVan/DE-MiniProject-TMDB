"""Independent SQL reference calculations; NOT substitutes for actual Power BI DAX results."""
from core import register

QUERIES={
'BI01':('KPI toàn danh mục, cùng tập phim finance-valid', '''
SELECT count(*) AS movies,
 count(*) FILTER(WHERE is_finance_valid=1) AS valid_movies,
 sum(revenue) FILTER(WHERE is_finance_valid=1) AS valid_revenue,
 sum(budget) FILTER(WHERE is_finance_valid=1) AS valid_budget,
 sum(profit) FILTER(WHERE is_finance_valid=1) AS total_profit,
 sum(profit) FILTER(WHERE is_finance_valid=1)/nullif(sum(budget) FILTER(WHERE is_finance_valid=1),0) AS roi_overall,
 percentile_cont(0.5) WITHIN GROUP (ORDER BY roi::float8) FILTER(WHERE is_finance_valid=1) AS roi_median,
 count(*) FILTER(WHERE is_revenue_over_budget=1)::numeric/nullif(count(*) FILTER(WHERE is_finance_valid=1),0) AS pct_over_budget
FROM dds.fact_movie'''),
'BI02':('Country USA + Year 2014 + Genre Action (không nhân đôi phim)', '''
WITH selected AS (
 SELECT DISTINCT f.movie_sk,f.revenue,f.profit,f.roi,f.is_finance_valid,f.is_revenue_over_budget
 FROM dds.fact_movie f JOIN dds.dim_date d ON d.date_sk=f.date_sk
 JOIN dds.bridge_movie_country bc ON bc.movie_sk=f.movie_sk JOIN dds.dim_country c ON c.country_sk=bc.country_sk
 JOIN dds.bridge_movie_genre bg ON bg.movie_sk=f.movie_sk JOIN dds.dim_genre g ON g.genre_sk=bg.genre_sk
 WHERE c.country_name='United States of America' AND d.year=2014 AND g.genre_name='Action'
)
SELECT count(*) AS movies, count(*) FILTER(WHERE is_finance_valid=1) AS valid_movies,
 sum(revenue) FILTER(WHERE is_finance_valid=1) AS valid_revenue,
 sum(profit) FILTER(WHERE is_finance_valid=1) AS total_profit,
 percentile_cont(0.5) WITHIN GROUP(ORDER BY roi::float8) FILTER(WHERE is_finance_valid=1) AS roi_median,
 count(*) FILTER(WHERE is_revenue_over_budget=1)::numeric/nullif(count(*) FILTER(WHERE is_finance_valid=1),0) AS pct_over_budget
FROM selected'''),
'BI03':('Weighted và Full: profit theo hãng, kiểm tra phân bổ', '''
WITH revenue_per_company AS (
 SELECT c.company_name, count(DISTINCT f.movie_sk) FILTER(WHERE f.is_finance_valid=1) AS valid_movies,
 sum(f.profit*b.weight_factor) FILTER(WHERE f.is_finance_valid=1) AS weighted_profit,
 sum(f.profit) FILTER(WHERE f.is_finance_valid=1) AS full_profit
 FROM dds.bridge_movie_company b JOIN dds.dim_company c ON c.company_sk=b.company_sk
 JOIN dds.fact_movie f ON f.movie_sk=b.movie_sk GROUP BY c.company_name
)
SELECT * FROM revenue_per_company WHERE valid_movies>=5 ORDER BY weighted_profit DESC NULLS LAST,company_name LIMIT 15'''),
'BI04':('SQL kiểm tra phân nhóm ít hơn 5 valid movies', '''
SELECT c.company_name,count(DISTINCT f.movie_sk) FILTER(WHERE f.is_finance_valid=1) AS valid_movies
FROM dds.dim_company c JOIN dds.bridge_movie_company b USING(company_sk)
JOIN dds.fact_movie f USING(movie_sk)
GROUP BY c.company_name HAVING count(DISTINCT f.movie_sk) FILTER(WHERE f.is_finance_valid=1) < 5
ORDER BY valid_movies DESC,c.company_name LIMIT 10'''),
'BI05':('Một phim nhiều genre, minh họa 1/k từ dữ liệu thật', '''
SELECT m.movie_nk,m.title,count(*) AS genre_count,
 min(bg.weight_factor) AS each_weight,sum(bg.weight_factor) AS total_weight,
 string_agg(g.genre_name,', ' ORDER BY g.genre_name) AS genres
FROM dds.bridge_movie_genre bg JOIN dds.dim_movie m USING(movie_sk)
JOIN dds.dim_genre g USING(genre_sk)
GROUP BY m.movie_nk,m.title HAVING count(*)>1
ORDER BY genre_count DESC,m.movie_nk LIMIT 5'''),
'BI06':('Phim có budget/revenue NULL, ví dụ dữ liệu thật', '''
SELECT m.movie_nk,m.title,f.budget,f.revenue,f.is_finance_valid,f.roi
FROM dds.fact_movie f JOIN dds.dim_movie m USING(movie_sk)
WHERE f.budget IS NULL OR f.revenue IS NULL
ORDER BY m.movie_nk LIMIT 10'''),
'Q1SQL':('Q1 Rating theo runtime/genre, chỉ phim đủ votes', '''
SELECT m.runtime_band,g.genre_name,count(DISTINCT f.movie_sk) AS movie_count,
 avg(f.runtime) AS avg_runtime,
 percentile_cont(0.5) WITHIN GROUP(ORDER BY f.vote_average::float8) AS median_rating
FROM dds.fact_movie f JOIN dds.dim_movie m USING(movie_sk)
JOIN dds.bridge_movie_genre bg USING(movie_sk) JOIN dds.dim_genre g USING(genre_sk)
WHERE f.vote_count>=100 AND f.vote_average IS NOT NULL
GROUP BY m.runtime_band,g.genre_name ORDER BY m.runtime_band,g.genre_name'''),
'Q2SQL':('Q2 Rating & popularity theo ngôn ngữ gốc (Min Votes=100)', '''
SELECT l.language_group,l.language_name,count(*) AS movies,
 percentile_cont(0.5) WITHIN GROUP (ORDER BY f.popularity::float8) AS median_popularity,
 percentile_cont(0.5) WITHIN GROUP (ORDER BY f.vote_average::float8) AS median_rating,
 sum(f.vote_count) AS total_votes
FROM dds.fact_movie f JOIN dds.dim_language l USING(language_sk)
WHERE f.vote_count>=100 AND f.vote_average IS NOT NULL
GROUP BY l.language_group,l.language_name ORDER BY median_popularity DESC NULLS LAST,l.language_name'''),
'Q3SQL':('Q3 Weighted genre profit qua các thập niên', '''
SELECT d.decade,g.genre_name,count(DISTINCT f.movie_sk) AS valid_movies,
 sum(f.revenue*bg.weight_factor) AS weighted_revenue,
 sum(f.profit*bg.weight_factor) AS weighted_profit
FROM dds.fact_movie f JOIN dds.dim_date d USING(date_sk)
JOIN dds.bridge_movie_genre bg USING(movie_sk) JOIN dds.dim_genre g USING(genre_sk)
WHERE f.is_finance_valid=1 GROUP BY d.decade,g.genre_name
ORDER BY d.decade,g.genre_name'''),
'Q4SQL':('Q4 ROI/Pct over budget theo budget band', '''
SELECT m.budget_band,count(*) AS valid_movies,
 percentile_cont(0.5) WITHIN GROUP(ORDER BY f.roi::float8) AS roi_median,
 count(*) FILTER(WHERE f.is_revenue_over_budget=1)::numeric/nullif(count(*),0) AS pct_over_budget
FROM dds.fact_movie f JOIN dds.dim_movie m USING(movie_sk)
WHERE f.is_finance_valid=1
GROUP BY m.budget_band ORDER BY m.budget_band'''),
'Q5SQL':('Q5 Hãng lợi nhuận Weighted vs Full (không nhân đôi hợp tác)', '''
WITH groups AS (
 SELECT c.company_name,count(DISTINCT f.movie_sk) AS valid_movies,
 sum(f.profit*bg.weight_factor) AS weighted_profit,sum(f.profit) AS full_profit
 FROM dds.fact_movie f JOIN dds.bridge_movie_company bg USING(movie_sk)
 JOIN dds.dim_company c USING(company_sk)
 WHERE f.is_finance_valid=1 GROUP BY c.company_name
)
SELECT * FROM groups WHERE valid_movies>=5 ORDER BY weighted_profit DESC NULLS LAST,company_name LIMIT 20'''),
'Q6SQL':('Q6 Profit/ROI theo tháng và thập niên', '''
SELECT d.decade,d.month,d.month_name,count(*) AS valid_movies,
 sum(f.profit) AS total_profit,
 percentile_cont(0.5) WITHIN GROUP(ORDER BY f.roi::float8) AS median_roi
FROM dds.fact_movie f JOIN dds.dim_date d USING(date_sk)
WHERE f.is_finance_valid=1 AND d.month IS NOT NULL
GROUP BY d.decade,d.month,d.month_name
ORDER BY d.decade,d.month'''),
'Q7SQL':('Q7 Quốc gia / single-multi / English-non-English', '''
SELECT c.country_name,m.country_type,l.language_group,
 count(DISTINCT f.movie_sk) AS valid_movies,
 percentile_cont(0.5) WITHIN GROUP(ORDER BY f.roi::float8) AS roi_median
FROM dds.fact_movie f JOIN dds.dim_movie m USING(movie_sk)
JOIN dds.dim_language l USING(language_sk)
JOIN dds.bridge_movie_country bc USING(movie_sk)
JOIN dds.dim_country c USING(country_sk)
WHERE f.is_finance_valid=1
GROUP BY c.country_name,m.country_type,l.language_group
ORDER BY c.country_name,m.country_type,l.language_group'''),
'Q8SQL':('Q8 Theme sequel/adaptation/superhero, chống trùng một phim nhiều keyword', '''
WITH movies AS (
 SELECT DISTINCT k.theme_group,f.movie_sk,f.profit,f.roi,f.is_finance_valid
 FROM dds.bridge_movie_keyword b JOIN dds.dim_keyword k USING(keyword_sk)
 JOIN dds.fact_movie f USING(movie_sk)
 WHERE k.theme_group IN ('Sequel','Adaptation','Superhero')
)
SELECT theme_group,count(DISTINCT movie_sk) AS movies,
 count(DISTINCT movie_sk) FILTER(WHERE is_finance_valid=1) AS valid_movies,
 sum(profit) FILTER(WHERE is_finance_valid=1) AS total_profit,
 percentile_cont(0.5) WITHIN GROUP(ORDER BY roi::float8) FILTER(WHERE is_finance_valid=1) AS median_roi
FROM movies GROUP BY theme_group ORDER BY theme_group'''),
}

for id,(name,sql) in QUERIES.items():
 register(id,'3.4',name,'SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI',
 category='Quy tắc project',steps='SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng',
 input_data='Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh',demo=id in ('BI01','BI02','BI05','Q5SQL'))

EXTRA={
'BI07':('Q2 bổ sung: popularity/rating theo genre và language', '''
SELECT l.language_name,g.genre_name,count(DISTINCT f.movie_sk) AS rated_movies,
 percentile_cont(0.5) WITHIN GROUP(ORDER BY f.popularity::float8) AS median_popularity,
 percentile_cont(0.5) WITHIN GROUP(ORDER BY f.vote_average::float8) AS median_rating
FROM dds.fact_movie f JOIN dds.dim_language l USING(language_sk)
JOIN dds.bridge_movie_genre bg USING(movie_sk) JOIN dds.dim_genre g USING(genre_sk)
WHERE f.vote_count>=100 AND f.vote_average IS NOT NULL
GROUP BY l.language_name,g.genre_name ORDER BY l.language_name,g.genre_name'''),
'BI08':('Q4 bổ sung: budget-revenue từng phim hợp lệ để đối chiếu scatter', '''
SELECT m.movie_nk,m.title,m.budget_band,f.budget,f.revenue,f.profit,f.roi
FROM dds.fact_movie f JOIN dds.dim_movie m USING(movie_sk)
WHERE f.is_finance_valid=1
ORDER BY f.budget,m.movie_nk LIMIT 50'''),
'BI09':('Q5 bổ sung: revenue/ROI của hãng Weighted và Full', '''
SELECT c.company_name,count(DISTINCT f.movie_sk) AS valid_movies,
 sum(f.revenue*b.weight_factor) AS weighted_revenue,
 sum(f.revenue) AS full_revenue,
 percentile_cont(0.5) WITHIN GROUP(ORDER BY f.roi::float8) AS roi_median
FROM dds.fact_movie f JOIN dds.bridge_movie_company b USING(movie_sk)
JOIN dds.dim_company c USING(company_sk)
WHERE f.is_finance_valid=1
GROUP BY c.company_name HAVING count(DISTINCT f.movie_sk)>=5
ORDER BY weighted_revenue DESC NULLS LAST,c.company_name LIMIT 20'''),
'BI10':('Ngưỡng Min Votes 100 và 1000 theo LanguageGroup', '''
SELECT l.language_group,
 count(DISTINCT f.movie_sk) FILTER(WHERE f.vote_count>=100 AND f.vote_average IS NOT NULL) AS movies_votes_100,
 count(DISTINCT f.movie_sk) FILTER(WHERE f.vote_count>=1000 AND f.vote_average IS NOT NULL) AS movies_votes_1000,
 count(DISTINCT f.movie_sk) FILTER(WHERE f.vote_count>=1000 AND f.vote_average IS NOT NULL AND f.is_finance_valid=1) AS valid_movies_votes_1000
FROM dds.fact_movie f JOIN dds.dim_language l USING(language_sk)
GROUP BY l.language_group ORDER BY l.language_group'''),
}
for id,(name,sql) in EXTRA.items():
 QUERIES[id]=(name,sql)
 register(id,'3.4',name,'SQL độc lập tính được giá trị tham chiếu cho UI; chưa chứng minh DAX đúng',
 category='Quy tắc project',input_data='Read-only dds (current snapshot)',
 steps='SELECT theo filter; ghi đầy đủ kết quả vào queries/<ID>.json',demo=id=='BI10')

# A SELECT producing rows is reference evidence, not a passed DAX comparison.
from core import CASES
for case_id in QUERIES:
 CASES[case_id]['observation']=True
