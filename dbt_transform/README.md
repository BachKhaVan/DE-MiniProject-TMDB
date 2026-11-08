# Giai đoạn 2 — dbt Transformation và DDS

> Tài liệu này là hướng dẫn triển khai riêng cho Giai đoạn 2 trong `dbt_transform/README.md`. Tài liệu không thay thế và không yêu cầu sửa README tổng ở repository root.
>
> **Kiến trúc đã thống nhất:** dbt là thành phần duy nhất materialize và quản lý vòng đời các bảng DDS. Docker chỉ tự động chạy `postgres/init/01_init.sql`. File `postgres/init/02_dds_schema.sql` được giữ làm DDL tham chiếu/Data Contract, **không được Docker tự động chạy và không chạy trước `dbt build`**.

---

## 1. Mục tiêu và phạm vi

Giai đoạn 2 chuyển dữ liệu Mage đã nạp vào PostgreSQL từ raw staging sang các mô hình phân tích trong schema `staging` và `dds` bằng dbt.

Phạm vi thực hiện:

1. Chuẩn hóa dữ liệu Movies và Credits từ schema `stage`.
2. Parse các trường JSON đa trị thành các mô hình staging riêng.
3. Nạp seeds phục vụ mapping quốc gia, từ khóa và ngôn ngữ.
4. Xây dựng 7 Dimension, 4 Bridge và 1 Fact theo Data Contract trong `Schema_Report.md`.
5. Kiểm tra chất lượng dữ liệu bằng dbt data tests và physical constraints được tạo trên PostgreSQL.
6. Sinh tài liệu mô hình bằng `dbt docs generate`.

Power BI, Semantic Model, dashboard và Generative AI chưa thuộc phạm vi triển khai của README này. Người thực hiện Giai đoạn 3 sử dụng các bảng DDS và quy tắc nghiệp vụ được mô tả ở Mục 12.

## 2. Kiến trúc triển khai và phân chia trách nhiệm

### 2.1. Các schema

| Schema | Vai trò | Thành phần tạo/quản lý |
|---|---|---|
| `stage` | Raw source tables do Mage nạp | Mage; PostgreSQL khởi tạo schema |
| `staging` | dbt views làm sạch, chuẩn hóa và parse JSON | dbt |
| `dds` | 7 Dimensions, 4 Bridges và FactMovie | dbt |
| `control` | Trạng thái điều phối, watermark Incremental | `01_init.sql` và Mage |

### 2.2. Quy tắc khởi tạo PostgreSQL và DDS

| File/thành phần | Trách nhiệm | Có chạy tự động khi tạo volume mới? |
|---|---|---|
| `postgres/init/01_init.sql` | Tạo `stage`, `staging`, `dds`, `control`; tạo `control.etl_watermark`; khởi tạo dòng `tmdb_incremental` | Có |
| `postgres/init/02_dds_schema.sql` | DDL tham chiếu theo Data Contract: kiểu dữ liệu, khóa và Unknown rows | **Không** |
| dbt models + contracts | Materialize các views/tables thuộc `staging` và `dds` | Chạy khi thực hiện `dbt build` |

Không mount toàn bộ thư mục `postgres/init` vào `/docker-entrypoint-initdb.d`. Trong `compose.yaml`, chỉ mount `postgres/init/01_init.sql`, ví dụ:

```yaml
volumes:
  - pg_data:/var/lib/postgresql/data
  - ./postgres/init/01_init.sql:/docker-entrypoint-initdb.d/01_init.sql:ro
```

Không xóa `02_dds_schema.sql`; file này được giữ để đối chiếu cấu trúc và Data Contract. Không chạy file này trong quy trình chuẩn vì dbt đã tạo các bảng DDS và physical constraints.

### 2.3. Phân chia trách nhiệm

| Thành phần | Trách nhiệm |
|---|---|
| Mage | Đọc dataset và nạp raw tables vào `stage` |
| `01_init.sql` | Khởi tạo schema và watermark |
| `02_dds_schema.sql` | Tài liệu DDL tham chiếu, đối chiếu Data Contract |
| dbt staging models | Làm sạch và chuẩn hóa raw sources; tách JSON |
| dbt seeds | Nạp các bảng mapping |
| dbt dimensions/bridges/facts | Tạo DDS và các ràng buộc được khai báo trong contracts |
| dbt data tests | Kiểm tra uniqueness, not-null, relationships, accepted values và bridge weights |

**Lưu ý về constraints:** model contracts/constraints được khai báo trong dbt và khi build trên môi trường đã kiểm thử, PostgreSQL thực tế có PK, UNIQUE, NOT NULL và 11 FK. Các dbt data tests vẫn được giữ riêng; không coi một loại kiểm tra là thay thế cho loại còn lại.

---

## 3. Môi trường cần cài đặt

Hướng dẫn dưới đây dành cho Windows 10/11, PowerShell và chạy dbt trực tiếp trên máy host; PostgreSQL và Mage chạy bằng Docker Compose.

### 3.1. Phần mềm cần có

| Phần mềm | Mục đích | Phiên bản/mức yêu cầu đã kiểm thử |
|---|---|---|
| Git for Windows | Clone/pull repository | Bản hiện hành phù hợp Windows |
| Docker Desktop | Chạy Mage và PostgreSQL bằng Compose | Có Docker Compose v2; Docker Desktop bật Linux containers/WSL2 |
| Python | Tạo môi trường ảo chạy dbt | Python 3.12.x; đã kiểm thử với 3.12.8 |
| VS Code | Soạn code và chọn Python interpreter | Tùy chọn nhưng khuyến nghị |
| dbt Core | Parse, compile, build và docs | `1.12.5` |
| dbt-postgres | Kết nối PostgreSQL | `1.11.0` |
| PostgreSQL | Data warehouse trong container | PostgreSQL `17` theo Compose |

Không cần cài PostgreSQL server riêng trên Windows nếu sử dụng đúng PostgreSQL container của repository.

### 3.2. Extension VS Code (khuyến nghị)

