with parsed as (
    select distinct
        m.movie_nk,
        nullif(btrim(item.value ->> 'iso_3166_1'), '')::varchar(10) as country_code,
        nullif(btrim(item.value ->> 'name'), '')::varchar(100) as country_name
    from {{ ref('stg_tmdb_movies') }} as m
    cross join lateral jsonb_array_elements(
        coalesce(nullif(btrim(m.production_countries_json), '')::jsonb, '[]'::jsonb)
    ) as item(value)
    where nullif(btrim(item.value ->> 'iso_3166_1'), '') is not null
      and nullif(btrim(item.value ->> 'name'), '') is not null
),

all_associations as (
    select movie_nk, country_code, country_name
    from parsed

    union all

    select m.movie_nk, 'unk'::varchar(10) as country_code, 'Unknown'::varchar(100) as country_name
    from {{ ref('stg_tmdb_movies') }} as m
    where not exists (
        select 1 from parsed as p where p.movie_nk = m.movie_nk
    )
)

select movie_nk, country_code, country_name
from all_associations
