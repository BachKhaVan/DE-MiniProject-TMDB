CREATE TABLE IF NOT EXISTS dds.dim_date (
    date_sk integer PRIMARY KEY,
    full_date date,
    day integer,
    month integer,
    month_name varchar(20),
    quarter integer,
    year integer,
    decade varchar(10)
);

CREATE TABLE IF NOT EXISTS dds.dim_language (
    language_sk integer PRIMARY KEY,
    language_nk varchar(10) UNIQUE NOT NULL,
    language_name varchar(100),
    language_group varchar(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.dim_movie (
    movie_sk integer PRIMARY KEY,
    movie_nk integer UNIQUE NOT NULL,
    title text NOT NULL,
    original_title text,
    status varchar(50),
    runtime_band varchar(50),
    budget_band varchar(50),
    country_count integer,
    country_type varchar(50)
);

CREATE TABLE IF NOT EXISTS dds.dim_genre (
    genre_sk integer PRIMARY KEY,
    genre_nk integer UNIQUE NOT NULL,
    genre_name varchar(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.dim_company (
    company_sk integer PRIMARY KEY,
    company_nk integer UNIQUE NOT NULL,
    company_name varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.dim_country (
    country_sk integer PRIMARY KEY,
    country_code varchar(10) UNIQUE NOT NULL,
    country_name varchar(100) NOT NULL,
    region varchar(100)
);

CREATE TABLE IF NOT EXISTS dds.dim_keyword (
    keyword_sk integer PRIMARY KEY,
    keyword_nk integer UNIQUE NOT NULL,
    keyword_name varchar(255) NOT NULL,
    theme_group varchar(50) NOT NULL
);

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

CREATE TABLE IF NOT EXISTS dds.fact_movie (
    movie_sk integer PRIMARY KEY REFERENCES dds.dim_movie (movie_sk),
    date_sk integer NOT NULL REFERENCES dds.dim_date (date_sk),
    language_sk integer NOT NULL REFERENCES dds.dim_language (language_sk),
    budget decimal(18, 0),
    revenue decimal(18, 0),
    profit decimal(18, 0),
    roi decimal(18, 4),
    runtime numeric(5, 1),
    popularity decimal(12, 6),
    vote_average decimal(4, 1),
    vote_count integer NOT NULL DEFAULT 0,
    is_finance_valid integer NOT NULL,
    is_revenue_over_budget integer NOT NULL,
    movie_count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS dds.bridge_movie_genre (
    movie_sk integer NOT NULL REFERENCES dds.dim_movie (movie_sk),
    genre_sk integer NOT NULL REFERENCES dds.dim_genre (genre_sk),
    weight_factor decimal(18, 10) NOT NULL,
    PRIMARY KEY (movie_sk, genre_sk)
);

CREATE TABLE IF NOT EXISTS dds.bridge_movie_company (
    movie_sk integer NOT NULL REFERENCES dds.dim_movie (movie_sk),
    company_sk integer NOT NULL REFERENCES dds.dim_company (company_sk),
    weight_factor decimal(18, 10) NOT NULL,
    PRIMARY KEY (movie_sk, company_sk)
);

CREATE TABLE IF NOT EXISTS dds.bridge_movie_country (
    movie_sk integer NOT NULL REFERENCES dds.dim_movie (movie_sk),
    country_sk integer NOT NULL REFERENCES dds.dim_country (country_sk),
    weight_factor decimal(18, 10) NOT NULL,
    PRIMARY KEY (movie_sk, country_sk)
);

CREATE TABLE IF NOT EXISTS dds.bridge_movie_keyword (
    movie_sk integer NOT NULL REFERENCES dds.dim_movie (movie_sk),
    keyword_sk integer NOT NULL REFERENCES dds.dim_keyword (keyword_sk),
    PRIMARY KEY (movie_sk, keyword_sk)
);
