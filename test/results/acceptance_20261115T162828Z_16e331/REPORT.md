# TMDB — Acceptance test report

- Run ID: `20261115T162828Z_16e331`
- UTC: `2026-11-15T16:28:35.281453+00:00`
- Mode: **integration**; Section: **31**
- Branch/commit: `main` / `d081ce2aa9b1e06fb95107c8795f415e35e39c40`; dirty=True
- **PASS 20 / FAIL 3 / BLOCKED 9 / SKIPPED 0**

## Bảng toàn bộ test (requirement → evidence → kết luận)

| Test ID | Mục | Loại | Tên | Kết quả | Bằng chứng |
|---|---|---|---|---|---|
| MG01 | 3.1 | Yêu cầu bắt buộc | test_csv_headers[MG01] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG02 | 3.1 | Yêu cầu bắt buộc | test_csv_headers[MG02] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG03 | 3.1 | Yêu cầu bắt buộc | test_csv_headers[MG03] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG04 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG04] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG05 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG05] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG06 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG06] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG07 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG07] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG08 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG08] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG09 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG09] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG10 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG10] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG11 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG11] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG12 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG12] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG13 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG13] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG14 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG14] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG15 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG15] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG16 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG16] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG17 | 3.1 | Yêu cầu bắt buộc | test_pipeline_risks[MG17] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG18 | 3.1 | Kiểm tra độ bền | test_pipeline_risks[MG18] | **FAIL** | `junit.xml; pytest_output.txt` |
| MG19 | 3.1 | Kiểm tra độ bền | test_pipeline_risks[MG19] | **FAIL** | `junit.xml; pytest_output.txt` |
| MG20 | 3.1 | Kiểm tra độ bền | test_pipeline_risks[MG20] | **FAIL** | `junit.xml; pytest_output.txt` |
| MG21 | 3.1 | Yêu cầu bắt buộc | test_mage_stage[MG21] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG22 | 3.1 | Yêu cầu bắt buộc | test_mage_stage[MG22] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG23 | 3.1 | Yêu cầu bắt buộc | test_mage_stage[MG23] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| MG24 | 3.1 | Kiểm tra độ bền | test_mage_stage[MG24] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MI01 | 3.1 | Yêu cầu bắt buộc | test_real_pipeline_scenarios[MI01] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MI02 | 3.1 | Yêu cầu bắt buộc | test_real_pipeline_scenarios[MI02] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MI03 | 3.1 | Yêu cầu bắt buộc | test_real_pipeline_scenarios[MI03] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MI04 | 3.1 | Kiểm tra độ bền | test_real_pipeline_scenarios[MI04] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MI05 | 3.1 | Kiểm tra độ bền | test_real_pipeline_scenarios[MI05] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MI06 | 3.1 | Kiểm tra độ bền | test_real_pipeline_scenarios[MI06] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MI07 | 3.1 | Kiểm tra độ bền | test_real_pipeline_scenarios[MI07] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MI08 | 3.1 | Yêu cầu bắt buộc | test_real_pipeline_scenarios[MI08] | **BLOCKED** | `junit.xml; pytest_output.txt` |

## Chi tiết FAIL/BLOCKED và test được chọn cho demo


