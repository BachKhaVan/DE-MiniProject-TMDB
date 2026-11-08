with associations as (
    select distinct movie_nk, keyword_nk
    from {{ ref('stg_movie_keywords') }}
),

weighted as (
    select
        movie_nk,
        keyword_nk,
        1.0 / count(*) over (partition by movie_nk) as weight_factor
    from associations
)

select
    m.movie_sk,
    k.keyword_sk,
    w.weight_factor
from weighted as w
join {{ ref('dim_movie') }} as m using (movie_nk)
join {{ ref('dim_keyword') }} as k using (keyword_nk)
