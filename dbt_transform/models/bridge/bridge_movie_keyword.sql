with associations as (
    select distinct movie_nk, keyword_nk
    from {{ ref('stg_movie_keywords') }}
)

select
    m.movie_sk,
    k.keyword_sk
from associations as a
join {{ ref('dim_movie') }} as m using (movie_nk)
join {{ ref('dim_keyword') }} as k using (keyword_nk)
