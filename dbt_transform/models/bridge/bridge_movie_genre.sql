with associations as (
    select distinct movie_nk, genre_nk
    from {{ ref('stg_movie_genres') }}
),

weighted as (
    select
        movie_nk,
        genre_nk,
        1.0 / count(*) over (partition by movie_nk) as weight_factor
    from associations
)

select
    m.movie_sk,
    g.genre_sk,
    w.weight_factor
from weighted as w
join {{ ref('dim_movie') }} as m using (movie_nk)
join {{ ref('dim_genre') }} as g using (genre_nk)