Cài từ Extensions (`Ctrl+Shift+X`):

- **Python** — Microsoft, extension ID `ms-python.python`.
- **Python Environments** — Microsoft, extension ID `ms-python.vscode-python-envs`.
- **Pylance** — Microsoft, extension ID `ms-python.vscode-pylance` (khuyến nghị).

Các extension chỉ hỗ trợ editor/interpreter; chúng không thay thế việc cài Python, dbt hoặc Docker.

### 3.3. Kiểm tra công cụ nền

Mở PowerShell mới:

```powershell
git --version
docker --version
docker compose version
py -3.12 --version
```

Kết quả mong đợi:

- Mỗi lệnh in ra phiên bản và không báo `command not found`.
- `py -3.12 --version` hiển thị Python 3.12.x.
- Docker Desktop đang chạy.

Nếu `py -3.12` không nhận diện Python 3.12, cài Python 3.12 trước khi tiếp tục.

---

## 4. Clone/pull repository và tạo môi trường dbt

### 4.1. Lấy code mới nhất

Nếu thành viên chưa có repository:

```powershell
git clone <REPOSITORY_URL>
cd DE-MiniProject-TMDB
```

Nếu đã clone repository:

```powershell
cd D:\DE-MiniProject-TMDB
git status --short
git pull --ff-only
```

Nếu `git status --short` cho thấy thay đổi local, không pull/ghi đè một cách mù quáng. Hãy backup hoặc stash thay đổi trước, sau đó mới đồng bộ code.

### 4.2. Tạo virtual environment

Chạy từ thư mục repository root:

```powershell
py -3.12 -m venv .venv
```

Kích hoạt môi trường:

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn script kích hoạt, không cần thay đổi execution policy; có thể chạy Python/dbt bằng đường dẫn đầy đủ như các ví dụ bên dưới.

Chọn interpreter trong VS Code:

1. Nhấn `Ctrl+Shift+P`.
2. Chọn `Python: Select Interpreter`.
3. Chọn `D:\DE-MiniProject-TMDB\.venv\Scripts\python.exe`.

Kiểm tra:

```powershell
.\.venv\Scripts\python.exe --version
```

Kết quả mong đợi: `Python 3.12.x`.

### 4.3. Cài đúng phiên bản dbt đã kiểm thử

**Không chỉ chạy `pip install dbt-postgres` không kèm phiên bản.** Cài bản mới nhất không pin có thể kéo dbt Core bản khác (ví dụ release candidate), làm môi trường không đồng nhất giữa các thành viên.

Từ repository root:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install "dbt-core==1.12.5" "dbt-postgres==1.11.0"
```

Kiểm tra phiên bản:

```powershell
.\.venv\Scripts\dbt.exe --version
.\.venv\Scripts\python.exe -m pip check
```

Kết quả mong đợi:

```text
Core:
  - installed: 1.12.5

Plugins:
  - postgres: 1.11.0
```

Và `pip check` trả về:

```text
No broken requirements found.
```

Nếu `dbt --version` hiển thị dbt Core `1.13.0-rc*` hoặc phiên bản khác với môi trường đã kiểm thử, chạy lại lệnh cài pin phiên bản ở trên.

### 4.4. Không đưa môi trường và secrets lên Git

Đảm bảo `.gitignore` bỏ qua tối thiểu:

```gitignore
.venv/
.env
profiles.yml
dbt_transform/profiles.yml
dbt_transform/target/
dbt_transform/logs/
dbt_transform/dbt_packages/
```

Kiểm tra (tùy cấu trúc ignore hiện tại, một số đường dẫn có thể được ignore bởi rule rộng hơn):

```powershell
git check-ignore .venv .env dbt_transform/profiles.yml
```

Không commit hoặc chia sẻ `.env`, `profiles.yml` chứa mật khẩu, API keys hoặc credentials.

---

## 5. Cấu hình biến môi trường và PostgreSQL

### 5.1. Tạo `.env`

Từ repository root, tạo `.env` dựa trên `.env.example` nếu repository có file mẫu:

```powershell
Copy-Item .env.example .env
notepad .env
```

Điền mật khẩu PostgreSQL do nhóm thống nhất. Cấu hình đang được kiểm thử dùng:

```dotenv
POSTGRES_DB=warehouse
POSTGRES_USER=labuser
POSTGRES_PASSWORD=<MAT_KHAU_CUA_THANH_VIEN>
```

Thay placeholder bằng mật khẩu thật tại máy thành viên; không ghi mật khẩu vào README, không gửi lên Git. Nếu Compose đã có default cho DB/user thì vẫn nên sử dụng đúng `warehouse` và `labuser` để khớp lệnh kiểm tra bên dưới.

### 5.2. Khởi động container

Từ repository root:

```powershell
docker compose config -q
docker compose up -d
docker compose ps
```

Nếu `docker compose config` báo thiếu `POSTGRES_PASSWORD`, kiểm tra `.env` nằm đúng repository root và có biến `POSTGRES_PASSWORD`.

Kết quả tham chiếu của môi trường đã kiểm thử:

| Service | Image | Port host | Trạng thái mong đợi |
|---|---|---:|---|
| `postgres` | `postgres:17` | `5432` | Up |
| `mage` | `mageai/mageai:latest` | `6789` | Up |

Mở Mage tại `http://localhost:6789` nếu cần chạy pipeline ingestion.

### 5.3. Kiểm tra PostgreSQL sẵn sàng

```powershell
docker compose exec postgres pg_isready -U labuser -d warehouse
```

Kết quả mong đợi:

```text
/var/run/postgresql:5432 - accepting connections
```

Kiểm tra database/user/quyền tạo schema:

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT current_database(), current_user, has_database_privilege(current_user, current_database(), 'CREATE') AS can_create_schema;"
```

Kết quả tham chiếu: database `warehouse`, user `labuser`, `can_create_schema = t`.

### 5.4. Kiểm tra bốn schema và watermark

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('stage','staging','dds','control') ORDER BY schema_name;"
```

Kết quả cần có đủ:

```text
control
dds
stage
staging
```

