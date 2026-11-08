with languages as (
    select distinct language_nk::varchar(10) as language_nk
    from {{ ref('stg_tmdb_movies') }}
    where language_nk is not null
      and lower(language_nk) <> 'unk'
),

known_languages as (
    select
        row_number() over (order by language_nk)::integer as language_sk,
        l.language_nk,
        coalesce(n.language_name, l.language_nk)::varchar(100) as language_name,
        case when lower(l.language_nk) = 'en' then 'English' else 'Non-English' end::varchar(20) as language_group
    from languages as l
    left join {{ ref('language_name_mapping') }} as n
      on lower(n.language_nk) = lower(l.language_nk)
)

select
    -1::integer as language_sk,
    'unk'::varchar(10) as language_nk,
    'Unknown'::varchar(100) as language_name,
    'Non-English'::varchar(20) as language_group

union all

select language_sk, language_nk, language_name, language_group
from known_languages
