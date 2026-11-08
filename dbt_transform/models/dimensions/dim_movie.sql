with country_counts as (
    select movie_nk, count(distinct country_code)::integer as country_count
    from {{ ref('stg_movie_countries') }}
    where country_code <> 'unk'
    group by movie_nk
),

ranked_movies as (
    select
        row_number() over (order by m.movie_nk)::integer as movie_sk,
        m.movie_nk,
        m.title,
        m.original_title,
        m.movie_status as status,
        m.runtime,
        m.budget,
        coalesce(c.country_count, 0)::integer as country_count,
        case
            when c.country_count is null or c.country_count = 0 then 'Unknown'
            when c.country_count = 1 then 'Single-country'
            else 'Multi-country'
        end as country_type
    from {{ ref('stg_tmdb_movies') }} as m
    left join country_counts as c using (movie_nk)
)

select
    movie_sk,
    movie_nk::integer as movie_nk,
    title::text as title,
    original_title::text as original_title,
    status::varchar(50) as status,
    case
        when runtime is null then 'Không rõ'
        when runtime < 90 then 'Dưới 90 phút'
        when runtime < 120 then '90–119 phút'
        when runtime < 150 then '120–149 phút'
        else 'Từ 150 phút trở lên'
    end::varchar(50) as runtime_band,
    case
        when budget is null then 'Không rõ'
        when budget < 1000000 then 'Dưới 1 triệu USD'
        when budget < 10000000 then '1–10 triệu'
        when budget < 50000000 then '10–50 triệu'
        when budget < 100000000 then '50–100 triệu'
        else 'Từ 100 triệu trở lên'
    end::varchar(50) as budget_band,
    country_count,
    country_type::varchar(50) as country_type
from ranked_movies
