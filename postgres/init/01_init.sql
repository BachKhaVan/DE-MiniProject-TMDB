CREATE SCHEMA IF NOT EXISTS stage;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS dds;
CREATE SCHEMA IF NOT EXISTS control;

CREATE TABLE IF NOT EXISTS control.etl_watermark (
    pipeline_name text PRIMARY KEY,
    lset timestamptz NOT NULL
);

INSERT INTO control.etl_watermark (pipeline_name, lset)
VALUES ('tmdb_incremental', TIMESTAMPTZ '2000-01-01 00:00:00+00')
ON CONFLICT (pipeline_name) DO NOTHING;
