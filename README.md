# TMDB 5000 — Movie Data Warehouse & BI Analytics

Mini project của **Nhóm 5** về phân tích hiệu quả tài chính và đặc điểm khán giả của các tác phẩm điện ảnh. Hệ thống sử dụng **Mage.ai → PostgreSQL → dbt → Power BI**, với mô hình kho dữ liệu gồm **7 Dimension, 4 Bridge và 1 Fact**.

**Cập nhật tài liệu: 16/11/2026.** Repository đã có pipeline ingestion, transformation, dashboard Power BI bốn trang và bộ kiểm thử nghiệm thu. Generative AI chưa triển khai. Các kết quả kiểm thử bên dưới là bằng chứng đã lưu của từng lượt chạy, không phải tuyên bố mọi yêu cầu đã đạt.

## 1. Tài liệu và sản phẩm bàn giao

| Nội dung | Tệp / hướng dẫn |
|---|---|
| Dashboard tương tác | [TMDB_Movie_Dashboard.pbix](powerbi_dashboard/TMDB_Movie_Dashboard.pbix) |
| Mở, Refresh và sử dụng Power BI | [README Power BI](powerbi_dashboard/README.md) |
| Bản PDF dashboard | [TMDB_Movie_Dashboard.pdf](docs/diagrams/TMDB_Movie_Dashboard.pdf) |
| Phụ lục công thức DAX | [Phụ lục C — 60 DAX](docs/reports/Phu_luc_C_60_DAX.pdf) |
| Phụ lục đối chiếu SQL–Power BI | [Phụ lục D — Kiểm chứng](docs/reports/Phu_luc_D_Kiem_chung_PostgreSQL_PowerBI.pdf) |
| Thiết kế mô hình / Data Contract | [Schema_Report.md](Schema_Report.md) |
| Kiểm chứng kho dữ liệu đã ghi nhận | [DW_Verification_Report.md](DW_Verification_Report.md) |
| Cài đặt và vận hành dbt | [README dbt](dbt_transform/README.md) |
| Chạy test từng bước 3.1–3.4 | [HUONG_DAN_CHAY_TEST.md](test/HUONG_DAN_CHAY_TEST.md), bắt đầu từ phần 10 |
| Ma trận yêu cầu và test cases | [MATRIX.md](test/acceptance/MATRIX.md) |
| Kiểm tra Power BI thủ công | [CHECKLIST_POWERBI.md](test/acceptance/CHECKLIST_POWERBI.md) |
| Kịch bản quay demo | [VIDEO_DEMO.md](test/acceptance/VIDEO_DEMO.md) |

