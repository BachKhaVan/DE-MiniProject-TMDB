with known_companies as (
    select
        row_number() over (order by company_nk)::integer as company_sk,
        company_nk,
        min(company_name)::varchar(255) as company_name
    from {{ ref('stg_movie_companies') }}
    where company_nk <> 0
    group by company_nk
)

select -1::integer as company_sk, 0::integer as company_nk, 'Unknown'::varchar(255) as company_name

union all

select company_sk, company_nk, company_name
from known_companies
