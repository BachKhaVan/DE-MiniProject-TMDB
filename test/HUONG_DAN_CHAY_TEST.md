# Hướng dẫn chạy test TMDB

**Cách dùng:** Nếu chạy từng phần 3.1–3.4 theo hướng dẫn trực tiếp, bắt đầu ở **phần 10** cuối file. Phần 1–9 giải thích phạm vi, môi trường và giới hạn. Chạy kiểm tra cơ bản trước; chỉ thực hiện scenarios ở phần 11 khi cần bổ sung bằng chứng 3.1.

## 1. Phạm vi và căn cứ

Đối chiếu `2627.Yêu cầu_unlocked.pdf` (3 trang) và `BaoCao_TongHop_TMDB_Nhom5.docx.pdf` (88 trang; phần triển khai, kết quả và mức độ hoàn thành). Các mục 3.1–3.5 dưới đây là số mục **trong đề**, không phải số mục cùng tên trong báo cáo.

Đề cho phép incremental mô phỏng batch tĩnh, không bắt buộc lọc LSET/CET. PostgreSQL nằm trong danh sách công nghệ ở phần mục tiêu, dù tiêu đề các mục sau ghi SQL Server. Số bảng và quy tắc Unknown/weight/ROI thuộc Data Contract của project; đề chỉ yêu cầu tối thiểu 2 trang dashboard.

| Phần | Tự động kiểm tra | Điều kiện/bằng chứng bổ sung |
|---|---|---|
| 3.1 Mage | CSV, AST cấu hình, hàm cleaner gốc trên fixtures, stage, so snapshots trước/sau | Khởi chạy pipeline thật và xuất log/run ID để chấm scenarios; log trạng thái/rowcounts/lỗi |
| 3.2 dbt | Models/seeds/tests, lineage/docs; build → rebuild → docs trên DB test; transformation | Mage đã nạp stage; không dùng artifact cũ chứng minh lần chạy mới |
| 3.3 DW | 59 SQL checks: grain, khóa/FK, Unknown, công thức, measures, Date, bốn Bridge; 5 negative controls | DB và dữ liệu có sẵn; negative controls chỉ trên DB test |
| 3.4 BI | PBIR, trang/visual/KPI/slicer; SQL Q1–Q8; so 6 KPI xuất từ DAX bằng comparator | Desktop: Refresh, relationships, hierarchy, drill/filter, Top N, ngữ cảnh DAX |
| 3.5 AI | Hiển thị AI01–AI04 BLOCKED để không bỏ sót yêu cầu | Báo cáo xác nhận chưa triển khai; chưa có adapter kiểm thử runtime |
| Sản phẩm nộp | Kiểm tra source/PBIX hiện diện trong phạm vi test | Rà PDF, Kaggle, tài liệu chạy, video demo và thành phần AI theo mục 4 của đề |

Không bảo đảm mọi test PASS. Mục tiêu là kết quả đúng và tái hiện được. PASS tĩnh/unit không chứng minh runtime; SQL tham chiếu INFO không chứng minh DAX đúng.

## 2. Cần khởi động gì?

| Cách chạy | Cần mở | Không bắt buộc |
|---|---|---|
| Unit/source | Terminal + Python và dependencies | Docker, Mage, Power BI |
| Readonly DW hiện tại | PostgreSQL chính; Docker Desktop nếu DB ở Docker | Mage nếu stage/DDS đã có; Power BI nếu chỉ đọc SQL |
| Integration/rebuild/negative | Docker Desktop + PostgreSQL TEST 55432 + Mage TEST 16789 | Stack chính 5432/6789; không cần tắt vì cổng khác |
| Power BI Refresh/DAX | Power BI Desktop + đúng PostgreSQL mà PBIX kết nối | Mage sau khi nguồn đã nạp |

Giữ nguồn ổn định khi chạy test: không chạy Mage/dbt/append batch đồng thời. Mỗi test có transaction READ ONLY riêng, tránh giữ khóa làm negative controls bị treo; không phải toàn bộ lượt chạy dùng chung một snapshot transaction.

## 3. Cài dependencies một lần

```powershell
Set-Location D:\DE-MiniProject-TMDB
py -3.12 -m venv .venv_test
.\.venv_test\Scripts\python.exe -m pip install -r .\test\acceptance\requirements.txt
.\.venv_test\Scripts\python.exe -m pip install dbt-core==1.12.5 dbt-postgres==1.11.0
$py = (Resolve-Path .\.venv_test\Scripts\python.exe).Path
& $py -m pip check
& $py -m pytest -c .\test\acceptance\pytest.ini .\test\unit -q
```

