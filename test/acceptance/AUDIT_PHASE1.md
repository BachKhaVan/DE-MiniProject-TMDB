# Pha 1 — Khảo sát từ ZIP, ma trận và ranh giới an toàn

**Nguồn:** `DE-MiniProject-TMDB.zip` được người dùng cung cấp tại phiên chat ngày 15/11/2026. Không phải kết quả kết nối tới máy Windows hoặc PostgreSQL thực của người dùng.

## A. Repository và công cụ

- Trong ZIP `.git/HEAD` trỏ `refs/heads/main`, ref main là `d081ce2aa9b1e06fb95107c8795f415e35e39c40`. Đây là thông tin **Git lưu trong ZIP**, không xác nhận working tree máy người dùng. `git status` live: **không xác định**. Không có `AGENTS.md` trong danh sách source.
- `compose.yaml` gốc: PostgreSQL 17, user mặc định `labuser`, database mặc định `warehouse`, host port `5432`, volume `pg_data`; Mage port `6789`, mount cả repo vào `/home/src`. Có `container_name` tĩnh `postgres` và `mage`, không phù hợp chạy thêm stack bằng cách dùng nguyên compose gốc.
- Mage: hai pipelines `tmdb_ingestion` và `tmdb_incremental`; Full Load exporters `if_exists='replace'`, Incremental exporter `append`; watermark đọc trong `control.etl_watermark`, nhánh update không downstream của export.
- dbt: 18 SQL models = 6 staging + 7 dims + 4 bridges + 1 fact, 3 mapping seeds, 2 sources; `schema.yml` có 14 model entries. Manifest kèm ZIP chứa 18 model nodes, 3 seed nodes, 87 test nodes. **Không** được xem những artifact này là lần chạy mới.
- SQL `postgres/init/01_init.sql` tạo các schema `stage`, `staging`, `dds`, `control` và bảng watermark trên database mới. `02_dds_schema.sql` là tài liệu DDL, không được dùng thay luồng dbt build chuẩn.
- Power BI: `TMDB_Movie_Dashboard.pbix` chứa định nghĩa báo cáo PBIR JSON, có thể đọc thông tin page/visual/measure references. `DataModel` bên trong là dữ liệu nén, chưa giải được DAX expression hoặc kiểm chứng Refresh trong môi trường này. Phải mở Power BI Desktop ở máy user.
- CSV `data/raw/tmdb_5000_movies.csv`, `tmdb_5000_credits.csv`, `tmdb_new_batch.csv` **không có trong ZIP**. Không có `mage_pipeline/io_config.yaml` trong ZIP. File cấu hình dbt mặc định có trong ZIP nhưng không được in nội dung có thể chứa credentials.
- Có `test/validate_tmdb.py`, `test/README_test.md`, `postgres/verify_dds_dw.sql`; đã giữ nguyên và kết nối thêm các bài kiểm thử để tránh dùng code pipeline giả.
- Môi trường ChatGPT hiện tại: Python 3.13, `pytest` có, `pandas` có, `PyYAML` có, `psycopg` không có, Docker CLI/dbt CLI/Mage CLI không có. **Môi trường máy người dùng: chưa xác định.** PostgreSQL hiện tại, containers, Power BI Desktop, Tabular Editor, DAX Studio, pbi-tools: **chưa xác định** (không có quyền truy cập máy Windows).

## B. Phương án cô lập

- Compose name `tmdb_test_acceptance`, image PostgreSQL 17, volume `tmdb_test_acceptance_pg_data`, database `tmdb_test_warehouse`, host port `127.0.0.1:55432`, Mage UI `127.0.0.1:16789`.
- Không dùng compose gốc để khởi động stack test. `compose.isolated.yaml` hoàn toàn độc lập, không dùng `container_name` của ứng dụng chính. `01_init.sql` được mount chỉ đọc để tạo schema/watermark khi volume isolated mới được init.
- Mage các block/pipeline metadata được copy **nguyên source** sang `test/acceptance/.runtime/workspace`, riêng `io_config.yaml` **mới** chỉ được tạo trong workspace, trỏ host `postgres` thuộc Compose isolated. Không sửa code nguồn hoặc file cấu hình gốc.
- dbt dùng `--profiles-dir` riêng ở `test/acceptance/.runtime/dbt_profiles`, profile tên `tmdb_transform`, target `isolated`, port 55432. `seed/build/docs` dùng artifact/log riêng `.runtime/`, không đụng `dbt_transform/target/` gốc.
- Ghi DB chỉ sau khi người dùng chủ động chạy `isolation.py` và cung cấp `--approved` hoặc `-IsolatedConfirmed` trong chế độ integration. Bộ test từ chat **không** tự khởi động Docker hay thay đổi database. `down --volumes` chỉ trong compose test.
- Rủi ro: Mage CLI/API và runtime do image `mageai/mageai:latest` có thể thay đổi; test ưu tiên gọi **pipeline thật qua Mage UI isolated** thay vì tự giả lập block. Nếu Mage UI không khởi chạy được, các MI test ghi BLOCKED. Việc cô lập phụ thuộc mount workspace mới và `io_config.yaml` được Mage nhận diện khi chạy thật.

## C. Ma trận, giả thuyết và quyết định

- Ma trận theo từng ID trong `MATRIX.md`. Bốn nhóm `3.1–3.4` được gắn markers `m31`, `m32`, `m33`, `m34` và `readonly`/`integration`.
- Incremental dedup: kiểm tra tĩnh `MG20`, replay thật `MI04`; chỉ kết luận lỗi runtime khi quan sát duplicate phát sinh từ snapshot thật.
- Watermark: graph tĩnh `MG18`, failure-injection trigger isolated + Mage run ID + trước/sau `MI07`.
- Full Load replace: `MG11–MG12`, hai lần chạy lại `MI01`, nhánh thất bại `MI08` (chỉ mô tả hành vi, không yêu cầu atomicity giả).
- DBT: staging de-dup/NULL/JSON/fallback `DW32–DW38`, key/grain/weight `DW05–DW40`, mapping seeds `DB02`; `DB11` chỉ có run_results mới sau isolated build.
- Surrogate key: `DB12` cần hai snapshot before/after và so natural keys, không FAIL chỉ vì `movie_sk` đổi sau full rebuild khi quan hệ còn đúng.
- BI: `PB01–PB06` quan sát từ PBIX; DAX, relationships, refresh, visual ranking, Q1–Q8 vẫn đòi desktop evidence theo `CHECKLIST_POWERBI.md`.

**Cần người dùng cung cấp/quyết định:** có đúng CSV gốc chưa; Docker Desktop và dbt có chạy trên Windows chưa; đồng ý bắt đầu stack isolated hay chưa; có cho quay/chụp màn hình Mage/Power BI không; sẽ dùng đúng snapshot nào làm chuẩn. Khi thiếu điều kiện, BLOCKED với đường tái hiện.

**Lưu ý thủ tục:** Yêu cầu ban đầu mô tả hai pha với phê duyệt sau Pha 1. Để đáp ứng yêu cầu mới là *bàn giao thư mục test trên chat online*, mã và hướng dẫn đã được soạn trước, nhưng **không chạy thao tác ghi DB/Docker**. Việc thực thi integration vẫn cần thao tác và phê duyệt trực tiếp trên máy người dùng.
