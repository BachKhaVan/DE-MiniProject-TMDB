-- =============================================================================
-- TMDB 5000 Data Warehouse - DDS Schema Definition (Reference DDL & Data Contract)
-- Phụ trách: Thịnh (Phần 3.3 – Data Warehouse)
-- Database Engine: PostgreSQL 17
-- Schema đích: dds
-- =============================================================================

CREATE SCHEMA IF NOT EXISTS dds;

-- -----------------------------------------------------------------------------
-- 1. DIMENSION TABLES (7 BẢNG CHIỀU ĐƠN TRỊ & ĐA TRỊ)
-- -----------------------------------------------------------------------------

-- 1.1 Chiều Thời gian phát hành (DimDate)
-- Phân cấp: Date -> Month -> Quarter -> Year -> Decade
CREATE TABLE IF NOT EXISTS dds.dim_date (
    date_sk integer PRIMARY KEY,                -- YYYYMMDD hoặc -1 (Unknown)
    full_date date,
    day integer,
    month integer,
    month_name varchar(20),
    quarter integer,
    year integer,
    decade varchar(10)                          -- VD: '1990s', '2000s', 'Unknown'
);

-- 1.2 Chiều Ngôn ngữ gốc (DimLanguage)
-- Phân cấp: LanguageName -> LanguageGroup ('English' / 'Non-English')
CREATE TABLE IF NOT EXISTS dds.dim_language (
    language_sk integer PRIMARY KEY,            -- Surrogate Key (-1 = Unknown)
    language_nk varchar(10) UNIQUE NOT NULL,    -- Mã ISO 639-1 (VD: 'en', 'fr', 'unk')
    language_name varchar(100),
    language_group varchar(20) NOT NULL         -- 'English' hoặc 'Non-English'
);

-- 1.3 Chiều Phim (DimMovie) - Quan hệ 1-1 với FactMovie & Điểm neo cho 4 Bridge
CREATE TABLE IF NOT EXISTS dds.dim_movie (
    movie_sk integer PRIMARY KEY,               -- Surrogate Key
    movie_nk integer UNIQUE NOT NULL,           -- ID nguồn TMDB (tmdb_5000_movies.id)
    title text NOT NULL,
    original_title text,
    status varchar(50),
    runtime_band varchar(50),                   -- Nhóm thời lượng (Câu 1)
    budget_band varchar(50),                    -- Nhóm ngân sách (Câu 4)
    country_count integer,                      -- Số quốc gia tham gia sản xuất
    country_type varchar(50)                    -- 'Single-country', 'Multi-country', 'Unknown' (Câu 7)
);

-- 1.4 Chiều Thể loại (DimGenre) - Chiều đa trị
CREATE TABLE IF NOT EXISTS dds.dim_genre (
    genre_sk integer PRIMARY KEY,               -- Surrogate Key (-1 = Unknown)
    genre_nk integer UNIQUE NOT NULL,           -- ID thể loại TMDB (0 = Unknown)
    genre_name varchar(100) NOT NULL
);

-- 1.5 Chiều Hãng sản xuất (DimCompany) - Chiều đa trị
CREATE TABLE IF NOT EXISTS dds.dim_company (
    company_sk integer PRIMARY KEY,             -- Surrogate Key (-1 = Unknown)
    company_nk integer UNIQUE NOT NULL,         -- ID hãng sản xuất TMDB (0 = Unknown)
    company_name varchar(255) NOT NULL
);

-- 1.6 Chiều Quốc gia sản xuất (DimCountry) - Chiều đa trị
-- Phân cấp: CountryName -> Region
CREATE TABLE IF NOT EXISTS dds.dim_country (
    country_sk integer PRIMARY KEY,             -- Surrogate Key (-1 = Unknown)
    country_code varchar(10) UNIQUE NOT NULL,   -- Mã ISO 3166-1 (VD: 'US', 'GB', 'unk')
    country_name varchar(100) NOT NULL,
    region varchar(100)                         -- Khu vực địa lý / Châu lục
);

-- 1.7 Chiều Từ khóa chủ đề (DimKeyword) - Chiều đa trị
-- Phân cấp: KeywordName -> ThemeGroup ('Sequel', 'Adaptation', 'Superhero', 'Other')
CREATE TABLE IF NOT EXISTS dds.dim_keyword (
    keyword_sk integer PRIMARY KEY,             -- Surrogate Key (-1 = Unknown)
    keyword_nk integer UNIQUE NOT NULL,         -- ID từ khóa TMDB (0 = Unknown)
    keyword_name varchar(255) NOT NULL,
    theme_group varchar(50) NOT NULL
);

-- -----------------------------------------------------------------------------
-- 2. DEFAULT UNKNOWN RECORDS (SK = -1) ĐẢM BẢO TOÀN VẸN THAM CHIẾU
-- -----------------------------------------------------------------------------

INSERT INTO dds.dim_date (
    date_sk, full_date, day, month, month_name, quarter, year, decade
)
VALUES (-1, NULL, NULL, NULL, 'Unknown', NULL, NULL, 'Unknown')
ON CONFLICT (date_sk) DO NOTHING;

