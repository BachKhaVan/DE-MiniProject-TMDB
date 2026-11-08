select
    md5('keyword:' || k.keyword_nk::text) as keyword_sk,
    k.keyword_nk,
    min(k.keyword_name) as keyword_name,
    coalesce(min(m.theme_group), 'Other') as theme_group
from {{ ref('stg_movie_keywords') }} as k
left join {{ ref('keyword_theme_mapping') }} as m
  on lower(m.keyword_name) = lower(k.keyword_name)
group by k.keyword_nk
