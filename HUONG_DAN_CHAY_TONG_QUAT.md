# Hướng dẫn chạy tổng TMDB 5000

Tài liệu này là lộ trình chạy duy nhất cho một máy Windows. Các file README trong Mage, dbt, Power BI và thư mục test chỉ cung cấp hướng dẫn chuyên sâu cho từng phần.

**Luồng bắt buộc:**

```text
Chuẩn bị CSV -> Docker/PostgreSQL -> Mage Full Load
-> dbt build -> Power BI Refresh -> chạy test
```

Không chạy các bước xếp chồng trên cùng một database khi chưa lưu snapshot/evidence. Để demo chính, dùng PostgreSQL/Mage mặc định trên `5432/6789`. Để nghiệm thu hoặc tạo bằng chứng kịch bản Mage, dùng môi trường test cô lập `55432/16789`.

## 1. Phần mềm cần có

- Docker Desktop, bật Linux containers/WSL2.
- Python 3.12.
- PowerShell.
- Power BI Desktop nếu cần mở hoặc Refresh dashboard.
- Git nếu clone/pull repository.

Kiểm tra:

```powershell
git --version
docker --version
docker compose version
py -3.12 --version
```

## 2. Chuẩn bị repository

```powershell
cd D:\DE-MiniProject-TMDB

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}

if (-not (Test-Path .venv)) {
    py -3.12 -m venv .venv
}

$py = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $py -m pip install --upgrade pip
& $py -m pip install "dbt-core==1.12.5" "dbt-postgres==1.11.0"
& $py -m pip install -r .\test\acceptance\requirements.txt
```

### CSV bắt buộc

Đặt ba file tại `data/raw/`:

| File | Dùng cho |
|---|---|
| `tmdb_5000_movies.csv` | Mage full load Movies |
| `tmdb_5000_credits.csv` | Mage full load Credits |
| `tmdb_new_batch.csv` | Pipeline incremental và test |

Tệp dữ liệu thô không được commit. File trong bản nộp có thể không chứa dữ liệu; tự tải đúng bộ TMDB trước khi chạy.

### Cấu hình mật khẩu và kết nối

Sửa file [.env.example](.env.example), lưu/copy thành `.env`:

```dotenv
POSTGRES_DB=warehouse
POSTGRES_USER=labuser
POSTGRES_PASSWORD=mật_khẩu_của_nhóm
```

Tạo `mage_pipeline/io_config.yaml`:

```yaml
version: 0.1.1
default:
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: warehouse
  POSTGRES_SCHEMA: stage
  POSTGRES_USER: labuser
  POSTGRES_PASSWORD: "mật_khẩu_giống_ở_.env"
  POSTGRES_HOST: postgres
  POSTGRES_PORT: 5432
```

Mage chạy trong container, nên host là `postgres`, không dùng `localhost`.

Tạo profile dbt:

```powershell
Copy-Item .\dbt_transform\profiles.yml.example .\dbt_transform\profiles.yml
```

Trong `dbt_transform/profiles.yml`, dùng `host: localhost`, `port: 5432`, `dbname: warehouse`, cùng `user/password` với `.env`.

**Không commit** `.env`, `io_config.yaml`, `profiles.yml` hoặc dữ liệu nguồn.

## 3. Khởi động Mage và PostgreSQL

```powershell
docker info
docker compose up -d
docker compose ps
docker compose exec postgres pg_isready -U labuser -d warehouse
```

Kết quả mong đợi: Mage và PostgreSQL ở trạng thái `Up` hoặc `running`, PostgreSQL báo `accepting connections`.

Nếu chỉ cần PostgreSQL kiểm dữ liệu cũ:

```powershell
docker compose up -d postgres
docker compose exec postgres pg_isready -U labuser -d warehouse
```

Không dùng `docker compose down -v` để sửa lỗi kết nối; lệnh này xóa volume dữ liệu PostgreSQL.

## 4. Chạy Mage Full Load

1. Mở `http://localhost:6789`.
2. Chọn pipeline `tmdb_ingestion`.
3. Chạy toàn pipeline; không chạy exporter hoặc transformer riêng trước loader.
4. Đợi cả nhánh Movies và Credits hoàn tất.
5. Ghi lại run status, run ID và số dòng nạp nếu cần quay video/demo.

Pipeline này nạp dữ liệu:

```text
Movies CSV  -> stage.stg_tmdb_movies
Credits CSV -> stage.stg_tmdb_credits
```

Sau khi Full Load thành công mới tiếp tục dbt.

## 5. Build Data Warehouse bằng dbt

Chạy từ thư mục gốc:

```powershell
& .\.venv\Scripts\dbt.exe debug `
    --project-dir .\dbt_transform `
    --profiles-dir .\dbt_transform

& .\.venv\Scripts\dbt.exe build `
    --project-dir .\dbt_transform `
    --profiles-dir .\dbt_transform

& .\.venv\Scripts\dbt.exe docs generate `
    --project-dir .\dbt_transform `
    --profiles-dir .\dbt_transform
```

Luồng dbt:

```text
stage -> staging views -> seed mappings -> dimensions -> bridges -> fact_movie
```

Lệnh `build` phải tạo các bảng dưới schema `dds`, ít nhất:

