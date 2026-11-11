# BÁO CÁO KIỂM TRA VÀ NGHIỆM THU DATA WAREHOUSE (DDS VERIFICATION REPORT)

* **Dự án:** TMDB 5000 Movie Data Warehouse & BI Analytics System
* **Người thực hiện:** Thịnh (Phụ trách Phần 3.3 – Data Warehouse)
* **Hạng mục bàn giao:** Kết quả kiểm tra số lượng bản ghi, tính hợp lệ của khóa (PK/FK/UNIQUE), trọng số `WeightFactor`, xử lý dữ liệu thiếu (`SK = -1`) và các chỉ số tài chính sau khi dbt nạp dữ liệu vào schema `dds`.
* **File SQL liên quan:**
  * DDL khởi tạo môi trường: [`postgres/init/01_init.sql`](postgres/init/01_init.sql)
  * DDL định nghĩa tầng DDS: [`postgres/init/02_dds_schema.sql`](postgres/init/02_dds_schema.sql)
  * Script SQL kiểm tra nghiệm thu DW: [`postgres/verify_dds_dw.sql`](postgres/verify_dds_dw.sql)
  * Tài liệu đặc tả Schema & Grain: [`Schema_Report.md`](Schema_Report.md)

---

## 1. KẾT QUẢ RÀ SOÁT VÀ KẾ THỪA CẤU TRÚC DATA WAREHOUSE

Thực hiện nhiệm vụ Mục 2.2 trong bản phân công công việc, toàn bộ cấu trúc tầng Data Warehouse (`dds` trên PostgreSQL 17) đã được rà soát, chuẩn hóa và đồng bộ 100% với thiết kế đa chiều (`modeling.pdf`) cũng như project `dbt_transform`:

1. **Chuẩn hóa Grain của `dds.fact_movie`:**
   * Mỗi dòng biểu diễn **một bộ phim điện ảnh duy nhất** (`movie_sk` vừa là `PRIMARY KEY` vừa là `FOREIGN KEY` tham chiếu 1–1 tới `dds.dim_movie`).
   * Không phát sinh nhân bản dòng từ các thuộc tính đa trị (`genres`, `production_companies`, `production_countries`, `keywords`).
2. **Hoàn thiện 7 bảng Dimension (`dim_*`) và 4 bảng Bridge (`bridge_movie_*`):**
   * **3 Dimension đơn trị:** `dds.dim_movie` (làm điểm neo trung tâm và chứa `runtime_band`, `budget_band`, `country_count`, `country_type`), `dds.dim_date` (phân cấp `Date -> Month -> Quarter -> Year -> Decade`), `dds.dim_language` (phân cấp `LanguageName -> LanguageGroup`).
   * **4 Dimension đa trị:** `dds.dim_genre`, `dds.dim_company`, `dds.dim_country`, `dds.dim_keyword`.
   * **4 Bridge Tables:** `dds.bridge_movie_genre`, `dds.bridge_movie_company`, `dds.bridge_movie_country` (có cột `weight_factor DECIMAL(18, 10)`) và `dds.bridge_movie_keyword` (không có cột `weight_factor`).

---

## 2. KIỂM TRA SỐ LƯỢNG BẢN GHI TRONG SCHEMA `dds` SAU KHI DBT NẠP DỮ LIỆU

Kết quả thực thi truy vấn kiểm đếm số dòng trên PostgreSQL 17 sau khi chạy `dbt build` thành công:

