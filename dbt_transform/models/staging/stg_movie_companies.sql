with parsed as (
    select distinct
        m.movie_nk,
        nullif(item.value ->> 'id', '')::integer as company_nk,
        nullif(btrim(item.value ->> 'name'), '')::varchar(255) as company_name
    from {{ ref('stg_tmdb_movies') }} as m
    cross join lateral jsonb_array_elements(
        coalesce(nullif(btrim(m.production_companies_json), '')::jsonb, '[]'::jsonb)
    ) as item(value)
    where nullif(item.value ->> 'id', '') is not null
      and nullif(btrim(item.value ->> 'name'), '') is not null
),

all_associations as (
    select movie_nk, company_nk, company_name
    from parsed

    union all

    select m.movie_nk, 0::integer as company_nk, 'Unknown'::varchar(255) as company_name
    from {{ ref('stg_tmdb_movies') }} as m
    where not exists (
        select 1 from parsed as p where p.movie_nk = m.movie_nk
    )
)

select movie_nk, company_nk, company_name
from all_associations
