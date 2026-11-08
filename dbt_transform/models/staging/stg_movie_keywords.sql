select distinct
    m.movie_nk,
    nullif(item.value ->> 'id', '')::integer as keyword_nk,
    nullif(btrim(item.value ->> 'name'), '') as keyword_name
from {{ ref('stg_tmdb_movies') }} as m
cross join lateral jsonb_array_elements(
    coalesce(nullif(btrim(m.keywords_json), '')::jsonb, '[]'::jsonb)
) as item(value)
where nullif(item.value ->> 'id', '') is not null
  and nullif(btrim(item.value ->> 'name'), '') is not null