Tên schema PostgreSQL thực tế là chữ thường `dds`.

Kiểm tra watermark:

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT * FROM control.etl_watermark;"
```

Kết quả tham chiếu ban đầu:

| pipeline_name | lset |
|---|---|
| `tmdb_incremental` | `2000-01-01 00:00:00+00` (có thể hiển thị theo timezone phiên kết nối) |

### 5.5. Lưu ý với PostgreSQL volume cũ

Docker entrypoint chỉ chạy các file trong `/docker-entrypoint-initdb.d` khi khởi tạo data directory/volume PostgreSQL mới. Sửa `compose.yaml` không tự chạy lại init SQL trên volume đã tồn tại.

Nếu volume cũ thiếu schema hoặc watermark, có thể áp dụng lại **chỉ `01_init.sql`** vì file này dùng `IF NOT EXISTS`/`ON CONFLICT`:

```powershell
docker compose exec -T postgres psql -U labuser -d warehouse -f /docker-entrypoint-initdb.d/01_init.sql
```

Sau đó chạy lại các truy vấn kiểm tra schema và watermark.

**Không chạy `02_dds_schema.sql` trong luồng chuẩn. Không chạy `docker compose down -v`, không xóa volume và không `DROP SCHEMA` để xử lý lỗi thông thường.** Nếu là database cũ có các bảng DDS tạo sẵn trước khi chuyển sang dbt, phải kiểm kê và backup trước khi lập kế hoạch migration riêng. Chỉ reset schema trên database local/dev được phép thay đổi và phải có xác nhận/backup.

---

## 6. Chạy Mage và xác minh raw source tables

Trước khi chạy dbt, Mage phải nạp hai bảng nguồn:

- `stage.stg_tmdb_movies`
- `stage.stg_tmdb_credits`

Chạy pipeline Full Load theo hướng dẫn Mage hiện có của nhóm, sau đó xác minh database.

### 6.1. Kiểm tra hai bảng nguồn tồn tại

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema = 'stage' AND table_type = 'BASE TABLE' ORDER BY table_name;"
```

Kết quả cần có hai bảng `stg_tmdb_movies` và `stg_tmdb_credits`.

### 6.2. Kiểm tra tên cột vật lý quan trọng

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_schema = 'stage' AND ((table_name = 'stg_tmdb_movies' AND column_name IN ('id','_status','genres','keywords','production_companies','production_countries')) OR (table_name = 'stg_tmdb_credits' AND column_name IN ('movie_id','_cast','crew'))) ORDER BY table_name, ordinal_position;"
```

Tên cột vật lý đã xác minh trong môi trường hiện tại:

- Movies: `id` là `integer`; `_status` là `text`.
- Credits: `movie_id` là `integer`; `_cast` là `text`.
- Các trường JSON trong Movies và `crew`/`_cast` được lưu dạng `text`.

Nếu tên cột khác, dừng trước `dbt build` và đối chiếu với Mage ingestion/SQL staging.

### 6.3. Kiểm tra số dòng, khóa NULL và khóa trùng

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT 'movies' AS table_name, COUNT(*) AS total_rows, COUNT(*) FILTER (WHERE id IS NULL) AS null_ids, COUNT(*) - COUNT(DISTINCT id) - COUNT(*) FILTER (WHERE id IS NULL) AS duplicate_id_rows FROM stage.stg_tmdb_movies UNION ALL SELECT 'credits', COUNT(*), COUNT(*) FILTER (WHERE movie_id IS NULL), COUNT(*) - COUNT(DISTINCT movie_id) - COUNT(*) FILTER (WHERE movie_id IS NULL) FROM stage.stg_tmdb_credits;"
```

Kết quả tham chiếu của dataset TMDB 5000 trong lần kiểm thử:

| Bảng | Total rows | Null IDs | Duplicate ID rows |
|---|---:|---:|---:|
| Movies | 4.803 | 0 | 0 |
| Credits | 4.803 | 0 | 0 |

Đây là số liệu của snapshot đã kiểm thử, không phải giá trị cố định cho mọi file nguồn.

### 6.4. Kiểm tra quan hệ Movies–Credits

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT COUNT(*) FILTER (WHERE EXISTS (SELECT 1 FROM stage.stg_tmdb_credits c WHERE c.movie_id = m.id)) AS matched_movies, COUNT(*) FILTER (WHERE NOT EXISTS (SELECT 1 FROM stage.stg_tmdb_credits c WHERE c.movie_id = m.id)) AS movies_without_credits FROM stage.stg_tmdb_movies m;"

docker compose exec postgres psql -U labuser -d warehouse -c "SELECT COUNT(*) AS orphan_credit_rows FROM stage.stg_tmdb_credits c WHERE NOT EXISTS (SELECT 1 FROM stage.stg_tmdb_movies m WHERE m.id = c.movie_id);"
```

Kết quả tham chiếu đã xác minh:

- `matched_movies = 4803`
- `movies_without_credits = 0`
- `orphan_credit_rows = 0`

Chỉ tiếp tục khi hai source tables tồn tại, tên cột tương thích và các source tests không phát hiện lỗi khóa.

---

## 7. Cấu hình dbt profile

### 7.1. Tạo profile riêng cho máy thành viên

Từ repository root:

```powershell
Copy-Item .\dbt_transform\profiles.yml.example .\dbt_transform\profiles.yml
notepad .\dbt_transform\profiles.yml
```

Nếu file `profiles.yml` đã tồn tại, không copy đè; mở và kiểm tra cấu hình.

Tên profile trong `dbt_project.yml` là `tmdb_transform`. Profile mẫu cần có cấu trúc tương đương:

```yaml
tmdb_transform:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: labuser
      password: "<MAT_KHAU_TRONG_ENV>"
      port: 5432
      dbname: warehouse
      schema: dds
      threads: 4
      connect_timeout: 10
