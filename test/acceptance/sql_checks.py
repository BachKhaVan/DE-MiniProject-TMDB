"""Independent, read-only violation queries against the *current* dds snapshot."""
from core import register

SQL={}
def add(id,title,query,*,section='3.3',category='Yêu cầu bắt buộc',demo=False,fix=None):
    SQL[id]=query
    register(id,section,title,'Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)',
             category=category,steps='Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự',
             input_data='PostgreSQL warehouse.dds (snapshot hiện tại)', demo=demo,fix=fix)

TABLES=['fact_movie','dim_movie','dim_date','dim_language','dim_genre','dim_company','dim_country','dim_keyword',
        'bridge_movie_genre','bridge_movie_company','bridge_movie_country','bridge_movie_keyword']
_EXPECTED_TABLES=','.join("('%s')"%t for t in TABLES)
add('DW01','Có đúng 12 bảng fact/dim/bridge',f"""
WITH exp(tbl) AS (VALUES {_EXPECTED_TABLES}), actual AS
 (SELECT table_name AS tbl FROM information_schema.tables WHERE table_schema='dds' AND table_type='BASE TABLE'
 AND (left(table_name,5)='fact_' OR left(table_name,4)='dim_' OR left(table_name,7)='bridge_'))
SELECT 'missing' AS problem, e.tbl FROM exp e LEFT JOIN actual a USING(tbl) WHERE a.tbl IS NULL
UNION ALL SELECT 'unexpected',a.tbl FROM actual a LEFT JOIN exp e USING(tbl) WHERE e.tbl IS NULL""",demo=True)
add('DW02','12 bảng có khóa chính vật lý',f"""
WITH exp(tbl) AS (VALUES {_EXPECTED_TABLES})
SELECT 'missing_primary_key' AS problem,e.tbl FROM exp e
WHERE NOT EXISTS (SELECT 1 FROM pg_constraint c JOIN pg_class t ON t.oid=c.conrelid
 JOIN pg_namespace n ON n.oid=t.relnamespace
 WHERE n.nspname='dds' AND t.relname=e.tbl AND c.contype='p')""")
_NAT=[('dim_movie','movie_nk'),('dim_language','language_nk'),('dim_genre','genre_nk'),('dim_company','company_nk'),('dim_country','country_code'),('dim_keyword','keyword_nk')]
_v=','.join("('%s','%s')"%x for x in _NAT)
add('DW03','UNIQUE vật lý cho các natural key',f"""
WITH exp(tbl,col) AS (VALUES {_v})
SELECT e.tbl,e.col FROM exp e WHERE NOT EXISTS (
 SELECT 1 FROM pg_constraint c JOIN pg_class t ON t.oid=c.conrelid
 JOIN pg_namespace n ON n.oid=t.relnamespace
 JOIN pg_attribute a ON a.attrelid=t.oid AND a.attname=e.col
 WHERE n.nspname='dds' AND t.relname=e.tbl AND c.contype IN ('u','p') AND a.attnum=ANY(c.conkey) AND array_length(c.conkey,1)=1)""")
_fks=[('fact_movie','movie_sk','dim_movie'),('fact_movie','date_sk','dim_date'),('fact_movie','language_sk','dim_language')]
for t,foreign in [('bridge_movie_genre','dim_genre'),('bridge_movie_company','dim_company'),('bridge_movie_country','dim_country'),('bridge_movie_keyword','dim_keyword')]:
    _fks +=[(t,'movie_sk','dim_movie'),(t,foreign.removeprefix('dim_')+'_sk',foreign)]