### MG01 — test_csv_headers[MG01]
- **1. Test ID:** MG01
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** CSV tmdb_5000_movies.csv tồn tại và có header
- **5. Đầu vào:** data/raw/tmdb_5000_movies.csv
- **6. Các bước:** csv.DictReader, đối chiếu cột thực tế
- **7. Expected:** CSV có đủ 20 cột bắt buộc, không trùng header
- **8. Actual:** {"header_count": 20, "rows": 4803, "missing": [], "duplicate_headers": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** Assertion đạt trên dữ liệu/mã hiện tại.
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG18 — test_pipeline_risks[MG18]
- **1. Test ID:** MG18
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Watermark phụ thuộc vào thành công export incremental
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** update_watermark có upstream export_incremental_stage
- **8. Actual:** {"pipeline": "tmdb_incremental", "errors": ["upstream hiện tại = ['get_watermark'], thiếu exporter"]}
- **9. Trạng thái:** FAIL
- **10. Nguyên nhân kết quả:** Đã quan sát vi phạm; AssertionError: upstream hiện tại = ['get_watermark'], thiếu exporter
assert not ["upstream hiện tại = ['get_watermark'], thiếu exporter"]
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG19 — test_pipeline_risks[MG19]
- **1. Test ID:** MG19
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Loader incremental lọc batch qua LSET/CET
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Batch mới được so với lset/cet trước export
- **8. Actual:** {"loader_uses_lset_or_cet": false}
- **9. Trạng thái:** FAIL
- **10. Nguyên nhân kết quả:** Đã quan sát vi phạm; AssertionError: Loader chỉ đọc nguyên batch CSV, không dùng LSET/CET
assert None
 +  where None = <function search at 0x000002BC79052FC0>('\\b(lset|cet)\\b', 'import pandas as pd\n\nif \'data_loader\' not in globals():\n    from mage_ai.data_preparation.decorators import data...    df = pd.read_csv(\'data/raw/tmdb_new_batch.csv\')\n    print(f"Đã đọc {len(df)} dòng dữ liệu mới.")\n    return df', re.IGNORECASE)
 +    where <function search at 0x000002BC79052FC0> = re.search
[+1 more line; full report in element text]
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG20 — test_pipeline_risks[MG20]
- **1. Test ID:** MG20
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Exporter incremental xử lý ID trùng khi replay
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có logic upsert/deduplicate hoặc unique key, không tạo bản ghi trùng
- **8. Actual:** {"deduplication_in_exporter": false}
- **9. Trạng thái:** FAIL
- **10. Nguyên nhân kết quả:** Đã quan sát vi phạm; AssertionError: Exporter append không thấy cơ chế chống trùng ở cấp exporter; cần thực nghiệm replay isolated
assert False
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG21 — test_mage_stage[MG21]
- **1. Test ID:** MG21
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Full load rowcount stage so với CSV sau làm sạch
- **5. Đầu vào:** CSV nguồn + database stage
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Số hàng stage bằng số hàng drop_duplicates + dropna của transformer
- **8. Actual:** {"comparison": [{"table": "stg_tmdb_movies", "cleaned_count": 4803, "actual_count": 4803}, {"table": "stg_tmdb_credits", "cleaned_count": 4803, "actual_count": 4803}]}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** Nếu stage đã append Incremental, cần đối chiếu snapshot trước khi khẳng định FAIL
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG24 — test_mage_stage[MG24]
- **1. Test ID:** MG24
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Metadata Mage có log run thực và rowcount
- **5. Đầu vào:** Mage runtime log
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Phải có log run mới có thể khẳng định các pipeline thực thi thành công
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Cần run ID và log Mage của lần chạy mới; metadata status=executed không đủ
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Mage UI, chạy trong isolated, cung cấp run ID/log block

### MI01 — test_real_pipeline_scenarios[MI01]
- **1. Test ID:** MI01
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Full Load chạy lại giữ nguyên dữ liệu
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py full_repeat before → Mage UI run thật → scenario.py full_repeat after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu before/after của Mage run thật; xem GUIDE_SCENARIOS.md
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MI02 — test_real_pipeline_scenarios[MI02]
- **1. Test ID:** MI02
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Incremental batch mới thêm phim không trùng
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py batch_new before → Mage UI run thật → scenario.py batch_new after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu before/after của Mage run thật; xem GUIDE_SCENARIOS.md
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MI03 — test_real_pipeline_scenarios[MI03]
- **1. Test ID:** MI03
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Incremental batch rỗng không thay đổi bảng
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py batch_empty before → Mage UI run thật → scenario.py batch_empty after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu before/after của Mage run thật; xem GUIDE_SCENARIOS.md
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MI04 — test_real_pipeline_scenarios[MI04]
- **1. Test ID:** MI04
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Incremental cùng batch replay không tạo trùng
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py batch_replay before → Mage UI run thật → scenario.py batch_replay after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu before/after của Mage run thật; xem GUIDE_SCENARIOS.md
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MI05 — test_real_pipeline_scenarios[MI05]
- **1. Test ID:** MI05
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Batch chứa ID đã có không tạo duplicate
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py batch_existing before → Mage UI run thật → scenario.py batch_existing after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu before/after của Mage run thật; xem GUIDE_SCENARIOS.md
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MI06 — test_real_pipeline_scenarios[MI06]
- **1. Test ID:** MI06
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Batch lỗi không làm bẩn stage
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py batch_invalid before → Mage UI run thật → scenario.py batch_invalid after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu before/after của Mage run thật; xem GUIDE_SCENARIOS.md
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MI07 — test_real_pipeline_scenarios[MI07]
- **1. Test ID:** MI07
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Export thất bại không cập nhật watermark
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py export_failure before → Mage UI run thật → scenario.py export_failure after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu before/after của Mage run thật; xem GUIDE_SCENARIOS.md
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MI08 — test_real_pipeline_scenarios[MI08]
- **1. Test ID:** MI08
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Full Load lỗi một nhánh có snapshot mô tả
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py partial_full before → Mage UI run thật → scenario.py partial_full after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu before/after của Mage run thật; xem GUIDE_SCENARIOS.md
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 31 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

## Giới hạn

- Kết quả tĩnh chỉ chứng minh nội dung các file trong repository; không chứng minh runtime đã chạy.
- Các hiện tượng Power BI chưa truy vấn được DAX expression / refresh trực tiếp được ghi BLOCKED.
- Kết quả từ `dbt_transform/target/` là artifacts cũ, không phải lần build mới.
- Đây không phải kết luận tổng thể thành công khi còn BLOCKED.

## Môi trường và snapshot (không chứa credentials)

```json
{
  "versions": {
    "python": "3.12.8",
    "pytest": "pytest 9.2.0",
    "dbt": "Không xác định",
    "docker": "Docker version 29.9.2, build a82e528",
    "compose": "Docker Compose version v5.6.1",
    "mage": "Không có trên PATH",
    "powerbi_desktop": "Không thể kiểm tra từ môi trường CLI này"
  },
  "sources": {
    "tmdb_5000_movies.csv": {
      "rows": 4803,
      "mtime": "2026-10-21T02:50:12+00:00"
    },
    "tmdb_5000_credits.csv": {
      "rows": 4803,
      "mtime": "2026-10-21T02:49:58+00:00"
    },
    "tmdb_new_batch.csv": {
      "rows": 2,
      "mtime": "2026-10-21T06:26:46+00:00"
    }
  },
  "target": {
    "host": "127.0.0.1",
    "port": 55432,
    "dbname": "tmdb_test_warehouse",
    "user": "tmdb_test_user"
  },
  "db_snapshot": {
    "database": "tmdb_test_warehouse",
    "postgres_version": "17.11 (Debian 17.11-1.pgdg13+2)",
    "server_timestamp_utc": "2026-11-15 16:28:37.025383",
    "snapshot_id": "811:811:",
    "stage_movies": {
      "rows": 4803,
      "duplicate_keys": 0
    },
    "stage_credits": {
      "rows": 4803,
      "duplicate_keys": 0
    },
    "fact": {
      "rows": 4803,
      "duplicate_keys": 0
    },
    "watermark_lset": "2000-01-01 00:00:00+00",
    "incremental_already_appended": "Không thể xác định chắc chắn nếu không có before/after snapshot Mage của cùng database",
    "status": "READ_ONLY_SNAPSHOT"
  }
}
```