INSERT INTO dds.dim_language (
    language_sk, language_nk, language_name, language_group
)
VALUES (-1, 'unk', 'Unknown', 'Non-English')
ON CONFLICT (language_sk) DO NOTHING;

INSERT INTO dds.dim_genre (genre_sk, genre_nk, genre_name)
VALUES (-1, 0, 'Unknown')
ON CONFLICT (genre_sk) DO NOTHING;

INSERT INTO dds.dim_company (company_sk, company_nk, company_name)
VALUES (-1, 0, 'Unknown')
ON CONFLICT (company_sk) DO NOTHING;

INSERT INTO dds.dim_country (country_sk, country_code, country_name, region)
VALUES (-1, 'unk', 'Unknown', 'Unknown')
ON CONFLICT (country_sk) DO NOTHING;

INSERT INTO dds.dim_keyword (keyword_sk, keyword_nk, keyword_name, theme_group)
VALUES (-1, 0, 'Unknown', 'Other')
ON CONFLICT (keyword_sk) DO NOTHING;

-- -----------------------------------------------------------------------------
-- 3. FACT TABLE (BẢNG DỮ KIỆN TRUNG TÂM - GRAIN: 1 DÒNG / 1 BỘ PHIM)
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS dds.fact_movie (
    movie_sk integer PRIMARY KEY REFERENCES dds.dim_movie (movie_sk),
    date_sk integer NOT NULL REFERENCES dds.dim_date (date_sk),
    language_sk integer NOT NULL REFERENCES dds.dim_language (language_sk),
    budget decimal(18, 0),                      -- Ngân sách (USD); nguồn = 0 -> NULL
    revenue decimal(18, 0),                     -- Doanh thu (USD); nguồn = 0 -> NULL
    profit decimal(18, 0),                      -- revenue - budget; NULL nếu thiếu 1 trong 2
    roi decimal(18, 4),                         -- profit / budget; NULL nếu budget NULL hoặc <= 0
    runtime numeric(5, 1),                      -- Thời lượng (phút)
    popularity decimal(12, 6),                  -- Chỉ số độ phổ biến TMDB
    vote_average decimal(4, 1),                 -- Điểm đánh giá TB; NULL nếu vote_count = 0
    vote_count integer NOT NULL DEFAULT 0,      -- Tổng số lượt bình chọn
    is_finance_valid integer NOT NULL,          -- 1 nếu budget > 0 và revenue > 0; ngược lại 0
    is_revenue_over_budget integer NOT NULL,    -- 1 nếu is_finance_valid = 1 và revenue > budget; ngược lại 0
    movie_count integer NOT NULL DEFAULT 1      -- Cờ đếm phim (luôn bằng 1)
);

-- -----------------------------------------------------------------------------
-- 4. BRIDGE TABLES (XỬ LÝ QUAN HỆ NHIỀU - NHIỀU GIỮA PHIM VÀ CHIỀU ĐA TRỊ)
-- -----------------------------------------------------------------------------

-- 4.1 Cầu nối Phim - Thể loại (Có trọng số phân bổ WeightFactor = 1/k)
CREATE TABLE IF NOT EXISTS dds.bridge_movie_genre (
    movie_sk integer NOT NULL REFERENCES dds.dim_movie (movie_sk),
    genre_sk integer NOT NULL REFERENCES dds.dim_genre (genre_sk),
    weight_factor decimal(18, 10) NOT NULL,
    PRIMARY KEY (movie_sk, genre_sk)
);

-- 4.2 Cầu nối Phim - Hãng sản xuất (Có trọng số phân bổ WeightFactor = 1/k)
CREATE TABLE IF NOT EXISTS dds.bridge_movie_company (
    movie_sk integer NOT NULL REFERENCES dds.dim_movie (movie_sk),
    company_sk integer NOT NULL REFERENCES dds.dim_company (company_sk),
    weight_factor decimal(18, 10) NOT NULL,
    PRIMARY KEY (movie_sk, company_sk)
);

-- 4.3 Cầu nối Phim - Quốc gia sản xuất (Có trọng số phân bổ WeightFactor = 1/k)
CREATE TABLE IF NOT EXISTS dds.bridge_movie_country (
    movie_sk integer NOT NULL REFERENCES dds.dim_movie (movie_sk),
    country_sk integer NOT NULL REFERENCES dds.dim_country (country_sk),
    weight_factor decimal(18, 10) NOT NULL,
    PRIMARY KEY (movie_sk, country_sk)
);

-- 4.4 Cầu nối Phim - Từ khóa (Tagging N-N, KHÔNG có WeightFactor theo thiết kế)
CREATE TABLE IF NOT EXISTS dds.bridge_movie_keyword (
    movie_sk integer NOT NULL REFERENCES dds.dim_movie (movie_sk),
    keyword_sk integer NOT NULL REFERENCES dds.dim_keyword (keyword_sk),
    PRIMARY KEY (movie_sk, keyword_sk)
);
