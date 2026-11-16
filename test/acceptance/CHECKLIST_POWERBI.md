# Kiểm tra Power BI Desktop — 3.4 + 8 câu hỏi nghiệp vụ

**Trạng thái khởi điểm:** `PB01–PB06` có thể kiểm tra **metadata PBIR bên trong PBIX**; còn `PB07–PB14`, `Q1–Q8` không được PASS nếu chưa có kết quả Power BI Desktop hoặc semantic model. Hãy điền **actual và ảnh thật** bên dưới; các số tham chiếu từ báo cáo nhóm chỉ là baseline snapshot cũ.

## 1. Các thao tác chung

1. Mở `powerbi_dashboard/TMDB_Movie_Dashboard.pbix` bằng Power BI Desktop. Ghi ngày, thời gian, file đang mở, server/database trong Data Source Settings; kiểm Storage mode của bảng trong Model view để xác định Import/DirectQuery. **Không coi số đang có trong Import là đã Refresh.**
2. Mở Model view, xem các bảng `fact_movie`, 7 `dim_*`, 4 `bridge_movie_*`, tham số `Allocation Mode`, `Min Votes`, `Min Movies`. Chụp relationship model: 3 quan hệ Fact–Dim, 4 đường đa trị qua Bridge, chiều filter và cardinality. Nếu không nhìn đủ, chia ảnh. Không suy luận hướng cross-filter từ màu đường nối.
3. Mở Model view hoặc Tabular Editor / DAX Studio (nếu đã có), chụp hoặc xuất **công thức DAX thật** của Movie Count, Valid Movies, Total Revenue, Total Budget, Total Profit, ROI Overall, ROI Median, Pct Over Budget, Profit by Genre/Company/Country, Median Rating, Avg Runtime, Median Popularity. Nếu chỉ có tên measure trong PBIX thì ghi `BLOCKED (thiếu expression)`.
4. Xác nhận bốn page hiển thị ở PBIX đã phân tích: **Overview**, **Financial drivers**, **Companies & Countries**, **Audience & Ratings**. Kiểm nội dung charts/card/slicer thực tế. Chụp tổng quan từng page và filter pane.
5. Xem `Country=All`, `Year=All`, `Genre=All`, `Allocation Mode=Weighted`, Min valid movies = 5, Min votes = 100 (nếu visual có dùng). Chụp bộ lọc kèm KPI. Chạy runner section 34 theo đúng nhánh integration/readonly ở phần 10.5 của [hướng dẫn](../HUONG_DAN_CHAY_TEST.md) để có `BI01` và các `QxSQL`. Bảo đảm cùng nguồn/snapshot mới dùng kết quả SQL để đối chiếu.
6. Chụp Refresh thật: Home → Refresh → kiểm thông báo hoàn tất; ghi thời gian, sau đó xem KPI có khớp SQL từ DDS. Nếu không thể Refresh hoặc không có credential, để `PB12 BLOCKED`.

## 2. Checklist hành vi cốt lõi

| Test ID | Thao tác | Expected/cần đối chiếu | Actual / ảnh |
|---|---|---|---|
| PB07 | Trên chart thời gian, chọn **Go to next level / Expand all down one level** qua Decade → Year → Quarter → MonthName | Độ phân giải thời gian đổi theo hierarchy, đủ cấp thực đang được dùng (nếu report không hỗ trợ thì ghi thực tế) | [ ] |
| PB08 | Model view → chọn từng relationship Fact–Dim và Bridge; chụp cardinality/filter direction | Cùng grain Fact và không nhân đôi phim qua nhiều bridge | [ ] |
| PB09 | Chọn 3 filter bất kỳ, so DAX numeric trước làm tròn với SQL độc lập | DAX và SQL khớp trên cùng tập movie_sk / ngữ cảnh lọc | [ ] |
| PB10 | Chọn chart Top N công ty/genre và xem Filters + Sort | Measure dùng để rank trùng measure người xem thấy; nếu không, ghi mức độ sai lệch | [ ] |
| PB11 | Đổi Min Movies = 5 → giá trị lớn hơn, Min Votes = 100 → 1.000 | Ngưỡng chỉ tác động các visuals được thiết kế; kiểm visual rating khác visual finance | [ ] |
| PB12 | Refresh thật, lưu màn hình báo hoàn tất và snapshot KPI | Không chỉ dựa vào dữ liệu Import đang hiển thị | [ ] |
| PB13 | Công ty Weighted → Full, cùng filter | Chỉ tiêu phân bổ thay đổi; rank thực được ghi lại (không mặc định mọi rank phải thay đổi) | [ ] |
| PB14 | Country=United States of America; Year=2014; Genre=Action | SQL `BI02` trả movie count, valid count, revenue, profit, median ROI, % over budget trên cùng bộ lọc | [ ] |

**Baseline cũ chưa xác minh:** toàn danh mục khoảng 4.803 movies, 3.229 valid, valid revenue 391,49 tỷ USD, total profit 260,22 tỷ, ROI Median 130,0%, Pct Over Budget 75,5%. Với US/2014/Action khoảng 47 movies, 41 valid, valid revenue 13,84 tỷ, profit 9,87 tỷ, ROI median 216,4%, Pct Over Budget 87,8%. Nếu số mới khác: đầu tiên kiểm snapshot, filters, weighted/full, ngưỡng, rounded display, rồi mới kết luận lỗi. **ROI Overall ≠ ROI Median** là đúng về định nghĩa.

