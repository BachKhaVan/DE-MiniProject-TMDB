with source_rows as (
    select
        movie_id::bigint as movie_nk,
        nullif(btrim(title::text), '') as title,
        "_cast"::text as cast_json,
        crew::text as crew_json
    from {{ source('tmdb_stage', 'stg_tmdb_credits') }}
),

ranked_rows as (
    select
        *,
        row_number() over (
            partition by movie_nk
            order by title, cast_json, crew_json
        ) as _row_number
    from source_rows
    where movie_nk is not null
)

select movie_nk, title, cast_json, crew_json
from ranked_rows
where _row_number = 1
