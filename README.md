# TMDB 5000 Movie Data Warehouse & BI Analytics

Dự án hướng tới xây dựng hệ thống BI tích hợp Generative AI cho TMDB 5000 Movie Dataset. Tài liệu này phân biệt mã nguồn đã có với pipeline đã chạy được xác nhận; số liệu trong báo cáo Giai đoạn 1 là bằng chứng lịch sử, không phải kết quả chạy lại ở máy hiện tại.

## Trạng thái hiện tại

| Hạng mục | Trạng thái |
|---|---|
| Mage Source → PostgreSQL Staging | Có Full Load với làm sạch cơ bản và exporter `replace`. Báo cáo Giai đoạn 1 ghi nhận 4.803 dòng cho mỗi bảng. |
| Incremental Load | Có batch demo append movies. Watermark không lọc batch và graph chưa bảo đảm append thành công trước khi cập nhật LSET; không chạy lặp batch. |
| Giai đoạn 2: dbt / DDS | Đã build thành công trên snapshot đã kiểm thử: 3 seeds, 18 models, 87 data tests; tổng `dbt build` là 108 PASS, 0 ERROR, 0 SKIP. `fact_movie` có 4.803 dòng. Chi tiết môi trường và SQL validation ở [README Giai đoạn 2](dbt_transform/README.md). |
| Power BI / Generative AI | Chưa triển khai trong repository. |

## Kiến trúc

| Tầng | Công nghệ | Nội dung |
|---|---|---|
| Source | Kaggle CSV | `tmdb_5000_movies.csv` và `tmdb_5000_credits.csv` |
| Raw Staging | Mage.ai + PostgreSQL | Bảng nguồn `stage.stg_tmdb_movies`, `stage.stg_tmdb_credits` |
| Transformation | dbt + PostgreSQL | Views chuẩn hóa trong `staging`; JSON associations; data tests |
| DDS | PostgreSQL | `dim_*`, `bridge_movie_*`, `fact_movie` trong schema `dds` |
| BI / AI | Power BI + LLM/API | Hai dashboard và AI-assisted analytics là các hạng mục sau, chưa có trong repo |

Fact có grain một dòng cho mỗi phim. Quan hệ đa trị được tách sang bốn Bridge. Ba bridge genre, company và country có `weight_factor = 1 / số liên kết của phim` để phân bổ measure khi tổng hợp; bridge keyword chỉ biểu diễn tagging nên không có `weight_factor`. Giá trị `budget = 0` và `revenue = 0` được chuẩn hóa thành `NULL`; `profit = revenue - budget`; `roi = profit / budget`.

## Cấu trúc repository

```text
DE-MiniProject-TMDB/
├── compose.yaml
├── postgres/init/01_init.sql       # Schema nền và watermark; Compose tự chạy
├── postgres/init/02_dds_schema.sql # DDL tham chiếu theo Data Contract, không tự chạy
├── mage_pipeline/                 # Loader, transformer, exporter, pipeline Mage
├── dbt_transform/
│   ├── dbt_project.yml
│   ├── profiles.yml.example
│   ├── models/staging/             # Sources, clean views, parsed JSON associations
│   ├── models/dimensions/          # Date, Movie, Language, Genre, Company, Country, Keyword
│   ├── models/bridge/              # Bốn movie association bridges
│   ├── models/facts/fact_movie.sql
│   ├── seeds/                      # Country, keyword và language mappings
│   └── macros/                     # Schema and data-test macros
├── powerbi_dashboard/              # Chưa có project Power BI
├── docs/                           # Chưa có sơ đồ/tài liệu được commit
└── test/                           # Script đối chiếu CSV và PostgreSQL
```

CSV nguồn, `.env`, Mage `io_config.yaml` và dbt `profiles.yml` là cục bộ, không commit. Compose chỉ mount `postgres/init/01_init.sql`, tạo schema `stage`, `staging`, `dds`, `control` và watermark row cho incremental demo. `postgres/init/02_dds_schema.sql` được giữ làm DDL tham chiếu/Data Contract; không chạy trong quy trình chuẩn. dbt materialize các bảng DDS và constraints khi build. Init SQL chỉ chạy khi PostgreSQL tạo data volume mới.