## 3. Tám câu hỏi nghiệp vụ (quy tắc project, không áp đặt thành yêu cầu giảng viên)

Mỗi Q phải đủ **4 bằng chứng**: trang/chart/measure nào trả lời; SQL tính lại từ `QxSQL`; giá trị Power BI cùng filter; đánh giá đủ các vế trong chính câu hỏi gốc. `QxSQL INFO` là kết quả SQL tham chiếu, **không** làm `Qx PASS`. Chỉ kết luận thủ công khi đã đối chiếu Power BI trên cùng nguồn và ngữ cảnh lọc.

| Q | Trang/điểm cần xác nhận | Phép so và baseline cũ để tham khảo | Hình/actual / kết luận |
|---|---|---|---|
| **Q1** | Audience & Ratings: rating theo runtime band và genre; avg runtime vs rating by genre | `Q1SQL`; ngưỡng Min Votes=100. Baseline: rating 5,9 → 7,3 theo nhóm thời lượng, Documentary ~102 phút/~7,25; War ~136 phút/~7,1. | [ ] |
| **Q2** | Audience & Ratings: popularity + rating theo original language và genre | `Q2SQL` + `BI07`; Japanese popularity median ~39/rating ~7,5; Portuguese rating ~7,8; English ~6,3/rất nhiều votes; documentary/war theo genre phải thấy riêng. | [ ] |
| **Q3** | Overview & Financial drivers: revenue/profit theo năm/genre/decade | `Q3SQL` weighted; Action ~34,6; Adventure ~34,4; Comedy ~34,0; Drama ~30,8 tỷ USD (cũ). Phải giải thích tăng/giảm theo thập niên. | [ ] |
| **Q4** | Financial drivers: ROI median và tỷ lệ vượt budget theo BudgetBand; hỏi có quan hệ Budget–Revenue ở mức phim không | `Q4SQL` + `BI08`; nhóm dưới 1 triệu ROI median ~924,6%; 50–100 triệu ~93,8%; >=100 triệu ~168,4%; kiểm có chart cấp phim nếu câu hỏi yêu cầu. | [ ] |
| **Q5** | Companies & Countries: rank hãng theo profit, đổi Weighted/Full | `Q5SQL` + `BI09`, ít nhất 5 phim hợp lệ; Weighted cũ Paramount ~10,9 tỷ, Universal ~10,4, Warner ~9,7; Full cũ Warner ~30,9, Universal ~29,5. Kiểm câu hỏi có yêu cầu revenue/ROI hãng mà dashboard chưa hiện không. | [ ] |
| **Q6** | Financial drivers: tháng phát hành và thập niên với profit/ROI median | `Q6SQL`; tháng 6 cũ profit ~42 tỷ và ROI ~190%; tháng 9 ~75–80% ROI. Cần so số liệu theo ngữ cảnh/time hierarchy. | [ ] |
| **Q7** | Companies & Countries: ROI quốc gia, CountryType Single/Multi, LanguageGroup | `Q7SQL`; Iceland ~212,8%, Japan ~202,5%, New Zealand ~187,6% chỉ là tham chiếu; xem ngưỡng số phim, nhóm Unknown và interaction CountryType+LanguageGroup. | [ ] |
| **Q8** | Companies & Countries: Themes/Keywords Sequel/Adaptation/Superhero | `Q8SQL`; baseline Adaptation 338 phim/38,96 tỷ/158,6% ROI; Sequel 98/20,15 tỷ/242,9%; Superhero 69/18,91 tỷ/205,6%. Keyword tagging chồng lấp: Total không cộng ba nhóm. | [ ] |

**Lưu ý phép tính:** Phân bổ Genre/Company/Country dùng 1/k và phải tránh double counting; Keyword không có `weight_factor`. Full cộng qua nhóm có thể vượt tổng Fact. ROI phải lưu thập phân và hiển thị Percentage (DAX không nhân 100 lần nữa). `Min Votes` là ngưỡng trên **phim**, không phải tổng votes của nhóm. Với ngưỡng 1.000, nếu chỉ còn English trong chart ngôn ngữ, dùng `BI10` kiểm các ngôn ngữ khác có thiếu số phim đủ votes không trước khi kết luận.

## 4. Mẫu ghi bằng chứng thủ công

```text
Test ID: PB12 hoặc Qx
Power BI file:
Page/Visual/Measure DAX thực (nếu truy cập được):
Ngày giờ & data source/snapshot:
Filter context: Country=...; Year=...; Genre=...; Allocation=...; MinVotes=...; MinMovies=...
Expected (định nghĩa, không phải số baseline mặc định):
Actual trên Power BI: ... (đơn vị, trước/sau làm tròn)
Actual từ SQL reference (`test/results/.../result.json`):
Sai lệch, tolerance & nguyên nhân có căn cứ:
Trạng thái: PASS / FAIL / BLOCKED
Ảnh chứng minh: <đường dẫn trong máy>
```

Không tự điền PASS cho DAX/relationships/refesh từ việc file PBIX tồn tại, và không dùng hình dashboard Import cũ làm bằng chứng dữ liệu mới.