```

Thay `<MAT_KHAU_TRONG_ENV>` bằng cùng mật khẩu đã khai báo trong `.env`. Password phải được đặt trong dấu ngoặc kép để YAML luôn đọc là chuỗi, kể cả khi password chỉ gồm chữ số.

Giải thích:

- `host: localhost`: dbt chạy trực tiếp trên Windows host.
- `port: 5432`: port PostgreSQL được Compose publish ra host.
- `dbname: warehouse`, `user: labuser`: khớp database/user của Compose.
- `schema: dds`: schema mặc định; dbt model config điều khiển schema đích của từng layer.

Không commit `dbt_transform/profiles.yml`.

### 7.2. Kiểm tra profile không bị Git theo dõi

Từ repository root:

```powershell
git check-ignore .env .venv dbt_transform/profiles.yml
```

Nếu một file secret chưa được ignore, bổ sung rule vào `.gitignore` trước khi commit bất kỳ thay đổi nào.

### 7.3. Kiểm tra kết nối dbt

Từ repository root:

```powershell
.\.venv\Scripts\dbt.exe debug --project-dir .\dbt_transform --profiles-dir .\dbt_transform
```

Kết quả mong đợi có:

```text
profiles.yml file [OK found and valid]
dbt_project.yml file [OK found and valid]
Registered adapter: postgres=1.11.0
Connection test: [OK connection ok]
All checks passed!
```

Nếu báo `2702 is not of type 'string'` hoặc tương tự, đặt password trong YAML thành chuỗi, ví dụ `password: "2702"`. Nếu báo `password authentication failed`, kiểm tra mật khẩu profile với mật khẩu PostgreSQL của volume đang chạy. Thay đổi `.env` không tự đổi password của PostgreSQL volume đã khởi tạo trước đó.

---

## 8. Quy trình kiểm tra dbt trước khi build

Các lệnh trong phần này chạy từ repository root để thống nhất đường dẫn.

### 8.1. Tắt dbt State nếu môi trường yêu cầu đăng nhập

Trong phiên PowerShell hiện tại, trước các lệnh dbt:

```powershell
$env:DBT_ENGINE_MANAGE_STATE = "0"
```

Trong môi trường đã kiểm thử, package `dbt-state` tự bật và `dbt compile` yêu cầu mở trình duyệt đăng nhập. Biến trên làm State adapter chuyển sang trạng thái disabled, không cần đăng nhập tài khoản dbt State.

Lưu ý: dbt Core 1.12.5 có thể in cảnh báo `EnvironmentVariableNamespaceDeprecation` vì tên biến bắt đầu bằng `DBT_ENGINE`. Cảnh báo này đã xuất hiện trong các lần build/docs của môi trường kiểm thử nhưng không làm build thất bại. **Không dùng `--no-manage-state` với dbt Core 1.12.5**; CLI này báo không hỗ trợ tùy chọn đó.

Biến môi trường chỉ có hiệu lực trong cửa sổ PowerShell hiện tại. Mở terminal mới thì cần đặt lại nếu State lại yêu cầu đăng nhập.

### 8.2. Kiểm tra phiên bản và kết nối

```powershell
.\.venv\Scripts\dbt.exe --version
.\.venv\Scripts\dbt.exe debug --project-dir .\dbt_transform --profiles-dir .\dbt_transform
```

Kết quả phiên bản đã kiểm thử: Core `1.12.5`, adapter `postgres 1.11.0`.

### 8.3. Parse project

```powershell
.\.venv\Scripts\dbt.exe parse --project-dir .\dbt_transform --profiles-dir .\dbt_transform
$LASTEXITCODE
```

Kết quả mong đợi: lệnh hoàn tất và `$LASTEXITCODE` bằng `0`. Lần parse đầu có thể báo không có saved manifest và chuyển sang full parse; đây không phải lỗi.

### 8.4. Liệt kê models và tests

```powershell
.\.venv\Scripts\dbt.exe ls --resource-type model --project-dir .\dbt_transform --profiles-dir .\dbt_transform
.\.venv\Scripts\dbt.exe ls --resource-type test --project-dir .\dbt_transform --profiles-dir .\dbt_transform
```

Kết quả tham chiếu:

- 18 models: 6 staging, 7 dimensions, 4 bridges, 1 fact.
- 3 seeds.
- 87 data tests.
- 2 sources.

### 8.5. Compile SQL/Jinja

```powershell
.\.venv\Scripts\dbt.exe compile --project-dir .\dbt_transform --profiles-dir .\dbt_transform
$LASTEXITCODE
```

Kết quả mong đợi: compile hoàn tất, exit code `0`. Compile không materialize các bảng DDS.

---

## 9. Build toàn bộ Giai đoạn 2

### 9.1. Trước khi chạy

Xác nhận:

- Docker services đang Up.
- PostgreSQL `pg_isready` trả về `accepting connections`.
- Hai raw sources có trong schema `stage`.
- `dbt debug` thành công.
- `dbt parse` và `dbt compile` exit code bằng `0`.
- Profile trỏ đúng database local/dev.

`dbt build` ghi dữ liệu vào database: nạp seeds, tạo/thay thế models và chạy tests theo dependency graph. Chỉ chạy trên database local/dev được phép thay đổi, không chạy trên production.

### 9.2. Lệnh build

Từ repository root:

```powershell
.\.venv\Scripts\dbt.exe build --project-dir .\dbt_transform --profiles-dir .\dbt_transform
```

### 9.3. Kết quả tham chiếu đã kiểm thử

Ở lần build thành công trên PostgreSQL 17:

```text
Found 18 models, 3 seeds, 87 data tests, 2 sources
Finished running 3 seeds, 12 table models, 87 data tests, 6 view models
Completed successfully
Done. PASS=108 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=108
```

Các loại resource trong tổng 108:

| Resource | Số lượng |
|---|---:|
| Seeds | 3 |
| Table models | 12 (7 Dimensions + 4 Bridges + 1 Fact) |
| View models | 6 (2 source staging views + 4 JSON association views) |
| Data tests | 87 |
| **Tổng** | **108** |

### 9.4. Row counts tham chiếu từ log build

| Bảng DDS | Số dòng đã quan sát |
|---|---:|
| `dim_date` | 36.679 |
| `dim_language` | 38 |
| `dim_movie` | 4.803 |
| `dim_company` | 5.048 |
| `dim_country` | 89 |
| `dim_genre` | 21 |
| `dim_keyword` | 9.814 |
| `bridge_movie_company` | 14.028 |
| `bridge_movie_country` | 6.610 |
| `bridge_movie_genre` | 12.188 |
| `bridge_movie_keyword` | 36.194 |
| `fact_movie` | 4.803 |

Các seed đã nạp:

| Seed | Số dòng |
|---|---:|
| `country_region` | 22 |
| `keyword_theme_mapping` | 13 |
| `language_name_mapping` | 84 |

Đây là số dòng quan sát trong snapshot đã kiểm thử. Nếu thành viên sử dụng nguồn hoặc seed khác phiên bản, số dòng Dimension/Bridge có thể khác. Không ép số liệu thành các giá trị kỳ vọng nếu dữ liệu nguồn thay đổi; phải ghi nhận kết quả thực tế.

### 9.5. Kiểm tra build exit code

Ngay sau build:

```powershell
$LASTEXITCODE
```

Kết quả mong đợi: `0`.

Chỉ ghi nhận build thành công khi log có `Completed successfully`, không có `ERROR`, không có test bị skip do dependency lỗi, và exit code bằng `0`.

---

## 10. SQL nghiệm thu DDS sau build

Các câu SQL dưới đây chạy từ PowerShell ở repository root. Mặc định sử dụng `labuser` và `warehouse`; thay nếu cấu hình Compose của nhóm khác.

### 10.1. Liệt kê tables/views của các layer

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT table_schema, table_name, table_type FROM information_schema.tables WHERE table_schema IN ('stage','staging','dds') ORDER BY table_schema, table_name;"
```