Phiên bản dbt trên là phiên bản repo ghi nhận. Nếu dùng `.venv` có sẵn, cài requirements trong chính venv đó và đặt `$py` tương ứng. Không cần Activate.ps1 hay đổi execution policy. Mỗi terminal mới cần đặt lại `$py`. Không dùng venv sao chép từ máy khác.

Trước khi prepare, cần đủ CSV thật trong `data/raw/`: `tmdb_5000_movies.csv`, `tmdb_5000_credits.csv`, `tmdb_new_batch.csv`. Không commit CSV thô, `.env`, `.runtime` hay credentials.

## 4. Kiểm nhanh DB hiện tại — chỉ đọc

Mở Docker Desktop, đợi Engine hoạt động. Nếu chưa bật PostgreSQL chính:

```powershell
docker info
docker compose up -d postgres
docker compose exec postgres pg_isready -U labuser -d warehouse
& $py .\test\acceptance\preflight.py --mode readonly --env-file .env
& $py .\test\acceptance\run.py --mode readonly --section all --env-file .env
```

`--env-file .env` đọc DB/user/password vào process, không in mật khẩu và không thực thi nội dung file. Biến `TMDB_DB_*` có sẵn được ưu tiên. Đổi host/port bằng `TMDB_DB_HOST`/`TMDB_DB_PORT`. Preflight Docker có thể BLOCKED nhưng SQL vẫn chạy được nếu dùng PostgreSQL độc lập/remote.

Nếu **biết chắc vừa Full Load và chưa append**, thêm `--snapshot full`:

```powershell
& $py .\test\acceptance\run.py --mode readonly --section 31 --env-file .env --snapshot full
& $py .\test\acceptance\run.py --mode readonly --section 33 --env-file .env
```

Nếu không biết trạng thái, giữ mặc định `unknown`: MG21 BLOCKED thay vì quy kết sai lệch số dòng là lỗi ingestion. Khi xác nhận full, sai số dòng sẽ FAIL. Readonly không tự load CSV/build/Refresh. Nếu thiếu stage/DDS, dùng môi trường test ở phần 5.

## 5. Luồng khuyến nghị: môi trường test riêng

### 5.1. Tạo và khởi động

```powershell
& $py .\test\acceptance\isolation.py prepare
& $py .\test\acceptance\isolation.py up
& $py .\test\acceptance\isolation.py ps
```

Prepare sao chép source Mage và CSV, tạo cấu hình riêng. Chỉ gọi một lần; nếu `.runtime` tồn tại thì dùng up/ps, không tạo lại password. Khi source/CSV đổi, dừng stack test, lưu bằng chứng, lưu trữ `.runtime` ở nơi được gitignore rồi prepare mới; không nghiệm thu bằng bản sao source cũ.

DB test: `tmdb_test_warehouse`, user `tmdb_test_user`, host `127.0.0.1`, port `55432`; Mage `http://127.0.0.1:16789`. Không dùng Mage chính cổng 6789 cho kịch bản thử lỗi.

### 5.2. Full Load bằng Mage thật

Mở Mage test, chạy toàn pipeline **tmdb_ingestion**, đợi cả Movies/Credits thành công. Giữ log thực có trạng thái và rowcounts. YAML `status: executed` không phải bằng chứng mới. Preflight có thể còn BLOCKED `dds.fact_movie` vì chưa build — đúng dự kiến.

Ngay sau ingestion, trước khi chạy incremental:

```powershell
& $py .\test\acceptance\run.py --mode integration --section 31 --approved --snapshot full
```

MI01–MI08 có thể BLOCKED khi chưa thu bằng chứng scenarios. Đây là phần chưa kiểm chứng, không phải PASS và không nhất thiết là lỗi ingestion.

### 5.3. Build/rebuild/docs và kiểm DW

```powershell
& $py .\test\acceptance\isolation.py dbt-build
if ($LASTEXITCODE -ne 0) { throw 'dbt chưa thành công; xem log trước khi tiếp tục' }
& $py .\test\acceptance\preflight.py --mode integration
& $py .\test\acceptance\run.py --mode integration --section 32 --approved --snapshot full
& $py .\test\acceptance\run.py --mode integration --section 33 --approved --snapshot full
```

dbt-build tự chạy **build → rebuild → docs generate**; build đã gồm seeds/tests. Nó lưu hashes DDS trước/sau. DB12 kiểm cùng nguồn có tái tạo cùng dữ liệu/SK không, không bắt SK bất biến khi thêm NK mới. Lần build mới vô hiệu bằng chứng thành công cũ trước khi bắt đầu.

`--approved` là cờ bảo vệ kỹ thuật, chỉ cho ghi trên DB test cố định. Negative controls tiêm lỗi rồi rollback trong finally; assertion sai vẫn FAIL. Có statement/lock timeout để tránh treo. Không chạy dbt với profile chính trong quy trình test này.

### 5.4. Mage scenarios: so tự động, kích hoạt pipeline và thu log trong UI

