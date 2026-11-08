select distinct
    m.movie_nk,
    nullif(btrim(item.value ->> 'iso_3166_1'), '') as country_code,
    nullif(btrim(item.value ->> 'name'), '') as country_name
from {{ ref('stg_tmdb_movies') }} as m
cross join lateral jsonb_array_elements(
    coalesce(nullif(btrim(m.production_countries_json), '')::jsonb, '[]'::jsonb)
) as item(value)
where nullif(btrim(item.value ->> 'iso_3166_1'), '') is not null
  and nullif(btrim(item.value ->> 'name'), '') is not null