- `dds.fact_movie`
- `dds.dim_movie`
- `dds.dim_date`
- `dds.dim_language`
- `dds.dim_genre`
- `dds.dim_company`
- `dds.dim_country`
- `dds.dim_keyword`
- Các bảng `dds.bridge_movie_*`

Chi tiết mô hình xem [Schema_Report.md](Schema_Report.md).

**Lưu ý:** Docker chỉ tự chạy `postgres/init/01_init.sql` khi tạo volume mới. Không chạy `postgres/init/02_dds_schema.sql` trước dbt; file đó là DDL tham chiếu.

## 6. Chạy incremental (tùy chọn demo)

Chỉ chạy sau khi đã có stage và dbt DDS baseline.

1. Kiểm tra `tmdb_new_batch.csv` tồn tại trong `data/raw/`.
2. Mở Mage `http://localhost:6789`.
3. Chạy toàn pipeline `tmdb_incremental`.
4. Đợi exporter thành công trước khi xem watermark.
5. Chạy lại dbt build để cập nhật DDS.
6. Sau đó mới Refresh hoặc mở lại Power BI.

Incremental hiện là mô phỏng batch CSV. Nó không lọc batch theo LSET/CET và không tự chạy dbt hoặc Refresh Power BI.

## 7. Refresh và kiểm tra Power BI

1. Mở [powerbi_dashboard/TMDB_Movie_Dashboard.pbix](powerbi_dashboard/TMDB_Movie_Dashboard.pbix).
2. Vào `File -> Options and settings -> Data source settings`.
3. Kiểm tra server `localhost:5432` và database `warehouse`.
4. Chọn `Home -> Refresh`.
5. Sau Refresh thành công, thử bộ lọc và mở cả 4 trang.
6. Lưu PBIX nếu đã xác nhận snapshot mới.

Nếu dùng môi trường test DB `55432`, PBIX phải dùng source DB test đúng hoặc bản sao PBIX riêng cho test.

PBIX mở được không chứng minh Refresh thành công, vì file có thể chứa dữ liệu Import cũ. Hướng dẫn chi tiết tại [powerbi_dashboard/README.md](powerbi_dashboard/README.md).

## 8. Chạy test nhanh

Kiểm tra database chính ở chế độ chỉ đọc:

```powershell
$py = (Resolve-Path .\.venv\Scripts\python.exe).Path

& $py .\test\acceptance\preflight.py `
    --mode readonly `
    --env-file .env

& $py .\test\acceptance\run.py `
    --mode readonly `
    --section all `
    --env-file .env
```

Chỉ dùng `--snapshot full` khi vừa hoàn thành Full Load và chưa chạy incremental/append:

```powershell
& $py .\test\acceptance\run.py `
    --mode readonly `
    --section all `
    --env-file .env `
    --snapshot full
```

Nếu không chắc database đang ở trạng thái nào, không dùng `--snapshot full`.

## 9. Chạy test trên môi trường cô lập

Môi trường test dùng PostgreSQL `55432` và Mage `16789`, không dùng stack chính để tạo kịch bản lỗi.

```powershell
$py = (Resolve-Path .\.venv\Scripts\python.exe).Path

& $py .\test\acceptance\isolation.py prepare
& $py .\test\acceptance\isolation.py up
& $py .\test\acceptance\isolation.py ps
```

Mở Mage test tại `http://127.0.0.1:16789`, chạy `tmdb_ingestion`, sau đó build dbt test:

```powershell
& $py .\test\acceptance\isolation.py dbt-build

& $py .\test\acceptance\preflight.py `
    --mode integration

& $py .\test\acceptance\run.py `
    --mode integration `
    --section all `
    --approved `
    --snapshot full
```

Để kiểm replay, batch mới, batch rỗng hoặc lỗi exporter, đọc phần scenarios trong [test/HUONG_DAN_CHAY_TEST.md](test/HUONG_DAN_CHAY_TEST.md). Luôn dùng pipeline Mage thật và lưu run ID/run log, không chỉ gọi hàm Python rồi coi là evidence.

## 10. Kiểm tra kết quả

Kết quả nằm dưới `test/results/acceptance_<UTC>_<id>/`.

| Trạng thái | Cách hiểu |
|---|---|
| PASS | Truy vấn/assertion đạt |
| FAIL | Truy vấn/assertion không đạt |
| BLOCKED | Thiếu điều kiện runtime/evidence |
| SKIPPED | Không chạy trong mode hiện tại |
| INFO | Quan sát tham chiếu, không thay bằng chứng PASS |

Report chính cần đọc:

- `REPORT.md`
- `result.json`
- `junit.xml`
- `pytest_output.txt`

SQL tham chiếu không tự chứng minh DAX hoặc thao tác trên Power BI đã đúng.

## 11. Thứ tự ghi evidence/release

1. Lưu log Mage Full Load.
2. Lưu output `dbt build` và `dbt docs generate`.
3. Lưu report SQL/dbt test hoặc acceptance test.
4. Chụp 4 trang Power BI sau Refresh, kèm bộ lọc và thời điểm.
5. Ghi rõ Generative AI chưa triển khai.
6. Không sửa report FAIL cũ thành PASS.
7. Đóng gói source, tài liệu, PDF, PBIX và CSV bắt buộc; không đóng gói `.git`, `.venv`, cache hoặc `.env`.
