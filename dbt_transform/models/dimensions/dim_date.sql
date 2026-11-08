with bounds as (
    select min(release_date) as min_date, max(release_date) as max_date
    from {{ ref('stg_tmdb_movies') }}
),

calendar as (
    select generated_date::date as full_date
    from bounds
    cross join lateral generate_series(
        min_date::timestamp,
        max_date::timestamp,
        interval '1 day'
    ) as dates(generated_date)
    where min_date is not null
      and max_date is not null
),

known_dates as (
    select
        to_char(full_date, 'YYYYMMDD')::integer as date_sk,
        full_date,
        extract(day from full_date)::smallint as day,
        extract(month from full_date)::smallint as month,
        to_char(full_date, 'FMMonth') as month_name,
        extract(quarter from full_date)::smallint as quarter,
        extract(year from full_date)::integer as year,
        (floor(extract(year from full_date) / 10) * 10)::integer as decade
    from calendar
)

select
    -1::integer as date_sk,
    null::date as full_date,
    null::smallint as day,
    null::smallint as month,
    'Unknown'::text as month_name,
    null::smallint as quarter,
    null::integer as year,
    null::integer as decade

union all

select date_sk, full_date, day, month, month_name, quarter, year, decade
from known_dates
