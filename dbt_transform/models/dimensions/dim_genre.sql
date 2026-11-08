with known_genres as (
    select
        row_number() over (order by genre_nk)::integer as genre_sk,
        genre_nk,
        min(genre_name)::varchar(100) as genre_name
    from {{ ref('stg_movie_genres') }}
    where genre_nk <> 0
    group by genre_nk
)

select -1::integer as genre_sk, 0::integer as genre_nk, 'Unknown'::varchar(100) as genre_name

union all

select genre_sk, genre_nk, genre_name
from known_genres
