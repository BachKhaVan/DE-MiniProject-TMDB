# TMDB Acceptance Tests — mục 3.1–3.4

Bộ kiểm thử **Python + pytest** cho repository `DE-MiniProject-TMDB`, bổ sung vào thư mục `test/` mà **không sửa bất kỳ file gốc nào**. Phạm vi: Mage.ai (3.1), dbt (3.2), Data Warehouse (3.3), Power BI (3.4), Q1–Q8 và negative control. Không kiểm thử 3.5 Generative AI.

> **Ranh giới bằng chứng:** (1) phát hiện trong code; (2) artifacts cũ; (3) kết quả chạy mới; (4) phần Power BI phải xác minh thủ công. `PASS` một phát hiện tĩnh KHÔNG có nghĩa pipeline đã chạy đúng. `BLOCKED` không đồng nghĩa `FAIL`. Các kiểm tra nâng cao không bắt buộc của đề được ghi `Kiểm tra độ bền`.

## 1. Đưa vào project

Giải nén ZIP giao tại thư mục gốc repository, **giữ nguyên cấu trúc** `test/acceptance/` và `test/run_acceptance.ps1`. ZIP chỉ có **file mới**; các file `test/validate_tmdb.py`, `test/README_test.md` hiện có được giữ nguyên. Bạn chạy trên **máy Windows của mình**, không phải chạy từ ChatGPT.

Cần Python 3.10+ (đề xuất 3.12), PowerShell, quyền đọc repository. Các gói cần thêm chỉ trong `requirements.txt` này; không dùng `.venv` trong ZIP nguồn làm môi trường tái sử dụng vì môi trường đóng gói từ máy khác.

```powershell
# Từ thư mục gốc DE-MiniProject-TMDB
py -3 -m venv .venv_test
.\.venv_test\Scripts\python.exe -m pip install -r .\test\acceptance\requirements.txt
# Dùng Python thuộc .venv_test cho các lệnh bên dưới, hoặc kích hoạt:
.\.venv_test\Scripts\Activate.ps1
```

Nếu PowerShell không cho phép kích hoạt venv, dùng `.\.venv_test\Scripts\python.exe` cho lệnh `python` và gọi script `.ps1` bằng PowerShell đã có Python trên PATH; **không** cần thay Execution Policy toàn hệ thống.

### Kiểm tra nhanh chỉ đọc — không cần Docker chạy

```powershell
python .\test\acceptance\run.py --mode readonly --section all
python .\test\acceptance\run.py --mode readonly --section 31
python .\test\acceptance\run.py --mode readonly --section 32
python .\test\acceptance\run.py --mode readonly --section 33
python .\test\acceptance\run.py --mode readonly --section 34
```

Tương đương một entry point PowerShell:

```powershell
.\test\run_acceptance.ps1 -Section all -Mode readonly
.\test\run_acceptance.ps1 -Section 33 -Mode readonly
```

Nếu hệ thống PowerShell chặn việc thực thi script, dùng `python .\test\acceptance\run.py` như trên. **Không** có lệnh ở chế độ `readonly` thực hiện `INSERT`, `UPDATE`, `DELETE`, `dbt build`, `dbt seed` hay Mage run.

### Cho phép đọc PostgreSQL demo hiện có

Thiết lập credentials **trong phiên terminal của bạn** (không commit hoặc quay màn hình lúc gõ mật khẩu); bộ test không tự in `.env`, `profiles.yml`, `io_config.yaml`:

```powershell
$env:TMDB_DB_HOST = '127.0.0.1'
$env:TMDB_DB_PORT = '5432'
$env:TMDB_DB_NAME = 'warehouse'
$env:TMDB_DB_USER = 'labuser'
$env:TMDB_DB_PASSWORD = Read-Host 'Mật khẩu PostgreSQL demo'
python .\test\acceptance\run.py --mode readonly --section 33
```

