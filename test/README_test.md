# Hướng dẫn kiểm tra luồng dữ liệu TMDB

Script `test/validate_tmdb.py` chỉ đọc CSV và truy vấn PostgreSQL. Script không
chạy pipeline, không thay đổi database và không cần cài dependency Python bổ sung.
Mỗi lần chạy tạo một báo cáo mới trong `test/results/`.

## Chuẩn bị chung

1. Mở Docker Desktop và chờ Docker Engine chạy.
2. Tạo `.env` từ `.env.example`, đặt mật khẩu riêng rồi khởi động dịch vụ:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   docker compose up -d
   docker compose ps
   ```

   Không commit `.env`. Cảnh báo Compose rằng thuộc tính `version` đã cũ không
   ngăn pipeline chạy; lỗi kết nối Docker Engine thì cần khởi động Docker Desktop.
3. Đặt hai CSV nguồn `tmdb_5000_movies.csv` và `tmdb_5000_credits.csv` trong
   `data/raw/`. Đảm bảo `mage_pipeline/io_config.yaml` đã cấu hình kết nối tới
   cùng PostgreSQL/database mà Compose sử dụng.
4. Chạy lệnh từ thư mục gốc repository bằng PowerShell:

   ```powershell
   python test\validate_tmdb.py --flow all
   ```

   Có thể chọn riêng từng luồng theo bảng bên dưới. Script in đường dẫn báo cáo
   sau khi hoàn tất; kiểm tra đó có thể kết thúc với exit code khác 0 nếu có
   mục `FAIL`.

## Các trường hợp kiểm tra

| Luồng kiểm tra | Điều kiện trước khi chạy | Lệnh hoặc thao tác trong Mage | Lệnh chạy script kiểm tra | Kết quả mong đợi | Ghi chú/rủi ro |
|---|---|---|---|---|---|
| **A. Full Load** | Docker Engine đang chạy; `docker compose up -d` đã khởi động PostgreSQL và Mage; hai CSV nguồn nằm trong `data/raw/`; cấu hình Mage kết nối đúng database. | Mở `http://localhost:6789`, chạy pipeline **`tmdb_ingestion`** bằng **Run pipeline now**, đợi cả hai nhánh movies và credits hoàn tất. | `python test\validate_tmdb.py --flow full` | Báo cáo xác nhận header/cấu trúc CSV; tính số dòng dự kiến sau `drop_duplicates` và bỏ dòng thiếu khóa cần thiết; so sánh với `stage.stg_tmdb_movies` và `stage.stg_tmdb_credits`. Kiểm tra khóa null/trùng, cột và kiểu dữ liệu, quan hệ movies/credits, watermark. | Transformer movies bỏ dòng thiếu `id` hoặc `title`; credits bỏ dòng thiếu `movie_id`. `release_date` được parse với `errors='coerce'` nhưng không loại dòng có ngày không hợp lệ. Full Load dùng `replace`, nên bảng stage phản ánh batch nguồn sau làm sạch, không phải tổng của các batch incremental. |
| **B. Incremental Load** | Đã chạy Full Load để tạo baseline; PostgreSQL/Mage đang chạy; `data/raw/tmdb_new_batch.csv` tồn tại, có header tương thích movies và chứa các ID mới chưa có trong nguồn/baseline. | Trong Mage, chạy **từng block riêng lẻ theo thứ tự**: `get_watermark` → `load_new_batch` → `export_incremental_stage`. Chỉ sau khi xác nhận exporter thành công, chạy `update_watermark`. | `python test\validate_tmdb.py --flow incremental` | Báo cáo kiểm tra batch, xác nhận ID batch có trong `stage.stg_tmdb_movies`, không đè ID nguồn và không tạo khóa trùng; so sánh row count với baseline + số dòng batch được append. Báo cáo watermark như một quan sát riêng. | **Exporter đang append thẳng CSV**, không deduplicate hay lọc batch theo watermark. Không chạy lặp pipeline incremental nếu chưa Full Load lại baseline: có thể append trùng khóa. Metadata hiện nối `get_watermark` → `update_watermark` ở một nhánh riêng, không nối sau `export_incremental_stage`; không dùng `Run pipeline now` để kết luận thứ tự watermark. Chạy block watermark sau export thành công và kiểm tra log riêng. Batch demo không có credits; credits không tăng theo batch là bình thường. |

### Giới hạn cần biết về watermark

`get_watermark` đọc `control.etl_watermark.lset`, còn loader incremental hiện
đọc CSV batch nguyên trạng và exporter append dữ liệu. Vì vậy script báo cáo
`lset` quan sát được, nhưng không coi watermark là bằng chứng exporter đã chạy
thành công hay batch được lọc theo watermark. Nếu thiếu bảng hoặc dòng watermark,
báo cáo sẽ ghi rõ trạng thái và lý do.

## Lựa chọn CLI

```powershell
python test\validate_tmdb.py --flow full
python test\validate_tmdb.py --flow incremental
python test\validate_tmdb.py --flow all
```

- `full`: kiểm tra hai CSV baseline và so sánh stage với số dòng hợp lệ sau
  quy tắc làm sạch của Full Load.
- `incremental`: kiểm tra baseline, batch (nếu thiếu sẽ ghi `FAIL` trong báo
  cáo), stage sau incremental và watermark.
- `all`: thực hiện cả kiểm tra baseline lẫn incremental trong cùng báo cáo; số
  movies mong đợi là baseline hợp lệ cộng số dòng batch append.

Các báo cáo nằm trong `test/results/validation_<timestamp>.md`. Không thực
hiện thao tác phá hủy/xóa volume hoặc dữ liệu database trong quy trình kiểm tra.
