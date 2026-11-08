# Giai đoạn 2 — dbt Transformation và DDS

README này là hướng dẫn riêng cho Giai đoạn 2. Nó ghi trạng thái triển khai dbt/DDS; không thay thế hoặc sửa README tổng ở repository root. Schema đích được căn theo data contract trong `Schema_Report.md`.

## Trạng thái

- Đã viết dbt models, seeds, data tests và contracts cho staging, dimensions, bridges, fact.
- Đã thêm DDL `postgres/init/02_dds_schema.sql` với kiểu dữ liệu, khóa và các dòng Unknown của DDS.
- `fact_movie.vote_count` có `DEFAULT 0` trong DDL và được đặt lại bằng dbt post-hook sau mỗi lần materialize bảng.
- Chưa chạy `dbt build` trên PostgreSQL của dự án; chưa xác nhận số dòng Fact, PK/FK vật lý hoặc kết quả data tests trên dữ liệu thật.
- Power BI và Generative AI nằm ngoài phạm vi Giai đoạn 2.

## Hợp đồng mô hình

`postgres/init/02_dds_schema.sql` khởi tạo các bảng trong `dds` theo snake_case. dbt contracts trong `models/schema.yml` khai báo đầy đủ cột và kiểu dữ liệu; constraints được định nghĩa trong model để dbt tái tạo đúng khi build.

### Dimensions

- `dim_movie`: integer `movie_sk`, natural key `movie_nk`, `status`, các nhóm runtime/budget theo nhãn trong data contract và `country_count`/`country_type`. Known SK được đánh số theo thứ tự natural key khi full rebuild.
- `dim_date`: integer key `YYYYMMDD`; Unknown là `date_sk = -1`; `decade` có dạng chuỗi như `1980s`.
- `dim_language`: integer SK; Unknown là `language_sk = -1`, `language_nk = 'unk'`, `language_name = 'Unknown'`, `language_group = 'Non-English'`.
- `dim_genre`, `dim_company`, `dim_country`, `dim_keyword`: integer SK, dòng Unknown SK `-1`; natural key mặc định của Unknown là `0`, riêng country code là `unk`.

SK dạng `row_number()` phù hợp với dataset snapshot và full rebuild hiện tại. Khi thêm natural keys có thứ tự nhỏ hơn, SK của các chiều có thể thay đổi; cần rebuild toàn bộ các bảng phụ thuộc cùng lượt.

### Bridges và Unknown association

- `bridge_movie_genre`, `bridge_movie_company`, `bridge_movie_country` có composite PK và `weight_factor DECIMAL(18,10) = 1/k`.
- Nếu JSON genre/company/country rỗng hoặc không có phần tử hợp lệ, model tạo association tới dimension Unknown với `weight_factor = 1.0`.
- `bridge_movie_keyword` chỉ có `(movie_sk, keyword_sk)`, **không có `weight_factor`**, theo data contract. Keyword được xem là tagging, không phân bổ measure tài chính.
- Data tests kiểm tra khóa ghép, FK logic và tổng `weight_factor = 1` theo phim trên ba bridge có trọng số.

### Fact và phép đo

`fact_movie` có một dòng/phim; `movie_sk` vừa là PK vừa là FK tới `dim_movie`. `date_sk` và `language_sk` là FK NOT NULL, dùng Unknown key khi thiếu dữ liệu.

- `budget`, `revenue`: `DECIMAL(18,0)`; nguồn bằng 0 thành NULL.
- `profit`: `revenue - budget`; NULL nếu thiếu một trong hai.
- `roi`: `profit / budget`; NULL nếu budget NULL hoặc `<= 0`.
- `runtime NUMERIC(5,1)`, `popularity DECIMAL(12,6)`, `vote_average DECIMAL(4,1)`, `vote_count INT` với NULL được thay bằng 0. `vote_average` thành NULL khi `vote_count = 0`.
- `is_finance_valid = 1` chỉ khi budget và revenue đều `> 0`.
- `is_revenue_over_budget = 1` chỉ khi finance hợp lệ và revenue > budget.
- `movie_count` luôn bằng 1.

## Layers và file chính

- Raw sources: `stage.stg_tmdb_movies`, `stage.stg_tmdb_credits` do Mage nạp.
- dbt views: `staging.stg_tmdb_movies`, `staging.stg_tmdb_credits` và bốn model parse JSON.
- DDS models: `models/dimensions/`, `models/bridge/`, `models/facts/fact_movie.sql`.
- Seeds: `country_region.csv`, `keyword_theme_mapping.csv`, `language_name_mapping.csv`.
- Contracts/tests: `models/schema.yml`; generic tests nằm trong `macros/`.

Staging SQL hiện dựa vào tên cột vật lý `"_status"` và `"_cast"` được ghi trong báo cáo ingestion. Đối chiếu hai tên này với PostgreSQL thực tế trước khi chạy build. JSON phải parse được thành array JSON; chuỗi JSON lỗi cú pháp sẽ làm model fail.

Country region và keyword theme là mapping biên tập ban đầu. Country chưa có trong seed thành `Unknown`; keyword chưa được ánh xạ thành `Other`. Language name dùng seed `language_name_mapping.csv`; mã ngôn ngữ chưa có trong seed hiện được giữ nguyên làm tên hiển thị, nên cần bổ sung mapping nếu mã đó xuất hiện trong staging để đáp ứng tên đầy đủ.

## Cài đặt và chạy

Yêu cầu dbt Core `>=1.10.5,<2.0.0` và PostgreSQL adapter:

```powershell
python -m pip install dbt-postgres
Copy-Item profiles.yml.example profiles.yml
```

Đặt password đúng với `.env` trong `profiles.yml`. Sau khi Mage tạo hai source tables, chạy từ thư mục `dbt_transform`:

```powershell
dbt debug --profiles-dir .
dbt build --profiles-dir .
dbt docs generate --profiles-dir .
```

`dbt build` tạo seeds/models và chạy data tests theo graph. Compose tự chạy `01_init.sql` rồi `02_dds_schema.sql` khi khởi tạo volume PostgreSQL mới. Với volume cũ, nếu DDS chưa được khởi tạo thì áp dụng DDL; nếu các bảng DDS đã được tạo bởi dbt, chạy `dbt build` để tái tạo chúng theo contracts và đặt lại default của `vote_count`. Lệnh áp dụng cho volume cũ:

```powershell
docker compose exec -T postgres psql -U labuser -d warehouse -f /docker-entrypoint-initdb.d/01_init.sql
docker compose exec -T postgres psql -U labuser -d warehouse -f /docker-entrypoint-initdb.d/02_dds_schema.sql
```

Thay user/database trong lệnh nếu `.env` dùng giá trị khác. Các lệnh dbt ghi dữ liệu vào schema `staging` và `dds`; chỉ chạy trên warehouse local/dev.
