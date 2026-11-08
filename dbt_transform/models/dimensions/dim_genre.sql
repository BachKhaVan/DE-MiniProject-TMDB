select
    md5('genre:' || genre_nk::text) as genre_sk,
    genre_nk,
    min(genre_name) as genre_name
from {{ ref('stg_movie_genres') }}
group by genre_nk
