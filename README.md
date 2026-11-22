# TMDB 5000 — Movie Data Warehouse và Business Intelligence

Repository của **Nhóm 5** triển khai pipeline dữ liệu và dashboard phân tích hiệu quả tài chính điện ảnh trên bộ dữ liệu TMDB 5000.

**Luồng tổng:** `CSV TMDB -> Mage.ai -> PostgreSQL stage -> dbt staging/dds -> Power BI`

> Nếu cô/anh chấm lần đầu, hãy mở [HUONG_DAN_CHAY_TONG_QUAT.md](HUONG_DAN_CHAY_TONG_QUAT.md). File này chỉ trình bày thứ tự chạy hệ thống, không cần tra từng README của Mage/dbt/Power BI.

## 1. Sản phẩm bàn giao

| Sản phẩm | Vị trí |
|---|---|
| Dashboard tương tác | [powerbi_dashboard/TMDB_Movie_Dashboard.pbix](powerbi_dashboard/TMDB_Movie_Dashboard.pbix) |
| Bản PDF dashboard | [docs/diagrams/TMDB_Movie_Dashboard.pdf](docs/diagrams/TMDB_Movie_Dashboard.pdf) |
| Báo cáo tổng hợp | [docs/reports/BaoCao_TongHop_TMDB_Nhom5.pdf](docs/reports/BaoCao_TongHop_TMDB_Nhom5.pdf) |
| Phụ lục công thức DAX | [docs/reports/Phu_luc_C_60_DAX.pdf](docs/reports/Phu_luc_C_60_DAX.pdf) |
| Phụ lục kiểm chứng SQL-Power BI | [docs/reports/Phu_luc_D_Kiem_chung_PostgreSQL_PowerBI.pdf](docs/reports/Phu_luc_D_Kiem_chung_PostgreSQL_PowerBI.pdf) |
| Data Contract / mô hình dữ liệu | [Schema_Report.md](Schema_Report.md) |
| Kết quả kiểm chứng Data Warehouse | [DW_Verification_Report.md](DW_Verification_Report.md) |
| Hướng dẫn xem tài liệu | [HUONG_DAN_DOC_TAI_LIEU.md](HUONG_DAN_DOC_TAI_LIEU.md) |
| Hướng dẫn chạy toàn hệ thống | [HUONG_DAN_CHAY_TONG_QUAT.md](HUONG_DAN_CHAY_TONG_QUAT.md) |
| Hướng dẫn chạy test chi tiết | [test/HUONG_DAN_CHAY_TEST.md](test/HUONG_DAN_CHAY_TEST.md) |

Dashboard có 4 trang:

1. Movie Portfolio Overview
2. Financial Drivers
3. Companies & Countries
4. Audience & Ratings

Các trang Dashboard, mốc KPI và quy tắc phân bổ được mô tả trong [powerbi_dashboard/README.md](powerbi_dashboard/README.md).

## 2. Kiến trúc chạy

| Thành phần | Trách nhiệm | Tài liệu riêng |
|---|---|---|
| Mage.ai | Đọc CSV, làm sạch cơ bản, nạp/append dữ liệu vào schema `stage` | [mage_pipeline/README_Ingestion.md](mage_pipeline/README_Ingestion.md) |
| PostgreSQL | Lưu `stage`, `staging`, `dds`, `control`; phục vụ dbt và Power BI | [postgres/](postgres/) |
| dbt | Chuẩn hóa dữ liệu, tạo 7 Dimension, 4 Bridge, 1 Fact và chạy test | [dbt_transform/README.md](dbt_transform/README.md) |
| Power BI | Trực quan hóa, semantic model và DAX | [powerbi_dashboard/README.md](powerbi_dashboard/README.md) |
| Bộ acceptance test | Kiểm tra source, pipeline, dbt, DW, Power BI và ghi evidence | [test/HUONG_DAN_CHAY_TEST.md](test/HUONG_DAN_CHAY_TEST.md) |

**Mô hình DDS:**

- 7 Dimension: Movie, Date, Language, Genre, Company, Country, Keyword.
- 4 Bridge: Movie-Genre, Movie-Company, Movie-Country, Movie-Keyword.
- 1 Fact: `dds.fact_movie`, mỗi dòng tương ứng một bộ phim.
- Dimension/Bridge/Fact được dbt tạo và quản lý vòng đời.

## 3. Bắt đầu nhanh

Yêu cầu: Windows 10/11, Docker Desktop bật Linux containers, Python 3.12 và Power BI Desktop nếu xem/dashboard.

### Bước 1 - Chuẩn bị môi trường

```powershell
Set-Location D:\DE-MiniProject-TMDB
Copy-Item .env.example .env
py -3.12 -m venv .venv

$py = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $py -m pip install --upgrade pip
& $py -m pip install "dbt-core==1.12.5" "dbt-postgres==1.11.0"
& $py -m pip install -r .\test\acceptance\requirements.txt
```

Sửa mật khẩu trong `.env`. CSV dữ liệu thô đặt vào `data/raw/`:

