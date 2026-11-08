with known_keywords as (
    select
        row_number() over (order by k.keyword_nk)::integer as keyword_sk,
        k.keyword_nk,
        min(k.keyword_name)::varchar(255) as keyword_name,
        coalesce(min(m.theme_group), 'Other')::varchar(50) as theme_group
    from {{ ref('stg_movie_keywords') }} as k
    left join {{ ref('keyword_theme_mapping') }} as m
      on lower(m.keyword_name) = lower(k.keyword_name)
    where k.keyword_nk <> 0
    group by k.keyword_nk
)

select
    -1::integer as keyword_sk,
    0::integer as keyword_nk,
    'Unknown'::varchar(255) as keyword_name,
    'Other'::varchar(50) as theme_group

union all

select keyword_sk, keyword_nk, keyword_name, theme_group
from known_keywords
