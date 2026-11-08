with languages as (
    select distinct language_nk
    from {{ ref('stg_tmdb_movies') }}
    where language_nk is not null
)

select
    '-1'::text as language_sk,
    null::text as language_nk,
    'Unknown'::text as language_name,
    'Unknown'::text as language_group

union all

select
    md5('language:' || language_nk) as language_sk,
    language_nk,
    language_nk as language_name,
    case when lower(language_nk) = 'en' then 'English' else 'Non-English' end as language_group
from languages
