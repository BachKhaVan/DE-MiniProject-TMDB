# Kiểm tra online (chỉ mã nguồn và PBIX, không kết nối máy người dùng)

Đây là lượt pytest chạy trên bản ZIP đã giải nén vào môi trường xử lý của ChatGPT. Không có ba CSV nguồn, PostgreSQL/Docker/Mage/dbt runtime hay Power BI Desktop. Những test phụ thuộc vào chúng phải là BLOCKED.

- Run ID: `20261115T144515Z_ac7308`
- **PASS 22, FAIL 4, BLOCKED 100, SKIPPED 13**

## Các FAIL đã thấy (phát hiện tĩnh, không phải chứng minh lỗi runtime)

- **MG18 (Kiểm tra độ bền):** Đã quan sát vi phạm; AssertionError: upstream hiện tại = ['get_watermark'], thiếu exporter
- **MG19 (Kiểm tra độ bền):** Đã quan sát vi phạm; AssertionError: Loader chỉ đọc nguyên batch CSV, không dùng LSET/CET
- **MG20 (Kiểm tra độ bền):** Đã quan sát vi phạm; AssertionError: Exporter append không thấy cơ chế chống trùng ở cấp exporter; cần thực nghiệm replay isolated
- **DB13 (Kiểm tra độ bền):** Đã quan sát vi phạm; AssertionError: Các model chưa được mô tả riêng: stg_movie_companies, stg_movie_countries, stg_movie_genres, stg_movie_keywords

Toàn bộ kết quả nằm trong `offline_audit/REPORT.md` và `offline_audit/result.json`. Sau khi ghép folder `test` vào project trên Windows, **chạy lại** để có evidence mới từ database và Power BI.
