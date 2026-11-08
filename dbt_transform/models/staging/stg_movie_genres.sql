select distinct
    m.movie_nk,
    nullif(item.value ->> 'id', '')::bigint as genre_nk,
    nullif(btrim(item.value ->> 'name'), '') as genre_name
from {{ ref('stg_tmdb_movies') }} as m
cross join lateral jsonb_array_elements(
    coalesce(nullif(btrim(m.genres_json), '')::jsonb, '[]'::jsonb)
) as item(value)
where nullif(item.value ->> 'id', '') is not null
  and nullif(btrim(item.value ->> 'name'), '') is not null
