# Hướng dẫn đọc tài liệu và xem sản phẩm — Nhóm 5

**Đề tài:** Xây dựng hệ thống Business Intelligence trên dữ liệu TMDB 5000 — Phân tích hiệu quả tài chính điện ảnh.

Tài liệu này giúp giảng viên xác định thứ tự xem sản phẩm, vị trí báo cáo và vai trò của từng thư mục trong bộ mã nguồn.

## 1. Thứ tự đọc và xem đề xuất

| Thứ tự | Tài liệu / sản phẩm | Nội dung cần xem |
|---|---|---|
| **1** | [Báo cáo tổng hợp](docs/reports/BaoCao_TongHop_TMDB_Nhom5.pdf) | Dataset, bài toán, kiến trúc, mô hình dữ liệu, triển khai, kết quả và phạm vi hoàn thành |
| **2** | [Thư mục video demo](https://drive.google.com/drive/folders/1x6fNNB01GWwsOE6fa5XxfcngMb8h902G?usp=sharing) | Minh họa vận hành pipeline, chuyển đổi dữ liệu, kiểm thử và thao tác Power BI |
| **3** | [Dashboard PDF](docs/diagrams/TMDB_Movie_Dashboard.pdf) | Xem nhanh các trang báo cáo mà không cần mở Power BI Desktop |
| **4** | [Dashboard Power BI (.pbix)](powerbi_dashboard/TMDB_Movie_Dashboard.pbix) | Mở mô hình và dashboard tương tác, xem các bộ lọc và measures |
| **5** | [Phụ lục C — 60 công thức DAX](docs/reports/Phu_luc_C_60_DAX.pdf) và [Phụ lục D — Kiểm chứng KPI](docs/reports/Phu_luc_D_Kiem_chung_PostgreSQL_PowerBI.pdf) | Tra công thức và bằng chứng đối chiếu PostgreSQL–Power BI |
| **6** | Mã nguồn và tài liệu kỹ thuật ở mục 2–3 bên dưới | Đối chiếu chi tiết triển khai hoặc chạy lại hệ thống |

Để đọc báo cáo, xem các PDF và video, không cần khởi động Docker hay cơ sở dữ liệu. Hai phụ lục C và D là các PDF riêng được nộp kèm báo cáo tổng hợp.

## 2. Vai trò từng thư mục

| Thư mục | Nội dung | Cách tra cứu |
|---|---|---|
| **`docs/`** | Tài liệu bàn giao | Xem [danh mục tài liệu](docs/README.md) |
| `docs/reports/` | Báo cáo tổng hợp và hai phụ lục C–D | Đây là nơi đọc nội dung báo cáo chính và các minh chứng bổ sung |
| `docs/diagrams/` | PDF dashboard | Xem bản tĩnh của dashboard; file hiện có không thay cho PBIX tương tác |
| **`mage_pipeline/`** | Mã nguồn thu thập và nạp dữ liệu bằng Mage.ai | Đọc [README Ingestion](mage_pipeline/README_Ingestion.md); xem `pipelines/`, `data_loaders/`, `transformers/`, `data_exporters/` |
| **`dbt_transform/`** | Mã nguồn chuyển đổi dữ liệu, mô hình kho, seeds và kiểm thử dbt | Đọc [README dbt](dbt_transform/README.md); xem `models/`, `seeds/`, `macros/`, `tests/` |
| **`postgres/`** | SQL khởi tạo và kiểm chứng kho dữ liệu | `init/01_init.sql` khởi tạo schema/watermark; `init/02_dds_schema.sql` là DDL tham chiếu; `verify_dds_dw.sql` kiểm chứng DDS |
| **`powerbi_dashboard/`** | File PBIX và hướng dẫn sử dụng | Đọc [README Power BI](powerbi_dashboard/README.md), sau đó mở `TMDB_Movie_Dashboard.pbix` |
| **`test/`** | Bộ kiểm thử và hướng dẫn chạy | Bắt đầu từ [HUONG_DAN_CHAY_TEST.md](test/HUONG_DAN_CHAY_TEST.md) |
| `test/acceptance/` | Kiểm thử theo các yêu cầu 3.1–3.5, ma trận và checklist | [MATRIX.md](test/acceptance/MATRIX.md) mô tả phạm vi; [CHECKLIST_POWERBI.md](test/acceptance/CHECKLIST_POWERBI.md) hướng dẫn kiểm chứng thủ công |
| `test/manual test/` | SQL và DAX đối chiếu nhiều tổ hợp lọc | Tra các truy vấn dùng để kiểm tra KPI giữa PostgreSQL và Power BI |
| `test/unit/` | Kiểm thử hồi quy của bộ kiểm thử | Kiểm tra logic của công cụ test; không thay kiểm thử toàn hệ thống |
| `test/results/` | Kết quả sinh ra sau mỗi lượt chạy test, nếu được lưu kèm | Đọc `REPORT.md` và `result.json` của đúng lượt; thư mục có thể trống trước khi chạy |
| **`data/raw/`** | CSV nguồn đặt cục bộ | Dữ liệu thô không được commit; tải dataset theo báo cáo/README và đặt đúng tên file khi tái chạy |
| `mage_data/` | Trạng thái chạy cục bộ của Mage | Được tạo khi vận hành; không phải tài liệu chính để chấm và không cần đóng gói vào source |

## 3. Các file quan trọng ở thư mục gốc

| File | Vai trò |
|---|---|
| [README.md](README.md) | Tổng quan project, sản phẩm bàn giao, cài đặt và trạng thái triển khai |
| [Schema_Report.md](Schema_Report.md) | Data Contract: grain, Dimension/Fact/Bridge, khóa, Unknown và quy tắc tính toán |
| [DW_Verification_Report.md](DW_Verification_Report.md) | Kết quả kiểm chứng kho dữ liệu và số liệu tham chiếu của phiên được ghi nhận |
| [compose.yaml](compose.yaml) | Cấu hình khởi động Mage và PostgreSQL bằng Docker Compose |
| [.env.example](.env.example) | Mẫu biến môi trường; cần cấu hình mật khẩu riêng trước khi chạy |

Luồng xử lý của hệ thống: **CSV → Mage → PostgreSQL `stage` → dbt `staging`/`dds` → Power BI**. Mô hình DDS gồm **7 Dimension, 4 Bridge và 1 Fact**, với một dòng Fact tương ứng một phim.

## 4. Đối chiếu theo yêu cầu của đề

Số mục dưới đây là số mục trong đề bài, không phải số chương tương ứng của báo cáo tổng hợp.

| Yêu cầu | Nơi xem triển khai và minh chứng |
|---|---|
| **3.1 — Data Ingestion** | `mage_pipeline/`; báo cáo mục 2.2; video chạy Full Load/Incremental và kiểm tra stage |
| **3.2 — Data Transformation** | `dbt_transform/`; báo cáo mục 2.3; log build/rebuild, dbt tests và lineage |
| **3.3 — Data Warehouse** | `Schema_Report.md`, `postgres/`, `DW_Verification_Report.md`; báo cáo mục 2.1, 2.4 và 3.2 |
| **3.4 — Power BI** | `powerbi_dashboard/`; báo cáo mục 2.5, 3.3–3.6; phụ lục C–D và video tương tác |
| **3.5 — Generative AI** | Báo cáo mục 2.6 và phần kết luận: **chưa triển khai**, được ghi rõ trong phạm vi hoàn thành |

Incremental hiện mô phỏng batch CSV, có bước tạo khóa chính, cấu hình upsert theo ID và dependency cập nhật watermark sau exporter. Loader chưa lọc dữ liệu theo LSET/CET. Phạm vi kiểm chứng replay/phục hồi được xác định theo bằng chứng từng kịch bản.

## 5. Xem Power BI và đọc kết quả test

**Power BI:** có bốn trang Overview, Financial Drivers, Companies & Countries, Audience & Ratings. PBIX có thể hiển thị snapshot Import đã lưu; muốn Refresh cần PostgreSQL/DDS và thông tin kết nối đúng. Không cần chạy lại pipeline chỉ để xem PDF dashboard.

**Kiểm thử:** đọc cả trạng thái và nguyên nhân của từng case. PASS là kiểm tra đạt; FAIL là assertion chưa đạt; BLOCKED là thiếu điều kiện hoặc bằng chứng tự động; SKIPPED là không thực hiện trong chế độ được chọn; INFO là số liệu tham chiếu. Kết quả SQL tham chiếu không tự chứng minh DAX hoặc tương tác Power BI đã đúng. Phần thao tác thủ công được đối chiếu qua video và minh chứng trong báo cáo/phụ lục.

Khi tái chạy, sử dụng [hướng dẫn test](test/HUONG_DAN_CHAY_TEST.md). Môi trường chính dùng PostgreSQL 5432/Mage 6789; môi trường test riêng dùng PostgreSQL 55432/Mage 16789. Khi so KPI, Power BI và SQL phải cùng nguồn dữ liệu, snapshot và bộ lọc.
