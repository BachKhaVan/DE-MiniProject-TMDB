select
    md5('country:' || c.country_code) as country_sk,
    c.country_code,
    min(c.country_name) as country_name,
    coalesce(min(r.region), 'Unknown') as region
from {{ ref('stg_movie_countries') }} as c
left join {{ ref('country_region') }} as r
  on upper(r.country_code) = upper(c.country_code)
group by c.country_code
