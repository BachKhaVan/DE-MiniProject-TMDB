# Ma trận yêu cầu → test → bằng chứng → kết luận

**Sinh từ catalog mã test**, cập nhật theo bản bàn giao. Kết luận ở `test/results/acceptance_<run_id>/result.json`.

| Test ID | Mục | Loại | Tiêu chí kiểm | Chế độ | Loại evidence | Kết luận |
|---|---|---|---|---|---|---|
| BI01 | 3.4 | Quy tắc project | KPI toàn danh mục, cùng tập phim finance-valid | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| BI02 | 3.4 | Quy tắc project | Country USA + Year 2014 + Genre Action (không nhân đôi phim) | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| BI03 | 3.4 | Quy tắc project | Weighted và Full: profit theo hãng, kiểm tra phân bổ | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| BI04 | 3.4 | Quy tắc project | SQL kiểm tra phân nhóm ít hơn 5 valid movies | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| BI05 | 3.4 | Quy tắc project | Một phim nhiều genre, minh họa 1/k từ dữ liệu thật | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| BI06 | 3.4 | Quy tắc project | Phim có budget/revenue NULL, ví dụ dữ liệu thật | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| BI07 | 3.4 | Quy tắc project | Q2 bổ sung: popularity/rating theo genre và language | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| BI08 | 3.4 | Quy tắc project | Q4 bổ sung: budget-revenue từng phim hợp lệ để đối chiếu scatter | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| BI09 | 3.4 | Quy tắc project | Q5 bổ sung: revenue/ROI của hãng Weighted và Full | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| BI10 | 3.4 | Quy tắc project | Ngưỡng Min Votes 100 và 1000 theo LanguageGroup | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DB01 | 3.2 | Yêu cầu bắt buộc | Đúng 18 dbt models SQL (6 staging + 7 dim + 4 bridge + 1 fact) | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| DB02 | 3.2 | Yêu cầu bắt buộc | Đúng ba seed mappings được khai báo | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| DB03 | 3.2 | Yêu cầu bắt buộc | Có generic/singular data tests trong schema.yml | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| DB04 | 3.2 | Yêu cầu bắt buộc | Có 2 sources tmdb_stage trỏ tới stage | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| DB05 | 3.2 | Yêu cầu bắt buộc | dbt refs/sources hình thành DAG hợp lệ | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| DB06 | 3.2 | Yêu cầu bắt buộc | dbt docs có manifest/catalog/index.html | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| DB07 | 3.2 | Yêu cầu bắt buộc | dbt project có schema staging/dds và post-hook | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| DB08 | 3.2 | Yêu cầu bắt buộc | dbt executable có thể khởi tạo | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DB09 | 3.2 | Yêu cầu bắt buộc | dbt model test được chạy trên snapshot hiện tại | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DB10 | 3.2 | Yêu cầu bắt buộc | dbt docs được sinh từ model hiện tại | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DB11 | 3.2 | Kiểm tra độ bền | Thực thi dbt build/rebuild trong database cô lập | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DB12 | 3.2 | Kiểm tra độ bền | Surrogate key ổn định theo natural key sau rebuild | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DB13 | 3.2 | Kiểm tra độ bền | Mức độ bao phủ model trong schema.yml | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW01 | 3.3 | Yêu cầu bắt buộc | Có đúng 12 bảng fact/dim/bridge | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW02 | 3.3 | Yêu cầu bắt buộc | 12 bảng có khóa chính vật lý | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW03 | 3.3 | Yêu cầu bắt buộc | UNIQUE vật lý cho các natural key | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW04 | 3.3 | Yêu cầu bắt buộc | 11 FK vật lý trỏ đúng bảng cha (confrelid) | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW05 | 3.3 | Yêu cầu bắt buộc | Grain Fact = dim_movie = số movie_sk distinct | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW06 | 3.3 | Yêu cầu bắt buộc | fact_movie không có movie_sk trùng | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW07 | 3.3 | Yêu cầu bắt buộc | Fact SK và cờ không NULL | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW08 | 3.3 | Yêu cầu bắt buộc | Fact → dim_movie 1:1 logic | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW09 | 3.3 | Yêu cầu bắt buộc | Fact không có FK logic mồ côi | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW10 | 3.3 | Yêu cầu bắt buộc | Bridge genre không có orphan | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW11 | 3.3 | Yêu cầu bắt buộc | Bridge company không có orphan | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW12 | 3.3 | Yêu cầu bắt buộc | Bridge country không có orphan | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW13 | 3.3 | Yêu cầu bắt buộc | Bridge keyword không có orphan | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW14 | 3.3 | Yêu cầu bắt buộc | Bridge genre không trùng cặp khóa | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW15 | 3.3 | Yêu cầu bắt buộc | Bridge company không trùng cặp khóa | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW16 | 3.3 | Yêu cầu bắt buộc | Bridge country không trùng cặp khóa | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW17 | 3.3 | Yêu cầu bắt buộc | Bridge keyword không trùng cặp khóa | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW18 | 3.3 | Yêu cầu bắt buộc | Bridge genre weight_factor dương, sum=1 | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW19 | 3.3 | Yêu cầu bắt buộc | Bridge company weight_factor dương, sum=1 | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW20 | 3.3 | Yêu cầu bắt buộc | Bridge country weight_factor dương, sum=1 | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW21 | 3.3 | Yêu cầu bắt buộc | Keyword bridge không có cột weight_factor | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW22 | 3.3 | Yêu cầu bắt buộc | 6 dimension (trừ dim_movie) có đúng 1 Unknown SK=-1 | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW23 | 3.3 | Yêu cầu bắt buộc | Các bridge genre/company/country bao phủ mọi phim | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW24 | 3.3 | Yêu cầu bắt buộc | dim_date có đủ chuỗi ngày liên tục (trừ Unknown) | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW25 | 3.3 | Yêu cầu bắt buộc | dim_date month_name English, decade dạng 1980s | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW26 | 3.3 | Yêu cầu bắt buộc | Fact profit=revenue-budget; ROI thập phân | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW27 | 3.3 | Yêu cầu bắt buộc | Cờ is_finance_valid và is_revenue_over_budget đúng | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW28 | 3.3 | Yêu cầu bắt buộc | Fact vote_count mặc định 0 và NOT NULL | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW29 | 3.3 | Yêu cầu bắt buộc | Fact movie_count luôn bằng 1 | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW30 | 3.3 | Yêu cầu bắt buộc | Votes không dương thì vote_average NULL | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW31 | 3.3 | Kiểm tra độ bền | Profit không âm/âm đều được, không loại phim không hợp lệ | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW32 | 3.2 | Yêu cầu bắt buộc | Staging chuẩn hóa budget/revenue 0 thành NULL | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW33 | 3.2 | Yêu cầu bắt buộc | Staging chuẩn hóa vote_average khi vote_count<=0 | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW34 | 3.2 | Yêu cầu bắt buộc | Staging phim có natural key/title và không trùng phim | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW35 | 3.2 | Yêu cầu bắt buộc | Language fallback giữ mã và Unknown hợp lệ | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW36 | 3.2 | Yêu cầu bắt buộc | Country region không được NULL khi chưa map | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW37 | 3.2 | Yêu cầu bắt buộc | Keyword theme_group không được NULL | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW38 | 3.2 | Yêu cầu bắt buộc | Fact không có finance-valid khi budget/revenue NULL | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW39 | 3.3 | Yêu cầu bắt buộc | Weighted profit across each bridge = fact profit for covered movies | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW40 | 3.3 | Kiểm tra độ bền | Vote-count, ROI và finance được dùng nhất quán khi tổng hợp | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW41 | 3.2 | Yêu cầu bắt buộc | Country region chính xác theo seed, fallback Unknown | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW42 | 3.2 | Yêu cầu bắt buộc | Keyword theme chính xác theo seed, fallback Other | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW43 | 3.2 | Yêu cầu bắt buộc | Language label fallback giữ code khi không có tên | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW44 | 3.2 | Yêu cầu bắt buộc | RuntimeBand trong dim_movie đúng theo staging | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW45 | 3.2 | Yêu cầu bắt buộc | BudgetBand trong dim_movie đúng theo staging | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW46 | 3.2 | Yêu cầu bắt buộc | CountryType và country_count từ quan hệ stage | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW47 | 3.3 | Yêu cầu bắt buộc | Bridge genre phải có đúng weight_factor = 1/k mỗi link | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW48 | 3.3 | Yêu cầu bắt buộc | Bridge company phải có đúng weight_factor = 1/k mỗi link | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| DW49 | 3.3 | Yêu cầu bắt buộc | Bridge country phải có đúng weight_factor = 1/k mỗi link | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG01 | 3.1 | Yêu cầu bắt buộc | CSV tmdb_5000_movies.csv tồn tại và có header | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG02 | 3.1 | Yêu cầu bắt buộc | CSV tmdb_5000_credits.csv tồn tại và có header | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG03 | 3.1 | Yêu cầu bắt buộc | CSV tmdb_new_batch.csv tồn tại và có header | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG04 | 3.1 | Kiểm tra độ bền | Movies: khóa id không null hoặc trùng trong file nguồn | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG05 | 3.1 | Kiểm tra độ bền | Credits: khóa movie_id không null hoặc trùng trong file nguồn | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG06 | 3.1 | Kiểm tra độ bền | Movie release_date parse được hoặc được ghi nhận coerce | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG07 | 3.1 | Kiểm tra độ bền | Các trường JSON phim đúng cú pháp hoặc ghi nhận bất thường | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG08 | 3.1 | Kiểm tra độ bền | Quan hệ CSV movies và credits hai chiều | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG09 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: clean_movies_data.py | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG10 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: clean_credits_data.py | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG11 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: export_movies_to_postgres.py | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG12 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: export_credits_to_postgres.py | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG13 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: export_incremental_stage.py | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG14 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: get_watermark.py | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG15 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: update_watermark.py | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG16 | 3.1 | Yêu cầu bắt buộc | Kiểm tra mã nguồn: load_new_batch.py | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG17 | 3.1 | Yêu cầu bắt buộc | Graph Full Load Movies/Credits đúng chuỗi | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG18 | 3.1 | Kiểm tra độ bền | Watermark phụ thuộc vào thành công export incremental | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG19 | 3.1 | Kiểm tra độ bền | Loader incremental lọc batch qua LSET/CET | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG20 | 3.1 | Kiểm tra độ bền | Exporter incremental xử lý ID trùng khi replay | Readonly hoặc static | Phát hiện tĩnh trong code | Xem result.json theo run ID |
| MG21 | 3.1 | Yêu cầu bắt buộc | Full load rowcount stage so với CSV sau làm sạch | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG22 | 3.1 | Yêu cầu bắt buộc | Quan hệ hai bảng stage và khóa null/trùng | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG23 | 3.1 | Yêu cầu bắt buộc | Bảng watermark tồn tại và có dòng incremental | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MG24 | 3.1 | Kiểm tra độ bền | Metadata Mage có log run thực và rowcount | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| MI01 | 3.1 | Yêu cầu bắt buộc | Full Load chạy lại giữ nguyên dữ liệu | Isolated, snapshot trước/sau | Kết quả chạy mới | Xem result.json theo run ID |
| MI02 | 3.1 | Yêu cầu bắt buộc | Incremental batch mới thêm phim không trùng | Isolated, snapshot trước/sau | Kết quả chạy mới | Xem result.json theo run ID |
| MI03 | 3.1 | Yêu cầu bắt buộc | Incremental batch rỗng không thay đổi bảng | Isolated, snapshot trước/sau | Kết quả chạy mới | Xem result.json theo run ID |
| MI04 | 3.1 | Kiểm tra độ bền | Incremental cùng batch replay không tạo trùng | Isolated, snapshot trước/sau | Kết quả chạy mới | Xem result.json theo run ID |
| MI05 | 3.1 | Kiểm tra độ bền | Batch chứa ID đã có không tạo duplicate | Isolated, snapshot trước/sau | Kết quả chạy mới | Xem result.json theo run ID |
| MI06 | 3.1 | Kiểm tra độ bền | Batch lỗi không làm bẩn stage | Isolated, snapshot trước/sau | Kết quả chạy mới | Xem result.json theo run ID |
| MI07 | 3.1 | Kiểm tra độ bền | Export thất bại không cập nhật watermark | Isolated, snapshot trước/sau | Kết quả chạy mới | Xem result.json theo run ID |
| MI08 | 3.1 | Yêu cầu bắt buộc | Full Load lỗi một nhánh có snapshot mô tả | Isolated, snapshot trước/sau | Kết quả chạy mới | Xem result.json theo run ID |
| NC01 | 3.3 | Kiểm tra độ bền | Bridge weight_factor phải bắt được sai lệch | Isolated, ghi+rollback | Kết quả chạy mới | Xem result.json theo run ID |
| NC02 | 3.3 | Kiểm tra độ bền | ROI/profit phải bắt được sai lệch | Isolated, ghi+rollback | Kết quả chạy mới | Xem result.json theo run ID |
| NC03 | 3.3 | Kiểm tra độ bền | FK logic phải bắt được orphan | Isolated, ghi+rollback | Kết quả chạy mới | Xem result.json theo run ID |
| NC04 | 3.3 | Kiểm tra độ bền | Grain phải bắt được fact duplicate | Isolated, ghi+rollback | Kết quả chạy mới | Xem result.json theo run ID |
| NC05 | 3.3 | Kiểm tra độ bền | Bridge không chấp nhận duplicate cặp | Isolated, ghi+rollback | Kết quả chạy mới | Xem result.json theo run ID |
| PB01 | 3.4 | Yêu cầu bắt buộc | PBIX là file có thể đọc được | Readonly hoặc static | Phát hiện tĩnh trong PBIX | Xem result.json theo run ID |
| PB02 | 3.4 | Yêu cầu bắt buộc | Có tối thiểu hai trang Dashboard | Readonly hoặc static | Phát hiện tĩnh trong PBIX | Xem result.json theo run ID |
| PB03 | 3.4 | Yêu cầu bắt buộc | Mỗi trang có ít nhất một biểu đồ | Readonly hoặc static | Phát hiện tĩnh trong PBIX | Xem result.json theo run ID |
| PB04 | 3.4 | Yêu cầu bắt buộc | Report có tham chiếu measure DAX | Readonly hoặc static | Phát hiện tĩnh trong PBIX | Xem result.json theo run ID |
| PB05 | 3.4 | Yêu cầu bắt buộc | Overview có các KPI chính | Readonly hoặc static | Phát hiện tĩnh trong PBIX | Xem result.json theo run ID |
| PB06 | 3.4 | Yêu cầu bắt buộc | Dashboard có khả năng đặt bộ lọc/slicer | Readonly hoặc static | Phát hiện tĩnh trong PBIX | Xem result.json theo run ID |
| PB07 | 3.4 | Yêu cầu bắt buộc | Drill-down thời gian hoạt động | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| PB08 | 3.4 | Yêu cầu bắt buộc | Relationships đúng cardinality và cross-filter | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| PB09 | 3.4 | Yêu cầu bắt buộc | DAX measures tính đúng với SQL | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| PB10 | 3.4 | Yêu cầu bắt buộc | Top N được sort theo measure hiển thị | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| PB11 | 3.4 | Yêu cầu bắt buộc | Ngưỡng Min Movies, Min Votes dùng đúng measure | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| PB12 | 3.4 | Yêu cầu bắt buộc | Refresh Import thành công và khớp DDS | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| PB13 | 3.4 | Quy tắc project | Allocation Weighted và Full đổi thứ hạng | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| PB14 | 3.4 | Quy tắc project | Country=USA, Year=2014, Genre=Action | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| Q1 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q1 | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| Q1SQL | 3.4 | Quy tắc project | Q1 Rating theo runtime/genre, chỉ phim đủ votes | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| Q2 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q2 | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| Q2SQL | 3.4 | Quy tắc project | Q2 Rating & popularity theo ngôn ngữ gốc (Min Votes=100) | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| Q3 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q3 | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| Q3SQL | 3.4 | Quy tắc project | Q3 Weighted genre profit qua các thập niên | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| Q4 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q4 | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| Q4SQL | 3.4 | Quy tắc project | Q4 ROI/Pct over budget theo budget band | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| Q5 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q5 | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| Q5SQL | 3.4 | Quy tắc project | Q5 Hãng lợi nhuận Weighted vs Full (không nhân đôi hợp tác) | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| Q6 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q6 | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| Q6SQL | 3.4 | Quy tắc project | Q6 Profit/ROI theo tháng và thập niên | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| Q7 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q7 | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| Q7SQL | 3.4 | Quy tắc project | Q7 Quốc gia / single-multi / English-non-English | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
| Q8 | 3.4 | Quy tắc project | Câu hỏi nghiệp vụ Q8 | Desktop, thủ công | Kết quả chạy mới | Xem result.json theo run ID |
| Q8SQL | 3.4 | Quy tắc project | Q8 Theme sequel/adaptation/superhero, chống trùng một phim nhiều keyword | Readonly hoặc static | Kết quả chạy mới | Xem result.json theo run ID |