_v=','.join("('%s','%s','%s')"%x for x in _fks)
add('DW04','11 FK vật lý trỏ đúng bảng cha (confrelid)',f"""
WITH exp(tbl,col,parent) AS (VALUES {_v})
SELECT e.tbl,e.col,e.parent FROM exp e WHERE NOT EXISTS (
 SELECT 1 FROM pg_constraint c JOIN pg_class child ON child.oid=c.conrelid
 JOIN pg_namespace n ON n.oid=child.relnamespace
 JOIN pg_class parent ON parent.oid=c.confrelid
 JOIN pg_namespace pn ON pn.oid=parent.relnamespace
 JOIN pg_attribute a ON a.attrelid=child.oid AND a.attname=e.col
 WHERE c.contype='f' AND n.nspname='dds' AND pn.nspname='dds'
 AND child.relname=e.tbl AND parent.relname=e.parent AND a.attnum=ANY(c.conkey)
 AND c.convalidated AND array_length(c.conkey,1)=1 AND array_length(c.confkey,1)=1
 AND EXISTS (SELECT 1 FROM pg_attribute pa WHERE pa.attrelid=parent.oid
             AND pa.attnum=c.confkey[1] AND pa.attname=e.col))""")
add('DW05','Grain Fact = dim_movie = số movie_sk distinct',"""
SELECT (SELECT count(*) FROM dds.fact_movie) AS fact_rows,
 (SELECT count(DISTINCT movie_sk) FROM dds.fact_movie) AS fact_distinct,
 (SELECT count(*) FROM dds.dim_movie) AS dim_rows
WHERE (SELECT count(*) FROM dds.fact_movie)<>(SELECT count(*) FROM dds.dim_movie)
 OR (SELECT count(*) FROM dds.fact_movie)<>(SELECT count(DISTINCT movie_sk) FROM dds.fact_movie)
""",demo=True)
add('DW06','fact_movie không có movie_sk trùng',"SELECT movie_sk,count(*) AS copies FROM dds.fact_movie GROUP BY movie_sk HAVING count(*)>1")
add('DW07','Fact SK và cờ không NULL',"""SELECT movie_sk,date_sk,language_sk FROM dds.fact_movie
 WHERE movie_sk IS NULL OR date_sk IS NULL OR language_sk IS NULL OR vote_count IS NULL
 OR is_finance_valid IS NULL OR is_revenue_over_budget IS NULL OR movie_count IS NULL""")
add('DW08','Fact → dim_movie 1:1 logic',"""SELECT f.movie_sk FROM dds.fact_movie f LEFT JOIN dds.dim_movie d ON f.movie_sk=d.movie_sk
 WHERE d.movie_sk IS NULL UNION ALL SELECT d.movie_sk FROM dds.dim_movie d LEFT JOIN dds.fact_movie f ON f.movie_sk=d.movie_sk WHERE f.movie_sk IS NULL""")
add('DW09','Fact không có FK logic mồ côi',"""SELECT f.movie_sk,f.date_sk,f.language_sk FROM dds.fact_movie f
 LEFT JOIN dds.dim_date d ON f.date_sk=d.date_sk
 LEFT JOIN dds.dim_language l ON f.language_sk=l.language_sk
 LEFT JOIN dds.dim_movie m ON f.movie_sk=m.movie_sk
 WHERE d.date_sk IS NULL OR l.language_sk IS NULL OR m.movie_sk IS NULL""",demo=True)
for i,(t,entity) in enumerate([('bridge_movie_genre','genre'),('bridge_movie_company','company'),('bridge_movie_country','country'),('bridge_movie_keyword','keyword')],10):
    fk=entity+'_sk'
    add(f'DW{i:02}','Bridge '+entity+' không có orphan',f"""SELECT b.movie_sk,b.{fk} FROM dds.{t} b
      LEFT JOIN dds.dim_movie m ON m.movie_sk=b.movie_sk
      LEFT JOIN dds.dim_{entity} d ON d.{fk}=b.{fk}
      WHERE b.movie_sk IS NULL OR b.{fk} IS NULL OR m.movie_sk IS NULL OR d.{fk} IS NULL""")
