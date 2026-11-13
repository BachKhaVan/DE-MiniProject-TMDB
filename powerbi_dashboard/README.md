# Power BI Dashboard — TMDB 5000 Movies

## 1. Mục tiêu

Dashboard Power BI phục vụ mini project **Phân tích hiệu quả tài chính của các tác phẩm điện ảnh** từ bộ dữ liệu **TMDB 5000 Movies**. Phần này đảm nhận lớp **BI / Semantic Model / Data Visualization**, sử dụng dữ liệu đã được Mage.ai nạp vào PostgreSQL và dbt chuyển đổi thành mô hình đa chiều (DDS).

**Phạm vi README:** mô tả dashboard và cách mở/kiểm tra báo cáo Power BI. Mã nguồn ingestion và transformation được quản lý tại `../mage_pipeline/` và `../dbt_transform/`.

## 2. Nội dung thư mục

```text
powerbi_dashboard/
├── README.md
└── TMDB_Movie_Dashboard.pbix
```

Tệp `.pbix` chứa báo cáo Power BI, mô hình dữ liệu, relationships, DAX measures, slicers và các trang trực quan hóa. **Không cần đưa các CSV nguồn vào thư mục này.**

## 3. Nguồn dữ liệu và mô hình

- **Nguồn gốc:** `tmdb_5000_movies.csv` và `tmdb_5000_credits.csv` (TMDB 5000 Movie Dataset).
- **Ingestion:** Mage.ai → bảng raw trong schema `stage` của PostgreSQL.
- **Transformation:** dbt → các bảng `dds.fact_movie`, `dds.dim_*`, `dds.bridge_movie_*`.
- **Power BI:** sử dụng mô hình DDS để định nghĩa relationships, DAX measures và dashboard tương tác.
- **Grain:** 1 dòng trong `fact_movie` = 1 phim (`movie_sk`). Các quan hệ đa trị Genre, Company, Country và Keyword được biểu diễn qua Bridge tables.

Ba Bridge Genre / Company / Country có `weight_factor` để phân bổ doanh thu, ngân sách và lợi nhuận khi phân tích theo nhóm; Bridge Keyword biểu diễn quan hệ gắn nhãn, **không** phân bổ trọng số. Dashboard có slicer **Allocation mode** (Weighted / Full) cho các phân tích có hỗ trợ chế độ phân bổ.

## 4. Các trang Dashboard

| Trang | Nội dung chính |
|---|---|
| **1. Movie Portfolio Overview** | KPI Revenue, Movies, Valid Movies, Profit, Median ROI, % Over Budget; xu hướng theo năm/thập niên; Top 10 Genre theo lợi nhuận. |
| **2. Financial Drivers** | Lợi nhuận và ROI theo tháng phát hành; ROI và tỷ lệ doanh thu vượt ngân sách theo nhóm Budget; phân tích Genre Portfolio và lợi nhuận theo thập niên. |
| **3. Companies & Countries** | Top 10 hãng theo Profit, Top 15 quốc gia theo Median ROI, Themes & Keywords, so sánh ROI theo loại hợp tác quốc gia và nhóm ngôn ngữ. |
| **4. Audience & Ratings** | Liên hệ Runtime–Rating theo Genre; Rating theo nhóm thời lượng và Genre; Popularity–Rating theo ngôn ngữ. |

Các trang có bộ lọc như Country, Year, Genre; một số trang có bộ lọc riêng gồm Allocation mode, Min valid movies per entity, Language group và Min votes per movie.

## 5. Định nghĩa chỉ số và quy tắc phân tích

- **Movies:** số dòng/phim trong FactMovie theo ngữ cảnh bộ lọc.
- **Valid Movies:** phim có `is_finance_valid = 1` (Budget và Revenue đều hợp lệ, lớn hơn 0).
- **Valid Revenue / Total Budget:** chỉ tính các phim tài chính hợp lệ.
- **Profit:** `Revenue - Budget` trên tập phim tài chính hợp lệ.
- **Movie ROI:** `Profit / Budget` khi đủ dữ liệu; **Median ROI** là trung vị ROI theo từng phim, không phải tỷ số tổng Profit trên tổng Budget.
- **ROI Overall:** `Total Profit / Total Budget`.
- **Pct Over Budget:** số phim có Revenue > Budget chia cho số phim tài chính hợp lệ.
- **Weighted allocation:** phân bổ chỉ tiêu tài chính của phim qua Genre / Company / Country theo `weight_factor = 1 / số liên kết` tương ứng. **Full allocation:** ghi nhận toàn bộ chỉ tiêu của phim cho từng nhóm có liên kết. Vì một phim có thể nằm trong nhiều nhóm, cộng số liệu ở chế độ Full có thể đếm lặp.
- **Audience / Ratings:** có thể đặt ngưỡng `Min votes per movie` để chỉ tính các phim đủ lượt đánh giá; một số biểu đồ còn yêu cầu tối thiểu 5 phim đủ điều kiện mỗi nhóm. Đây là ngưỡng hiển thị/phân tích, không phải kiểm định thống kê.
- **Themes / Keywords:** các nhóm chủ đề có thể chồng lấp; phim thiếu keyword không đóng góp vào các dòng Theme nhưng vẫn được tính trong Total toàn bộ danh mục nếu không có bộ lọc Theme.

