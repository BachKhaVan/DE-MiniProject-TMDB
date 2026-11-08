with associations as (
    select distinct movie_nk, company_nk
    from {{ ref('stg_movie_companies') }}
),

weighted as (
    select
        movie_nk,
        company_nk,
        (1.0::decimal(18, 10) / count(*) over (partition by movie_nk))::decimal(18, 10) as weight_factor
    from associations
)

select
    m.movie_sk,
    c.company_sk,
    w.weight_factor
from weighted as w
join {{ ref('dim_movie') }} as m using (movie_nk)
join {{ ref('dim_company') }} as c using (company_nk)