for i,(t,entity) in enumerate([('bridge_movie_genre','genre'),('bridge_movie_company','company'),('bridge_movie_country','country'),('bridge_movie_keyword','keyword')],14):
    fk=entity+'_sk'
    add(f'DW{i:02}','Bridge '+entity+' không trùng cặp khóa',f"""SELECT movie_sk,{fk},count(*) AS copies
    FROM dds.{t} GROUP BY movie_sk,{fk} HAVING count(*)>1""")
for i,(t,entity) in enumerate([('bridge_movie_genre','genre'),('bridge_movie_company','company'),('bridge_movie_country','country')],18):
    add(f'DW{i:02}','Bridge '+entity+' weight_factor dương, sum=1',f"""
    SELECT movie_sk,count(*) AS links,sum(weight_factor) AS total_weight
    FROM dds.{t} GROUP BY movie_sk
    HAVING count(*) FILTER(WHERE weight_factor IS NULL OR weight_factor<=0)>0
       OR abs(sum(weight_factor)-1)>0.0000001 OR sum(weight_factor) IS NULL""",demo=True)
add('DW21','Keyword bridge không có cột weight_factor',"""
SELECT column_name FROM information_schema.columns
WHERE table_schema='dds' AND table_name='bridge_movie_keyword' AND column_name='weight_factor'""")
_dims=[('dim_date','date_sk'),('dim_language','language_sk'),('dim_genre','genre_sk'),('dim_company','company_sk'),('dim_country','country_sk'),('dim_keyword','keyword_sk')]
_v=' UNION ALL '.join(f"SELECT '{table}' AS table_name, count(*) AS n FROM dds.{table} WHERE {sk}=-1" for table,sk in _dims)
add('DW22','6 dimension (trừ dim_movie) có đúng 1 Unknown SK=-1',f"SELECT * FROM ({_v}) v WHERE n<>1")
add('DW23','Các bridge genre/company/country bao phủ mọi phim',"""
SELECT 'genre' AS bridge,m.movie_sk FROM dds.dim_movie m LEFT JOIN dds.bridge_movie_genre b ON b.movie_sk=m.movie_sk WHERE b.movie_sk IS NULL
UNION ALL SELECT 'company',m.movie_sk FROM dds.dim_movie m LEFT JOIN dds.bridge_movie_company b ON b.movie_sk=m.movie_sk WHERE b.movie_sk IS NULL
UNION ALL SELECT 'country',m.movie_sk FROM dds.dim_movie m LEFT JOIN dds.bridge_movie_country b ON b.movie_sk=m.movie_sk WHERE b.movie_sk IS NULL""")
add('DW24','dim_date có đủ chuỗi ngày liên tục (trừ Unknown)',"""
WITH bounds AS (SELECT min(full_date) AS lo,max(full_date) AS hi FROM dds.dim_date WHERE date_sk<>-1),
actual AS (SELECT count(*) AS n,count(DISTINCT full_date) AS uniq FROM dds.dim_date WHERE date_sk<>-1)
SELECT lo,hi,n,uniq FROM bounds CROSS JOIN actual
WHERE lo IS NULL OR hi IS NULL OR n <> (hi-lo+1) OR uniq<>n""")
add('DW25','dim_date month_name English, decade dạng 1980s','''
SELECT date_sk,full_date,month_name,decade FROM dds.dim_date
WHERE date_sk<>-1 AND (month_name IS NULL OR month_name NOT IN
 ('January','February','March','April','May','June','July','August','September','October','November','December')
 OR decade IS NULL OR decade <> ((floor(extract(year FROM full_date)/10)*10)::integer::text || 's'))''')
add('DW26','Fact profit=revenue-budget; ROI thập phân',"""
SELECT movie_sk,budget,revenue,profit,roi FROM dds.fact_movie
WHERE (budget IS NULL OR revenue IS NULL) AND (profit IS NOT NULL OR roi IS NOT NULL)
 OR (budget IS NOT NULL AND revenue IS NOT NULL AND (profit IS DISTINCT FROM revenue-budget
 OR (budget>0 AND (roi IS NULL OR abs(roi-(revenue-budget)/budget)>0.00011))
 OR (budget<=0 AND roi IS NOT NULL)))""",demo=True)