Sau Full Load lần 1, ví dụ kiểm replay:

```powershell
& $py .\test\acceptance\scenario.py full_repeat before
# Trong Mage test: chạy tmdb_ingestion lần 2, đợi hoàn tất, xuất log.
$mageRunId = Read-Host 'Run ID thật trong trang Runs của Mage'
$mageLog = Read-Host 'Đường dẫn file log xuất từ lần chạy đó'
& $py .\test\acceptance\scenario.py full_repeat after --mage-run-id $mageRunId --run-status success --mage-log $mageLog
```

Run ID lấy từ **pipeline → Runs → lần chạy vừa thực hiện**, không dùng ID phim, tên pipeline, UUID tự đặt hay chữ `ID_THUC_TE`. Nếu chưa có bằng chứng, giữ BLOCKED. Bộ test không gọi riêng hàm Python rồi coi đó là lần điều phối Mage.

| Test | Case snapshot | Chuẩn bị trước before | Sau chạy |
|---|---|---|---|
| MI01 | full_repeat | Stage đã Full Load lần 1 | Ingestion lần 2 success |
| MI02 | batch_new | `scenario_data.py new`; batch có ID mới | Incremental success, phim tăng, không thêm duplicate |
| MI03 | batch_empty | `scenario_data.py empty` | success, stage không đổi |
| MI04 | batch_replay | Đã chạy new một lần, giữ batch | success, không trùng |
| MI05 | batch_existing | `scenario_data.py existing` | success, không trùng |
| MI06 | batch_invalid | `scenario_data.py invalid` | Kiểm cách xử lý JSON lỗi; yêu cầu độ bền bổ sung |
| MI07 | export_failure | `scenario_data.py new`, `isolation.py failure-on` | failed; log chứa `tmdb_test_injected_export_failure`; watermark không đổi |
| MI08 | partial_full | Thiết lập lỗi một nhánh chỉ trên bản sao test | failed; INFO quan sát, không yêu cầu atomic tuyệt đối |

Mỗi case: chuẩn bị batch → before → chạy pipeline thật → after có `--run-status success`/`failed` và `--mage-log`. Không chạy chồng case. Test kiểm case/phase/database, thứ tự thời gian, hash log. Snapshots cũ thiếu metadata mới sẽ BLOCKED; lưu trữ `.runtime/scenarios` trước lượt mới, không ghi đè.

Sau injection **luôn** gọi failure-off kể cả khi lỗi. Sau tất cả scenarios, khôi phục Full Load sạch và build lại trước khi nghiệm thu DW:

```powershell
& $py .\test\acceptance\isolation.py failure-off
# Chạy tmdb_ingestion trong Mage test, đợi thành công.
& $py .\test\acceptance\isolation.py dbt-build
& $py .\test\acceptance\run.py --mode integration --section all --approved --snapshot full
```

## 6. Power BI: đối chiếu đúng snapshot/filter

Đọc `acceptance/CHECKLIST_POWERBI.md`. Xác nhận PBIX dùng 5432/warehouse hay 55432/tmdb_test_warehouse. Nếu thử DB test, dùng bản sao PBIX để giữ cấu hình demo. Refresh thành công, đặt filter đúng, dừng thay đổi DB rồi chạy SQL với mode tương ứng. PBIX mở được từ Import cũ không chứng minh Refresh thành công.

PB07–PB14 và Q1–Q8 vẫn BLOCKED trong runner vì chưa có adapter Desktop. Ghi kết quả tương tác vào checklist kèm ảnh/filter/thời điểm, không sửa thành PASS dựa vào sự hiện diện của PBIX.

Có thể so tự động 6 KPI sau khi xuất DAX CSV. Trong DAX Query View, chạy cho trạng thái không lọc:

```dax
EVALUATE
ROW(
    "movies", [Movie Count],
    "valid_movies", [Valid Movies],
    "valid_revenue", [Total Revenue],
    "total_profit", [Total Profit],
    "roi_median", [ROI Median],
    "pct_over_budget", [Pct Over Budget]
)
```

Query View không tự kế thừa slicers. Dùng BI01 cho query trên; BI02 chỉ khi query cũng đặt filter USA–2014–Action tường minh. Xuất CSV 1 dòng, 6 cột trên, số thô: không %, $, bn hay dấu hàng nghìn; ROI dạng tỷ lệ. Header `[movies]` được chấp nhận.

```powershell
$reference = Read-Host 'Đường dẫn queries/BI01.json của lượt SQL vừa chạy'
$daxCsv = Read-Host 'Đường dẫn CSV xuất từ DAX'
& $py .\test\acceptance\compare_powerbi.py --reference $reference --actual $daxCsv --confirm-same-snapshot
```

