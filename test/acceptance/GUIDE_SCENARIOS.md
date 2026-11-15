# Mage Integration — chỉ chạy trên DB cô lập, bằng pipeline thật

**Không dùng `docker compose up` tại root trong lúc test integration. Không chạy incremental trên database `warehouse` demo.** Chỉ mở `http://127.0.0.1:16789` (port test), không phải cổng `6789` của ứng dụng chính.

## 1. Chuẩn bị và Full Load

```powershell
python .\test\acceptance\isolation.py prepare
python .\test\acceptance\isolation.py up
python .\test\acceptance\isolation.py ps
```

Hãy kiểm tra có đủ CSV trong `data/raw/` **trước** `prepare`; vì dữ liệu nguồn ZIP thiếu, không thể chạy Full Load khi chưa bổ sung. Mở Mage test, chọn pipeline **`tmdb_ingestion`** (trong workspace shadow được tạo từ chính source project), nhấn Run pipeline now; ghi Mage run ID và trạng thái từng block, đặc biệt `export_movies_to_postgres`, `export_credits_to_postgres`. Kiểm tra terminal/log rằng PostgreSQL test database tên `tmdb_test_warehouse`.

Để test Full Load replay, ghi lại snapshot sau Full Load lần 1:

```powershell
python .\test\acceptance\scenario.py full_repeat before
# Chạy tmdb_ingestion LẦN 2 trong Mage TEST và đợi cả hai exporter xong
python .\test\acceptance\scenario.py full_repeat after --mage-run-id '<RUN_ID_THẬT>'
```

Test MI01 so sánh hash nội dung **cả 2 bảng**, không chỉ row count. `scenario.py` chỉ SELECT từ DB isolated; không tự chạy Mage. Dấu `<RUN_ID_THẬT>` phải thay bằng ID nhìn thấy ở Mage; không điền giả.

## 2. Incremental — các tình huống có trước/sau

Mỗi tình huống dưới đây cần: chọn batch trong shadow workspace, chụp `before`, **chạy tmdb_incremental thật trong Mage TEST**, lưu run ID/ảnh/log, chụp `after`. Mỗi kịch bản chỉ chạy khi preconditions phù hợp và chỉ tại stack isolated. Nếu dùng cùng snapshot trước một kịch bản khác, kết quả có thể bị nhiễu; nên dùng một lần Full Load test để reset stage khi cần (chỉ trên DB test). `scenario.py` từ chối ghi đè snapshot cũ; lưu evidence và chuyển archive thư mục `.runtime/scenarios` trước lần chạy mới.

| Tình huống | Setup batch chỉ trong `.runtime/workspace/data/raw` | Snapshot case | Kiểm tra |
|---|---|---|---|
| **Batch mới** | `python .\test\acceptance\scenario_data.py new` (cần batch thật của nhóm) | `batch_new` | Stage tăng, không thêm key trùng; `MI02` |
| **Batch rỗng** | `python .\test\acceptance\scenario_data.py empty` | `batch_empty` | Stage bất biến, kiểm tra log exporter; `MI03` |
| **Chạy lại** | Sau chạy batch mới, để nguyên `new`, chạy lại | `batch_replay` | Nếu append gây trùng, `MI04` FAIL độ bền, không tự xem là yêu cầu UPSERT bắt buộc |
| **ID đã tồn tại** | `python .\test\acceptance\scenario_data.py existing` | `batch_existing` | Dùng dòng movie thực từ CSV nguồn; `MI05` |
| **JSON hỏng** | `python .\test\acceptance\scenario_data.py invalid` | `batch_invalid` | Trường genres hỏng được đưa vào bản sao dòng thực; `MI06` chỉ kiểm stage, đừng kết luận toàn bộ dbt nếu chưa chạy build |
| **Export thất bại** | `new`, sau đó `isolation.py failure-on` | `export_failure` | Trigger có chủ đích làm `INSERT` lỗi; kiểm watermark trước/sau và log exporter thật; `MI07` |
| **Full Load một nhánh lỗi** | Thiết lập lỗi riêng trong isolated khi phù hợp | `partial_full` | Chỉ mô tả cả hai bảng bị ảnh hưởng ra sao; `MI08` không yêu cầu atomic tuyệt đối |

Ví dụ cú pháp cho từng case (thay `batch_new` bằng tên cột thứ ba phía trên):

```powershell
python .\test\acceptance\scenario.py batch_new before
# Mở Mage TEST chạy tmdb_incremental, ghi run id và trạng thái các block
python .\test\acceptance\scenario.py batch_new after --mage-run-id '<RUN_ID_THẬT>'
```

**Đặc biệt với failure injection:**

```powershell
python .\test\acceptance\scenario_data.py new
python .\test\acceptance\scenario.py export_failure before
python .\test\acceptance\isolation.py failure-on
# Chạy tmdb_incremental trong Mage TEST, xác nhận block exporter FAIL trong Mage UI,
# quan sát update_watermark có chạy hay không; ghi đúng run ID
python .\test\acceptance\scenario.py export_failure after --mage-run-id '<RUN_ID_THẬT>'
python .\test\acceptance\isolation.py failure-off
```

`failure-on/off` chỉ tạo/xóa function và trigger có tên `tmdb_test_fail_insert` trên bảng **isolated**. Bất kể kết quả, luôn chạy `failure-off` sau kịch bản; nếu lỗi này không tạo được, ghi BLOCKED, không giả định injection thành công. Trước khi chạy lại Full Load, luôn tắt trigger.

**Quan trọng:** `update_watermark` có nhánh riêng theo metadata và có thể chạy khác thời điểm với exporter. Để kiểm chứng fail thật, cần chụp cả run state/log và kết quả đọc `LSET` trước/sau. Snapshot/hàm SQL không tự chứng minh exporter đã fail.

## 3. dbt isolated build/test/docs và negative control

Sau khi Full Load test có đủ stage và bạn muốn thử `dbt build`:

```powershell
python .\test\acceptance\isolation.py dbt-build
python .\test\acceptance\run.py --mode integration --section 32 --approved
python .\test\acceptance\run.py --mode integration --section 33 --approved
python .\test\acceptance\run.py --mode integration --section 31 --approved
```

`dbt-build` chạy **đúng** models/seeds/tests của repo thông qua dbt Core và cấu hình `profiles-dir` mới. Negative controls `NC01–NC05` trên các bảng đã build inject sai số trọng số, profit/ROI, orphan, duplicate grain, duplicate bridge trong **một transaction được rollback**, sau đó so số vi phạm. Khi chưa có bảng DDS hoặc constraints không cho phép, case trả BLOCKED; không đụng database demo.

Nếu DBT không có trên PATH, cài dbt Core và adapter `dbt-postgres` phù hợp với `dbt_project.yml` (yêu cầu dbt >=1.10.5,<2.0), rồi chạy lại trên Windows. Không sử dụng artifacts cũ từ `dbt_transform/target/` để tuyên bố dbt build mới PASS.

## 4. Dọn dẹp

```powershell
python .\test\acceptance\isolation.py failure-off  # nếu còn trigger
python .\test\acceptance\isolation.py down
```

`down` dọn **chỉ** Compose test + volume tên `tmdb_test_acceptance_pg_data`. Snapshot/report bên trong `test/results/` cần được lưu trước. Các file `.runtime` được giữ để xem bằng chứng và cấu hình còn dùng; **không commit**, do có mật khẩu. Nếu muốn xóa `.runtime`, thực hiện thủ công sau khi `down` và sao lưu báo cáo đã mask.
