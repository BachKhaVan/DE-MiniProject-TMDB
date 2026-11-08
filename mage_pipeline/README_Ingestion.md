# Mage ingestion: Source → Staging

## Trạng thái

Full Load và các bước làm sạch cơ bản đã được triển khai. Báo cáo Giai đoạn 1 ghi nhận 4.803 dòng trong mỗi bảng staging; đây là kết quả được báo cáo trước đó, chưa phải xác minh trên database hiện tại. Incremental Load hiện là batch demo đơn giản, chưa phải luồng watermark an toàn.

## Bảng staging

| CSV | Bảng | Quy tắc làm sạch Full Load |
|---|---|---|
| `tmdb_5000_movies.csv` | `stage.stg_tmdb_movies` | Bỏ duplicate toàn dòng; bỏ dòng thiếu `id` hoặc `title`; parse `release_date` với `errors='coerce'`. |
| `tmdb_5000_credits.csv` | `stage.stg_tmdb_credits` | Bỏ duplicate toàn dòng; bỏ dòng thiếu `movie_id`. |

Các cột đa trị như `genres`, `keywords`, `production_companies`, `production_countries`, `cast` và `crew` được giữ ở dạng chuỗi JSON trong Staging để xử lý ở giai đoạn transformation. Mage/PostgreSQL có thể đổi tên một số cột dành riêng; báo cáo ghi nhận `_status` và `_cast`.

## Kết nối

Compose mặc định dùng database `warehouse`, user `labuser`, port `5432`; Mage kết nối nội bộ bằng host `postgres`, còn chương trình trên host dùng `localhost`. Mật khẩu lấy từ `.env`. Tạo riêng `mage_pipeline/io_config.yaml` theo profile Mage và không commit file này.

`postgres/init/01_init.sql` tạo các schema `stage`, `staging`, `dds`, `control`, bảng `control.etl_watermark` và dòng khởi tạo cho `tmdb_incremental`. Compose chỉ chạy init scripts khi tạo data volume PostgreSQL mới; nếu volume đã tồn tại từ trước, cần áp dụng DDL này thủ công.

## Full Load

Pipeline `tmdb_ingestion` có hai nhánh độc lập (movies và credits), mỗi nhánh gồm loader → transformer → exporter. Exporter dùng `if_exists='replace'`, vì vậy chạy lại sẽ dựng lại bảng staging từ CSV nguồn. Transformer in số dòng đã qua làm sạch vào Mage log.

Chạy `docker compose up -d`, mở `http://localhost:6789`, rồi chạy `tmdb_ingestion`. Kiểm tra số dòng và chất lượng theo [`test/README_test.md`](../test/README_test.md).

## Incremental Load demo và giới hạn

Pipeline `tmdb_incremental` có hai nhánh độc lập:

- `load_new_batch` → `export_incremental_stage`: đọc `data/raw/tmdb_new_batch.csv` và append nguyên batch vào `stage.stg_tmdb_movies`.
- `get_watermark` → `update_watermark`: đọc `lset`, tạo `cet`, rồi cập nhật watermark.

Hiện loader không lọc dữ liệu theo `lset`, exporter không deduplicate hay kiểm tra khóa đã tồn tại, batch không có nhánh credits, và graph không bảo đảm updater chỉ chạy sau khi export thành công. Chạy lặp batch có thể tạo ID trùng; chạy updater độc lập có thể đánh dấu watermark trước khi append hoàn tất. Vì vậy không nên mô tả luồng này là idempotent hoặc an toàn khi retry.

`get_watermark` cần bảng `control.etl_watermark` có dòng `pipeline_name='tmdb_incremental'`; init SQL hiện tạo sẵn trên database mới. Nếu database dùng volume cũ, áp dụng DDL bằng `docker compose exec -T postgres psql -U labuser -d warehouse -f /docker-entrypoint-initdb.d/01_init.sql`. Khi demo, chạy Full Load tạo baseline, chạy loader và exporter batch đúng một lần, xác nhận exporter thành công, rồi mới chạy updater. Script kiểm tra cũng có thể ghi nhận watermark nhưng không thay đổi database.

## Dữ liệu nguồn

Đặt `tmdb_5000_movies.csv` và `tmdb_5000_credits.csv` trong `data/raw/`. Batch demo `tmdb_new_batch.csv` cũng đặt tại đây. Thư mục/file dữ liệu nguồn được gitignore; không commit CSV thô.