Comparator kiểm số phim chính xác, tiền sai số ≤0,01, tỷ lệ ≤0,000001. Không tự xác minh lời xác nhận snapshot/filter và không chấm toàn bộ DAX/relationships/Refresh. Lưu JSON output cùng evidence nếu dùng nghiệm thu.

## 7. Đọc kết quả và xử lý lỗi

Mỗi lượt tạo `test/results/acceptance_<UTC>_<id>/`: REPORT.md, result.json, junit.xml, pytest_output.txt, queries khi SQL chạy được. Integration lưu bằng chứng build/scenarios trong runtime_evidence, không sao chép profiles/password. Dùng Run ID vừa in ở terminal, không nhầm report cũ.

| Trạng thái | Ý nghĩa |
|---|---|
| PASS | Assertion đạt đúng phạm vi; tĩnh/unit không thay runtime |
| INFO | Profile nguồn/SQL tham chiếu, chưa phải nghiệm thu nghiệp vụ |
| FAIL | Quan sát assertion sai; đọc Actual và loại yêu cầu |
| BLOCKED | Thiếu điều kiện/bằng chứng; không cộng vào PASS |
| SKIPPED | Không chạy theo mode, như negative control trong readonly |

Exit 0: không FAIL/BLOCKED/SKIPPED trong phạm vi chọn; 1: có FAIL; 2: không FAIL nhưng có BLOCKED/SKIPPED. INFO tách riêng. Không dùng tỷ lệ PASS trên IDs để suy ra điểm đồ án.

| Hiện tượng | Xử lý |
|---|---|
| Docker permission denied/Engine tắt | Mở Docker Desktop và terminal có quyền; thử docker info; không xóa volume |
| Không kết nối DB | Kiểm mode/cổng/password; readonly dùng --env-file .env, integration tự lấy secret test |
| Thiếu pandas/pytest/psycopg/yaml | Cài requirements bằng đúng `$py` |
| Thiếu dbt | Cài trong cùng venv; harness tìm cạnh Python trước PATH |
| Thiếu stage/DDS | Ingestion trước, dbt-build sau |
| MG18 FAIL | Graph watermark chưa phụ thuộc thành công exporter; phát hiện độ bền hiện có |
| MG19 INFO | Không thấy lọc LSET/CET; batch tĩnh được đề cho phép |
| MG20 BLOCKED | Cấu hình upsert chưa chứng minh UNIQUE/replay thực tế; cần MI04/MI05 |
| MG24 BLOCKED | Chưa có adapter thu runtime logs tự động; kiểm log/rowcount trong Mage |
| DB13 FAIL | Bốn staging association models thiếu mô tả riêng; kiểm tra tài liệu bổ sung |
| DB09–DB12 BLOCKED readonly | Bằng chứng build thuộc DB test; chạy integration sau dbt-build |
| AI01–AI04 BLOCKED | Chưa triển khai AI; là yêu cầu còn thiếu, không chữa bằng mở thêm dịch vụ |

## 8. Dừng môi trường

Sau khi lưu bằng chứng:

```powershell
& $py .\test\acceptance\isolation.py down
```

Lệnh này **xóa volume TEST** tmdb_test_acceptance_pg_data, không xóa volume chính. Muốn giữ DB test, dừng container test trong Docker Desktop. Không dùng docker compose down -v ở root để sửa lỗi.

## 9. Giới hạn xác minh trong phiên chỉnh bộ test ban đầu (lịch sử)

**Cập nhật 16/11/2026:** các giới hạn dưới đây mô tả phiên chỉnh bộ test ban đầu. Sau đó đã có report integration 3.1–3.4 trong `test/results/`; bảng các lượt gần nhất được dẫn tại [README tổng](../README.md). Không dùng kết quả readonly lịch sử dưới đây làm trạng thái nghiệm thu hiện tại.

Đã kiểm syntax/import/collection, chạy regression tests cho harness và chạy readonly để kiểm phân loại. Phiên này không truy cập được Docker Engine/PostgreSQL; cài pandas bị chặn do không phân giải pypi.org. Chưa xác nhận runtime của SQL mới, build/rebuild, negative controls và cleaner fixtures trên môi trường thật. Cần chạy lại theo hướng dẫn trên ở terminal có quyền Docker và dependencies.

Kết quả kiểm harness: **15 regression tests PASS**. Lượt readonly `acceptance_20261115T165841Z_049e65`: **26 PASS, 2 FAIL, 112 BLOCKED, 13 SKIPPED, 6 INFO**. Hai FAIL là MG18 (dependency watermark) và DB13 (mô tả bốn staging models); đều được phân loại kiểm tra độ bền bổ sung. Các con số này chỉ mô tả lần chạy trong môi trường bị giới hạn, không phải nghiệm thu toàn hệ thống.

