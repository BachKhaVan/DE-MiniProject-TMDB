# TMDB — Acceptance test report

- Run ID: `20261115T172849Z_c3ee49`
- UTC: `2026-11-15T17:28:57.448582+00:00`
- Mode: **integration**; Section: **34**
- Branch/commit: `main` / `5448edbc4512312737138cb078f1c615cbdbc247`; dirty=True
- **PASS 6 / FAIL 0 / BLOCKED 16 / SKIPPED 0 / INFO 18**

INFO là số liệu quan sát hoặc SQL tham chiếu; không tính là nghiệm thu đạt.

## Bảng toàn bộ test (requirement → evidence → kết luận)

| Test ID | Mục | Loại | Tên | Kết quả | Bằng chứng |
|---|---|---|---|---|---|
| PB01 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB01] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB02 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB02] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB03 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB03] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB04 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB04] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB05 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB05] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB06 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB06] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB07 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB07] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB08 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB08] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB09 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB09] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB10 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB10] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB11 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB11] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB12 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB12] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB13 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[PB13] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB14 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[PB14] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| Q1 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[Q1] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| Q2 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[Q2] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| Q3 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[Q3] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| Q4 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[Q4] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| Q5 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[Q5] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| Q6 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[Q6] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| Q7 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[Q7] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| Q8 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[Q8] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI01 | 3.4 | Quy tắc project | test_independent_bi_sql[BI01] | **INFO** | `junit.xml; pytest_output.txt; queries/BI01.json` |
| BI02 | 3.4 | Quy tắc project | test_independent_bi_sql[BI02] | **INFO** | `junit.xml; pytest_output.txt; queries/BI02.json` |
| BI03 | 3.4 | Quy tắc project | test_independent_bi_sql[BI03] | **INFO** | `junit.xml; pytest_output.txt; queries/BI03.json` |
| BI04 | 3.4 | Quy tắc project | test_independent_bi_sql[BI04] | **INFO** | `junit.xml; pytest_output.txt; queries/BI04.json` |
| BI05 | 3.4 | Quy tắc project | test_independent_bi_sql[BI05] | **INFO** | `junit.xml; pytest_output.txt; queries/BI05.json` |
| BI06 | 3.4 | Quy tắc project | test_independent_bi_sql[BI06] | **INFO** | `junit.xml; pytest_output.txt; queries/BI06.json` |
| Q1SQL | 3.4 | Quy tắc project | test_independent_bi_sql[Q1SQL] | **INFO** | `junit.xml; pytest_output.txt; queries/Q1SQL.json` |
| Q2SQL | 3.4 | Quy tắc project | test_independent_bi_sql[Q2SQL] | **INFO** | `junit.xml; pytest_output.txt; queries/Q2SQL.json` |
| Q3SQL | 3.4 | Quy tắc project | test_independent_bi_sql[Q3SQL] | **INFO** | `junit.xml; pytest_output.txt; queries/Q3SQL.json` |
| Q4SQL | 3.4 | Quy tắc project | test_independent_bi_sql[Q4SQL] | **INFO** | `junit.xml; pytest_output.txt; queries/Q4SQL.json` |
| Q5SQL | 3.4 | Quy tắc project | test_independent_bi_sql[Q5SQL] | **INFO** | `junit.xml; pytest_output.txt; queries/Q5SQL.json` |
| Q6SQL | 3.4 | Quy tắc project | test_independent_bi_sql[Q6SQL] | **INFO** | `junit.xml; pytest_output.txt; queries/Q6SQL.json` |
| Q7SQL | 3.4 | Quy tắc project | test_independent_bi_sql[Q7SQL] | **INFO** | `junit.xml; pytest_output.txt; queries/Q7SQL.json` |
| Q8SQL | 3.4 | Quy tắc project | test_independent_bi_sql[Q8SQL] | **INFO** | `junit.xml; pytest_output.txt; queries/Q8SQL.json` |
| BI07 | 3.4 | Quy tắc project | test_independent_bi_sql[BI07] | **INFO** | `junit.xml; pytest_output.txt; queries/BI07.json` |
| BI08 | 3.4 | Quy tắc project | test_independent_bi_sql[BI08] | **INFO** | `junit.xml; pytest_output.txt; queries/BI08.json` |
| BI09 | 3.4 | Quy tắc project | test_independent_bi_sql[BI09] | **INFO** | `junit.xml; pytest_output.txt; queries/BI09.json` |
| BI10 | 3.4 | Quy tắc project | test_independent_bi_sql[BI10] | **INFO** | `junit.xml; pytest_output.txt; queries/BI10.json` |