add('DW27','Cờ is_finance_valid và is_revenue_over_budget đúng','''
SELECT movie_sk,budget,revenue,is_finance_valid,is_revenue_over_budget FROM dds.fact_movie
WHERE is_finance_valid IS DISTINCT FROM (CASE WHEN budget>0 AND revenue>0 THEN 1 ELSE 0 END)
OR is_revenue_over_budget IS DISTINCT FROM (CASE WHEN budget>0 AND revenue>0 AND revenue>budget THEN 1 ELSE 0 END)''')
add('DW28','Fact vote_count mặc định 0 và NOT NULL',"""
SELECT table_name,column_name,is_nullable,column_default FROM information_schema.columns
WHERE table_schema='dds' AND table_name='fact_movie' AND column_name='vote_count'
AND (is_nullable<>'NO' OR column_default IS NULL OR column_default NOT IN ('0','0::integer'))
UNION ALL SELECT 'fact_movie','vote_count','missing','missing' WHERE NOT EXISTS
(SELECT 1 FROM information_schema.columns WHERE table_schema='dds' AND table_name='fact_movie' AND column_name='vote_count')""",demo=True)
add('DW29','Fact movie_count luôn bằng 1',"SELECT movie_sk,movie_count FROM dds.fact_movie WHERE movie_count IS DISTINCT FROM 1")
add('DW30','Votes không dương thì vote_average NULL',"SELECT movie_sk,vote_count,vote_average FROM dds.fact_movie WHERE coalesce(vote_count,0)<=0 AND vote_average IS NOT NULL")
add('DW31','Profit không âm/âm đều được, không loại phim không hợp lệ',"""
SELECT movie_sk FROM dds.fact_movie WHERE is_finance_valid=0 AND (profit IS NOT NULL OR roi IS NOT NULL)""",category='Kiểm tra độ bền')
add('DW32','Staging chuẩn hóa budget/revenue 0 thành NULL',"""
SELECT movie_nk,budget,revenue FROM staging.stg_tmdb_movies WHERE budget=0 OR revenue=0""",section='3.2')
add('DW33','Staging chuẩn hóa vote_average khi vote_count<=0',"""
SELECT movie_nk,vote_average,vote_count FROM staging.stg_tmdb_movies WHERE coalesce(vote_count,0)<=0 AND vote_average IS NOT NULL""",section='3.2')
add('DW34','Staging phim có natural key/title và không trùng phim',"""
SELECT movie_nk,count(*) AS n FROM staging.stg_tmdb_movies GROUP BY movie_nk
HAVING movie_nk IS NULL OR count(*)>1 OR count(*) FILTER(WHERE title IS NULL OR btrim(title)='')>0""",section='3.2')
add('DW35','Language fallback giữ mã và Unknown hợp lệ',"""
SELECT language_sk,language_nk,language_name FROM dds.dim_language
WHERE language_nk IS NULL OR language_name IS NULL OR btrim(language_name)=''""",section='3.2')
add('DW36','Country region không được NULL khi chưa map',"""
SELECT country_sk,country_code,region FROM dds.dim_country WHERE region IS NULL OR btrim(region)=''""",section='3.2')
add('DW37','Keyword theme_group không được NULL',"SELECT keyword_sk,keyword_nk,theme_group FROM dds.dim_keyword WHERE theme_group IS NULL OR btrim(theme_group)=''",section='3.2')
add('DW38','Fact không có finance-valid khi budget/revenue NULL',"""
SELECT movie_sk,budget,revenue,is_finance_valid FROM dds.fact_movie
WHERE (budget IS NULL OR revenue IS NULL) AND is_finance_valid<>0""",section='3.2')
add('DW39','Weighted profit across each bridge = fact profit for covered movies',"""
SELECT bridge_type, sum_allocated, sum_fact FROM (
 SELECT 'genre' AS bridge_type,
 (SELECT sum(b.weight_factor*f.profit) FROM dds.bridge_movie_genre b JOIN dds.fact_movie f USING(movie_sk) WHERE f.is_finance_valid=1) AS sum_allocated,
 (SELECT sum(f.profit) FROM dds.fact_movie f JOIN (SELECT DISTINCT movie_sk FROM dds.bridge_movie_genre) b USING(movie_sk) WHERE f.is_finance_valid=1) AS sum_fact
 UNION ALL SELECT 'company',
 (SELECT sum(b.weight_factor*f.profit) FROM dds.bridge_movie_company b JOIN dds.fact_movie f USING(movie_sk) WHERE f.is_finance_valid=1),
 (SELECT sum(f.profit) FROM dds.fact_movie f JOIN (SELECT DISTINCT movie_sk FROM dds.bridge_movie_company) b USING(movie_sk) WHERE f.is_finance_valid=1)
 UNION ALL SELECT 'country',
 (SELECT sum(b.weight_factor*f.profit) FROM dds.bridge_movie_country b JOIN dds.fact_movie f USING(movie_sk) WHERE f.is_finance_valid=1),
 (SELECT sum(f.profit) FROM dds.fact_movie f JOIN (SELECT DISTINCT movie_sk FROM dds.bridge_movie_country) b USING(movie_sk) WHERE f.is_finance_valid=1)
 ) a WHERE sum_allocated IS NULL OR sum_fact IS NULL OR abs(sum_allocated-sum_fact)>1""",demo=True)