## 10. Chạy từng phần 3.1–3.4: làm theo thứ tự

### 10.1. Mỗi lần mở terminal mới

Mở Docker Desktop, đợi Engine chạy. Mở PowerShell trong project. Các lệnh dưới đây dùng `.venv` đang có trên máy; nếu đã tạo `.venv_test` ở phần 3 thì thay duy nhất đường dẫn gán `$py`.

```powershell
Set-Location D:\DE-MiniProject-TMDB
$py = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $py --version
docker info --format '{{.ServerVersion}}'
Test-Path .\test\acceptance\.runtime\isolated.json
Get-ChildItem .\data\raw\*.csv | Select-Object Name
```

Cần thấy Python và Docker trả phiên bản; CSV có đủ ba tên ở phần 3. `Test-Path` False nghĩa là chưa có cấu hình test; True thì giữ cấu hình hiện có. Nếu Python không tồn tại, làm phần 3 trước. Nếu thiếu thư viện, cài requirements và dbt trong đúng Python đã gán `$py`.

```powershell
if (-not (Test-Path .\test\acceptance\.runtime\isolated.json)) {
    & $py .\test\acceptance\isolation.py prepare
    if ($LASTEXITCODE -ne 0) { throw 'Prepare lỗi; dừng và xem output' }
}
& $py .\test\acceptance\isolation.py up
if ($LASTEXITCODE -ne 0) { throw 'Khởi động lỗi; xem phần 12' }
& $py .\test\acceptance\isolation.py ps
```

Cần PostgreSQL test `healthy`, Mage `running` và truy cập được http://127.0.0.1:16789. Mage không có healthcheck trong compose hiện tại, nên `running` chưa đủ chứng minh web sẵn sàng. Không chạy prepare lại khi đã có cấu hình.

### 10.2. Phần 3.1 — Mage ingestion

1. Mở Mage **cổng 16789**, chọn `tmdb_ingestion`.
2. Chạy toàn pipeline, chờ các block và trạng thái run kết thúc thành công. Chụp trạng thái; lưu log theo phần 11.1.
3. Chưa chạy `tmdb_incremental`. Chạy:

```powershell
& $py .\test\acceptance\run.py --mode integration --section 31 --approved --snapshot full
```

Cuối terminal cần có đường dẫn `Run: ...`, thống kê PASS/FAIL/BLOCKED/SKIPPED/INFO. Mở `REPORT.md` của đúng lượt đó. Nếu ingestion thất bại hoặc test dữ liệu stage FAIL, dừng để kiểm tra Actual/log. Nếu chỉ thiếu snapshots MI01–MI08 hoặc bằng chứng log, có thể sang 3.2 nhưng ghi rõ 3.1 chưa nghiệm thu đủ. Làm phần 11 để bổ sung scenarios.

`--snapshot full` chỉ dùng khi vừa Full Load và chưa append. Nếu đã incremental, bỏ cờ này hoặc chạy lại Full Load sạch trước. Runner không tự chạy Mage.

### 10.3. Phần 3.2 — dbt

Điều kiện: ingestion đã thành công, DB test đang chạy. Không chạy pipeline song song.

```powershell
& $py .\test\acceptance\isolation.py dbt-build
if ($LASTEXITCODE -ne 0) { throw 'dbt lỗi; đọc log trước khi chạy test 3.2' }
& $py .\test\acceptance\run.py --mode integration --section 32 --approved --snapshot full
```

Cần thấy cả `dbt build exit 0`, `dbt rebuild exit 0`, `dbt docs exit 0`. Nếu thiếu bước hoặc exit khác 0, đọc log tương ứng `test/acceptance/.runtime/dbt_build.log`, `dbt_rebuild.log`, `dbt_docs.log`. Không dùng kết quả build cũ thay cho lần thất bại mới. Nếu nguồn đã append, bỏ `--snapshot full`.

Nếu build thành công nhưng test FAIL, đọc ID/Expected/Actual để phân biệt lỗi dữ liệu với kiểm tra tài liệu. Các phát hiện source ghi ở phần 9 là kết quả lịch sử, không mặc định còn đúng trong lượt mới.

### 10.4. Phần 3.3 — Data Warehouse

Sau build thành công, giữ DB test chạy; không cần chạy lại ingestion/dbt.

```powershell
& $py .\test\acceptance\run.py --mode integration --section 33 --approved
```

Đọc REPORT mới. Negative controls chỉ chạy trên DB test và rollback sau kiểm tra. Nếu bị ngắt giữa chừng hoặc kết nối lỗi, kiểm trạng thái DB rồi chạy lại; không tự sửa/xóa dữ liệu để làm PASS. Có FAIL nghĩa là cần xem assertion cụ thể; BLOCKED nghĩa là thiếu điều kiện, chưa có kết luận đạt.

