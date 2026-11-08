select
    movie.movie_sk::integer as movie_sk,
    coalesce(date_dim.date_sk, -1)::integer as date_sk,
    coalesce(language.language_sk, -1)::integer as language_sk,
    movies.budget::numeric(18, 0) as budget,
    movies.revenue::numeric(18, 0) as revenue,
    case
        when movies.budget is null or movies.revenue is null then null::numeric(18, 0)
        else (movies.revenue - movies.budget)::numeric(18, 0)
    end as profit,
    case
        when movies.budget is null or movies.budget <= 0 then null::numeric(18, 4)
        else ((movies.revenue - movies.budget) / movies.budget)::numeric(18, 4)
    end as roi,
    movies.runtime::numeric(5, 1) as runtime,
    movies.popularity::numeric(12, 6) as popularity,
    movies.vote_average::numeric(4, 1) as vote_average,
    coalesce(movies.vote_count, 0)::integer as vote_count,
    case
        when movies.budget > 0 and movies.revenue > 0 then 1
        else 0
    end::integer as is_finance_valid,
    case
        when movies.budget > 0
         and movies.revenue > 0
         and movies.revenue > movies.budget then 1
        else 0
    end::integer as is_revenue_over_budget,
    1::integer as movie_count
from {{ ref('stg_tmdb_movies') }} as movies
join {{ ref('dim_movie') }} as movie using (movie_nk)
left join {{ ref('dim_date') }} as date_dim
  on date_dim.full_date = movies.release_date
left join {{ ref('dim_language') }} as language
  on language.language_nk = coalesce(movies.language_nk, 'unk')