**Lưu ý:** năm trên trục thời gian là **năm phát hành phim**, không phải năm ghi nhận doanh thu. Dữ liệu 2016–2017 không đầy đủ; các nhóm thập niên đầu, quốc gia hoặc ngôn ngữ có ít phim có thể có chỉ số trung vị biến động mạnh.

## 6. Mở báo cáo và Refresh dữ liệu

### 6.1. Mở Dashboard

1. Mở `TMDB_Movie_Dashboard.pbix` bằng **Microsoft Power BI Desktop** (phiên bản tương thích hoặc mới hơn phiên bản đã tạo báo cáo).
2. Tệp PBIX lưu mô hình, DAX, biểu đồ và có thể kèm **dữ liệu Import từ lần nạp trước**. Vì vậy, báo cáo có thể vẫn hiển thị KPI dù PostgreSQL đang tắt. **Mở được file không đồng nghĩa với Refresh thành công.**
3. Nếu chỉ cần xem báo cáo từ snapshot đã lưu, không bắt buộc phải Refresh. Muốn lấy dữ liệu mới từ Data Warehouse thì làm tiếp các bước dưới đây.

### 6.2. Chuẩn bị nguồn PostgreSQL trước khi Refresh

**Trường hợp sử dụng PostgreSQL Docker của nhóm trên máy đang mở Power BI:**

1. Mở **Docker Desktop** và bảo đảm Docker Engine đang chạy.
2. Mở PowerShell/Terminal ở **thư mục gốc repository** (nơi chứa `compose.yaml`), chạy:

   ```powershell
   docker compose ps
   docker compose up -d postgres
   ```

   Lệnh `up -d postgres` khởi động dịch vụ PostgreSQL; không tự nạp lại CSV hoặc tự chạy dbt. Với cấu hình mặc định trong `compose.yaml`, máy Windows truy cập PostgreSQL qua **`localhost:5432`**, database **`warehouse`**, user **`labuser`**. Các giá trị database/user có thể được thay đổi bằng cấu hình môi trường.

3. Kiểm tra dịch vụ đã sẵn sàng:

   ```powershell
   docker compose exec postgres pg_isready -U labuser -d warehouse
   ```

   Kỳ vọng là thông báo có `accepting connections`. Có thể kiểm tra thêm cổng trên Windows PowerShell:

   ```powershell
   Test-NetConnection localhost -Port 5432
   ```

   Nếu kết nối được, `TcpTestSucceeded` sẽ là `True`.

4. Đảm bảo trong PostgreSQL **đã có dữ liệu ở schema `dds`**, tối thiểu gồm `dds.fact_movie`, các bảng `dds.dim_*` và `dds.bridge_movie_*`. **Container chạy thành công nhưng DDS chưa được Mage/dbt tạo thì chưa đủ để Refresh.** Nếu dữ liệu chưa có, cần chạy phần ingestion/transformation theo hướng dẫn ở README gốc của repo hoặc nhờ thành viên phụ trách Mage/dbt.

**Trường hợp dùng PostgreSQL của máy khác hoặc server dùng chung:** Không cần khởi động Docker cục bộ; phải bảo đảm server đó đang hoạt động, mạng/cổng có thể truy cập và tài khoản có quyền đọc các bảng `dds`. Khi đó **không mặc định dùng `localhost`**.

> **Bảo mật:** Không đưa mật khẩu PostgreSQL vào README, mã DAX hoặc commit Git. Nếu Docker Compose báo thiếu `POSTGRES_PASSWORD`, cấu hình biến này trong file `.env` cục bộ theo hướng dẫn của nhóm (không commit `.env`). Không dùng `docker compose down -v` để sửa lỗi kết nối, vì lệnh này có thể xóa volume PostgreSQL.

### 6.3. Refresh trong Power BI Desktop

1. Mở file `.pbix` và vào **File → Options and settings → Data source settings**.
2. Chọn nguồn **PostgreSQL** tương ứng với file báo cáo; kiểm tra server, database và quyền truy cập. Nếu chạy PostgreSQL mặc định trên máy này, cấu hình kết nối tương ứng **server `localhost:5432`**, **database `warehouse`**. Nếu dùng server khác, nhập đúng thông tin do nhóm cung cấp.
3. Nếu Power BI yêu cầu xác thực, chọn phương thức đăng nhập PostgreSQL phù hợp và nhập thông tin đăng nhập của môi trường đang dùng. Trường hợp đổi máy hoặc đổi server có thể phải cập nhật thông tin nguồn và credentials trước khi Refresh.
4. Chọn **Home → Refresh** trong Power BI Desktop. Đợi Power BI cập nhật xong các bảng Fact, Dimension và Bridge từ PostgreSQL.
5. Kiểm tra không còn hộp thoại lỗi; mở cả 4 trang, thử slicer Country/Year/Genre và xác nhận số liệu. Sau khi Refresh thành công, bấm **Ctrl + S** để lưu snapshot cập nhật vào `.pbix`.