add('DW40','Vote-count, ROI và finance được dùng nhất quán khi tổng hợp',"""
SELECT count(*) AS n FROM dds.fact_movie
WHERE (is_revenue_over_budget=1 AND is_finance_valid<>1) OR
 (is_finance_valid=1 AND (profit IS NULL OR roi IS NULL))
HAVING count(*)>0""",category='Kiểm tra độ bền')

add('DW41','Country region chính xác theo seed, fallback Unknown',"""
SELECT c.country_sk,c.country_code,c.region,r.region AS mapping_region
FROM dds.dim_country c LEFT JOIN dds.country_region r
 ON upper(c.country_code)=upper(r.country_code)
WHERE c.region IS DISTINCT FROM coalesce(r.region,'Unknown')""",section='3.2',demo=True)
add('DW42','Keyword theme chính xác theo seed, fallback Other',"""
SELECT k.keyword_sk,k.keyword_nk,k.keyword_name,k.theme_group,m.theme_group AS mapping_theme
FROM dds.dim_keyword k LEFT JOIN dds.keyword_theme_mapping m
 ON lower(k.keyword_name)=lower(m.keyword_name)
WHERE k.theme_group IS DISTINCT FROM coalesce(m.theme_group,'Other')""",section='3.2')
add('DW43','Language label fallback giữ code khi không có tên',"""
SELECT l.language_sk,l.language_nk,l.language_name,m.language_name AS mapping_name
FROM dds.dim_language l LEFT JOIN dds.language_name_mapping m
 ON lower(l.language_nk)=lower(m.language_nk)
WHERE l.language_sk<>-1
AND (l.language_name IS DISTINCT FROM coalesce(m.language_name,l.language_nk)
OR l.language_group IS DISTINCT FROM CASE WHEN lower(l.language_nk)='en' THEN 'English' ELSE 'Non-English' END)""",section='3.2')
add('DW44','RuntimeBand trong dim_movie đúng theo staging',"""
SELECT d.movie_nk,d.runtime_band,s.runtime FROM dds.dim_movie d
JOIN staging.stg_tmdb_movies s USING(movie_nk)
WHERE d.runtime_band IS DISTINCT FROM (CASE
WHEN s.runtime IS NULL THEN 'Không rõ'
WHEN s.runtime<90 THEN 'Dưới 90 phút'
WHEN s.runtime<120 THEN '90–119 phút'
WHEN s.runtime<150 THEN '120–149 phút'
ELSE 'Từ 150 phút trở lên' END)""",section='3.2')
add('DW45','BudgetBand trong dim_movie đúng theo staging',"""
SELECT d.movie_nk,d.budget_band,s.budget FROM dds.dim_movie d
JOIN staging.stg_tmdb_movies s USING(movie_nk)
WHERE d.budget_band IS DISTINCT FROM (CASE
WHEN s.budget IS NULL THEN 'Không rõ'
WHEN s.budget<1000000 THEN 'Dưới 1 triệu USD'
WHEN s.budget<10000000 THEN '1–10 triệu'
WHEN s.budget<50000000 THEN '10–50 triệu'
WHEN s.budget<100000000 THEN '50–100 triệu'
ELSE 'Từ 100 triệu trở lên' END)""",section='3.2')
add('DW46','CountryType và country_count từ quan hệ stage',"""
WITH counts AS (
 SELECT movie_nk,count(DISTINCT country_code) AS n FROM staging.stg_movie_countries
 WHERE country_code<>'unk' GROUP BY movie_nk
)
SELECT d.movie_nk,d.country_count,d.country_type,coalesce(c.n,0) AS expected_count
FROM dds.dim_movie d LEFT JOIN counts c USING(movie_nk)
WHERE d.country_count IS DISTINCT FROM coalesce(c.n,0)
 OR d.country_type IS DISTINCT FROM CASE WHEN coalesce(c.n,0)=0 THEN 'Unknown'
 WHEN c.n=1 THEN 'Single-country' ELSE 'Multi-country' END""",section='3.2')
