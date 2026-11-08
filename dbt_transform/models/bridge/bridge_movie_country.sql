with associations as (
    select distinct movie_nk, country_code
    from {{ ref('stg_movie_countries') }}
),

weighted as (
    select
        movie_nk,
        country_code,
        1.0 / count(*) over (partition by movie_nk) as weight_factor
    from associations
)

select
    m.movie_sk,
    c.country_sk,
    w.weight_factor
from weighted as w
join {{ ref('dim_movie') }} as m using (movie_nk)
join {{ ref('dim_country') }} as c using (country_code)
