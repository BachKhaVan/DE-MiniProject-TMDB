# Mage ingestion: Source → Staging

## Trạng thái hiện tại

Full Load Movies/Credits và incremental Movies theo batch CSV đã được triển khai. Bản cập nhật incremental bổ sung dependency tuần tự, bước tạo khóa chính `id` nếu chưa có và cấu hình upsert theo ID. Đây là mô phỏng incremental bằng batch tĩnh; loader chưa chọn bản ghi theo khoảng LSET/CET.

Report 3.1 đã đọc ngày 16/11/2026 (`20261116T071641Z_03ce5c`) ghi nhận 22 PASS, 0 FAIL, 10 BLOCKED, 6 INFO; MG18 kiểm graph watermark đã PASS. Các case replay/failure cần snapshot và log thật để kết luận runtime, không suy ra chỉ từ cấu hình code.

## Bảng staging

| CSV | Bảng | Quy tắc làm sạch Full Load |
|---|---|---|
| `tmdb_5000_movies.csv` | `stage.stg_tmdb_movies` | Bỏ duplicate toàn dòng; bỏ dòng thiếu `id` hoặc `title`; parse `release_date` với `errors='coerce'`. |
| `tmdb_5000_credits.csv` | `stage.stg_tmdb_credits` | Bỏ duplicate toàn dòng; bỏ dòng thiếu `movie_id`. |

Các cột đa trị được giữ ở dạng chuỗi JSON trong stage để dbt xử lý. Snapshot Full Load của lượt test trên có 4.803 dòng mỗi bảng, không trùng khóa. Không dùng số này làm expected sau khi nạp batch mới.

## Kết nối và Full Load

Compose chính dùng PostgreSQL `localhost:5432`, database `warehouse`, user `labuser`; Mage trong Docker dùng host `postgres`. Tạo `mage_pipeline/io_config.yaml` với password khớp `.env`; không commit credentials.

`postgres/init/01_init.sql` tạo schema và `control.etl_watermark` khi khởi tạo volume mới. Với volume cũ, kiểm tra trước và chỉ áp dụng lại init SQL khi thiếu cấu trúc cần thiết.

Pipeline `tmdb_ingestion` có hai nhánh Movies/Credits, mỗi nhánh loader → transformer → exporter. Exporter dùng `replace`, dựng lại stage từ nguồn. Chạy `docker compose up -d`, mở Mage chính ở http://localhost:6789 và chạy toàn pipeline. Hướng dẫn kiểm thử: [README acceptance](../test/acceptance/README.md).

## Incremental Load theo batch

Graph hiện tại chạy theo thứ tự:

1. `get_watermark`: đọc LSET từ `control.etl_watermark`, trả thông tin LSET/CET.
2. `load_new_batch`: đọc toàn bộ `data/raw/tmdb_new_batch.csv`.
3. `export_incremental_stage`: thực hiện SQL tạo PRIMARY KEY (`id`) nếu chưa phát hiện khóa chính, rồi nạp bằng `if_exists='append'`, `unique_conflict_method='UPDATE'`, `unique_constraints=['id']`.
4. `update_watermark`: là downstream của exporter, cập nhật LSET bằng `execution_date` do Mage cung cấp, hoặc thời gian hiện tại nếu không có.

`append` ở đây đi cùng cấu hình xử lý xung đột ID; không mô tả là append thuần không chống trùng. Dependency đặt updater sau exporter trong lần chạy toàn pipeline. Không chạy riêng updater để demo luồng thành công.

### Cách demo và kiểm chứng

- Full Load tạo baseline, sau đó chạy **toàn pipeline** `tmdb_incremental`.
- Xem log exporter, số dòng/ID trước và sau, khóa chính của stage và watermark.
- Để chứng minh replay không thêm trùng, chạy lại cùng batch trên DB test và so snapshot; để chứng minh exporter lỗi không cập nhật watermark, dùng kịch bản lỗi có chủ đích trên DB test.
- Các bước thu bằng chứng: [GUIDE_SCENARIOS.md](../test/acceptance/GUIDE_SCENARIOS.md). Dùng Mage test cổng 16789 và DB test cổng 55432 cho các thử nghiệm lỗi.
- Sau khi stage thay đổi, chạy dbt build rồi Refresh Power BI để cập nhật DDS/dashboard; incremental Mage không tự thực hiện hai bước này.

### Giới hạn còn đúng với source hiện tại

- Loader chưa dùng LSET/CET để lọc CSV. Watermark được lưu nhưng chưa quyết định tập bản ghi đọc; đây là batch simulation, chưa phải CDC.
- Chỉ bổ sung Movies, chưa có nhánh incremental Credits. Batch không đi qua transformer Full Load.
- Tạo PK yêu cầu dữ liệu stage hiện có không chứa ID NULL/trùng. Câu truy vấn kiểm sự tồn tại PK hiện xét tên bảng, chưa lọc schema; cần lưu ý nếu có bảng cùng tên ở schema khác.
- Cấu hình PK/upsert và graph không tự chứng minh mọi tình huống retry, batch lỗi hoặc chạy đồng thời. Chỉ kết luận những tình huống đã có bằng chứng runtime.

## Dữ liệu nguồn

Đặt Movies, Credits và `tmdb_new_batch.csv` trong `data/raw/`. Dữ liệu thô được gitignore. Tổng quan hệ thống và bàn giao: [README tổng](../README.md).
