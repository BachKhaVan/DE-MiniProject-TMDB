select
    md5('company:' || company_nk::text) as company_sk,
    company_nk,
    min(company_name) as company_name
from {{ ref('stg_movie_companies') }}
group by company_nk