## Chi tiết FAIL/BLOCKED và test được chọn cho demo


### PB02 — test_powerbi_metadata_and_manual[PB02]
- **1. Test ID:** PB02
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Có tối thiểu hai trang Dashboard
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Ít nhất 2 trang theo đề; ghi nhận 4 trang là trạng thái báo cáo
- **8. Actual:** {"page_count": 4, "names": ["Overview", "Financial drivers", "Companies & Countries", "Audience & Ratings"]}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** Assertion đạt trên dữ liệu/mã hiện tại.
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB07 — test_powerbi_metadata_and_manual[PB07]
- **1. Test ID:** PB07
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Drill-down thời gian hoạt động
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Dùng giao diện Power BI Desktop để mở và thao tác drill-down
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB08 — test_powerbi_metadata_and_manual[PB08]
- **1. Test ID:** PB08
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Relationships đúng cardinality và cross-filter
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Truy vấn semantic model hoặc TMDL; DataModel nén không thể xác minh tĩnh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB09 — test_powerbi_metadata_and_manual[PB09]
- **1. Test ID:** PB09
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** DAX measures tính đúng với SQL
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Phải đọc DAX expression và cùng filter-context rồi mới kết luận
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB10 — test_powerbi_metadata_and_manual[PB10]
- **1. Test ID:** PB10
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Top N được sort theo measure hiển thị
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cần truy vấn/mở visual và xem sortBy hay ranking filter
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB11 — test_powerbi_metadata_and_manual[PB11]
- **1. Test ID:** PB11
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Ngưỡng Min Movies, Min Votes dùng đúng measure
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Kiểm tra khi đổi các tham số trong Desktop và truy vấn SQL
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB12 — test_powerbi_metadata_and_manual[PB12]
- **1. Test ID:** PB12
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Refresh Import thành công và khớp DDS
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cần refresh thật, thời điểm refresh, các KPI sau refresh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB13 — test_powerbi_metadata_and_manual[PB13]
- **1. Test ID:** PB13
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Allocation Weighted và Full đổi thứ hạng
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cần quan sát report + đối chiếu SQL cùng snapshot
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB14 — test_powerbi_metadata_and_manual[PB14]
- **1. Test ID:** PB14
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Country=USA, Year=2014, Genre=Action
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cần cùng filter context tại Desktop và số liệu SQL độc lập
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### Q1 — test_powerbi_metadata_and_manual[Q1]
- **1. Test ID:** Q1
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Câu hỏi nghiệp vụ Q1
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có visual/measure trả lời đủ các vế + SQL cùng snapshot + ảnh xác minh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chụp visual trang liên quan đến Q1; đối chiếu giá trị SQL với đúng filters

### Q2 — test_powerbi_metadata_and_manual[Q2]
- **1. Test ID:** Q2
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Câu hỏi nghiệp vụ Q2
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có visual/measure trả lời đủ các vế + SQL cùng snapshot + ảnh xác minh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chụp visual trang liên quan đến Q2; đối chiếu giá trị SQL với đúng filters

### Q3 — test_powerbi_metadata_and_manual[Q3]
- **1. Test ID:** Q3
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Câu hỏi nghiệp vụ Q3
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có visual/measure trả lời đủ các vế + SQL cùng snapshot + ảnh xác minh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chụp visual trang liên quan đến Q3; đối chiếu giá trị SQL với đúng filters

### Q4 — test_powerbi_metadata_and_manual[Q4]
- **1. Test ID:** Q4
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Câu hỏi nghiệp vụ Q4
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có visual/measure trả lời đủ các vế + SQL cùng snapshot + ảnh xác minh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chụp visual trang liên quan đến Q4; đối chiếu giá trị SQL với đúng filters

### Q5 — test_powerbi_metadata_and_manual[Q5]
- **1. Test ID:** Q5
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Câu hỏi nghiệp vụ Q5
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có visual/measure trả lời đủ các vế + SQL cùng snapshot + ảnh xác minh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chụp visual trang liên quan đến Q5; đối chiếu giá trị SQL với đúng filters