Kết quả mong đợi sau build: raw tables ở `stage`; staging views ở `staging`; 12 tables ở `dds`.

### 10.2. Kiểm tra Fact grain và FK logic

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT COUNT(*) AS total_rows, COUNT(DISTINCT f.movie_sk) AS distinct_movies, COUNT(*) FILTER (WHERE m.movie_sk IS NULL) AS missing_movie_fk, COUNT(*) FILTER (WHERE d.date_sk IS NULL) AS missing_date_fk, COUNT(*) FILTER (WHERE l.language_sk IS NULL) AS missing_language_fk FROM dds.fact_movie f LEFT JOIN dds.dim_movie m ON f.movie_sk = m.movie_sk LEFT JOIN dds.dim_date d ON f.date_sk = d.date_sk LEFT JOIN dds.dim_language l ON f.language_sk = l.language_sk;"
```

Kết quả đã xác minh cho snapshot hiện tại:

| Chỉ tiêu | Kết quả |
|---|---:|
| `total_rows` | 4.803 |
| `distinct_movies` | 4.803 |
| `missing_movie_fk` | 0 |
| `missing_date_fk` | 0 |
| `missing_language_fk` | 0 |

### 10.3. Kiểm tra Unknown rows

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT 'dim_date' AS dimension, COUNT(*) AS unknown_rows FROM dds.dim_date WHERE date_sk = -1 UNION ALL SELECT 'dim_language', COUNT(*) FROM dds.dim_language WHERE language_sk = -1 UNION ALL SELECT 'dim_movie', COUNT(*) FROM dds.dim_movie WHERE movie_sk = -1 UNION ALL SELECT 'dim_genre', COUNT(*) FROM dds.dim_genre WHERE genre_sk = -1 UNION ALL SELECT 'dim_company', COUNT(*) FROM dds.dim_company WHERE company_sk = -1 UNION ALL SELECT 'dim_country', COUNT(*) FROM dds.dim_country WHERE country_sk = -1 UNION ALL SELECT 'dim_keyword', COUNT(*) FROM dds.dim_keyword WHERE keyword_sk = -1;"
```

Kết quả đã xác minh:

| Dimension | Số Unknown |
|---|---:|
| `dim_date` | 1 |
| `dim_language` | 1 |
| `dim_movie` | 0 |
| `dim_genre` | 1 |
| `dim_company` | 1 |
| `dim_country` | 1 |
| `dim_keyword` | 1 |

`dim_movie` không có Unknown row theo Data Contract hiện tại; không tự thêm phim giả với SK `-1`.

### 10.4. Kiểm tra tổng WeightFactor của ba Bridge

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT 'bridge_movie_genre' AS bridge, COUNT(*) AS movies_with_invalid_weight FROM (SELECT movie_sk FROM dds.bridge_movie_genre GROUP BY movie_sk HAVING ABS(SUM(weight_factor) - 1.0) > 0.0000001) q UNION ALL SELECT 'bridge_movie_company', COUNT(*) FROM (SELECT movie_sk FROM dds.bridge_movie_company GROUP BY movie_sk HAVING ABS(SUM(weight_factor) - 1.0) > 0.0000001) q UNION ALL SELECT 'bridge_movie_country', COUNT(*) FROM (SELECT movie_sk FROM dds.bridge_movie_country GROUP BY movie_sk HAVING ABS(SUM(weight_factor) - 1.0) > 0.0000001) q;"
```

Kết quả mong đợi: cả ba bridge có `movies_with_invalid_weight = 0`.

`bridge_movie_keyword` không có `weight_factor` theo Data Contract; không chạy phép kiểm tra trọng số cho bridge này.

Kiểm tra cột `weight_factor` không tồn tại trong keyword bridge:

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT column_name FROM information_schema.columns WHERE table_schema = 'dds' AND table_name = 'bridge_movie_keyword' AND column_name = 'weight_factor';"
```

Kết quả mong đợi: `0 rows`.