## Cài đặt và chạy

### 1. Khởi chạy Mage và PostgreSQL

1. Tạo `.env` từ `.env.example` và đặt mật khẩu riêng.
2. Đặt hai CSV nguồn trong `data/raw/`.
3. Tạo `mage_pipeline/io_config.yaml` trỏ đến PostgreSQL Compose (mặc định database `warehouse`, user `labuser`, host nội bộ Docker `postgres`).
4. Chạy `docker compose up -d`, mở Mage tại `http://localhost:6789` và chạy pipeline `tmdb_ingestion`.

### 2. Chạy dbt trên máy host

Yêu cầu Python và adapter PostgreSQL của dbt. Từ thư mục gốc repository, chạy:

```powershell
python -m pip install dbt-core==1.12.5 dbt-postgres==1.11.0
Copy-Item dbt_transform\profiles.yml.example dbt_transform\profiles.yml
```

Sửa mật khẩu trong `dbt_transform/profiles.yml` cho trùng `.env`, rồi chạy:

```powershell
Set-Location dbt_transform
dbt debug --profiles-dir .
dbt build --profiles-dir .
dbt docs generate --profiles-dir .
```

`dbt build` sẽ tạo seed, models và chạy data tests theo dependency graph. Source tables phải được tạo trước bằng Mage. Chi tiết model và mapping nằm trong [dbt_transform/README.md](dbt_transform/README.md); profile có mật khẩu thật bị gitignore.

### 3. Đối chiếu dữ liệu nguồn và staging

Từ thư mục gốc repository:

```powershell
python test\validate_tmdb.py --flow full
```

Script chỉ đọc CSV và PostgreSQL, sau đó ghi báo cáo mới vào `test/results/`; nó không chạy pipeline hay sửa database. Hướng dẫn Incremental Load và các giới hạn hiện tại ở [test/README_test.md](test/README_test.md).

## Mô hình DDS

- `dim_date`: ngày phát hành, thuộc tính ngày/tháng/quý/năm/thập niên; `date_sk = -1` là ngày không rõ.
- `dim_movie`: tiêu đề, trạng thái, nhóm runtime/budget và loại hợp tác quốc gia.
- `dim_language`: mã ngôn ngữ gốc; `language_name` tra từ seed `language_name_mapping`, mã chưa được map được giữ nguyên làm tên hiển thị.
- `dim_genre`, `dim_company`, `dim_country`, `dim_keyword`: các chiều đa trị tách từ JSON.
- `bridge_movie_genre`, `bridge_movie_company`, `bridge_movie_country`: có `weight_factor` để phân bổ measure; `bridge_movie_keyword` chỉ lưu quan hệ tagging và không có trọng số.
- `fact_movie`: một dòng/phim với budget, revenue, profit, ROI và chỉ số khán giả.

Country region seed hiện chỉ ánh xạ một số mã phổ biến; quốc gia chưa được map có `region = 'Unknown'`. Keyword theme seed là mapping biên tập ban đầu; từ khóa chưa ánh xạ vào `Other`. Language code chưa có trong seed được giữ làm tên hiển thị, nên tên ngôn ngữ có thể chưa đầy đủ. Các mapping này cần được rà soát trước khi dùng kết quả cho dashboard. Khi tổng hợp measure qua genre/company/country, dùng `weight_factor`; keyword bridge là tagging và không có trọng số phân bổ.

## Quy ước nhóm và Git

Nhóm tích hợp qua `develop`, làm việc trên `feat/<phạm-vi>-<tên>` và mở pull request vào `develop`. Không push trực tiếp lên `main` hoặc `develop`. Commit theo mẫu `<type>(<scope>): <mô tả>`, ví dụ `feat(dbt): build movie fact and dimensions` hoặc `docs(report): update phase status`.

Không commit `.env`, mật khẩu, cấu hình kết nối riêng hoặc CSV thô. Khi tổng hợp qua chiều đa trị, dùng `weight_factor` để tránh nhân lặp measures.