### Q6 — test_powerbi_metadata_and_manual[Q6]
- **1. Test ID:** Q6
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Câu hỏi nghiệp vụ Q6
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có visual/measure trả lời đủ các vế + SQL cùng snapshot + ảnh xác minh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chụp visual trang liên quan đến Q6; đối chiếu giá trị SQL với đúng filters

### Q7 — test_powerbi_metadata_and_manual[Q7]
- **1. Test ID:** Q7
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Câu hỏi nghiệp vụ Q7
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có visual/measure trả lời đủ các vế + SQL cùng snapshot + ảnh xác minh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chụp visual trang liên quan đến Q7; đối chiếu giá trị SQL với đúng filters

### Q8 — test_powerbi_metadata_and_manual[Q8]
- **1. Test ID:** Q8
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Câu hỏi nghiệp vụ Q8
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có visual/measure trả lời đủ các vế + SQL cùng snapshot + ảnh xác minh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Chụp visual trang liên quan đến Q8; đối chiếu giá trị SQL với đúng filters

### BI01 — test_independent_bi_sql[BI01]
- **1. Test ID:** BI01
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** KPI toàn danh mục, cùng tập phim finance-valid
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** {"total_rows": 1, "sample": [{"movies": 4803, "valid_movies": 3229, "valid_revenue": "391493508997", "valid_budget": "131273202176", "total_profit": "260220306821", "roi_overall": "1.9822804845738328", "roi_median": 1.3004, "pct_over_budget": "0.75503251780737070300"}]}
- **9. Trạng thái:** INFO
- **10. Nguyên nhân kết quả:** SQL reference độc lập; chưa so với giá trị DAX/screenshot/Refresh Power BI
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt; queries/BI01.json
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI02 — test_independent_bi_sql[BI02]
- **1. Test ID:** BI02
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Country USA + Year 2014 + Genre Action (không nhân đôi phim)
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** {"total_rows": 1, "sample": [{"movies": 47, "valid_movies": 41, "valid_revenue": "13838380577", "total_profit": "9874580577", "roi_median": 2.1637, "pct_over_budget": "0.87804878048780487805"}]}
- **9. Trạng thái:** INFO
- **10. Nguyên nhân kết quả:** SQL reference độc lập; chưa so với giá trị DAX/screenshot/Refresh Power BI
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt; queries/BI02.json
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI05 — test_independent_bi_sql[BI05]
- **1. Test ID:** BI05
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Một phim nhiều genre, minh họa 1/k từ dữ liệu thật
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** {"total_rows": 5, "sample": [{"movie_nk": 11904, "title": "Young Sherlock Holmes", "genre_count": 7, "each_weight": "0.1428571429", "total_weight": "1.0000000003", "genres": "Action, Adventure, Crime, Drama, Family, Mystery, Thriller"}, {"movie_nk": 12589, "title": "Jimmy Neutron: Boy Genius", "genre_count": 7, "each_weight": "0.1428571429", "total_weight": "1.0000000003", "genres": "Action, Adventure, Animation, Comedy, Family, Fantasy, Science Fiction"}, {"movie_nk": 15173, "title": "Jonah: A VeggieTales Movie", "genre_count": 7, "each_weight": "0.1428571429", "total_weight": "1.0000000003", "genres": "Action, Adventure, Animation, Comedy, Family, Fantasy, Romance"}, {"movie_nk": 17130, "title": "Crossroads", "genre_count": 7, "each_weight": "0.1428571429", "total_weight": "1.0000000003", "genres": "Action, Adventure, Comedy, Drama, Family, Music, Romance"}, {"movie_nk": 182, "title": "The Good German", "genre_count": 6, "each_weight": "0.1666666667", "total_weight": "1.0000000002", "genres": "Crime, Drama, Mystery, Romance, Thriller, War"}]}
- **9. Trạng thái:** INFO
- **10. Nguyên nhân kết quả:** SQL reference độc lập; chưa so với giá trị DAX/screenshot/Refresh Power BI
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt; queries/BI05.json
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### Q5SQL — test_independent_bi_sql[Q5SQL]
- **1. Test ID:** Q5SQL
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Q5 Hãng lợi nhuận Weighted vs Full (không nhân đôi hợp tác)
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** {"total_rows": 20, "sample": [{"company_name": "Paramount Pictures", "valid_movies": 245, "weighted_profit": "10928177432.6972330126", "full_profit": "27748862805"}, {"company_name": "Universal Pictures", "valid_movies": 273, "weighted_profit": "10374951894.1988289844", "full_profit": "29509237061"}, {"company_name": "Warner Bros.", "valid_movies": 280, "weighted_profit": "9660550129.0395710841", "full_profit": "30938380614"}, {"company_name": "Twentieth Century Fox Film Corporation", "valid_movies": 201, "weighted_profit": "9434182190.6842137858", "full_profit": "28642711776"}, {"company_name": "Walt Disney Pictures", "valid_movies": 96, "weighted_profit": "8444901487.5892091283", "full_profit": "19266982158"}, {"company_name": "Columbia Pictures", "valid_movies": 167, "weighted_profit": "6862093615.1617417835", "full_profit": "17971759867"}, {"company_name": "DreamWorks Animation", "valid_movies": 31, "weighted_profit": "5964348052.1658855045", "full_profit": "9085011861"}, {"company_name": "Marvel Studios", "valid_movies": 13, "weighted_profit": "5182928472.3791532102", "full_profit": "7768400680"}, {"company_name": "New Line Cinema", "valid_movies": 142, "weighted_profit": "5000763213.0109750884", "full_profit": "13593525592"}, {"company_name": "Pixar Animation Studios", "valid_movies": 16, "weighted_profit": "4776188843.9886229380", "full_profit": "7508792788"}, {"company_name": "Lucasfilm", "valid_movies": 14, "weighted_profit": "3897027781.4980190823", "full_profit": "5810309700"}, {"company_name": "Amblin Entertainment", "valid_movies": 47, "weighted_profit": "3596092271.4722603167", "full_profit": "12605035147"}, {"company_name": "DreamWorks SKG", "valid_movies": 67, "weighted_profit": "2796564203.6503601714", "full_profit": "10032033626"}, {"company_name": "Eon Productions", "valid_movies": 22, "weighted_profit": "2431311563.2916863888", "full_profit": "3869339899"}, {"company_name": "Touchstone Pictures", "valid_movies": 93, "weighted_profit": "2352710145.5330990236", "full_profit": "5928998765"}, {"company_name": "Metro-Goldwyn-Mayer (MGM)", "valid_movies": 92, "weighted_profit": "2071088820.6812497289", "full_profit": "6106230207"}, {"company_name": "Dune Entertainment", "valid_movies": 54, "weighted_profit": "2059240626.3653134239", "full_profit": "9728281204"}, {"company_name": "Columbia Pictures Corporation", "valid_movies": 86, "weighted_profit": "1959980868.6745915722", "full_profit": "5424132526"}, {"company_name": "Twentieth Century Fox Animation", "valid_movies": 11, "weighted_profit": "1896739823.9841646110", "full_profit": "3975552091"}, {"company_name": "Blue Sky Studios", "valid_movies": 9, "weighted_profit": "1834612369.4891914288", "full_profit": "3777310451"}]}
- **9. Trạng thái:** INFO
- **10. Nguyên nhân kết quả:** SQL reference độc lập; chưa so với giá trị DAX/screenshot/Refresh Power BI
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt; queries/Q5SQL.json
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI10 — test_independent_bi_sql[BI10]
- **1. Test ID:** BI10
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Ngưỡng Min Votes 100 và 1000 theo LanguageGroup
- **5. Đầu vào:** Read-only dds (current snapshot)
- **6. Các bước:** SELECT theo filter; ghi đầy đủ kết quả vào queries/<ID>.json
- **7. Expected:** SQL độc lập tính được giá trị tham chiếu cho UI; chưa chứng minh DAX đúng
- **8. Actual:** {"total_rows": 2, "sample": [{"language_group": "English", "movies_votes_100": 3018, "movies_votes_1000": 912, "valid_movies_votes_1000": 899}, {"language_group": "Non-English", "movies_votes_100": 144, "movies_votes_1000": 12, "valid_movies_votes_1000": 12}]}
- **9. Trạng thái:** INFO
- **10. Nguyên nhân kết quả:** SQL reference độc lập; chưa so với giá trị DAX/screenshot/Refresh Power BI
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt; queries/BI10.json
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section 34 -Mode integration -IsolatedConfirmed
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
    "server_timestamp_utc": "2026-11-15 17:29:00.995615",
    "snapshot_id": "926:926:",
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