### 10.5. Kiểm tra Physical Foreign Keys

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT conrelid::regclass AS child_table, conname, confrelid::regclass AS referenced_table, pg_get_constraintdef(oid) AS definition FROM pg_constraint WHERE contype = 'f' AND connamespace = 'dds'::regnamespace ORDER BY 1, 2;"
```

Kết quả đã xác minh có **11 physical foreign keys**:

- Fact: 3 FK tới `dim_movie`, `dim_date`, `dim_language`.
- Bridge Company: 2 FK.
- Bridge Country: 2 FK.
- Bridge Genre: 2 FK.
- Bridge Keyword: 2 FK.

Tên constraint có thể chứa hậu tố `__dbt_tmp` do cách dbt materialize bảng. Điều cần kiểm tra là `referenced_table` trỏ đúng các bảng thật trong schema `dds`, không phải tên bảng tạm.

Kiểm tra PK/UNIQUE/CHECK nếu cần:

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT tc.table_name, tc.constraint_type, tc.constraint_name FROM information_schema.table_constraints tc WHERE tc.table_schema = 'dds' ORDER BY tc.table_name, tc.constraint_type;"
```

### 10.6. Kiểm tra DEFAULT của vote_count

```powershell
docker compose exec postgres psql -U labuser -d warehouse -c "SELECT column_name, data_type, is_nullable, column_default FROM information_schema.columns WHERE table_schema = 'dds' AND table_name = 'fact_movie' AND column_name = 'vote_count';"
```

Kết quả mong đợi: kiểu `integer`, `is_nullable = NO`, `column_default` thể hiện giá trị `0` (cách PostgreSQL hiển thị biểu thức default có thể khác nhau).

---

## 11. Kiểm tra chạy lại (rebuild) và dbt Documentation

### 11.1. Rebuild lần hai

Sau khi build lần đầu và đã có các bảng DDS với physical FKs, chạy lại chính lệnh build trên cùng database local/dev:

```powershell
.\.venv\Scripts\dbt.exe build --project-dir .\dbt_transform --profiles-dir .\dbt_transform
```

Không DROP schema, không xóa volume và không xóa FK trước khi thử. Mục tiêu là kiểm tra dbt có thay thế các bảng hiện hữu và giữ khả năng build lại hay không.

Kết quả tham chiếu lần rebuild thứ hai đã xác minh:

```text
Completed successfully
Done. PASS=108 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=108
```

Nếu thành viên gặp lỗi FK/relation khi rebuild, lưu toàn bộ log và dừng để phân tích; không tự ý xóa physical constraints.

### 11.2. Generate dbt Documentation

```powershell
.\.venv\Scripts\dbt.exe docs generate --project-dir .\dbt_transform --profiles-dir .\dbt_transform
```

Kiểm tra file:

```powershell
Test-Path .\dbt_transform\target\index.html
Test-Path .\dbt_transform\target\manifest.json
Test-Path .\dbt_transform\target\catalog.json
```

Kết quả mong đợi: cả ba trả về `True`.

### 11.3. Xem giao diện và Lineage Graph

```powershell
.\.venv\Scripts\dbt.exe docs serve --project-dir .\dbt_transform --profiles-dir .\dbt_transform --port 8081
```

Mở `http://localhost:8081`.

Dùng cổng `8081` nếu `8080` đang được Airflow hoặc một dịch vụ khác sử dụng. Giữ terminal docs serve mở trong lúc xem; nhấn `Ctrl+C` để dừng server.

Trong dbt Docs:

- Tab **Project** hiển thị cấu trúc models, seeds và macros.
- Tab **Database** hiển thị các relations trong PostgreSQL.
- **Graph Exploration** hiển thị lineage/dependency giữa Source, staging, dimensions, bridges và fact.

---

## 12. Data Contract và bàn giao cho Giai đoạn 3

Phần này là tài liệu nền cho thành viên phụ trách Power BI/BI ở Giai đoạn 3. Khi dùng dữ liệu thật, cần đối chiếu lại schema bằng `information_schema` và dữ liệu bằng SQL; không chỉ dựa trên mô tả dưới đây.

### 12.1. Danh sách bảng DDS

| Nhóm | Bảng | Grain/ý nghĩa |
|---|---|---|
| Dimension | `dim_movie` | Một dòng cho mỗi phim; khóa tự nhiên `movie_nk` |
| Dimension | `dim_date` | Một dòng cho mỗi ngày trong calendar; Unknown `date_sk = -1` |
| Dimension | `dim_language` | Một dòng cho mỗi mã ngôn ngữ; Unknown `language_sk = -1` |
| Dimension | `dim_genre` | Một dòng cho mỗi genre; Unknown `genre_sk = -1` |
| Dimension | `dim_company` | Một dòng cho mỗi company; Unknown `company_sk = -1` |
| Dimension | `dim_country` | Một dòng cho mỗi country; Unknown `country_sk = -1` |
| Dimension | `dim_keyword` | Một dòng cho mỗi keyword; Unknown `keyword_sk = -1` |
| Bridge | `bridge_movie_genre` | Một liên kết Movie–Genre; có WeightFactor |
| Bridge | `bridge_movie_company` | Một liên kết Movie–Company; có WeightFactor |
| Bridge | `bridge_movie_country` | Một liên kết Movie–Country; có WeightFactor |
| Bridge | `bridge_movie_keyword` | Một liên kết Movie–Keyword; không có WeightFactor |
| Fact | `fact_movie` | **Một dòng cho một Movie**; `movie_sk` là PK đồng thời FK tới `dim_movie` |

### 12.2. FactMovie — grain và measures

Grain: một dòng hợp lệ cho một Movie ID từ `tmdb_5000_movies.csv`. Snapshot này có 4.803 dòng.

Các trường tài chính:

| Cột | Quy tắc |
|---|---|
| `budget` | `DECIMAL(18,0)`; nguồn bằng 0 được chuyển thành NULL |
| `revenue` | `DECIMAL(18,0)`; nguồn bằng 0 được chuyển thành NULL |
| `profit` | `revenue - budget`; NULL nếu một trong hai đầu vào NULL |
| `roi` | `profit / budget`; NULL nếu budget NULL hoặc `<= 0` |
| `is_finance_valid` | 1 khi cả budget và revenue đều > 0; ngược lại 0 |
| `is_revenue_over_budget` | 1 khi finance hợp lệ và revenue > budget; ngược lại 0 |
| `movie_count` | Luôn bằng 1 |