**Mốc kiểm tra với snapshot TMDB ban đầu, khi các slicer ở All:** Movies = **4.803**, Valid Movies = **3.229**, Valid Revenue ≈ **$391,49bn**, Profit ≈ **$260,22bn**, Median ROI = **130,0%**, Pct Over Budget = **75,5%**. Nếu nguồn `dds` đã thay đổi do incremental load hoặc điều chỉnh dbt, các mốc này có thể thay đổi.

### 6.4. Xử lý lỗi Refresh thường gặp

| Thông báo/hiện tượng | Nguyên nhân có thể | Cách kiểm tra/xử lý |
|---|---|---|
| `No connection could be made because the target machine actively refused it` | PostgreSQL chưa chạy; sai host/port; dịch vụ không công bố cổng | Kiểm tra Docker/`docker compose ps`, `pg_isready`, cổng `5432` và Data source settings; khởi động đúng server |
| `password authentication failed` hoặc lỗi đăng nhập | Sai user/password hoặc credentials đã lưu thuộc máy khác | Kiểm tra lại tài khoản PostgreSQL và thiết lập quyền truy cập nguồn trong Power BI; không chia sẻ mật khẩu |
| `relation dds... does not exist` hoặc thiếu bảng | Đang kết nối nhầm database, hoặc Mage/dbt chưa hoàn thành | Xác minh database, schema `dds` và kết quả chạy dbt |
| Dashboard vẫn hiển thị số cũ sau khi có lỗi | PBIX còn dữ liệu Import đã lưu | Xem kết quả Refresh; không coi số liệu hiển thị là bằng chứng đã lấy được dữ liệu mới |
| Một số chỉ số thay đổi sau Refresh thành công | Nguồn DDS thay đổi hoặc người dùng vẫn đang chọn slicer | Đặt lại slicer về All; đối chiếu bản ghi mới và logic transformation |

**Lưu ý khi bàn giao:** Nhóm đã thực hiện thao tác Refresh thành công trên môi trường đang phát triển Dashboard, nhưng **máy khác vẫn phải có nguồn PostgreSQL/DDS và cấu hình kết nối phù hợp**. Hướng dẫn này áp dụng cho **Refresh trong Power BI Desktop**; không mặc định đồng nghĩa với lịch Refresh tự động trên Power BI Service.

## 7. Giá trị tham chiếu để kiểm tra

Với snapshot TMDB gốc được nhóm sử dụng, khi Country / Year / Genre = **All**, Allocation mode = **Weighted**:

| Chỉ số Overview | Giá trị tham chiếu |
|---|---:|
| Movies | 4.803 |
| Valid Movies | 3.229 |
| Valid Revenue | xấp xỉ **391,49 tỷ USD** |
| Profit | xấp xỉ **260,22 tỷ USD** |
| Median ROI | **130,0%** |
| Pct Over Budget | **75,5%** |

Các con số trên là **mốc kiểm thử cho snapshot nguồn ban đầu**, không phải cam kết giữ nguyên sau khi nạp dữ liệu mới hoặc thay đổi logic xử lý.

Một số bài test gợi ý:

- Đổi `Min votes per movie` từ 100 thành 1.000: nhiều nhóm Genre/Language có thể không còn đủ 5 phim để hiển thị; đó là hành vi dự kiến.
- Đổi `Allocation mode` giữa Weighted và Full: các biểu đồ lợi nhuận theo Genre/Company thay đổi theo chế độ phân bổ; các KPI tài chính tổng quan không phụ thuộc chế độ này.
- Kết hợp Country + Year + Genre để kiểm tra relationships và filter context.

## 8. Quy ước commit và bàn giao

- Commit file `.pbix` và `README.md` vào thư mục `powerbi_dashboard/`.
- **Không commit** mật khẩu, `.env`, thông tin xác thực hoặc dữ liệu nhạy cảm. Kiểm tra các đường dẫn nguồn/metadata lưu trong PBIX trước khi chia sẻ.
- Với file PBIX lớn, kiểm tra giới hạn dung lượng của dịch vụ Git đang sử dụng; nếu cần Git LFS thì thống nhất với nhóm trước khi commit.
- Làm việc trên nhánh tính năng và mở pull request vào `develop` theo quy ước ở README gốc của repository.
- Sau khi thêm PBIX, cập nhật **README gốc** (dòng trạng thái và cây thư mục) để không còn ghi rằng Power BI chưa được triển khai.

## 9. Phạm vi hoàn thành

Hạng mục này bàn giao **Power BI Semantic Model, DAX và 4 trang Dashboard**. **Generative AI / AI-assisted analytics**, kiểm thử chạy xuyên suốt pipeline trên môi trường triển khai chung và các phần việc Mage/dbt là phạm vi tích hợp của nhóm, không mặc định được hoàn tất chỉ vì đã có file PBIX.