Nếu bạn đã dùng cổng/DB khác, đổi biến tương ứng; không chỉnh `compose.yaml` hay `.env`. Connection pytest tạo session `default_transaction_read_only=on`, `REPEATABLE READ READ ONLY`. Mất kết nối sẽ trả `BLOCKED`; SQL có số vi phạm khác 0 mới là `FAIL`.

**CSV không có trong ZIP:** `data/raw/tmdb_5000_movies.csv`, `data/raw/tmdb_5000_credits.csv`, `data/raw/tmdb_new_batch.csv`. Hãy chép các CSV thực của nhóm vào đúng vị trí trong project **trước khi chạy** (không điền số liệu giả). Các test phụ thuộc thiếu CSV trả `BLOCKED`.

## 2. Chế độ isolated — chỉ chạy khi đồng ý cho phép ghi vào database test

Chỉ sử dụng Compose **riêng**, tuyệt đối **không chạy cùng** `compose.yaml` gốc; không chạy Full Load, Incremental, `dbt seed` hay `dbt build` trên `warehouse` demo. Hướng dẫn đầy đủ ở `GUIDE_SCENARIOS.md`.

Định danh cố định: Compose `tmdb_test_acceptance`; volume `tmdb_test_acceptance_pg_data`; Postgres `tmdb_test_warehouse`, user `tmdb_test_user`, **localhost:55432**, Mage UI **localhost:16789**. `postgres/init/01_init.sql` gốc được mount chỉ đọc và tự chạy khi volume test mới khởi tạo. Cấu hình `io_config.yaml` và `profiles.yml` **mới** được tạo **bên trong `test/acceptance/.runtime/`**, không chỉnh cấu hình chính. Mage sử dụng **bản sao không sửa** của source blocks + metadata pipeline thật.

```powershell
python .\test\acceptance\isolation.py prepare
python .\test\acceptance\isolation.py up
python .\test\acceptance\isolation.py ps
# Mở http://127.0.0.1:16789, chạy pipeline tmdb_ingestion trên Mage TEST
# Chạy các kịch bản Incremental trên Mage TEST theo GUIDE_SCENARIOS.md
python .\test\acceptance\isolation.py dbt-build
python .\test\acceptance\run.py --mode integration --section all --approved
# Dọn CHỈ tài nguyên riêng của bộ test, sau khi lưu evidence:
python .\test\acceptance\isolation.py down
```

Trong PowerShell có thể chạy thay dòng acceptance bằng:

```powershell
.\test\run_acceptance.ps1 -Mode integration -Section all -IsolatedConfirmed
```

`prepare` **không** tự ý ghi đè cấu hình test có sẵn. Các file có password trong `.runtime/` bị `.gitignore`; không mở/chụp/quay/commit chúng. `down` chỉ hạ stack có project name test và volume test; không xóa `pg_data` hay Docker containers của project gốc. `dbt-build` chạy `seed → build → docs generate` với `--profiles-dir` riêng và artifact/log trong `.runtime/`. Mọi thao tác này cần DB/Mage/Docker thực sự đang chạy trên máy bạn.

## 3. Cấu trúc bàn giao

```text
test/
├── validate_tmdb.py                 # có sẵn — KHÔNG SỬA
├── README_test.md                  # có sẵn — KHÔNG SỬA
├── run_acceptance.ps1              # mới, gọi một lệnh PowerShell
└── acceptance/
    ├── README.md
    ├── AUDIT_PHASE1.md
    ├── MATRIX.md
    ├── CHECKLIST_POWERBI.md
    ├── GUIDE_SCENARIOS.md
    ├── VIDEO_DEMO.md
    ├── requirements.txt
    ├── pytest.ini
    ├── core.py, conftest.py, run.py
    ├── sql_checks.py, bi_queries.py
    ├── test_31_mage.py, test_31_scenarios.py
    ├── test_32_dbt.py, test_32_sql.py
    ├── test_33_warehouse.py, test_33_negative.py
    ├── test_34_powerbi.py, test_34_sql_reference.py
    ├── isolation.py, compose.isolated.yaml
    ├── scenario.py, scenario_data.py
    └── .gitignore
```

