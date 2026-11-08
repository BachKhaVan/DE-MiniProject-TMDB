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
        extract(day from full_date)::integer as day,
        extract(month from full_date)::integer as month,
        case extract(month from full_date)::integer
            when 1 then 'January'
            when 2 then 'February'
            when 3 then 'March'
            when 4 then 'April'
            when 5 then 'May'
            when 6 then 'June'
            when 7 then 'July'
            when 8 then 'August'
            when 9 then 'September'
            when 10 then 'October'
            when 11 then 'November'
            when 12 then 'December'
        end::varchar(20) as month_name,
        extract(quarter from full_date)::integer as quarter,
        extract(year from full_date)::integer as year,
        (to_char((floor(extract(year from full_date) / 10) * 10)::integer, 'FM9999') || 's')::varchar(10) as decade
    from calendar
)

select
    -1::integer as date_sk,
    null::date as full_date,
    null::integer as day,
    null::integer as month,
    'Unknown'::varchar(20) as month_name,
    null::integer as quarter,
    null::integer as year,
    'Unknown'::varchar(10) as decade

union all

select date_sk, full_date, day, month, month_name, quarter, year, decade
from known_dates
