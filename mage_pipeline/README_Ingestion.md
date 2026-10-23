# BÁO CÁO & BÀN GIAO DATA INGESTION (SOURCE ➔ STAGING)
 
**Trạng thái:** 🟢 Hoàn thành & Ổn định  

Tài liệu này tổng hợp toàn bộ quy trình, kiến trúc hệ thống và các thông số kỹ thuật của Giai đoạn 1 nhằm mục đích bàn giao cho team Transformation, đồng thời cung cấp metadata chuẩn xác cho các công cụ AI/Agent tự động đọc hiểu.

---

## 1. Thông Tin Bảng Dữ Liệu (Staging Metadata)

Dữ liệu thô từ 2 file CSV (Kaggle) đã được xử lý qua pipeline, làm sạch cơ bản và nạp thành công vào PostgreSQL.

*   **Schema lưu trữ:** `stage` (và schema `control` dùng để lưu log hệ thống).
*   **Chi tiết bảng dữ liệu:**

| Nguồn File CSV | Tên bảng đích (Staging) | Số lượng bản ghi | Trạng thái Data Quality (Tiền xử lý) |
| :--- | :--- | :--- | :--- |
| `tmdb_5000_movies.csv` | `stg_tmdb_movies` | **4.803** | Đã xóa trùng lặp; Xóa dòng null `id` & `title`. |
| `tmdb_5000_credits.csv` | `stg_tmdb_credits` | **4.803** | Đã xóa trùng lặp; Xóa dòng null `movie_id`. |

---

## 2. Cấu Hình Kết Nối Cơ Sở Dữ Liệu (Database Connection)

Team dbt vui lòng dùng thông tin kết nối dưới đây để thiết lập file `profiles.yml`, `io_config.yaml` hoặc truy cập qua DBeaver/pgAdmin.

*(Mật khẩu được cấu hình riêng trong `.env`; không ghi mật khẩu thật vào tài liệu hoặc commit file `.env`.)*

*   **Host:** `localhost` *(Từ máy host)* HOẶC `postgres` *(Nếu gọi nội bộ trong mạng Docker)*
*   **Port:** `5432`
*   **Database:** Giá trị `POSTGRES_DB` trong `.env` (mặc định: `warehouse`)
*   **User:** Giá trị `POSTGRES_USER` trong `.env` (mặc định: `labuser`)
*   **Password:** Giá trị `POSTGRES_PASSWORD` trong `.env`

**Truy vấn kiểm tra nhanh (Sample Query cho AI/Agent):**
```sql
-- Kiểm tra tổng số bản ghi đảm bảo tính toàn vẹn (Expected: 4803)
SELECT COUNT(*) FROM stage.stg_tmdb_movies;
SELECT COUNT(*) FROM stage.stg_tmdb_credits;

-- Lấy mẫu 5 dòng đầu tiên để phân tích cấu trúc JSON
SELECT id, title, genres, production_companies 
FROM stage.stg_tmdb_movies 
LIMIT 5;
```

---

## 3. Kiến Trúc Pipeline & Bằng Chứng Thực Thi (Execution Proof)

Quy trình nạp dữ liệu được điều phối hoàn toàn bằng **Mage.ai**, đảm bảo khả năng mở rộng và theo dõi trực quan.

### 3.1. Cấu trúc Pipeline (`tmdb_ingestion`)
Đường ống được thiết kế theo 2 nhánh song song (Movies và Credits), đi qua 3 bước ELT cơ bản:
1.  **Data Loader (Extract):** Sử dụng Pandas đọc dữ liệu từ thư mục local `data/raw/`.
2.  **Transformer (Transform):** Áp dụng các quy tắc Data Quality cơ bản (Drop duplicates, Drop null primary keys).
3.  **Data Exporter (Load):** Nạp vào PostgreSQL với cơ chế ghi đè linh hoạt.



### 3.2. Cơ chế nạp dữ liệu (Load Strategy)
*   **Luồng chính (Full Load):** Cấu hình `if_exists='replace'`, cho phép Tuấn an tâm bấm chạy lại (re-run) pipeline bất cứ lúc nào nếu quá trình parse JSON của dbt làm hỏng dữ liệu gốc.
*   **Luồng phụ (Incremental Load):** Đã triển khai mô phỏng pipeline `tmdb_incremental` ứng dụng cơ chế `LSET/CET` kết hợp bảng `control.etl_watermark` nhằm cập nhật các batch phim mới.




---

## 4. Hướng Dẫn Khởi Chạy Hệ Thống (Local Setup)

Dành cho các thành viên khác khi clone code về máy cá nhân:

**Bước 1: Chuẩn bị dữ liệu và Môi trường**
*   Copy 2 file `tmdb_5000_movies.csv` và `tmdb_5000_credits.csv` vào thư mục `data/raw/`.
*   Tạo `.env` từ `.env.example`, đổi mật khẩu mẫu, rồi dùng cùng thông tin đó trong `io_config.yaml` và `profiles.yml` cục bộ.

**Bước 2: Khởi động hệ thống**
Khởi chạy Docker Container chứa Mage.ai và PostgreSQL:
```bash
docker compose up -d
```

**Bước 3: Thực thi Pipeline**
1.  Truy cập UI của Mage.ai tại: `http://localhost:6789`
2.  Mở pipeline `tmdb_ingestion` và nhấn **Run pipeline now** (Hoặc Play từng khối lệnh).
3.  Kiểm tra thanh log hiển thị báo cáo số dòng đã được xử lý và nạp thành công.

## 3. Hướng dẫn chạy mô phỏng Incremental Load (Chỉ dùng khi quay Demo)

Luồng `tmdb_incremental` được thiết kế để giải quyết tiêu chí "Mô phỏng nạp dữ liệu tăng dần" của Đề bài 3.1. Luồng này sử dụng cơ chế Watermark (LSET/CET) để chỉ nạp những bộ phim mới phát hành.

**Lưu ý quan trọng cho nhóm dbt:** KHÔNG CẦN chạy luồng này khi phát triển dbt để tránh làm rác dữ liệu thực tế. Nếu đã lỡ chạy, vui lòng chạy lại luồng Full Load (`tmdb_ingestion`) để reset kho dữ liệu về mốc 4.803 dòng.

**Cách test luồng Incremental:**
1. Tạo một file tên là `tmdb_new_batch.csv` trong thư mục `data/raw/` trên máy cá nhân.
2. Dán đoạn dữ liệu giả lập (2 bộ phim mới) sau đây vào file và lưu lại:
   ```csv
   budget,genres,homepage,id,keywords,original_language,original_title,overview,popularity,production_companies,production_countries,release_date,revenue,runtime,spoken_languages,status,tagline,title,vote_average,vote_count
   100000000,"[{""id"": 28, ""name"": ""Action""}]",,999991,,"en","New Movie 1","Overview 1",50.0,"[]","[]",2026-10-21,500000000,120,"[]","Released",,"New Movie 1",8.5,100
   100000000,"[{""id"": 28, ""name"": ""Action""}]",,999992,,"en","New Movie 2","Overview 2",50.0,"[]","[]",2026-10-21,500000000,120,"[]","Released",,"New Movie 2",8.5,100
---
*Báo cáo được tự động hóa chuẩn bị cho bước Data Transformation bằng dbt.*