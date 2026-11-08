# dbt Transformation and DDS

This project transforms Mage's raw tables in PostgreSQL schema `stage` into cleaned views in `staging` and tables in `dds`. Relations use snake_case names to avoid quoted identifiers. A custom schema macro writes the configured schemas directly (`staging`, `dds`).

## Models

- Staging views: normalized movie and credits rows, plus parsed genre/company/country/keyword associations.
- Dimensions: date, movie, language, genre, company, country, keyword.
- Bridges: movie to genre, company, country, keyword. Each bridge includes `weight_factor = 1 / association_count`, including the keyword bridge.
- Fact: `fact_movie`, one row per movie. Financial zeros become `NULL`; `profit = revenue - budget`; `roi = profit / budget`; finance flags preserve the denominator for revenue-over-budget rate.
- Seeds: `country_region.csv` is a starter region map; unmapped country codes become `Unknown`. `keyword_theme_mapping.csv` is curated; unlisted keywords become `Other`.

The current report describes PascalCase business names. Physical PostgreSQL relations use snake_case, for example `dds.fact_movie` and `dds.bridge_movie_genre`.

## Local setup

Install the PostgreSQL adapter with `python -m pip install dbt-postgres`. Copy `profiles.yml.example` to `profiles.yml` in this directory, then set the local PostgreSQL password. The real `profiles.yml` is ignored by Git. The profile connects to `localhost:5432`, database `warehouse`, user `labuser` by default.

After Mage Full Load has populated the source tables:

```powershell
Set-Location dbt_transform
dbt debug --profiles-dir .
dbt build --profiles-dir .
dbt docs generate --profiles-dir .
```

`dbt build` orders seeds, models, and data tests according to the project graph. It has not yet been run against this machine's database. The source staging tables must exist first; see the repository root README for Compose and Mage setup.
