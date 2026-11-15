# TMDB — Acceptance test report

- Run ID: `20261115T172423Z_6d2ae5`
- UTC: `2026-11-15T17:24:51.325426+00:00`
- Mode: **integration**; Section: **32**
- Branch/commit: `main` / `5448edbc4512312737138cb078f1c615cbdbc247`; dirty=True
- **PASS 33 / FAIL 1 / BLOCKED 0 / SKIPPED 0 / INFO 0**

INFO là số liệu quan sát hoặc SQL tham chiếu; không tính là nghiệm thu đạt.

## Bảng toàn bộ test (requirement → evidence → kết luận)

| Test ID | Mục | Loại | Tên | Kết quả | Bằng chứng |
|---|---|---|---|---|---|
| DB01 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB01] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB02 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB02] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB03 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB03] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB04 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB04] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB05 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB05] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB06 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB06] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB07 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB07] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB08 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB08] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DB09 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB09] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DB10 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB10] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DB11 | 3.2 | Kiểm tra độ bền | test_dbt_structure[DB11] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DB12 | 3.2 | Kiểm tra độ bền | test_dbt_structure[DB12] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DB13 | 3.2 | Kiểm tra độ bền | test_dbt_structure[DB13] | **FAIL** | `junit.xml; pytest_output.txt` |
| DW32 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW32] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW33 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW33] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW34 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW34] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW35 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW35] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW36 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW36] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW37 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW37] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW38 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW38] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW41 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW41] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW42 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW42] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW43 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW43] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW44 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW44] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW45 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW45] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW46 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW46] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW51 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW51] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW52 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW52] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW53 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW53] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW55 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW55] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW56 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW56] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW57 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW57] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW58 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW58] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |
| DW59 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW59] | **PASS** | `junit.xml; pytest_output.txt (Kết quả chạy mới)` |

## Chi tiết FAIL/BLOCKED và test được chọn cho demo


### DB05 — test_dbt_structure[DB05]
- **1. Test ID:** DB05
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** dbt refs/sources hình thành DAG hợp lệ
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** manifest hiện có đọc được, DAG không có cycle và bao phủ các SQL models
- **8. Actual:** {"models_in_old_manifest": 18, "source_node_count": 2}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** Đồ thị của artifact cũ, không phải build mới
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 32 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DB09 — test_dbt_structure[DB09]
- **1. Test ID:** DB09
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** dbt model test được chạy trên snapshot hiện tại
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có run_results của lần chạy này và DB quyền chỉ đọc
- **8. Actual:** {"build_test_nodes": 87, "statuses": {"success": 21, "pass": 87}}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** Dựa vào run_results của isolated build mới, không dùng target gốc
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 32 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DB13 — test_dbt_structure[DB13]
- **1. Test ID:** DB13
- **2. Mục:** 3.2
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Mức độ bao phủ model trong schema.yml
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cả 18 models được mô tả riêng trong schema.yml (mức mong muốn, không phải điều kiện tối thiểu của đề)
- **8. Actual:** {"models_sql": 18, "documented": 14, "missing_models": ["stg_movie_companies", "stg_movie_countries", "stg_movie_genres", "stg_movie_keywords"]}
- **9. Trạng thái:** FAIL
- **10. Nguyên nhân kết quả:** Đã quan sát vi phạm; AssertionError: Các model chưa được mô tả riêng: stg_movie_companies, stg_movie_countries, stg_movie_genres, stg_movie_keywords
assert not ['stg_movie_companies', 'stg_movie_countries', 'stg_movie_genres', 'stg_movie_keywords']
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 32 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DW41 — test_transformation_invariant[DW41]
- **1. Test ID:** DW41
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Country region chính xác theo seed, fallback Unknown
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** {"violations": 0, "samples": []}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** DW41
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Kết quả chạy mới)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 32 -Mode integration -IsolatedConfirmed
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
    "server_timestamp_utc": "2026-11-15 17:24:54.978612",
    "snapshot_id": "921:921:",
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