- `tmdb_5000_movies.csv`
- `tmdb_5000_credits.csv`
- `tmdb_new_batch.csv` nếu chạy incremental hoặc test đầy đủ

### Bước 2 - Cấu hình Mage và dbt

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

Tạo profile dbt:

```powershell
Copy-Item .\dbt_transform\profiles.yml.example .\dbt_transform\profiles.yml
```

Sửa `host`, `user`, `password`, `port`, `dbname` trong profile sao cho khớp `.env`. Máy chạy dbt dùng `localhost`; Mage chạy trong Docker dùng `postgres`.

Không commit `.env`, `io_config.yaml`, `profiles.yml`, mật khẩu hoặc dữ liệu thô.

### Bước 3 - Khởi động và nạp dữ liệu

```powershell
docker compose up -d
docker compose ps
docker compose exec postgres pg_isready -U labuser -d warehouse
```

Mở Mage tại `http://localhost:6789`, chạy toàn pipeline `tmdb_ingestion`, đợi cả nhánh Movies và Credits thành công.

Sau đó build Data Warehouse:

```powershell
& .\.venv\Scripts\dbt.exe debug --project-dir .\dbt_transform --profiles-dir .\dbt_transform
& .\.venv\Scripts\dbt.exe build --project-dir .\dbt_transform --profiles-dir .\dbt_transform
& .\.venv\Scripts\dbt.exe docs generate --project-dir .\dbt_transform --profiles-dir .\dbt_transform
```

`postgres/init/01_init.sql` được Docker chạy khi tạo volume mới. `postgres/init/02_dds_schema.sql` là DDL tham chiếu; không chạy trước dbt và không coi đó là thay thế cho `dbt build`.

### Bước 4 - Mở và Refresh Power BI

Mở [powerbi_dashboard/TMDB_Movie_Dashboard.pbix](powerbi_dashboard/TMDB_Movie_Dashboard.pbix), kiểm `Data source settings`, kết nối đúng PostgreSQL và chọn `Home -> Refresh`.

PBIX có thể mở cùng dữ liệu Import đã lưu dù container đang tắt. Chỉ khi Refresh thành công mới xem đó là dữ liệu mới lấy từ PostgreSQL.

### Bước 5 - Chạy kiểm thử

```powershell
& $py .\test\acceptance\preflight.py --mode readonly --env-file .env
& $py .\test\acceptance\run.py --mode readonly --section all --env-file .env
```

Để integration, rebuild và kịch bản Mage cô lập, xem [HUONG_DAN_CHAY_TONG_QUAT.md](HUONG_DAN_CHAY_TONG_QUAT.md) hoặc [test/HUONG_DAN_CHAY_TEST.md](test/HUONG_DAN_CHAY_TEST.md).

## 4. Phân biệt trạng thái kiểm thử

| Trạng thái | Ý nghĩa |
|---|---|
| PASS | Assertion đạt trong phạm vi test |
| FAIL | Assertion không đạt hoặc evidence không phù hợp |
| BLOCKED | Thiếu điều kiện/runtime/evidence |
| SKIPPED | Không chạy trong mode được chọn |
| INFO | Quan sát hoặc số liệu tham chiếu, không phải chứng minh đạt |

Luồng test tạo report tại `test/results/acceptance_<UTC>_<id>/`. Không tự động xem report cũ là kết quả của lần chạy hiện tại.

## 5. Cấu trúc thư mục

| Thư mục | Nội dung |
|---|---|
| `mage_pipeline/` | Loaders, transformers, exporters và pipeline Mage |
| `dbt_transform/` | Models, seeds, macros, tests, profile mẫu |
| `postgres/init/` | SQL khởi tạo và DDL tham chiếu |
| `postgres/verify_dds_dw.sql` | SQL kiểm chứng kho dữ liệu |
| `powerbi_dashboard/` | PBIX và hướng dẫn Refresh |
| `docs/` | PDF dashboard, báo cáo và phụ lục |
| `test/acceptance/` | Runner, môi trường cô lập, scenario và checklist |
| `test/unit/` | Test hồi quy cho harness |
| `test/results/` | Evidence của các lượt test được lưu |
| `data/raw/` | CSV nguồn cục bộ; không commit |

## 6. Giới hạn cần trình bày

- Generative AI 3.5 **chưa triển khai** và không được trình bày là đã hoàn thành.
- Incremental hiện mô phỏng batch CSV, có upsert theo `id` và cập nhật watermark sau exporter; loader chưa lọc bản ghi theo LSET/CET.
- PBIX có thể chứa snapshot Import cũ; Refresh, tương tác và kết quả DAX cần evidence trên cùng nguồn/snapshot/filter.
- Một số mapping country/keyword/language có fallback; dữ liệu TMDB là snapshot nên năm phát hành không nhất thiết là năm ghi nhận doanh thu.
- Không chạy `docker compose down -v` để khắc phục lỗi thông thường vì lệnh này có thể xóa toàn bộ volume PostgreSQL.

Video demo chính thức được nhóm lưu tại [Google Drive](https://drive.google.com/drive/folders/1x6fNNB01GWwsOE6fa5XxfcngMb8h902G?usp=sharing).