| Nhóm bảng | Tên bảng vật lý | Số lượng bản ghi (Rows) | Ghi chú kiểm tra |
| :--- | :--- | ---: | :--- |
| **Fact** | `dds.fact_movie` | **4.803** | Khớp chính xác 4.803 bộ phim hợp lệ từ nguồn `stage.stg_tmdb_movies`. |
| **Dimension (Đơn trị)** | `dds.dim_movie` | **4.803** | Quan hệ 1–1 tuyệt đối với `dds.fact_movie` (0 dòng Unknown). |
| **Dimension (Đơn trị)** | `dds.dim_date` | **36.679** | Dải lịch liên tục từ `1916-09-04` đến `2017-02-03` (`36.678` ngày) + `1` dòng Unknown (`date_sk = -1`). |
| **Dimension (Đơn trị)** | `dds.dim_language` | **38** | `37` mã ngôn ngữ gốc ISO 639-1 trong dataset + `1` dòng Unknown (`language_sk = -1`). |
| **Dimension (Đa trị)** | `dds.dim_genre` | **21** | `20` thể loại phim TMDB + `1` dòng Unknown (`genre_sk = -1`). |
| **Dimension (Đa trị)** | `dds.dim_company` | **5.048** | `5.047` hãng sản xuất phân biệt + `1` dòng Unknown (`company_sk = -1`). |
| **Dimension (Đa trị)** | `dds.dim_country` | **89** | `88` quốc gia ISO 3166-1 + `1` dòng Unknown (`country_sk = -1`). |
| **Dimension (Đa trị)** | `dds.dim_keyword` | **9.814** | `9.813` từ khóa TMDB + `1` dòng Unknown (`keyword_sk = -1`). |
| **Bridge** | `dds.bridge_movie_genre` | **12.188** | Bao phủ đủ 4.803 phim (gồm 28 liên kết fallback về `genre_sk = -1`). |
| **Bridge** | `dds.bridge_movie_company` | **14.028** | Bao phủ đủ 4.803 phim (gồm 351 liên kết fallback về `company_sk = -1`). |
| **Bridge** | `dds.bridge_movie_country` | **6.610** | Bao phủ đủ 4.803 phim (gồm 174 liên kết fallback về `country_sk = -1`). |
| **Bridge** | `dds.bridge_movie_keyword` | **36.194** | Các cặp liên kết `(movie_sk, keyword_sk)` phân biệt. |

---

## 3. KIỂM TRA TÍNH HỢP LỆ CỦA KHÓA CHÍNH, KHÓA NGOẠI VÀ RÀNG BUỘC VẬT LÝ

### 3.1. Kiểm tra Grain và Toàn vẹn tham chiếu (Referential Integrity) của `dds.fact_movie`
Kết quả chạy Mục 2 trong [`postgres/verify_dds_dw.sql`](postgres/verify_dds_dw.sql):

```text
 total_fact_rows | distinct_movie_sk | total_dim_movie_rows | orphan_movie_fk | orphan_date_fk | orphan_language_fk 
-----------------+-------------------+----------------------+-----------------+----------------+--------------------
            4803 |              4803 |                 4803 |               0 |              0 |                  0
```
* **Kết luận:** Không có bản ghi trùng lặp (`total_fact_rows = distinct_movie_sk = 4.803`), không có bất kỳ khóa ngoại mồ côi nào (`orphan_*_fk = 0`). Phim duy nhất thiếu `release_date` trong nguồn đã được gán đúng về `date_sk = -1`.

### 3.2. Kiểm tra 11 Khóa ngoại vật lý (Physical Foreign Keys) trên PostgreSQL
Kết quả kiểm tra `pg_constraint` (`contype = 'f'` trong schema `dds`):

| STT | Bảng con (`child_table`) | Cột FK | Bảng tham chiếu (`referenced_table`) | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| 1 | `dds.fact_movie` | `movie_sk` | `dds.dim_movie(movie_sk)` | ✅ Hợp lệ |
| 2 | `dds.fact_movie` | `date_sk` | `dds.dim_date(date_sk)` | ✅ Hợp lệ |
| 3 | `dds.fact_movie` | `language_sk` | `dds.dim_language(language_sk)` | ✅ Hợp lệ |
| 4 | `dds.bridge_movie_genre` | `movie_sk` | `dds.dim_movie(movie_sk)` | ✅ Hợp lệ |
| 5 | `dds.bridge_movie_genre` | `genre_sk` | `dds.dim_genre(genre_sk)` | ✅ Hợp lệ |
| 6 | `dds.bridge_movie_company` | `movie_sk` | `dds.dim_movie(movie_sk)` | ✅ Hợp lệ |
| 7 | `dds.bridge_movie_company` | `company_sk` | `dds.dim_company(company_sk)` | ✅ Hợp lệ |
| 8 | `dds.bridge_movie_country` | `movie_sk` | `dds.dim_movie(movie_sk)` | ✅ Hợp lệ |
| 9 | `dds.bridge_movie_country` | `country_sk` | `dds.dim_country(country_sk)` | ✅ Hợp lệ |
| 10 | `dds.bridge_movie_keyword` | `movie_sk` | `dds.dim_movie(movie_sk)` | ✅ Hợp lệ |
| 11 | `dds.bridge_movie_keyword` | `keyword_sk` | `dds.dim_keyword(keyword_sk)` | ✅ Hợp lệ |