**ROI được lưu dưới dạng tỷ lệ thập phân, không nhân 100.** Ví dụ `roi = 0.5` tương đương `50%`; khi hiển thị trong Power BI, format measure/column thành Percentage thay vì nhân thêm 100 trong DAX.

Các measure khác:

- `runtime NUMERIC(5,1)` — thời lượng phút.
- `popularity DECIMAL(12,6)` — độ phổ biến.
- `vote_average DECIMAL(4,1)` — NULL khi `vote_count = 0`.
- `vote_count INT` — NULL nguồn chuyển thành 0; cột có `DEFAULT 0` sau dbt post-hook.

Gợi ý khi tổng hợp:

- Budget, Revenue và Profit có thể SUM ở cấp Fact.
- ROI không additive; dùng MEDIAN ở cấp phim hoặc tính ROI tổng hợp bằng `SUM(profit) / SUM(budget)` với cùng tập phim hợp lệ.
- Không lấy AVG/ SUM ROI một cách tùy tiện để thay cho ROI tổng hợp.
- Khi tính tỷ lệ vượt ngân sách: `SUM(is_revenue_over_budget) / SUM(is_finance_valid)` trên tập dữ liệu thích hợp.

### 12.3. Bridge và cách tổng hợp đa trị

Ba bridge có trọng số:

- `bridge_movie_genre`
- `bridge_movie_company`
- `bridge_movie_country`

Với mỗi phim trong mỗi bridge, `weight_factor = 1/k`, trong đó `k` là số liên kết của phim ở chiều tương ứng. Tổng weight factor theo phim bằng 1.

Hai phương pháp nghiệp vụ:

1. **Full Credit:** gán toàn bộ giá trị phim cho từng thành viên liên kết. Phù hợp với các phân tích trung vị, ROI và số phim theo thành viên, nhưng khi cộng tổng doanh thu/lợi nhuận qua tất cả thành viên thì một phim đa trị có thể bị đếm nhiều lần.
2. **Fractional Allocation:** nhân measure additive với `weight_factor` trước khi SUM. Ví dụ `Allocated Profit = SUM(profit * weight_factor)`. Cách này giúp tổng phân bổ giữa các thành viên của một chiều khớp với tổng phim gốc, trong sai số làm tròn.

`bridge_movie_keyword` không có `weight_factor`. Keyword là tag; một phim có thể có nhiều keyword và các theme có thể giao nhau. Khi đếm phim theo keyword/theme, dùng `COUNT(DISTINCT movie_sk)`. Không kỳ vọng tổng Profit/Revenue giữa mọi keyword cộng lại bằng tổng Fact vì không có trọng số phân bổ ở bridge này.

### 12.4. Unknown handling

Các dimension hiện có dòng Unknown SK `-1`: Date, Language, Genre, Company, Country và Keyword. `dim_movie` không có dòng Unknown theo Data Contract hiện tại.

Quy tắc tham chiếu:

- Thiếu `release_date` → `date_sk = -1`.
- Không có genre/company/country hợp lệ → bridge tương ứng có association tới dimension Unknown với `weight_factor = 1.0`.
- Unknown language → `language_sk = -1`.
- Keyword chưa map theme → `theme_group = 'Other'`.

### 12.5. Mapping và các giới hạn cần biết

Các seed trong phiên bản đã kiểm thử:

| Seed | Quy mô tham chiếu | Quy tắc fallback |
|---|---:|---|
| `country_region.csv` | 22 dòng | Country không được map có Region `Unknown` |
| `keyword_theme_mapping.csv` | 13 dòng | Keyword chưa map theme thành `Other` |
| `language_name_mapping.csv` | 84 dòng | Language code chưa có mapping được giữ nguyên làm tên hiển thị |

Các mapping Country/Keyword là mapping biên tập ban đầu, không bao phủ toàn bộ thế giới/từ khóa. Language name chưa đảm bảo mọi mã đều có tên đầy đủ. Khi Giai đoạn 3 cần tên hiển thị hoàn chỉnh, hãy thống kê mã chưa map và đề xuất cập nhật seed; không tự suy đoán tên ngôn ngữ.

### 12.6. Surrogate keys và giới hạn full rebuild

Một số Dimension sinh SK bằng `row_number()` theo thứ tự natural key. Cách này phù hợp với dataset snapshot và quy trình full rebuild đã kiểm thử. Tuy nhiên, nếu bổ sung natural key mới đứng trước các key hiện tại, SK có thể thay đổi sau full rebuild.

Vì vậy:

- Không dùng SK như định danh bền vững bên ngoài lần build hiện tại.
- Dùng NK (`movie_nk`, `genre_nk`, `company_nk`, `keyword_nk`, `language_nk`,...) để đối chiếu nguồn/nghiệp vụ.
- Nếu Giai đoạn 3 mở rộng thành pipeline incremental/historical, cần thiết kế chiến lược surrogate key ổn định trước khi giữ dữ liệu lịch sử hoặc tạo quan hệ ngoài DDS.

### 12.7. Phân biệt `stage` và `staging`

- `stage.stg_tmdb_movies`, `stage.stg_tmdb_credits`: bảng raw do Mage nạp.
- `staging.stg_tmdb_movies`, `staging.stg_tmdb_credits`: dbt views chuẩn hóa Movies/Credits.
- `staging.stg_movie_genres`, `staging.stg_movie_companies`, `staging.stg_movie_countries`, `staging.stg_movie_keywords`: dbt views parse các quan hệ JSON.
- `dds`: các bảng Dimension, Bridge và Fact dùng cho phân tích.

Đừng nhầm hai schema `stage` và `staging` khi viết SQL/DAX hoặc khi cấu hình Power BI.

---

## 13. Hạn chế và lưu ý vận hành