### 10.5. Phần 3.4 — Power BI và SQL tham chiếu

1. Mở `powerbi_dashboard/TMDB_Movie_Dashboard.pbix`. Vào **File → Options and settings → Data source settings** để xác định server/database.
2. Chọn đúng một nhánh dưới đây theo nguồn Power BI. Chỉ dùng SQL trên cùng DB với PBIX để so số.

| Nguồn Power BI | Lệnh SQL phù hợp |
|---|---|
| `localhost:55432` hoặc `127.0.0.1:55432`, database `tmdb_test_warehouse` | integration |
| `localhost:5432`, database `warehouse` | readonly với `.env` trỏ đúng DB chính |
| Nguồn khác hoặc chưa xác định | Xác minh cấu hình trước khi đối chiếu |

```powershell
# Chọn nhánh này nếu PBIX kết nối DB TEST:
& $py .\test\acceptance\run.py --mode integration --section 34 --approved

# HOẶC nhánh này nếu PBIX kết nối DB CHÍNH và .env khớp nguồn:
& $py .\test\acceptance\run.py --mode readonly --section 34 --env-file .env
```

Biến môi trường `TMDB_DB_*` có sẵn có thể ghi đè `.env`; kiểm nguồn nếu số liệu bất thường. Nếu đổi PBIX sang DB test, dùng **Save As** tạo bản sao trước. Nhập thông tin DB test ở phần 5.1; lấy password từ cấu hình cục bộ `test/acceptance/.runtime/isolated.json`, không đưa password vào ảnh/log gửi kèm.

3. **Home → Refresh**, đợi hoàn tất. Nếu lỗi kết nối/credential thì giữ kiểm tra Refresh là BLOCKED, xử lý kết nối trước. Giữ DB ổn định từ lúc Refresh đến lúc xuất DAX và chạy SQL; nếu DB đã đổi, Refresh và tạo SQL reference lại.
4. Thực hiện checklist [CHECKLIST_POWERBI.md](acceptance/CHECKLIST_POWERBI.md): ảnh bốn trang, relationships, drill-down, filters, Weighted/Full, ngưỡng và Q1–Q8. Xem Storage mode ở thuộc tính bảng trong Model view khi cần xác nhận Import/DirectQuery.
5. Mở **DAX Query View**, dán query sáu KPI ở phần 6 và chạy. Nếu không tìm thấy measure, kiểm tên/công thức thực trong model; không đổi sang measure khác chỉ để hết lỗi. Query này không tự lấy slicer của trang.
6. Nếu giao diện có xuất CSV, xuất kết quả. Nếu không, copy bảng kết quả vào file CSV UTF-8 bằng trình soạn thảo/bảng tính; giữ header và đúng một dòng dữ liệu. Phải dùng số thô, dấu chấm thập phân, dấu phẩy phân cột, không làm tròn hoặc thêm ký hiệu tiền/%.

Header cần có:

```csv
movies,valid_movies,valid_revenue,total_profit,roi_median,pct_over_budget
```

Thêm dòng số thực lấy từ DAX bên dưới, không dùng các baseline trong checklist để điền. Kiểm tra CSV bằng trình soạn thảo trước khi so.

7. Lấy đường dẫn thư mục `Run:` vừa tạo ở bước 2. Kiểm có `queries/BI01.json` rồi chạy comparator (BI01 dành cho query không lọc ở phần 6):

```powershell
$reference = Read-Host 'Đường dẫn đầy đủ tới queries/BI01.json của lượt vừa chạy'
$daxCsv = Read-Host 'Đường dẫn đầy đủ tới CSV DAX vừa xuất'
& $py .\test\acceptance\compare_powerbi.py --reference $reference --actual $daxCsv --confirm-same-snapshot
```

Chỉ dùng cờ xác nhận khi đã bảo đảm cùng snapshot và filter. Kết quả cần có sáu metric PASS; nếu FAIL thì xem sai lệch và tolerance, không sửa số CSV cho khớp. Nếu muốn lưu output, chạy lại lệnh và nối `| Out-File -Encoding utf8 .\test\results\powerbi_comparison.json` (chọn tên riêng nếu đã có file).

Comparator không cập nhật REPORT của runner và không tự chuyển PB07–PB14/Q1–Q8 thành PASS. Lưu kết quả so cùng checklist thủ công. Với BI02 cần query lọc tường minh USA–2014–Action; chỉ bấm slicer rồi chạy query BI01 là chưa đủ.

## 11. Bổ sung kịch bản Mage 3.1

### 11.1. Thu log và Run ID thật