add('DW47','Bridge genre phải có đúng weight_factor = 1/k mỗi link',"""
WITH weights AS (SELECT movie_sk,genre_sk,weight_factor,
 count(*) OVER(PARTITION BY movie_sk) AS k FROM dds.bridge_movie_genre)
SELECT movie_sk,genre_sk,weight_factor,k FROM weights
WHERE weight_factor IS NULL OR abs(weight_factor-1.0/k)>0.0000001""",section='3.3')
add('DW48','Bridge company phải có đúng weight_factor = 1/k mỗi link',"""
WITH weights AS (SELECT movie_sk,company_sk,weight_factor,
 count(*) OVER(PARTITION BY movie_sk) AS k FROM dds.bridge_movie_company)
SELECT movie_sk,company_sk,weight_factor,k FROM weights
WHERE weight_factor IS NULL OR abs(weight_factor-1.0/k)>0.0000001""",section='3.3')
add('DW49','Bridge country phải có đúng weight_factor = 1/k mỗi link',"""
WITH weights AS (SELECT movie_sk,country_sk,weight_factor,
 count(*) OVER(PARTITION BY movie_sk) AS k FROM dds.bridge_movie_country)
SELECT movie_sk,country_sk,weight_factor,k FROM weights
WHERE weight_factor IS NULL OR abs(weight_factor-1.0/k)>0.0000001""",section='3.3')

add('DW50','Stage, staging và Fact có dữ liệu để nghiệm thu',"""
SELECT 'stage_movies' AS relation WHERE NOT EXISTS (SELECT 1 FROM stage.stg_tmdb_movies)
UNION ALL SELECT 'staging_movies' WHERE NOT EXISTS (SELECT 1 FROM staging.stg_tmdb_movies)
UNION ALL SELECT 'fact_movie' WHERE NOT EXISTS (SELECT 1 FROM dds.fact_movie)""")

add('DW51','Không mất hoặc thêm Movie NK giữa staging và DDS',"""
SELECT 'missing_in_dds' AS problem,s.movie_nk FROM staging.stg_tmdb_movies s
LEFT JOIN dds.dim_movie m USING(movie_nk) WHERE m.movie_sk IS NULL
UNION ALL SELECT 'unexpected_in_dds',m.movie_nk FROM dds.dim_movie m
LEFT JOIN staging.stg_tmdb_movies s USING(movie_nk) WHERE s.movie_nk IS NULL""",section='3.2')