1. **Incremental hiện là mô phỏng batch.** Theo mô tả Mage hiện tại, batch được append nguyên trạng, chưa lọc LSET và chưa deduplicate; nhánh cập nhật watermark không phụ thuộc vào kết quả exporter. Không mô tả pipeline này là retry-safe/production incremental nếu chưa sửa graph và kiểm thử lại.
2. **Dataset TMDB 5000 là snapshot tĩnh.** Các chỉ số popularity, vote average và vote count là ảnh chụp tại thời điểm thu thập, không phải chuỗi thời gian.
3. **JSON nguồn cần được kiểm soát.** Các cột JSON đang là text trong raw staging. Nếu có JSON sai cú pháp hoặc sai cấu trúc, cần xem source tests và lỗi build thực tế; không âm thầm bỏ qua dữ liệu lỗi.
4. **Mapping có phạm vi giới hạn.** Country/Keyword/Language cần được bổ sung khi nghiệp vụ yêu cầu độ bao phủ cao hơn.
5. **SK có thể đổi khi full rebuild** nếu natural key set/thứ tự thay đổi; xem Mục 12.6.
6. **Physical FK không thay thế dbt tests.** Duy trì cả database constraints và data tests.
7. Chỉ chạy `dbt build` trên local/dev. Không chạy trên production.

---

## 14. Lưu log và ảnh minh chứng cho báo cáo

Khuyến nghị tạo thư mục lưu bằng chứng, ví dụ:

```powershell
New-Item -ItemType Directory -Force .\docs\evidence\phase2 | Out-Null
```

Có thể lưu log build bằng PowerShell:

```powershell
& .\.venv\Scripts\dbt.exe build --project-dir .\dbt_transform --profiles-dir .\dbt_transform 2>&1 | Tee-Object -FilePath .\docs\evidence\phase2\dbt-build.log
$buildExitCode = $LASTEXITCODE
"dbt build exit code: $buildExitCode" | Add-Content .\docs\evidence\phase2\dbt-build.log
```

Ảnh minh chứng nên có:

1. Docker Compose services `mage` và `postgres` đang Up.
2. PostgreSQL readiness và danh sách schema.
3. Source table counts, NULL/duplicate IDs và Movies–Credits matching.
4. `dbt --version` và `dbt debug`.
5. `dbt parse`/`dbt compile` thành công.
6. `dbt build` lần đầu và lần rebuild thứ hai.
7. SQL Fact grain/FK validation.
8. Physical FK query.
9. Unknown rows và bridge weight validation.
10. dbt Docs overview và Lineage Graph.

Không chụp hoặc lưu `.env`, password, `profiles.yml` thật hay thông tin xác thực.

---

## 15. Checklist nhanh cho thành viên mới pull code

- [ ] Pull đúng branch/code mới nhất; working tree không có thay đổi cần bảo toàn.
- [ ] Cài Git, Docker Desktop và Python 3.12.x.
- [ ] Tạo `.venv` và cài `dbt-core==1.12.5`, `dbt-postgres==1.11.0`.
- [ ] Tạo `.env` riêng; không commit secrets.
- [ ] Xác nhận Compose chỉ mount `postgres/init/01_init.sql`.
- [ ] Chạy Docker Compose và kiểm tra PostgreSQL/Mage.
- [ ] Xác nhận bốn schema và watermark; với volume cũ chỉ reapply `01_init.sql` khi cần.
- [ ] Chạy Mage Full Load và xác nhận `stage.stg_tmdb_movies`, `stage.stg_tmdb_credits`.
- [ ] Tạo `dbt_transform/profiles.yml` từ file mẫu và kiểm tra `.gitignore`.
- [ ] Chạy `dbt debug`, `dbt parse`, `dbt ls`, `dbt compile`.
- [ ] Chạy `dbt build` trên local/dev và lưu log.
- [ ] Chạy SQL validation Fact, Unknown, Bridge weights, physical FKs và vote_count default.
- [ ] Chạy rebuild lần hai.
- [ ] Chạy `dbt docs generate` và xem Lineage Graph.
- [ ] Ghi nhận kết quả thực tế; không sao chép số dòng tham chiếu nếu dataset khác.

## 16. Trạng thái triển khai đã xác minh của phiên bản hiện tại

Các kết quả sau là bằng chứng từ một lần triển khai trên Windows 11, Docker Compose, PostgreSQL 17 và dbt chạy trong `.venv`:

| Hạng mục | Kết quả đã xác minh |
|---|---|
| Python | 3.12.8 |
| dbt Core | 1.12.5 |
| dbt-postgres | 1.11.0 |
| PostgreSQL | 17 |
| Database/user | `warehouse` / `labuser` |
| Source Movies/Credits | 4.803 / 4.803 dòng trong snapshot đã kiểm thử |
| Movies có Credits | 4.803; thiếu Credits 0 |
| Credits mồ côi | 0 |
| dbt models | 18 |
| dbt seeds | 3 |
| dbt data tests | 87 |
| dbt build lần đầu | 108 PASS; 0 ERROR; 0 SKIP |
| dbt build lần hai | 108 PASS; 0 ERROR; 0 SKIP |
| FactMovie | 4.803 dòng; 4.803 Movie SK khác nhau |
| Missing Fact FKs trong SQL validation | 0 cho Movie/Date/Language |
| Physical Foreign Keys | 11 |
| Unknown rows | 1 ở Date, Language, Genre, Company, Country, Keyword; 0 ở Movie |
| dbt Documentation | `index.html`, `manifest.json`, `catalog.json` được tạo; giao diện docs mở được trên port 8081 |

Một cảnh báo deprecation về biến `DBT_ENGINE_MANAGE_STATE` có xuất hiện trong log khi tắt dbt State. Nó không làm các lần build/docs nêu trên thất bại. Thành viên mới nên ghi lại warning nếu xuất hiện; không tuyên bố mọi log hoàn toàn không cảnh báo.

**Khi triển khai trên máy khác, kết quả thực tế của máy đó là căn cứ nghiệm thu.** Các row counts và kết quả trong Mục 16 là số tham chiếu từ lần chạy đã xác minh, không thay thế việc chạy lại kiểm tra.
