select
    movie.movie_sk,
    coalesce(date_dim.date_sk, -1)::integer as date_sk,
    coalesce(language.language_sk, '-1') as language_sk,
    movies.budget,
    movies.revenue,
    movies.revenue - movies.budget as profit,
    (movies.revenue - movies.budget) / nullif(movies.budget, 0) as roi,
    movies.runtime,
    movies.popularity,
    movies.vote_average,
    movies.vote_count,
    case
        when movies.budget is not null and movies.revenue is not null then 1
        else 0
    end::smallint as is_finance_valid,
    case
        when movies.budget is not null
         and movies.revenue is not null
         and movies.revenue > movies.budget then 1
        else 0
    end::smallint as is_revenue_over_budget,
    1::smallint as movie_count
from {{ ref('stg_tmdb_movies') }} as movies
join {{ ref('dim_movie') }} as movie using (movie_nk)
left join {{ ref('dim_date') }} as date_dim
  on date_dim.full_date = movies.release_date
left join {{ ref('dim_language') }} as language
  on language.language_nk = movies.language_nk
