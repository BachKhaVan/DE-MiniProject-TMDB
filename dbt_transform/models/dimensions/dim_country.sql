with known_countries as (
    select
        row_number() over (order by c.country_code)::integer as country_sk,
        c.country_code::varchar(10) as country_code,
        min(c.country_name)::varchar(100) as country_name,
        coalesce(min(r.region), 'Unknown')::varchar(100) as region
    from {{ ref('stg_movie_countries') }} as c
    left join {{ ref('country_region') }} as r
      on upper(r.country_code) = upper(c.country_code)
    where lower(c.country_code) <> 'unk'
    group by c.country_code
)

select
    -1::integer as country_sk,
    'unk'::varchar(10) as country_code,
    'Unknown'::varchar(100) as country_name,
    'Unknown'::varchar(100) as region

union all

select country_sk, country_code, country_name, region
from known_countries