Trong pipeline, mở trang **Runs**, chọn lần chạy vừa kết thúc, lấy ID từ chi tiết run hoặc URL nếu URL hiển thị ID của run đó. Không dùng ID phim hay tên pipeline. Lưu ảnh có trạng thái/thời điểm. Mở log các block thuộc đúng run, xuất log nếu UI hỗ trợ; nếu không, copy nguyên văn nội dung log vào file UTF-8 `.txt`/`.log`, giữ tên block và timestamp. Không viết lại log theo kết quả mong đợi. Run tương tác không hiện trong Runs thì chưa đủ để điền ID; cần tạo lần chạy có lịch sử hoặc giữ BLOCKED.

Chạy từng case riêng, theo **chuẩn bị → before → chạy Mage → chờ kết thúc → after**. Mẫu dùng chung:

```powershell
# Đặt tên case theo bảng 11.2, ví dụ full_repeat:
$case = 'full_repeat'
& $py .\test\acceptance\scenario.py $case before
if ($LASTEXITCODE -ne 0) { throw 'Chưa lưu before; không chạy pipeline' }
# DỪNG TẠI ĐÂY: chạy đúng pipeline trong Mage test và đợi kết thúc.
```

Sau khi pipeline kết thúc mới chạy khối sau:

```powershell
$mageRunId = Read-Host 'Run ID thật vừa chạy'
$mageLog = Read-Host 'Đường dẫn file log UTF-8 của run đó'
$runStatus = Read-Host 'Trạng thái thực tế: success hoặc failed'
& $py .\test\acceptance\scenario.py $case after --mage-run-id $mageRunId --run-status $runStatus --mage-log $mageLog
```

Cần thấy thông báo lưu snapshot cả before/after. Sau khi thu bằng chứng, runner mới chấm kết quả; việc lưu snapshot thành công chưa phải case PASS. Nếu file snapshot đã tồn tại, dừng; lưu trữ bộ bằng chứng cũ trước khi bắt đầu lượt mới, không xóa/ghi đè tùy tiện.

### 11.2. Thứ tự các case

Khởi đầu bằng Full Load sạch. Với mỗi dòng, chạy lệnh chuẩn bị (nếu có), đặt `$case`, rồi dùng hai khối 11.1. **Chạy MI04 ngay sau MI02**, trước khi đổi batch.

| Thứ tự | Case / ID | Chuẩn bị trước before | Pipeline trong Mage | Kết quả cần kiểm |
|---|---|---|---|---|
| 1 | `full_repeat` / MI01 | Đã ingestion lần 1 | `tmdb_ingestion` lần 2 | success; Movies/Credits giữ nguyên |
| 2 | `batch_new` / MI02 | `& $py .\test\acceptance\scenario_data.py new` | `tmdb_incremental` | success; thêm đúng các ID chưa có |
| 3 | `batch_replay` / MI04 | Giữ nguyên batch của MI02 | `tmdb_incremental` | success; không đổi dữ liệu/không thêm trùng |
| 4 | `batch_empty` / MI03 | `& $py .\test\acceptance\scenario_data.py empty` | `tmdb_incremental` | success; Movies giữ nguyên |
| 5 | `batch_existing` / MI05 | `& $py .\test\acceptance\scenario_data.py existing` | `tmdb_incremental` | success; Movies giữ nguyên |
| 6 | `batch_invalid` / MI06 | `& $py .\test\acceptance\scenario_data.py invalid` | `tmdb_incremental` | Ghi trạng thái thực; Movies không bị thay đổi |

`new` chỉ sao chép batch thật, không tự sinh ID mới. Nếu toàn bộ ID đã có ở stage, MI02 sẽ BLOCKED; quay lại Full Load sạch trước một lượt scenario mới. Không sửa snapshot để tạo ID vắng mặt giả.

**MI07 — export_failure:** sau các case trên, tắt injection nếu có, chạy Full Load sạch để batch thật có thể được nạp mới. Chạy `scenario_data.py new`, rồi `isolation.py failure-on`; đặt `$case = 'export_failure'` và chụp before. Chạy `tmdb_incremental`, đợi kết thúc, lưu log lỗi và after theo 11.1. Cần log chứa `tmdb_test_injected_export_failure`, trạng thái thực là failed và watermark không tăng. Nếu pipeline vẫn success hoặc không thấy lỗi injection, không khai failed; kịch bản chưa được kích hoạt đúng.

Ngay sau case, **kể cả after lỗi**, chạy:

```powershell
& $py .\test\acceptance\isolation.py failure-off
```

**MI08 — partial_full:** harness chưa có lệnh tự động thiết lập lỗi riêng một nhánh Full Load. Cần thiết kế can thiệp trên bản sao test, lưu thay đổi/log và khôi phục sau thử nghiệm. Nếu chưa thực hiện có kiểm soát, giữ MI08 BLOCKED; không dùng `failure-on` rồi mặc định đó là lỗi riêng một nhánh Full Load. Case này thu quan sát, không chứng minh Full Load có transaction nguyên tử.