**Video demo:** [Thư mục video demo trên Google Drive](https://drive.google.com/drive/folders/1x6fNNB01GWwsOE6fa5XxfcngMb8h902G?usp=sharing).

**Báo cáo tổng hợp bản nộp:** CHỜ BỔ SUNG FILE/LINK PDF CHỐT. Hiện `docs/reports/` có hai phụ lục ở bảng trên; không coi các phụ lục là báo cáo tổng hợp. Khi thêm báo cáo, cập nhật liên kết tại đây và [danh mục tài liệu](docs/README.md).

## 2. Phạm vi triển khai hiện tại

Số mục 3.1–3.5 trong bảng là số mục yêu cầu được bộ test sử dụng.

| Phần | Đã có trong repository | Phạm vi còn cần xác minh / giới hạn |
|---|---|---|
| 3.1 — Mage | Full Load Movies/Credits, làm sạch và nạp `stage`; pipeline incremental dùng batch CSV | Đã nối watermark sau exporter, thêm bước tạo PK và cấu hình upsert theo ID. Loader đọc batch tĩnh, chưa lọc LSET/CET; replay/failure runtime cần bằng chứng riêng |
| 3.2 — dbt | 6 staging views, 7 dimensions, 4 bridges, 1 fact; 3 seeds; tests, contracts và docs | Build/rebuild cần nguồn stage hợp lệ; mô tả bốn staging association models còn bị DB13 phát hiện thiếu trong lượt test đã lưu |
| 3.3 — Data Warehouse | DDS có grain một dòng/phim, constraints, Unknown members và trọng số Bridge | Lượt integration gần nhất đã lưu đạt 43 PASS trong section 33; không suy rộng thành toàn bộ project PASS |
| 3.4 — Power BI | PBIX, semantic model, DAX và 4 trang dashboard; SQL tham chiếu, comparator 6 KPI | Refresh, filter context, drill-down, relationships và Q1–Q8 cần bằng chứng Desktop cùng snapshot |
| 3.5 — Generative AI | Các case AI01–AI04 ghi nhận phạm vi chưa hoàn thành | Chưa có tích hợp LLM/API hoặc runtime AI để nghiệm thu |

## 3. Kiến trúc và quy tắc dữ liệu

| Tầng | Công nghệ / schema | Trách nhiệm |
|---|---|---|
| Nguồn | TMDB 5000 Movie Dataset, CSV | Movies, Credits và batch demo incremental |
| Nạp dữ liệu | Mage.ai → PostgreSQL `stage` | Đọc, làm sạch cơ bản và nạp raw staging |
| Chuyển đổi | dbt → schema `staging` | Chuẩn hóa kiểu dữ liệu, parse quan hệ JSON |
| Kho phân tích | dbt → PostgreSQL `dds` | Dimensions, Bridges, Fact và seeds mapping |
| Báo cáo | Power BI Desktop | Semantic model, DAX, trực quan hóa và lọc tương tác |
| Kiểm thử | Python/pytest + SQL + đối chiếu Desktop | Kiểm source, dữ liệu, build/rebuild, negative controls và KPI |

- `fact_movie`: một dòng cho một phim; tham chiếu Movie, Date và Language.
- Bảy dimension: Movie, Date, Language, Genre, Company, Country, Keyword.
- Bốn bridge: Movie–Genre, Movie–Company, Movie–Country, Movie–Keyword.
- Genre/Company/Country dùng `weight_factor = 1/k` khi phân bổ chỉ tiêu cộng được. Keyword là tagging, không có trọng số; các theme có thể chồng lấp.
- Budget/Revenue bằng 0 được chuẩn hóa thành NULL. Profit = Revenue − Budget; ROI = Profit / Budget khi đủ điều kiện. ROI lưu dạng tỷ lệ, hiển thị Percentage.
- Median ROI theo phim khác ROI Overall (`SUM(profit) / SUM(budget)`). Không cộng ROI hoặc cộng các nhóm Full allocation rồi coi là tổng danh mục.
- `stage` là bảng Mage nạp; `staging` là views dbt chuẩn hóa; `dds` là lớp Power BI sử dụng.

PostgreSQL chỉ tự chạy [01_init.sql](postgres/init/01_init.sql) khi tạo volume mới. [02_dds_schema.sql](postgres/init/02_dds_schema.sql) là DDL tham chiếu; không chạy trước dbt. **dbt quản lý vòng đời bảng DDS.**

## 4. Cấu trúc repository

| Đường dẫn | Nội dung |
|---|---|
| `compose.yaml`, `.env.example` | Stack chính và mẫu cấu hình PostgreSQL |
| `data/raw/` | CSV cục bộ; không commit dữ liệu thô |
| `mage_pipeline/` | Loaders, transformers, exporters và hai pipeline |
| `postgres/init/` | Khởi tạo schema/watermark và DDL tham chiếu |
| `dbt_transform/` | Models, seeds, macros, tests, profile mẫu và tài liệu dbt |
| `powerbi_dashboard/` | PBIX và hướng dẫn sử dụng/Refresh |
| `docs/` | PDF dashboard, phụ lục và danh mục tài liệu bàn giao |
| `test/acceptance/` | Runner, preflight, môi trường cô lập, scenarios, SQL và checklist |
| `test/unit/` | Test hồi quy cho bộ kiểm thử |
| `test/results/` | REPORT, JSON, JUnit, log và SQL evidence của các lượt đã chạy |
| `test/validate_tmdb.py` | Script đối chiếu CSV–staging bổ trợ; không thay bộ acceptance |

## 5. Khởi chạy môi trường chính để demo

### 5.1. Chuẩn bị

Máy cần Docker Desktop (Linux containers), Python 3.12 và Power BI Desktop nếu xem/Refresh PBIX. Mở PowerShell tại thư mục gốc repository. Các lệnh này dành cho **môi trường chính**, khác môi trường test ở phần 6.

Đặt `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv` trong `data/raw/`. Thêm `tmdb_new_batch.csv` nếu chạy incremental hoặc bộ kiểm thử đầy đủ. CSV phải lấy từ bộ dữ liệu của project; tên file không bảo đảm nội dung đúng snapshot.

```powershell
# Chỉ tạo nếu chưa có cấu hình/môi trường cục bộ:
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
if (-not (Test-Path .venv)) { py -3.12 -m venv .venv }
$py = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $py -m pip install dbt-core==1.12.5 dbt-postgres==1.11.0
& $py -m pip install -r .\test\acceptance\requirements.txt
```

Sửa `.env`, thay mật khẩu mẫu bằng mật khẩu riêng. Tạo `mage_pipeline/io_config.yaml` cục bộ theo cấu trúc:

```yaml
version: 0.1.1
default:
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: warehouse
  POSTGRES_SCHEMA: stage
  POSTGRES_USER: labuser
  POSTGRES_PASSWORD: 'THAY_BANG_MAT_KHAU_TRONG_ENV'
  POSTGRES_HOST: postgres
  POSTGRES_PORT: 5432
```

Mage chạy trong container nên host là `postgres`; dbt/Power BI chạy trên máy host dùng `localhost`. Nếu đổi database/user trong `.env`, đồng bộ cả Mage và dbt.

```powershell
if (-not (Test-Path .\dbt_transform\profiles.yml)) {
    Copy-Item .\dbt_transform\profiles.yml.example .\dbt_transform\profiles.yml
}
```

Sửa password/host/database/user trong profile cho khớp môi trường. Không commit `.env`, `io_config.yaml`, `profiles.yml` thật hoặc `.runtime`.

### 5.2. Nạp dữ liệu và build DDS

```powershell
docker info --format '{{.ServerVersion}}'
docker compose config -q
docker compose up -d
docker compose ps
docker compose exec postgres pg_isready -U labuser -d warehouse
```

Đợi PostgreSQL nhận kết nối. Mở [Mage chính](http://localhost:6789), chạy toàn pipeline **`tmdb_ingestion`**, đợi thành công trước khi build:

```powershell
& .\.venv\Scripts\dbt.exe debug --project-dir .\dbt_transform --profiles-dir .\dbt_transform
if ($LASTEXITCODE -ne 0) { throw 'dbt debug lỗi; kiểm tra kết nối' }
& .\.venv\Scripts\dbt.exe build --project-dir .\dbt_transform --profiles-dir .\dbt_transform
if ($LASTEXITCODE -ne 0) { throw 'dbt build lỗi; kiểm tra log' }
& .\.venv\Scripts\dbt.exe docs generate --project-dir .\dbt_transform --profiles-dir .\dbt_transform
```

Chi tiết debug, docs và mô hình: [README dbt](dbt_transform/README.md). Không chạy incremental lặp trên dữ liệu demo để thử chống trùng; thực hiện scenarios trên DB test riêng.

### 5.3. Mở Power BI

Mở [PBIX](powerbi_dashboard/TMDB_Movie_Dashboard.pbix), kiểm **Data source settings** và kết nối đúng PostgreSQL, rồi **Home → Refresh**. Bốn trang gồm Overview, Financial Drivers, Companies & Countries, Audience & Ratings. Xem [README Power BI](powerbi_dashboard/README.md) để biết chỉ số và thao tác.

PBIX có thể hiển thị dữ liệu Import cũ khi PostgreSQL tắt. Mở được dashboard không chứng minh Refresh thành công. Snapshot ban đầu có 4.803 phim; số liệu đó là tham chiếu lịch sử, không thay kết quả SQL của DB đang dùng.

## 6. Chạy kiểm thử

**Hướng dẫn đầy đủ:** [HUONG_DAN_CHAY_TEST.md](test/HUONG_DAN_CHAY_TEST.md). Phần 10 hướng dẫn riêng 3.1–3.4; phần 11 là scenarios Mage; phần 12 xử lý lỗi cổng Mage; phần 13 lưu bằng chứng.

| Môi trường | PostgreSQL | Mage | Cách dùng |
|---|---|---|---|
| Chính | `localhost:5432`, `warehouse` | `localhost:6789` | Demo, Refresh PBIX và kiểm readonly |
| Test cô lập | `127.0.0.1:55432`, `tmdb_test_warehouse` | `127.0.0.1:16789` | Integration, rebuild và negative controls |

Kiểm chỉ đọc DB chính đã có dữ liệu:

```powershell
$py = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $py .\test\acceptance\preflight.py --mode readonly --env-file .env
& $py .\test\acceptance\run.py --mode readonly --section all --env-file .env
```

Với DB test, làm đủ **prepare (một lần) → up → Mage ingestion → dbt-build → runner** theo hướng dẫn, không chỉ đổi `--mode`. Cờ `--snapshot full` chỉ đúng sau Full Load và trước append. Runner không tự chạy Mage hoặc Refresh Power BI.

Mỗi lượt tạo thư mục `test/results/acceptance_<UTC>_<id>/`. PASS là assertion đạt trong phạm vi test; INFO chỉ là số liệu quan sát/tham chiếu; BLOCKED thiếu điều kiện/bằng chứng; SKIPPED chưa chạy theo mode; FAIL là assertion không đạt. Comparator sáu KPI không thay kiểm tra toàn bộ DAX hoặc UI.

### Kết quả kiểm thử đã ghi nhận

Lượt 3.1 `20261116T071641Z_03ce5c` đã được đọc ngày 16/11/2026: **22 PASS, 0 FAIL, 10 BLOCKED, 0 SKIPPED, 6 INFO**. MG18 kiểm dependency watermark đã PASS. Lượt 3.2 `20261116T072911Z_a683f3`: **33 PASS, 1 FAIL**; DB13 còn thiếu mô tả riêng của bốn staging association models.

Các kết quả này là ghi nhận từ report đã đọc, không phải lượt chạy mới khi chỉnh tài liệu. Các thư mục report hiện không còn trong `test/results/` tại thời điểm rà soát; cần lưu lại report được chọn khi nộp, không dẫn liên kết tới file đã xóa. Không dùng FAIL MG18 của lượt cũ để mô tả code hiện tại.

Phần Power BI được nhóm xác nhận đã kiểm tra thủ công trong video; xem thư mục video ở mục 1; ghi mốc thời gian tương ứng khi đối chiếu từng case. Trạng thái BLOCKED của runner chỉ phản ánh chưa có adapter/bằng chứng tự động cho từng case, không thay kết luận kiểm thủ công. Không sửa report cũ thành PASS.

## 7. Giới hạn cần trình bày trong báo cáo

- Incremental đã có bước tạo PK, cấu hình upsert và graph cập nhật watermark sau exporter. Loader vẫn đọc batch tĩnh, chưa lọc LSET/CET; khả năng replay/failure cần đánh giá theo kịch bản thực đã chạy. Xem [README Mage](mage_pipeline/README_Ingestion.md).
- Một số surrogate keys sinh theo thứ tự natural key; thêm natural key mới có thể làm SK đổi khi rebuild. Dùng NK khi đối chiếu giữa các snapshot.
- Country/Keyword/Language mappings có fallback, chưa bao phủ mọi trường hợp. Dataset là snapshot; năm phát hành không phải năm ghi nhận doanh thu.
- Kiểm thử Power BI cần cùng nguồn, snapshot và bộ lọc. Refresh và tương tác phải có bằng chứng thật.
- Generative AI chưa triển khai; không mô tả hạng mục này là đã hoàn thành.

## 8. Checklist trước khi nộp

- [x] Bổ sung link thư mục video ở phần 1.
- [ ] Kiểm quyền xem video bằng phiên chưa đăng nhập tài khoản chủ sở hữu.
- [ ] Thêm file/link báo cáo tổng hợp PDF chốt và đồng bộ số liệu với đúng snapshot.
- [ ] Kiểm PBIX, PDF dashboard và các phụ lục là phiên bản muốn nộp.
- [ ] Lưu report kiểm thử đã chọn và checklist/ảnh Power BI; giải thích FAIL/BLOCKED còn lại.
- [ ] Ghi rõ phần AI chưa triển khai và giới hạn incremental.
- [ ] Kiểm tài liệu hướng dẫn và liên kết; cung cấp nguồn dataset theo yêu cầu nộp, không đóng gói credentials.
- [ ] Kiểm `git status` và diff trước khi commit; không đưa `.venv`, `.env`, `.runtime`, password hoặc CSV thô lên Git.

Không dùng `docker compose down -v` để sửa lỗi kết nối. `isolation.py down` cũng xóa volume **test**; muốn giữ dữ liệu để tiếp tục demo/test thì chỉ dừng container.

Nhóm tích hợp qua `develop`, làm việc trên `feat/<phạm-vi>-<tên>` và mở pull request theo quy ước nhóm. Việc chỉnh tài liệu không tự thực hiện commit/push hoặc thay đổi dữ liệu.
