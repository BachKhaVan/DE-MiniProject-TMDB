# TMDB — Acceptance test report

- Run ID: `20261115T180604Z_9be138`
- UTC: `2026-11-15T18:06:11.371445+00:00`
- Mode: **integration**; Section: **33**
- Branch/commit: `main` / `5448edbc4512312737138cb078f1c615cbdbc247`; dirty=True
- **PASS 42 / FAIL 1 / BLOCKED 0 / SKIPPED 0 / INFO 0**

INFO là số liệu quan sát hoặc SQL tham chiếu; không tính là nghiệm thu đạt.

## Bảng toàn bộ test (requirement → evidence → kết luận)

| Test ID | Mục | Loại | Tên | Kết quả | Bằng chứng |
|---|---|---|---|---|---|
| NC01 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC01] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| NC02 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC02] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| NC03 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC03] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| NC04 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC04] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| NC05 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC05] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW01 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW01] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW02 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW02] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW03 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW03] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW04 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW04] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW05 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW05] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW06 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW06] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW07 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW07] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW08 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW08] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW09 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW09] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW10 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW10] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW11 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW11] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW12 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW12] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW13 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW13] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW14 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW14] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW15 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW15] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW16 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW16] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW17 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW17] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW18 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW18] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW19 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW19] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW20 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW20] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW21 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW21] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW22 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW22] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW23 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW23] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW24 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW24] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW25 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW25] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW26 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW26] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW27 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW27] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW28 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW28] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW29 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW29] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW30 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW30] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW31 | 3.3 | Kiểm tra độ bền | test_warehouse_invariant[DW31] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW39 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW39] | **FAIL** | `junit.xml; pytest_output.txt` |
| DW40 | 3.3 | Kiểm tra độ bền | test_warehouse_invariant[DW40] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW47 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW47] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW48 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW48] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW49 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW49] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW50 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW50] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW54 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW54] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |

## Chi tiết FAIL/BLOCKED và test được chọn cho demo


### NC01 — test_negative_controls[NC01]
- **1. Test ID:** NC01
- **2. Mục:** 3.3
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Bridge weight_factor phải bắt được sai lệch
- **5. Đầu vào:** Chỉ tmdb_test_warehouse ở localhost:55432
- **6. Các bước:** BEGIN → injection có chủ đích → chạy nguyên assertion DW → ROLLBACK
- **7. Expected:** Tạo lỗi trong isolated, SQL DW18 bắt được, sau đó rollback
- **8. Actual:** {"assertion": "DW18", "before_violations": 0, "after_injected_violations": 1, "sample": [{"movie_sk": 1, "links": 2, "total_weight": 1.25}]}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** Negative control; transaction rollback in finally
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW01 — test_warehouse_invariant[DW01]
- **1. Test ID:** DW01
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Có đúng 12 bảng fact/dim/bridge
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 0, "samples": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** DW01
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW05 — test_warehouse_invariant[DW05]
- **1. Test ID:** DW05
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Grain Fact = dim_movie = số movie_sk distinct
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 0, "samples": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** DW05
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW09 — test_warehouse_invariant[DW09]
- **1. Test ID:** DW09
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact không có FK logic mồ côi
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 0, "samples": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** DW09
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW18 — test_warehouse_invariant[DW18]
- **1. Test ID:** DW18
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge genre weight_factor dương, sum=1
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 0, "samples": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** DW18
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW19 — test_warehouse_invariant[DW19]
- **1. Test ID:** DW19
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge company weight_factor dương, sum=1
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 0, "samples": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** DW19
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW20 — test_warehouse_invariant[DW20]
- **1. Test ID:** DW20
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge country weight_factor dương, sum=1
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 0, "samples": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** DW20
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW26 — test_warehouse_invariant[DW26]
- **1. Test ID:** DW26
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact profit=revenue-budget; ROI thập phân
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 0, "samples": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** DW26
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW28 — test_warehouse_invariant[DW28]
- **1. Test ID:** DW28
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact vote_count mặc định 0 và NOT NULL
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 0, "samples": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** DW28
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW39 — test_warehouse_invariant[DW39]
- **1. Test ID:** DW39
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Weighted profit across each bridge = fact profit for covered movies
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 2, "samples": [{"bridge_type": "country", "sum_allocated": 260220306819.6707, "sum_fact": 260220306821}, {"bridge_type": "genre", "sum_allocated": 260220306810.52356, "sum_fact": 260220306821}]}
- **9. Trạng thái:** FAIL
- **10. Nguyên nhân kết quả:** DW39
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 33 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

## Giới hạn

- Kết quả tĩnh chỉ chứng minh nội dung các file trong repository; không chứng minh runtime đã chạy.
- Các hiện tượng Power BI chưa truy vấn được DAX expression / refresh trực tiếp được ghi BLOCKED.
- Kết quả từ `dbt_transform/target/` là artifacts cũ, không phải lần build mới.
- Đây không phải kết luận tổng thể thành công khi còn BLOCKED.
- Mục 3.5 là yêu cầu của đề nhưng chưa triển khai; AI01–AI04 luôn BLOCKED cho tới khi có implementation và adapter kiểm thử.
- Unit test cleaner không thay thế thực thi Mage; SQL reference INFO không chứng minh DAX đúng.

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
    "server_timestamp_utc": "2026-11-15 18:06:12.879068",
    "snapshot_id": "931:931:",
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