Không thực hiện commit/push. Một lượt chạy `run.py` tạo một thư mục **mới**:

```text
test/results/acceptance_<UTC>_<6ký-tự>/
├── result.json          # mỗi test: 14 trường và metadata
├── REPORT.md            # ma trận/tóm tắt và chi tiết FAIL/BLOCKED/demo
├── junit.xml            # bằng chứng pytest có dữ liệu actual trong properties
└── pytest_output.txt    # log đã mask secret theo environment
```

`result.json` gồm branch/commit/dirty nếu có Git local, versions và snapshot CSV nếu có. Thông tin từ PBIX không chứng minh refresh. Runner phân biệt **0 = đạt hoàn toàn trong phạm vi chạy**, **1 = có FAIL**, **2 = không FAIL nhưng có BLOCKED hoặc SKIPPED theo mode**. Không sử dụng tỷ lệ PASS để tuyên bố project đã đạt bao nhiêu % yêu cầu.

## 4. Ý nghĩa từng nhóm

| Nhóm | Những gì kiểm được | Bằng chứng giới hạn |
|---|---|---|
| `MG01–MG24` | CSV/transformer/Mage metadata/rowcounts stage/watermark | Tĩnh + SQL read-only; dữ liệu thiếu thì BLOCKED |
| `MI01–MI08` | Full reload, incremental new/empty/replay/existing/malformed/failure/partial | Cần hai snapshot, Mage run ID thật trong isolated |
| `DB01–DB13` | SQL models, seeds, YAML tests, sources, DAG, docs/build | Artifacts cũ chỉ là tĩnh; isolated build mới là runtime |
| `DW01–DW49` | 12 bảng DDS, keys/FKs, grain, Unknown, bridges, weight, financial, dates | Query violation SQL độc lập, `FAIL` khi có dòng sai |
| `NC01–NC05` | Injection lỗi FK/duplicate/ROI/weights | Chỉ database isolated, rollback mọi transaction |
| `PB01–PB14` | Số trang/visuals/measure refs trong PBIX và checklist DAX/UI | Không khẳng định DAX/relationships/Refresh khi chỉ đọc PBIX |
| `BI01–BI10`, `Q1SQL–Q8SQL` | Tham chiếu SQL KPI/Q1–Q8/định lượng demo | PASS nghĩa tính được SQL, **chưa** chứng minh bằng DAX |
| `Q1–Q8` | Đối chiếu báo cáo từng câu hỏi nghiệp vụ | Phải có số từ Power BI cùng snapshot/bộ lọc |

Test fail về *độ bền bổ sung* như thiếu dedup/upsert không mặc định là trượt mục 3.1 của đề. Test `DB13` chỉ rà độ phủ tài liệu cho mọi model, **không** là yêu cầu bắt buộc rằng từng model phải có entry riêng. Các baseline 4.803 phim và 391,49 tỷ là số từ tài liệu snapshot cũ, **không** phải expected cứng trên database hiện tại.

## 5. Kiểm tra nhanh toàn vẹn harness

```powershell
python -m pytest -c .\test\acceptance\pytest.ini .\test\acceptance --collect-only -q
python -m py_compile .\test\acceptance\*.py  # dùng riêng từng file nếu PowerShell không mở rộng wildcard
```

`postgres/verify_dds_dw.sql` và `test/validate_tmdb.py` gốc được giữ để dùng thêm khi demo: `python .\test\validate_tmdb.py --flow full`. Lưu ý script cũ có semantics FAIL riêng, **không** dùng nó để khẳng định snapshot đã là Full Load khi Incremental đã append.

## 6. Quan trọng trước video nghiệm thu

Đọc `VIDEO_DEMO.md` và `CHECKLIST_POWERBI.md`. Những phần không kiểm chứng được do đang ở ChatGPT online phải để `BLOCKED`, không điền kết quả mong muốn thành actual. Khi chạy Docker/Mage/Power BI trên máy bạn, lưu lại đúng run ID, ảnh, thời điểm, filter và refresh.