### 11.3. Kết thúc scenarios

```powershell
& $py .\test\acceptance\isolation.py failure-off
& $py .\test\acceptance\scenario_data.py restore
```

Sau đó chạy `tmdb_ingestion` trong Mage test, chờ thành công để khôi phục stage sạch. Chạy lại build và bộ test:

```powershell
& $py .\test\acceptance\isolation.py dbt-build
if ($LASTEXITCODE -ne 0) { throw 'Build lỗi; dừng trước nghiệm thu' }
& $py .\test\acceptance\run.py --mode integration --section all --approved --snapshot full
```

Không lấy `restore` làm bằng chứng đã khôi phục DB: lệnh đó chỉ khôi phục CSV. `all` vẫn có thể BLOCKED ở BI thủ công, AI chưa triển khai, MI08 hoặc phần chưa có log; ghi đúng giới hạn.

## 12. Mage 16789 không mở được

Thử http://127.0.0.1:16789 trên Chrome/Edge ở chính máy chạy Docker. Sau đó chạy:

```powershell
& $py .\test\acceptance\isolation.py ps
docker ps -a --filter 'label=com.docker.compose.project=tmdb_test_acceptance' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
Test-NetConnection 127.0.0.1 -Port 16789
$mageContainer = docker ps -aq --filter 'label=com.docker.compose.project=tmdb_test_acceptance' --filter 'label=com.docker.compose.service=mage'
if ($mageContainer) { docker logs --tail 100 $mageContainer }
```

- Không có container: kiểm `isolated.json`, chạy `isolation.py up`, đọc lỗi.
- Mage `Exited`/`Restarting`: đọc log; không lặp up liên tục để che lỗi.
- Mage `running`, TCP mở nhưng web chưa trả dữ liệu: xem log khởi động, đợi khởi động xong rồi tải lại. PostgreSQL healthy không bảo đảm Mage web sẵn sàng.
- Docker báo permission denied/không kết nối Engine: sửa Docker/terminal trước; đây chưa phải lỗi dữ liệu pipeline.
- Cổng bị chiếm: xác định ứng dụng đang giữ cổng trước khi dừng nó; không đổi cổng riêng trong compose vì harness cố định DB test 55432.

Không xóa volume hoặc prepare lại để chữa lỗi web chưa phản hồi. Khi gửi log nhờ kiểm tra, che credential nếu xuất hiện.

## 13. Bằng chứng cần giữ và cách tiếp tục hôm sau

| Phần | Tối thiểu cần giữ |
|---|---|
| Mỗi lượt runner | Cả thư mục `test/results/acceptance_<UTC>_<id>/`, đặc biệt REPORT.md, result.json, junit.xml, pytest_output.txt |
| 3.1 | Run ID, ảnh trạng thái, log thật; các cặp before/after và log scenarios, metadata batch |
| 3.2 | Log build/rebuild/docs và bằng chứng provenance/hash trong `runtime_evidence` của lượt integration |
| 3.3 | Kết quả SQL/assertions và negative controls trong report/output của đúng lượt |
| 3.4 | Nguồn DB, thời điểm Refresh, ảnh bốn trang/model/tương tác, checklist đã điền; DAX CSV + BI01/BI02 JSON cùng snapshot + output comparator |

Giữ nguyên bằng chứng gốc; ghi phân tích/sửa lỗi trong bản ghi riêng. Không gửi nguyên `.runtime` vì chứa credentials; ưu tiên `runtime_evidence` đã được runner chọn lọc và kiểm tra file trước khi chia sẻ. Tên thư mục kết quả dùng UTC, có thể lệch 7 giờ so với giờ Việt Nam.

**Muốn nghỉ và giữ DB test**, dừng đúng hai container của project test trong Docker Desktop. Hôm sau mở Docker, đặt `$py` theo 10.1 rồi chạy `isolation.py up` và `ps`. Không chạy prepare lại. Nếu dữ liệu/source không đổi thì không cần nạp lại chỉ để mở môi trường; chọn cờ snapshot theo trạng thái dữ liệu thực tế.

**Chỉ dùng `isolation.py down` khi chấp nhận xóa dữ liệu DB test.** Sau down, up tạo lại DB trống: phải ingestion và dbt-build lại; bằng chứng cũ chỉ là lịch sử, không chứng minh DB mới. Khi source Mage/CSV thay đổi, xem phần 5.1 về bản sao workspace trước khi nghiệm thu.

**Điểm dừng nghiệm thu:** lệnh chạy xong và có REPORT chỉ xác nhận đã thực thi runner. Hoàn thành từng phần cần giải thích các FAIL/BLOCKED/SKIPPED và đính kèm bằng chứng thủ công còn thiếu; không cần và không được ép tất cả thành PASS.
