# Ma trận kiểm thử theo đề và báo cáo

Nguồn: 2627.Yêu cầu_unlocked.pdf (3 trang); BaoCao_TongHop_TMDB_Nhom5.docx.pdf (88 trang).
Đây là danh mục coverage, không phải kết quả chạy. Xem hướng dẫn ../HUONG_DAN_CHAY_TEST.md.
AI chưa triển khai; UI/Refresh/DAX không được suy ra từ PBIX. Sản phẩm nộp/video cần rà thủ công theo mục 4 đề.

| ID | Mục đề | Loại | Kiểm tra | Bằng chứng | Khi thành công |
|---|---|---|---|---|---|
| AI01 | 3.5 | Yêu cầu bắt buộc | Tích hợp LLM hoặc dịch vụ Generative AI | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| AI02 | 3.5 | Yêu cầu bắt buộc | Tự động tạo summary từ KPI và ngữ cảnh lọc | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| AI03 | 3.5 | Yêu cầu bắt buộc | Giải thích xu hướng/biến động bằng số liệu | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| AI04 | 3.5 | Yêu cầu bắt buộc | Kiểm chứng số liệu và hạn chế suy diễn không có căn cứ | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| BI01 | 3.4 | Quy tắc project | KPI toàn danh mục, cùng tập phim finance-valid | Kết quả chạy mới | INFO |
| BI02 | 3.4 | Quy tắc project | Country USA + Year 2014 + Genre Action (không nhân đôi phim) | Kết quả chạy mới | INFO |
| BI03 | 3.4 | Quy tắc project | Weighted và Full: profit theo hãng, kiểm tra phân bổ | Kết quả chạy mới | INFO |
| BI04 | 3.4 | Quy tắc project | SQL kiểm tra phân nhóm ít hơn 5 valid movies | Kết quả chạy mới | INFO |
| BI05 | 3.4 | Quy tắc project | Một phim nhiều genre, minh họa 1/k từ dữ liệu thật | Kết quả chạy mới | INFO |
| BI06 | 3.4 | Quy tắc project | Phim có budget/revenue NULL, ví dụ dữ liệu thật | Kết quả chạy mới | INFO |
| BI07 | 3.4 | Quy tắc project | Q2 bổ sung: popularity/rating theo genre và language | Kết quả chạy mới | INFO |
| BI08 | 3.4 | Quy tắc project | Q4 bổ sung: budget-revenue từng phim hợp lệ để đối chiếu scatter | Kết quả chạy mới | INFO |
| BI09 | 3.4 | Quy tắc project | Q5 bổ sung: revenue/ROI của hãng Weighted và Full | Kết quả chạy mới | INFO |
| BI10 | 3.4 | Quy tắc project | Ngưỡng Min Votes 100 và 1000 theo LanguageGroup | Kết quả chạy mới | INFO |
| DB01 | 3.2 | Yêu cầu bắt buộc | Đúng 18 dbt models SQL (6 staging + 7 dim + 4 bridge + 1 fact) | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| DB02 | 3.2 | Yêu cầu bắt buộc | Đúng ba seed mappings được khai báo | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| DB03 | 3.2 | Yêu cầu bắt buộc | Có generic/singular data tests trong schema.yml | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| DB04 | 3.2 | Yêu cầu bắt buộc | Có 2 sources tmdb_stage trỏ tới stage | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| DB05 | 3.2 | Yêu cầu bắt buộc | dbt refs/sources hình thành DAG hợp lệ | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| DB06 | 3.2 | Yêu cầu bắt buộc | dbt docs có manifest/catalog/index.html | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| DB07 | 3.2 | Yêu cầu bắt buộc | dbt project có schema staging/dds và post-hook | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| DB08 | 3.2 | Yêu cầu bắt buộc | dbt executable có thể khởi tạo | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DB09 | 3.2 | Yêu cầu bắt buộc | dbt model test được chạy trên snapshot hiện tại | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DB10 | 3.2 | Yêu cầu bắt buộc | dbt docs được sinh từ model hiện tại | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DB11 | 3.2 | Kiểm tra độ bền | Thực thi dbt build/rebuild trong database cô lập | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DB12 | 3.2 | Kiểm tra độ bền | Surrogate key ổn định theo natural key sau rebuild | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DB13 | 3.2 | Kiểm tra độ bền | Mức độ bao phủ model trong schema.yml | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW01 | 3.3 | Yêu cầu bắt buộc | Có đúng 12 bảng fact/dim/bridge | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW02 | 3.3 | Yêu cầu bắt buộc | 12 bảng có khóa chính vật lý | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW03 | 3.3 | Yêu cầu bắt buộc | UNIQUE vật lý cho các natural key | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW04 | 3.3 | Yêu cầu bắt buộc | 11 FK vật lý trỏ đúng bảng cha (confrelid) | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW05 | 3.3 | Yêu cầu bắt buộc | Grain Fact = dim_movie = số movie_sk distinct | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW06 | 3.3 | Yêu cầu bắt buộc | fact_movie không có movie_sk trùng | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW07 | 3.3 | Yêu cầu bắt buộc | Fact SK và cờ không NULL | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW08 | 3.3 | Yêu cầu bắt buộc | Fact → dim_movie 1:1 logic | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW09 | 3.3 | Yêu cầu bắt buộc | Fact không có FK logic mồ côi | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW10 | 3.3 | Yêu cầu bắt buộc | Bridge genre không có orphan | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW11 | 3.3 | Yêu cầu bắt buộc | Bridge company không có orphan | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW12 | 3.3 | Yêu cầu bắt buộc | Bridge country không có orphan | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW13 | 3.3 | Yêu cầu bắt buộc | Bridge keyword không có orphan | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW14 | 3.3 | Yêu cầu bắt buộc | Bridge genre không trùng cặp khóa | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW15 | 3.3 | Yêu cầu bắt buộc | Bridge company không trùng cặp khóa | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW16 | 3.3 | Yêu cầu bắt buộc | Bridge country không trùng cặp khóa | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW17 | 3.3 | Yêu cầu bắt buộc | Bridge keyword không trùng cặp khóa | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW18 | 3.3 | Yêu cầu bắt buộc | Bridge genre weight_factor dương, sum=1 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW19 | 3.3 | Yêu cầu bắt buộc | Bridge company weight_factor dương, sum=1 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW20 | 3.3 | Yêu cầu bắt buộc | Bridge country weight_factor dương, sum=1 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW21 | 3.3 | Yêu cầu bắt buộc | Keyword bridge không có cột weight_factor | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW22 | 3.3 | Yêu cầu bắt buộc | 6 dimension (trừ dim_movie) có đúng 1 Unknown SK=-1 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW23 | 3.3 | Yêu cầu bắt buộc | Các bridge genre/company/country bao phủ mọi phim | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW24 | 3.3 | Yêu cầu bắt buộc | dim_date có đủ chuỗi ngày liên tục (trừ Unknown) | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW25 | 3.3 | Yêu cầu bắt buộc | dim_date month_name English, decade dạng 1980s | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW26 | 3.3 | Yêu cầu bắt buộc | Fact profit=revenue-budget; ROI thập phân | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW27 | 3.3 | Yêu cầu bắt buộc | Cờ is_finance_valid và is_revenue_over_budget đúng | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW28 | 3.3 | Yêu cầu bắt buộc | Fact vote_count mặc định 0 và NOT NULL | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW29 | 3.3 | Yêu cầu bắt buộc | Fact movie_count luôn bằng 1 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW30 | 3.3 | Yêu cầu bắt buộc | Votes không dương thì vote_average NULL | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW31 | 3.3 | Kiểm tra độ bền | Profit không âm/âm đều được, không loại phim không hợp lệ | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW32 | 3.2 | Yêu cầu bắt buộc | Staging chuẩn hóa budget/revenue 0 thành NULL | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW33 | 3.2 | Yêu cầu bắt buộc | Staging chuẩn hóa vote_average khi vote_count<=0 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW34 | 3.2 | Yêu cầu bắt buộc | Staging phim có natural key/title và không trùng phim | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW35 | 3.2 | Yêu cầu bắt buộc | Language fallback giữ mã và Unknown hợp lệ | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW36 | 3.2 | Yêu cầu bắt buộc | Country region không được NULL khi chưa map | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW37 | 3.2 | Yêu cầu bắt buộc | Keyword theme_group không được NULL | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW38 | 3.2 | Yêu cầu bắt buộc | Fact không có finance-valid khi budget/revenue NULL | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW39 | 3.3 | Yêu cầu bắt buộc | Weighted profit across each bridge = fact profit for covered movies | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW40 | 3.3 | Kiểm tra độ bền | Vote-count, ROI và finance được dùng nhất quán khi tổng hợp | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW41 | 3.2 | Yêu cầu bắt buộc | Country region chính xác theo seed, fallback Unknown | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW42 | 3.2 | Yêu cầu bắt buộc | Keyword theme chính xác theo seed, fallback Other | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW43 | 3.2 | Yêu cầu bắt buộc | Language label fallback giữ code khi không có tên | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW44 | 3.2 | Yêu cầu bắt buộc | RuntimeBand trong dim_movie đúng theo staging | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW45 | 3.2 | Yêu cầu bắt buộc | BudgetBand trong dim_movie đúng theo staging | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW46 | 3.2 | Yêu cầu bắt buộc | CountryType và country_count từ quan hệ stage | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW47 | 3.3 | Yêu cầu bắt buộc | Bridge genre phải có đúng weight_factor = 1/k mỗi link | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW48 | 3.3 | Yêu cầu bắt buộc | Bridge company phải có đúng weight_factor = 1/k mỗi link | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW49 | 3.3 | Yêu cầu bắt buộc | Bridge country phải có đúng weight_factor = 1/k mỗi link | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW50 | 3.3 | Yêu cầu bắt buộc | Stage, staging và Fact có dữ liệu để nghiệm thu | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW51 | 3.2 | Yêu cầu bắt buộc | Không mất hoặc thêm Movie NK giữa staging và DDS | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW52 | 3.2 | Yêu cầu bắt buộc | Measures của Fact khớp từng phim nguồn staging | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW53 | 3.2 | Yêu cầu bắt buộc | Fact liên kết đúng ngày và ngôn ngữ nguồn, kể cả Unknown | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW54 | 3.3 | Yêu cầu bắt buộc | Các thành phần hierarchy Date đúng ngày thực | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW55 | 3.2 | Yêu cầu bắt buộc | Bridge genre giữ đúng tập liên kết nguồn (hai chiều) | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW56 | 3.2 | Yêu cầu bắt buộc | Bridge company giữ đúng tập liên kết nguồn (hai chiều) | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW57 | 3.2 | Yêu cầu bắt buộc | Bridge country giữ đúng tập liên kết nguồn (hai chiều) | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW58 | 3.2 | Yêu cầu bắt buộc | Bridge keyword giữ đúng tập liên kết nguồn (hai chiều) | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| DW59 | 3.2 | Yêu cầu bắt buộc | dim_movie giữ đúng title/original_title/status nguồn | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MC01 | 3.1 | Yêu cầu bắt buộc | Movies bỏ dòng trùng toàn bộ | Unit test thực thi hàm transformer gốc; không thay thế Mage runtime | PASS (nếu đủ điều kiện và assertion đạt) |
| MC02 | 3.1 | Yêu cầu bắt buộc | Movies bỏ ID/title NULL | Unit test thực thi hàm transformer gốc; không thay thế Mage runtime | PASS (nếu đủ điều kiện và assertion đạt) |
| MC03 | 3.1 | Yêu cầu bắt buộc | Movies ép ngày sai thành NaT | Unit test thực thi hàm transformer gốc; không thay thế Mage runtime | PASS (nếu đủ điều kiện và assertion đạt) |
| MC04 | 3.1 | Yêu cầu bắt buộc | Credits bỏ dòng trùng và movie_id NULL | Unit test thực thi hàm transformer gốc; không thay thế Mage runtime | PASS (nếu đủ điều kiện và assertion đạt) |
| MC05 | 3.1 | Yêu cầu bắt buộc | Movies xử lý batch rỗng có schema | Unit test thực thi hàm transformer gốc; không thay thế Mage runtime | PASS (nếu đủ điều kiện và assertion đạt) |
| MC06 | 3.1 | Yêu cầu bắt buộc | Cleaner thiếu cột bắt buộc phát sinh lỗi rõ ràng | Unit test thực thi hàm transformer gốc; không thay thế Mage runtime | PASS (nếu đủ điều kiện và assertion đạt) |
| MG01 | 3.1 | Yêu cầu bắt buộc | CSV tmdb_5000_movies.csv tồn tại và có header | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MG02 | 3.1 | Yêu cầu bắt buộc | CSV tmdb_5000_credits.csv tồn tại và có header | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MG03 | 3.1 | Yêu cầu bắt buộc | CSV tmdb_new_batch.csv tồn tại và có header | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MG04 | 3.1 | Kiểm tra độ bền | Movies: khóa id không null hoặc trùng trong file nguồn | Kết quả chạy mới | INFO |
| MG05 | 3.1 | Kiểm tra độ bền | Credits: khóa movie_id không null hoặc trùng trong file nguồn | Kết quả chạy mới | INFO |
| MG06 | 3.1 | Kiểm tra độ bền | Movie release_date parse được hoặc được ghi nhận coerce | Kết quả chạy mới | INFO |
| MG07 | 3.1 | Kiểm tra độ bền | Các trường JSON phim đúng cú pháp hoặc ghi nhận bất thường | Kết quả chạy mới | INFO |
| MG08 | 3.1 | Kiểm tra độ bền | Quan hệ CSV movies và credits hai chiều | Kết quả chạy mới | INFO |
| MG09 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: clean_movies_data.py | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG10 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: clean_credits_data.py | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG11 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: export_movies_to_postgres.py | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG12 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: export_credits_to_postgres.py | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG13 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: export_incremental_stage.py | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG14 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: get_watermark.py | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG15 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: update_watermark.py | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG16 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: load_new_batch.py | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG17 | 3.1 | Yêu cầu bắt buộc | Graph Full Load Movies/Credits đúng chuỗi | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG18 | 3.1 | Kiểm tra độ bền | Watermark phụ thuộc vào thành công export incremental | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG19 | 3.1 | Kiểm tra độ bền | Loader incremental lọc batch qua LSET/CET | Phát hiện tĩnh trong code | INFO |
| MG20 | 3.1 | Kiểm tra độ bền | Exporter incremental xử lý ID trùng khi replay | Phát hiện tĩnh trong code | PASS (nếu đủ điều kiện và assertion đạt) |
| MG21 | 3.1 | Yêu cầu bắt buộc | Full load rowcount stage so với CSV sau làm sạch | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MG22 | 3.1 | Yêu cầu bắt buộc | Quan hệ hai bảng stage và khóa null/trùng | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MG23 | 3.1 | Yêu cầu bắt buộc | Bảng watermark tồn tại và có dòng incremental | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MG24 | 3.1 | Yêu cầu bắt buộc | Metadata Mage có log run thực và rowcount | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MI01 | 3.1 | Yêu cầu bắt buộc | Full Load chạy lại giữ nguyên dữ liệu | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MI02 | 3.1 | Yêu cầu bắt buộc | Incremental batch mới thêm phim không trùng | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MI03 | 3.1 | Yêu cầu bắt buộc | Incremental batch rỗng không thay đổi bảng | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MI04 | 3.1 | Kiểm tra độ bền | Incremental cùng batch replay không tạo trùng | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MI05 | 3.1 | Kiểm tra độ bền | Batch chứa ID đã có không tạo duplicate | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MI06 | 3.1 | Kiểm tra độ bền | Batch lỗi không làm bẩn stage | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MI07 | 3.1 | Kiểm tra độ bền | Export thất bại không cập nhật watermark | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| MI08 | 3.1 | Kiểm tra độ bền | Full Load lỗi một nhánh có snapshot mô tả | Kết quả chạy mới | INFO |
| NC01 | 3.3 | Kiểm tra độ bền | Bridge weight_factor phải bắt được sai lệch | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| NC02 | 3.3 | Kiểm tra độ bền | ROI/profit phải bắt được sai lệch | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| NC03 | 3.3 | Kiểm tra độ bền | FK logic phải bắt được orphan | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| NC04 | 3.3 | Kiểm tra độ bền | Grain phải bắt được fact duplicate | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| NC05 | 3.3 | Kiểm tra độ bền | Bridge không chấp nhận duplicate cặp | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| PB01 | 3.4 | Yêu cầu bắt buộc | PBIX là file có thể đọc được | Phát hiện tĩnh trong PBIX | PASS (nếu đủ điều kiện và assertion đạt) |
| PB02 | 3.4 | Yêu cầu bắt buộc | Có tối thiểu hai trang Dashboard | Phát hiện tĩnh trong PBIX | PASS (nếu đủ điều kiện và assertion đạt) |
| PB03 | 3.4 | Yêu cầu bắt buộc | Mỗi trang có ít nhất một biểu đồ | Phát hiện tĩnh trong PBIX | PASS (nếu đủ điều kiện và assertion đạt) |
| PB04 | 3.4 | Yêu cầu bắt buộc | Report có tham chiếu measure DAX | Phát hiện tĩnh trong PBIX | PASS (nếu đủ điều kiện và assertion đạt) |
| PB05 | 3.4 | Yêu cầu bắt buộc | Overview có các KPI chính | Phát hiện tĩnh trong PBIX | PASS (nếu đủ điều kiện và assertion đạt) |
| PB06 | 3.4 | Yêu cầu bắt buộc | Dashboard có khả năng đặt bộ lọc/slicer | Phát hiện tĩnh trong PBIX | PASS (nếu đủ điều kiện và assertion đạt) |
| PB07 | 3.4 | Yêu cầu bắt buộc | Drill-down thời gian hoạt động | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| PB08 | 3.4 | Yêu cầu bắt buộc | Relationships đúng cardinality và cross-filter | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| PB09 | 3.4 | Yêu cầu bắt buộc | DAX measures tính đúng với SQL | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| PB10 | 3.4 | Yêu cầu bắt buộc | Top N được sort theo measure hiển thị | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| PB11 | 3.4 | Yêu cầu bắt buộc | Ngưỡng Min Movies, Min Votes dùng đúng measure | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| PB12 | 3.4 | Yêu cầu bắt buộc | Refresh Import thành công và khớp DDS | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| PB13 | 3.4 | Quy tắc project | Allocation Weighted và Full đổi thứ hạng | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| PB14 | 3.4 | Quy tắc project | Country=USA, Year=2014, Genre=Action | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| Q1 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q1 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| Q1SQL | 3.4 | Quy tắc project | Q1 Rating theo runtime/genre, chỉ phim đủ votes | Kết quả chạy mới | INFO |
| Q2 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q2 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| Q2SQL | 3.4 | Quy tắc project | Q2 Rating & popularity theo ngôn ngữ gốc (Min Votes=100) | Kết quả chạy mới | INFO |
| Q3 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q3 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| Q3SQL | 3.4 | Quy tắc project | Q3 Weighted genre profit qua các thập niên | Kết quả chạy mới | INFO |
| Q4 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q4 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| Q4SQL | 3.4 | Quy tắc project | Q4 ROI/Pct over budget theo budget band | Kết quả chạy mới | INFO |
| Q5 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q5 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| Q5SQL | 3.4 | Quy tắc project | Q5 Hãng lợi nhuận Weighted vs Full (không nhân đôi hợp tác) | Kết quả chạy mới | INFO |
| Q6 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q6 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| Q6SQL | 3.4 | Quy tắc project | Q6 Profit/ROI theo tháng và thập niên | Kết quả chạy mới | INFO |
| Q7 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q7 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| Q7SQL | 3.4 | Quy tắc project | Q7 Quốc gia / single-multi / English-non-English | Kết quả chạy mới | INFO |
| Q8 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q8 | Kết quả chạy mới | PASS (nếu đủ điều kiện và assertion đạt) |
| Q8SQL | 3.4 | Quy tắc project | Q8 Theme sequel/adaptation/superhero, chống trùng một phim nhiều keyword | Kết quả chạy mới | INFO |
