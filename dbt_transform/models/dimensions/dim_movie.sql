with country_counts as (
    select movie_nk, count(distinct country_code)::integer as country_count
    from {{ ref('stg_movie_countries') }}
    group by movie_nk
)

select
    md5('movie:' || m.movie_nk::text) as movie_sk,
    m.movie_nk as movie_nk,
    m.title,
    m.original_title,
    m.movie_status,
    case
        when m.runtime is null then 'Unknown'
        when m.runtime < 90 then 'Under 90 minutes'
        when m.runtime < 120 then '90-119 minutes'
        when m.runtime < 150 then '120-149 minutes'
        else '150 minutes or more'
    end as runtime_band,
    case
        when m.budget is null then 'Unknown'
        when m.budget < 1000000 then 'Under $1M'
        when m.budget < 10000000 then '$1M-$10M'
        when m.budget < 50000000 then '$10M-$50M'
        when m.budget < 100000000 then '$50M-$100M'
        else '$100M or more'
    end as budget_band,
    coalesce(c.country_count, 0) as country_count,
    case
        when c.country_count is null or c.country_count = 0 then 'Unknown'
        when c.country_count = 1 then 'Single-country'
        else 'Multi-country'
    end as country_type
from {{ ref('stg_tmdb_movies') }} as m
left join country_counts as c using (movie_nk)