add('DW52','Measures của Fact khớp từng phim nguồn staging',"""
SELECT m.movie_nk FROM staging.stg_tmdb_movies s JOIN dds.dim_movie m USING(movie_nk)
JOIN dds.fact_movie f USING(movie_sk)
WHERE f.budget IS DISTINCT FROM s.budget::numeric(18,0)
 OR f.revenue IS DISTINCT FROM s.revenue::numeric(18,0)
 OR f.runtime IS DISTINCT FROM s.runtime::numeric(5,1)
 OR f.popularity IS DISTINCT FROM s.popularity::numeric(12,6)
 OR f.vote_average IS DISTINCT FROM s.vote_average::numeric(4,1)
 OR f.vote_count IS DISTINCT FROM coalesce(s.vote_count,0)""",section='3.2')

add('DW53','Fact liên kết đúng ngày và ngôn ngữ nguồn, kể cả Unknown',"""
SELECT m.movie_nk,f.date_sk,f.language_sk FROM staging.stg_tmdb_movies s
JOIN dds.dim_movie m USING(movie_nk) JOIN dds.fact_movie f USING(movie_sk)
LEFT JOIN dds.dim_date d ON d.date_sk=f.date_sk
LEFT JOIN dds.dim_language l ON l.language_sk=f.language_sk
WHERE d.full_date IS DISTINCT FROM s.release_date
 OR (s.release_date IS NULL AND f.date_sk<>-1)
 OR l.language_nk IS DISTINCT FROM coalesce(s.language_nk,'unk')""",section='3.2')

add('DW54','Các thành phần hierarchy Date đúng ngày thực',"""
SELECT date_sk,full_date FROM dds.dim_date WHERE date_sk<>-1 AND (
 full_date IS NULL OR date_sk IS DISTINCT FROM to_char(full_date,'YYYYMMDD')::integer
 OR day IS DISTINCT FROM extract(day FROM full_date)::integer
 OR month IS DISTINCT FROM extract(month FROM full_date)::integer
 OR quarter IS DISTINCT FROM extract(quarter FROM full_date)::integer
 OR year IS DISTINCT FROM extract(year FROM full_date)::integer
 OR month_name IS DISTINCT FROM (ARRAY['January','February','March','April','May','June',
 'July','August','September','October','November','December'])[extract(month FROM full_date)::integer])""")

for number,entity,nk in [(55,'genre','genre_nk'),(56,'company','company_nk'),
                          (57,'country','country_code'),(58,'keyword','keyword_nk')]:
    plural={'genre':'genres','company':'companies','country':'countries','keyword':'keywords'}[entity]
    add(f'DW{number}','Bridge '+entity+' giữ đúng tập liên kết nguồn (hai chiều)',f"""
    WITH expected AS (SELECT DISTINCT movie_nk,{nk} FROM staging.stg_movie_{plural}),
    actual AS (SELECT m.movie_nk,d.{nk} FROM dds.bridge_movie_{entity} b
       JOIN dds.dim_movie m USING(movie_sk) JOIN dds.dim_{entity} d USING({entity}_sk))
    SELECT 'missing' AS problem,* FROM (SELECT * FROM expected EXCEPT SELECT * FROM actual) a
    UNION ALL SELECT 'unexpected',* FROM (SELECT * FROM actual EXCEPT SELECT * FROM expected) b
    """,section='3.2')

add('DW59','dim_movie giữ đúng title/original_title/status nguồn',"""
SELECT s.movie_nk FROM staging.stg_tmdb_movies s JOIN dds.dim_movie m USING(movie_nk)
WHERE m.title IS DISTINCT FROM s.title
 OR m.original_title IS DISTINCT FROM s.original_title
 OR m.status IS DISTINCT FROM s.movie_status::varchar(50)""",section='3.2')