* Ngoài 11 khóa ngoại vật lý, toàn bộ 12 bảng đều có `PRIMARY KEY`, các cột Natural Key (`movie_nk`, `language_nk`, `genre_nk`, `company_nk`, `country_code`, `keyword_nk`) đều có ràng buộc `UNIQUE NOT NULL`, và cột `dds.fact_movie.vote_count` có `is_nullable = NO`, `column_default = 0`.

---

## 4. KIỂM TRA BẢN GHI UNKNOWN (`SK = -1`) VÀ TRỌNG SỐ `weight_factor`

### 4.1. Kiểm tra dòng mặc định Unknown (`SK = -1`)
| Bảng Dimension | Khóa thay thế (`SK`) | Khóa tự nhiên (`NK`) | Giá trị hiển thị & Nhóm mặc định | Số dòng Unknown |
| :--- | :---: | :---: | :--- | :---: |
| `dds.dim_date` | `-1` | `NULL` | `month_name = 'Unknown'`, `decade = 'Unknown'` | `1` |
| `dds.dim_language` | `-1` | `'unk'` | `language_name = 'Unknown'`, `language_group = 'Non-English'` | `1` |
| `dds.dim_genre` | `-1` | `0` | `genre_name = 'Unknown'` | `1` |
| `dds.dim_company` | `-1` | `0` | `company_name = 'Unknown'` | `1` |
| `dds.dim_country` | `-1` | `'unk'` | `country_name = 'Unknown'`, `region = 'Unknown'` | `1` |
| `dds.dim_keyword` | `-1` | `0` | `keyword_name = 'Unknown'`, `theme_group = 'Other'` | `1` |
| `dds.dim_movie` | *(Không tạo)* | - | Không tạo phim giả `SK = -1` theo đúng thiết kế 1–1 với Fact. | `0` |

### 4.2. Kiểm tra tính toàn vẹn trọng số `weight_factor` trên các bảng Bridge
Kết quả chạy Mục 5 trong [`postgres/verify_dds_dw.sql`](postgres/verify_dds_dw.sql):

```text
    bridge_table      | distinct_movies_covered | unknown_fallback_links | invalid_weight_sum_movies 
----------------------+-------------------------+------------------------+---------------------------
 bridge_movie_genre   |                    4803 |                     28 |                         0
 bridge_movie_company |                    4803 |                    351 |                         0
 bridge_movie_country |                    4803 |                    174 |                         0
```
* **Kết luận:**
  * Cả 3 bảng Bridge có trọng số đều bao phủ đủ **4.803/4.803 bộ phim** (các phim có mảng JSON rỗng `[]` ở nguồn đã được sinh đúng 1 dòng fallback về `SK = -1` với `weight_factor = 1.0`).
  * Số bộ phim có tổng trọng số $\left|\sum \text{weight\_factor} - 1.0\right| > 10^{-7}$ bằng **`0`** trên cả 3 bảng Bridge.
  * Bảng `dds.bridge_movie_keyword` được xác nhận **không có cột `weight_factor`** (`0 rows` trong `information_schema.columns`).

---

## 5. KIỂM TRA CÁC CHỈ SỐ ĐỊNH LƯỢNG (MEASURES) TRONG `dds.fact_movie`

### 5.1. Kiểm tra quy tắc tính toán và xử lý giá trị `0` / `NULL`
Kết quả chạy Mục 6 trong [`postgres/verify_dds_dw.sql`](postgres/verify_dds_dw.sql):

