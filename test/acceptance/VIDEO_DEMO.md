# Kịch bản quay video nghiệm thu — TMDB 3.1–3.4

Giữ video trung thực: chỉ nói “đã kiểm chứng” khi có runtime + đường dẫn report; với `FAIL` giải thích lỗi đã quan sát; với `BLOCKED` nêu rõ cần thao tác gì. Thời lượng tùy bài, không bịa kết quả. Chuẩn bị PowerShell tại gốc repository; không quay terminal khi nhập password hoặc file `.env`/`profiles.yml`/`io_config.yaml`.

**Link video chính thức:** [Thư mục video demo trên Google Drive](https://drive.google.com/drive/folders/1x6fNNB01GWwsOE6fa5XxfcngMb8h902G?usp=sharing). Chuẩn bị môi trường theo [hướng dẫn test, phần 10](../HUONG_DAN_CHAY_TEST.md); các cảnh dưới dùng DB test cô lập đã nạp/build thành công. Nếu quay PBIX kết nối DB chính, chạy SQL readonly với `.env` đúng nguồn theo phần 10.5, không so với DB test.

## Cảnh 1 — Giới thiệu kiến trúc (mục 3.1–3.4)

- **Màn hình:** cây thư mục `mage_pipeline/`, `dbt_transform/models/`, `postgres/`, `powerbi_dashboard/`, `test/acceptance/` (không mở file secret).
- **Nói:** “Nguồn CSV TMDB đi qua Mage vào `stage`; dbt tạo 6 staging views, Dimensions, Bridges và Fact dưới `dds`; Power BI phân tích qua mô hình semantic. Bộ test chia bốn nhóm và phân biệt tự động với thủ công.”
- **Expected:** thấy đúng source files và report; không nhầm source code với dữ liệu đã nạp.

## Cảnh 2 — Kiểm tra môi trường

```powershell
$py = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $py --version
& $py -m pytest --version
docker compose version
& $py .\test\acceptance\isolation.py ps
& $py .\test\acceptance\run.py --mode integration --section all --approved
```

- **Màn hình:** Python, Docker (nếu có), status Compose test, output test và đường dẫn `REPORT.md`.
- **Nói:** “Nếu máy chưa kết nối PostgreSQL hoặc chưa có CSV, test báo BLOCKED, không được hiểu là dữ liệu đã sai. Run ID và kết quả được lưu mới mỗi lần.”

## Cảnh 3 — Mage 3.1

1. **Màn hình:** Mage TEST ở `http://127.0.0.1:16789`, pipeline `tmdb_ingestion`, loader/transformer/exporter logs và run ID.
2. **Lệnh:** `& $py .\test\acceptance\run.py --mode integration --section 31 --approved` **sau khi có stack isolated và run thật**. Nếu chưa sẵn, dừng để chuẩn bị môi trường; không dùng kết quả từ DB khác thay cho run test.
3. **Chỉ rõ:** Full Load dùng `replace`; Incremental thêm bước tạo PK và dùng `append` kèm upsert theo `id`. Graph hiện nối get_watermark → load_new_batch → exporter → update_watermark; loader vẫn đọc batch tĩnh. Với `MI01`, mở before/after hash; với `MI04`, nhìn duplicate count khi replay batch; với `MI07`, chụp block FAIL và watermark LSET.
4. **Nói:** “Một test robust có thể FAIL dù project vẫn hỗ trợ mô phỏng incremental; tôi sẽ phân biệt yêu cầu đề và khả năng chống trùng bổ sung.”

## Cảnh 4 — dbt 3.2

- **Màn hình:** cây `dbt_transform/models/`, `schema.yml`, sources & seeds; DAG trong dbt docs nếu có.
- **Lệnh safe:**

```powershell
& $py .\test\acceptance\run.py --mode integration --section 32 --approved
# Chỉ trên isolated, khi đã chạy Mage Full Load test:
& $py .\test\acceptance\isolation.py dbt-build
& $py .\test\acceptance\run.py --mode integration --section 32 --approved
```

- **Expected:** `DB01–DB07` cho thấy cấu trúc; DB09–DB11 chỉ chứng minh run nếu `.runtime/dbt_build_run_results.json` sinh mới từ isolated build. `dbt docs generate` sinh riêng trong `.runtime/dbt_target/`.
- **Nói:** “dbt dùng `ref/source`, quality tests và docs. Các file `target/` cũ trong ZIP không được xem là kết quả từ lần kiểm thử hôm nay.”

## Cảnh 5 — Data Warehouse 3.3 (ưu tiên bằng chứng định lượng)

```powershell
& $py .\test\acceptance\run.py --mode integration --section 33 --approved
```

- **Màn hình:** `REPORT.md` và `result.json` các test DW được chọn trong section 33 (đối chiếu MATRIX hiện tại); nếu đủ isolated, chạy `NC01–NC05` để chứng minh các assertion bắt lỗi.
- **Trước các ví dụ BI:** chạy `& $py .\test\acceptance\run.py --mode integration --section 34 --approved` để sinh SQL tham chiếu trên DB test. Section 33 không sinh các kết quả BI này.
- **Ví dụ thật:** đọc `BI05` lấy **`movie_nk`/`title` thực tế** của phim có nhiều Genre, chỉ rõ `weight_factor = 1/k`, tổng ≈1 và test DW18. Đọc `BI06` lấy phim có `budget/revenue IS NULL` và `is_finance_valid=0`; nói vì sao ROI/profit không được tính từ dữ liệu thiếu.
- **Ví dụ KPI:** `BI01` tính total phim, valid phim, revenue, profit, ROI Overall, ROI Median bằng SQL độc lập; không đánh đồng ROI trung bình/trung vị.
- **Nói:** “Các SQL assertions tìm dòng vi phạm, không chỉ chạy SELECT thành công. Negative control trên database isolated cố ý tạo dữ liệu sai rồi rollback, xác minh test có thực sự bắt được lỗi.”

## Cảnh 6 — Power BI 3.4 + Q1–Q8

1. Mở PBIX thật, xác nhận 4 trang hiển thị `Overview`, `Financial drivers`, `Companies & Countries`, `Audience & Ratings`.
2. Overview: chụp 6 KPIs và filter **All**. Đối chiếu với BI01 từ SQL. Đặt Country = `United States of America`, Year = `2014`, Genre = `Action`; đối chiếu kết quả BI02. Chỉ dùng baseline 47 phim/41 phim hợp lệ nếu DB vẫn đúng snapshot.
3. Trên chart thời gian, click drill-down Decade → Year → Quarter → MonthName. Chụp màn hình trước/sau.
4. Trang Companies & Countries: chuyển Weighted → Full, ghi thứ hạng công ty thay đổi ra sao và so `BI03`/`Q5SQL` trên cùng snapshot.
5. Audience & Ratings: đổi `Min votes per movie` từ 100 → 1.000, kiểm ảnh hưởng đến nhóm Language. Nếu chỉ còn English, kiểm bằng SQL trước khi suy luận “không có dữ liệu”.
6. Chạy Refresh thật; chụp thông báo hoàn tất và số liệu sau Refresh. Không coi báo cáo Import đang hiện ra là Refresh đã thành công.
7. Mở `CHECKLIST_POWERBI.md`, lần lượt báo cáo Q1–Q8; với câu chưa có DAX/chưa chứng thực visual, nói `BLOCKED` và nêu cách làm tiếp.

**Nói:** “Mô hình BI được kiểm tra hai lớp: số liệu chuẩn tính độc lập từ DDS và kết quả thực trên semantic model. SQL chạy được không đồng nghĩa đã kiểm xong công thức DAX.”

## Cảnh 7 — Kết luận và xuất bằng chứng

```powershell
& $py .\test\acceptance\run.py --mode integration --section all --approved
# Mở file mới nhất trong test/results/acceptance_<run id>/REPORT.md
```

- **Màn hình:** PASS/FAIL/BLOCKED/SKIPPED/INFO; ma trận requirement→test→bằng chứng; phần 14 trường của FAIL/BLOCKED; `result.json` và `junit.xml`.
- **Nói:** “Tôi đánh giá 3.1–3.4 theo yêu cầu bắt buộc riêng, 8 câu hỏi nghiệp vụ riêng, các kiểm tra độ bền riêng. Phần nào chưa chạy vì thiếu môi trường thì giữ BLOCKED, không suy luận từ log cũ.”
- **Trước khi nộp video:** kiểm lại thông tin nhạy cảm trong ảnh/video (password, server address cá nhân, email, token). Không commit thư mục `.runtime/` vì có mật khẩu test; chỉ dùng báo cáo đã che secrets.
