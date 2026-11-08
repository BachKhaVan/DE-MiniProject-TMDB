with source_rows as (
    select
        id::bigint as movie_nk,
        nullif(btrim(title::text), '') as title,
        nullif(btrim(original_title::text), '') as original_title,
        nullif(btrim("_status"::text), '') as movie_status,
        nullif(btrim(original_language::text), '') as language_nk,
        release_date::date as release_date,
        nullif(budget::numeric, 0) as budget,
        nullif(revenue::numeric, 0) as revenue,
        runtime::numeric as runtime,
        popularity::numeric as popularity,
        case when vote_count > 0 then vote_average::numeric end as vote_average,
        vote_count::integer as vote_count,
        genres::text as genres_json,
        production_companies::text as production_companies_json,
        production_countries::text as production_countries_json,
        keywords::text as keywords_json
    from {{ source('tmdb_stage', 'stg_tmdb_movies') }}
),

valid_rows as (
    select *
    from source_rows
    where movie_nk is not null
      and title is not null
),

ranked_rows as (
    select
        *,
        row_number() over (
            partition by movie_nk
            order by
                release_date desc nulls last,
                budget desc nulls last,
                revenue desc nulls last,
                title,
                genres_json,
                production_companies_json
        ) as _row_number
    from valid_rows
)

select
    movie_nk,
    title,
    original_title,
    movie_status,
    language_nk,
    release_date,
    budget,
    revenue,
    runtime,
    popularity,
    vote_average,
    vote_count,
    genres_json,
    production_companies_json,
    production_countries_json,
    keywords_json
from ranked_rows
where _row_number = 1