| Chỉ tiêu kiểm tra quy tắc nghiệp vụ trên `dds.fact_movie` | Số dòng vi phạm | Đánh giá |
| :--- | :---: | :---: |
| Số dòng có `budget <= 0` (chưa chuyển sang `NULL`) | `0` | ✅ Đạt (`1.037` phim có `budget = 0` đã chuyển thành `NULL`) |
| Số dòng có `revenue <= 0` (chưa chuyển sang `NULL`) | `0` | ✅ Đạt (`1.427` phim có `revenue = 0` đã chuyển thành `NULL`) |
| Số dòng sai lệch cờ `is_finance_valid` so với trạng thái `NULL` của `budget`, `revenue`, `profit`, `roi` | `0` | ✅ Đạt (`3.229` phim hợp lệ có đủ 4 chỉ số; `1.574` phim thiếu có `profit` và `roi` là `NULL`) |
| Số dòng tính sai công thức `profit = revenue - budget` | `0` | ✅ Đạt |
| Số dòng tính sai công thức `roi = (revenue - budget) / budget` | `0` | ✅ Đạt |
| Số dòng gán sai cờ `is_revenue_over_budget` | `0` | ✅ Đạt |
| Số dòng có `vote_count = 0` nhưng `vote_average IS NOT NULL` | `0` | ✅ Đạt (`62` phim có `vote_count = 0` đều có `vote_average IS NULL`) |
| Số dòng có `movie_count <> 1` | `0` | ✅ Đạt |

### 5.2. Số liệu tổng hợp chuẩn (Baseline) bàn giao cho bộ phận Power BI (Vân – Phần 3.4)
Để bộ phận Power BI đối chiếu độ chính xác của các DAX Measures trên Dashboard 1 (Overview) và Dashboard 2 (Detailed), dưới đây là các con số chuẩn truy vấn trực tiếp từ `dds.fact_movie`:

* **Tổng số bộ phim (`SUM(movie_count)`):** `4.803` phim
* **Số bộ phim có dữ liệu tài chính hợp lệ (`SUM(is_finance_valid)`):** `3.229` phim (chiếm `67,23%`)
* **Số bộ phim có doanh thu vượt ngân sách (`SUM(is_revenue_over_budget)`):** `2.438` phim (chiếm **`75,50%`** trên tập 3.229 phim có tài chính hợp lệ)
* **Tổng ngân sách của 3.229 phim hợp lệ (`is_finance_valid = 1`):** `131.273.202.176 USD` (~`131,27 tỷ USD`) *(Lưu ý: Nếu cộng cả 537 phim có `budget > 0` nhưng `revenue IS NULL`, tổng cột `budget` là `139.515.792.884 USD` — khuyến nghị trên Power BI lọc `is_finance_valid = 1` khi phân tích tài chính để đồng nhất mẫu số)*.
* **Tổng doanh thu của 3.229 phim hợp lệ (`is_finance_valid = 1`):** `391.493.508.997 USD` (~`391,49 tỷ USD`)
* **Tổng lợi nhuận ước tính (`SUM(profit)`):** `260.220.306.821 USD` (~`260,22 tỷ USD`)
* **Tỷ suất hoàn vốn tổng hợp (`SUM(profit) / SUM(budget)` với `is_finance_valid = 1`):** `1,9823` (tương đương **`198,23%`**)

---

## 6. KẾT LUẬN NGHIỆM THU BÀN GIAO (PHẦN 3.3 – DATA WAREHOUSE)

1. Toàn bộ 12 bảng thuộc tầng `dds` (`1 Fact`, `7 Dimensions`, `4 Bridges`) cùng 11 khóa ngoại vật lý, khóa chính, ràng buộc `UNIQUE`/`NOT NULL` đã được khởi tạo đầy đủ, chính xác và kiểm chứng khả năng chạy lại trên PostgreSQL 17.
2. Toàn bộ sản phẩm bàn giao của Phần 3.3 (Data Warehouse) đã hoàn tất và sẵn sàng cho Phần 3.4 (Power BI Dashboard).

