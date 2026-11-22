# TMDB 5000 — AI Companion

Ứng dụng Streamlit hỗ trợ phân tích kho dữ liệu TMDB 5000 bằng tiếng Việt. Ứng dụng đọc dữ liệu từ PostgreSQL schema `dds`, hiển thị KPI và các bảng đối chứng, đồng thời dùng Groq hoặc Google Gemini để diễn giải số liệu và hỗ trợ Text-to-SQL.

> **Phạm vi dữ liệu:** ứng dụng sử dụng snapshot TMDB đã nạp vào DDS, không truy vấn dữ liệu bên ngoài TMDB. Năm 2016–2017 chưa đầy đủ; kết quả cần được hiểu trong giới hạn đó.

## 1. Tính năng

| Khu vực | Chức năng |
|---|---|
| Sidebar | Trạng thái kết nối PostgreSQL; lọc Quốc gia, Năm phát hành, Thể loại; chọn Weighted hoặc Full. Mặc định là Weighted và không chọn bộ lọc nào. |
| **Tóm tắt KPI** | Sáu KPI Overview, Top 5 phim theo lợi nhuận, tóm tắt AI và bảng căn cứ dữ liệu. |
| **Giải thích xu hướng** | Chọn tối đa bốn biểu đồ trong bốn nhóm trang Power BI, nhập trọng tâm tùy chọn, nhận diễn giải AI và xem dữ liệu đối chứng. |
| **Hỏi đáp dữ liệu** | Hỏi bằng tiếng Việt hoặc chạy câu hỏi mẫu; hệ thống sinh SQL chỉ-đọc, trả bảng kết quả và diễn giải. Lịch sử hiển thị lượt mới nhất trước, có thể xóa riêng từng lượt. |

Tab 2 hiện dùng danh mục biểu đồ Power BI, không còn giao diện chọn tám câu hỏi Q1–Q8. Các hàm chẩn đoán Q1–Q8 vẫn có trong `queries.py` để sử dụng từ mã Python.

## 2. Cấu trúc và phụ thuộc

```text
<repository-root>/
├── .env                         # cấu hình cục bộ; không commit
├── .streamlit/config.toml       # theme Streamlit đang dùng
├── ai_assistant/
│   ├── app.py                   # giao diện và trạng thái phiên Streamlit
│   ├── db.py                    # kết nối PostgreSQL, READ ONLY, kiểm duyệt SQL
│   ├── queries.py               # bộ lọc, KPI và truy vấn biểu đồ
│   ├── llm.py                   # Groq/Gemini, diễn giải AI, Text-to-SQL
│   ├── requirements.txt
│   └── README.md
├── dbt_transform/               # tạo và quản lý các bảng DDS
└── test/manual test/
    └── verify_ai_manual.sql     # SQL đối chiếu thủ công cho AI Companion
```

`ai_assistant` không tạo bảng, không chạy dbt và không ghi dữ liệu vào PostgreSQL. Hãy chuẩn bị PostgreSQL và schema `dds` trước khi chạy. Quy trình dựng warehouse được hướng dẫn tại [README tổng](../README.md) và [README dbt](../dbt_transform/README.md); cách mở và làm mới Power BI tại [README Power BI](../powerbi_dashboard/README.md).

## 3. Mô hình dữ liệu và quy tắc KPI

Ứng dụng đọc 12 bảng trong schema `dds`:

- Fact: `fact_movie` (grain: một dòng cho một phim).
- Dimensions: `dim_movie`, `dim_date`, `dim_genre`, `dim_company`, `dim_country`, `dim_language`, `dim_keyword`.
- Bridges: `bridge_movie_genre`, `bridge_movie_company`, `bridge_movie_country`, `bridge_movie_keyword`.

Quy tắc nghiệp vụ được áp dụng trong truy vấn:

- Phim tài chính hợp lệ có `is_finance_valid = 1` (ngân sách và doanh thu lớn hơn 0). Doanh thu, lợi nhuận và ROI tài chính chỉ tính trên tập hợp hợp lệ.
- `roi` lưu dạng thập phân: `0.5` tương ứng `50%`. ROI trung vị dùng `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY roi)`; không cộng ROI và không dùng `AVG(roi)`.
- Weighted chỉ nhân `weight_factor` cho doanh thu/lợi nhuận khi phân tích theo bridge Genre hoặc Company có phân bổ. Full ghi toàn bộ chỉ tiêu cho mỗi nhóm liên kết. Không nhân trọng số vào ROI, rating hoặc số lượng phim.
- KPI Overview được tính ở grain phim và không đổi theo chế độ Weighted/Full. Chế độ phân bổ ảnh hưởng những biểu đồ tài chính theo nhóm có hỗ trợ phân bổ.
- `bridge_movie_keyword` không có `weight_factor`; số phim theo chủ đề dùng `COUNT(DISTINCT movie_sk)`. Một phim có thể thuộc nhiều nhóm chủ đề.
- Lọc Genre/Country dùng `EXISTS` để tránh nhân dòng Fact khi một phim có nhiều liên kết. Các dimension Unknown bị loại khỏi danh sách lọc và nhóm phù hợp.

Sáu thẻ KPI ở Tab 1, theo thứ tự:

1. `Valid Revenue ($bn)`
2. `Movies`
3. `Valid movies`
4. `Profit ($bn)`
5. `Median ROI (%)`
6. `Pct Over Budget (%)`

Top 5 phim được xếp theo lợi nhuận giảm dần, chỉ gồm phim hợp lệ. Median rating được giữ trong bảng căn cứ KPI, không phải thẻ KPI thứ bảy.

## 4. Danh mục biểu đồ Tab 2

Các tên dưới đây là nhãn biểu đồ trong giao diện. Mỗi truy vấn dùng các lựa chọn Country, Year, Genre từ Sidebar; chỉ các biểu đồ được chọn mới được truy vấn. Hệ thống giới hạn tối đa bốn biểu đồ mỗi lượt.

| Nhóm trang | Tên biểu đồ | Ghi chú về số liệu |
|---|---|---|
| Overview | `Revenue & Profit by Release Year` | Số phim và chỉ tiêu tài chính theo năm phát hành; loại năm Unknown; doanh thu/lợi nhuận chỉ tính phim tài chính hợp lệ. |
| Overview | `Profit by Genre (Top 10)` | Top 10 Genre theo lợi nhuận; Weighted/Full áp dụng cho lợi nhuận theo Genre. |
| Overview | `Profit & Median ROI by Decade` | Lợi nhuận và ROI trung vị theo thập niên; chỉ phim tài chính hợp lệ. |
| Financial drivers | `Genre Profit Ranking by Decade` | Xếp hạng lợi nhuận Genre theo thập niên; áp dụng Weighted/Full; mỗi nhóm cần ít nhất 5 phim hợp lệ. |
| Financial drivers | `Genre Portfolio: Valid Volume vs Median ROI` | Số phim hợp lệ và ROI trung vị theo Genre; tối thiểu 5 phim mỗi nhóm. |
| Financial drivers | `Seasonality: Profit & Median ROI by Month` | Lợi nhuận, số phim hợp lệ và ROI trung vị theo tháng phát hành; loại tháng/ngày Unknown. |
| Financial drivers | `ROI & Over-Budget Rate by Budget Band` | ROI trung vị và tỷ lệ doanh thu vượt ngân sách theo nhóm ngân sách; chỉ phim tài chính hợp lệ. |
| Companies & Countries | `Top 15 Countries by Median ROI` | Top 15 quốc gia theo ROI trung vị; tối thiểu 5 phim hợp lệ mỗi quốc gia. |
| Companies & Countries | `Median ROI by Country Type & Language` | ROI trung vị theo nhóm loại quốc gia và ngôn ngữ; loại Unknown; tối thiểu 5 phim mỗi nhóm. |
| Companies & Countries | `Themes & Keywords` | Số phim, số phim hợp lệ và chỉ tiêu tài chính theo Adaptation, Sequel, Superhero, Other; tối thiểu 5 phim mỗi theme; keyword không có trọng số, các nhóm có thể chồng lấp. |
| Companies & Countries | `Top 10 Companies by Profit` | Top 10 hãng theo lợi nhuận; áp dụng Weighted/Full; tối thiểu 5 phim hợp lệ mỗi hãng. |
| Audience & Ratings | `Runtime vs Rating by Genre` | Runtime trung bình và rating trung vị theo Genre; phim có ít nhất 100 votes, nhóm cần tối thiểu 5 phim. |
| Audience & Ratings | `Median Rating by Genre` | Rating trung vị theo Genre; phim có ít nhất 100 votes và tối thiểu 5 phim mỗi nhóm. |
| Audience & Ratings | `Median Rating by Runtime Band` | Rating trung vị theo nhóm thời lượng; phim có ít nhất 100 votes và nhóm cần tối thiểu 5 phim. |
| Audience & Ratings | `Popularity vs Rating by Language` | Popularity và rating trung vị theo ngôn ngữ; phim có ít nhất 100 votes, tối thiểu 5 phim mỗi nhóm. |

Ngưỡng trên là điều kiện trong truy vấn hiện tại, không phải kiểm định thống kê. Sidebar không có bộ lọc Language group; ngôn ngữ vẫn là một chiều phân nhóm trong các biểu đồ liên quan.

## 5. Cấu hình

Tạo hoặc cập nhật file `.env` tại **thư mục gốc repository**. Không đặt file này trong `ai_assistant/`.

```env
POSTGRES_DB=warehouse
POSTGRES_USER=labuser
POSTGRES_PASSWORD=mat_khau_cua_ban
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Groq được ưu tiên tự động nếu có GROQ_API_KEY và không đặt LLM_PROVIDER.
GROQ_API_KEY=khoa_groq_cua_ban
# Tùy chọn; mặc định hiện tại: openai/gpt-oss-120b
# GROQ_MODEL=openai/gpt-oss-120b

# Có thể chọn Gemini thay Groq.
# LLM_PROVIDER=gemini
# GEMINI_API_KEY=khoa_gemini_cua_ban
# Tùy chọn; mặc định hiện tại: gemini-2.5-flash-lite
# GEMINI_MODEL=gemini-2.5-flash-lite
```

| Biến | Ý nghĩa |
|---|---|
| `POSTGRES_DB`, `POSTGRES_USER` | Tên database và user kết nối DDS. |
| `POSTGRES_PASSWORD` | Mật khẩu PostgreSQL; giữ riêng tư và không commit. |
| `POSTGRES_HOST`, `POSTGRES_PORT` | Tùy chọn; mặc định `localhost`, `5432`. Với Docker trên máy host, thường dùng `localhost`; container Mage dùng cấu hình host riêng. |
| `LLM_PROVIDER` | `groq` hoặc `gemini`. Nếu bỏ trống, chọn Groq khi có `GROQ_API_KEY`, nếu không chọn Gemini. |
| `GROQ_API_KEY`, `GEMINI_API_KEY` | Khóa tương ứng với nhà cung cấp. Ít nhất một khóa cần có để gọi tính năng AI. |
| `GROQ_MODEL`, `GEMINI_MODEL` | Tùy chọn để đổi model mặc định. Model phải còn khả dụng và được API key cho phép. |

Nếu có cả hai khóa, Groq được chọn khi không đặt `LLM_PROVIDER`. Có thể đặt `LLM_PROVIDER=gemini` để chủ động dùng Gemini. **Hiện tại đây là lựa chọn nhà cung cấp, không phải tự động chuyển sang Gemini khi một yêu cầu Groq lỗi.** Khởi động lại ứng dụng sau khi đổi cấu hình. Khóa lấy tại [Groq Console](https://console.groq.com/keys) hoặc [Google AI Studio](https://aistudio.google.com/apikey).

## 6. Cài đặt và chạy trên Windows

Chạy các lệnh từ thư mục gốc repository để ứng dụng đọc đúng `.env` và theme ở `.streamlit/config.toml`.

```powershell
# Chỉ tạo môi trường khi máy chưa có .venv_ai
if (-not (Test-Path .\.venv_ai\Scripts\python.exe)) {
    py -3.12 -m venv .venv_ai
}

$py = (Resolve-Path .\.venv_ai\Scripts\python.exe).Path
& $py -m pip install --upgrade pip
& $py -m pip install -r .\ai_assistant\requirements.txt
& $py -m streamlit run .\ai_assistant\app.py
```

Mã dùng cú pháp Python 3.10 trở lên; môi trường `.venv_ai` hiện tại của project được kiểm tra với Python 3.13.3. Nếu `py -3.12` không có trên máy, thay bằng launcher của một Python 3.10+ đã cài. Để kiểm tra hoặc chạy các lệnh Python của AI Companion, dùng đúng `.\.venv_ai\Scripts\python.exe`, không nhầm với `.venv` của các phần khác.

Trình duyệt mặc định mở tại <http://localhost:8501>. Để dừng, nhấn `Ctrl+C` tại cửa sổ đang chạy Streamlit.

### Theme

Theme chính được cấu hình tại [`.streamlit/config.toml`](../.streamlit/config.toml): nền sáng, Navy `#09152B`, Vàng `#C9A227`, nền trang `#F8F9FB`. Chạy lệnh Streamlit từ thư mục gốc để nhận theme này.

## 7. Quy trình sử dụng

### 7.1. Sidebar và KPI

1. Chọn tùy chọn ở Sidebar theo thứ tự Quốc gia → Năm phát hành → Thể loại; mặc định không chọn gì nghĩa là toàn bộ dữ liệu.
2. Chế độ phân bổ mặc định là Weighted. Chế độ này chỉ ảnh hưởng đến biểu đồ nhóm tài chính được phân bổ; sáu KPI Overview vẫn tính trên grain phim.
3. Tab **Tóm tắt KPI** hiển thị sáu chỉ số, Top 5 phim lợi nhuận cao nhất và bảng căn cứ. Bấm **Tạo tóm tắt** để yêu cầu AI diễn giải phạm vi hiện tại.
4. Bấm **Làm mới** ở Sidebar để xóa cache truy vấn và các phần giải thích đã lưu trong phiên.

### 7.2. Chọn biểu đồ để AI phân tích

1. Mở Tab **Giải thích xu hướng** và chọn biểu đồ theo một hoặc nhiều nhóm trang.
2. Có thể bấm **Bỏ chọn tất cả**; tối đa bốn biểu đồ được chọn mỗi lượt.
3. Có thể nhập câu hỏi trọng tâm, ví dụ: `Vì sao ROI thập niên 1910s–1920s cao bất thường?`
4. Bấm **Phân tích biểu đồ đã chọn**. AI nhận tối đa 20 dòng sạch cho mỗi biểu đồ; ứng dụng hiển thị bảng dữ liệu PostgreSQL trong **Căn cứ dữ liệu đối chiếu**.
5. Với một biểu đồ, yêu cầu AI nêu xu hướng, biến động/điểm bất thường và lưu ý dữ liệu. Với nhiều biểu đồ, yêu cầu AI nhận xét từng biểu đồ và liên hệ các mẫu quan sát được. AI không được khẳng định nhân quả tuyệt đối.

### 7.3. Hỏi đáp Text-to-SQL

1. Mở Tab **Hỏi đáp dữ liệu**, chọn một câu mẫu hoặc nhập câu hỏi bằng `st.chat_input`.
2. AI lập kế hoạch SQL có cấu trúc; ứng dụng kiểm duyệt rồi mới chạy truy vấn. Bảng kết quả thực được hiển thị cùng phần diễn giải.
3. Lịch sử hội thoại chỉ tồn tại trong phiên Streamlit hiện tại, giữ tối đa 20 lượt gần nhất; nút **Xóa đoạn này** xóa riêng lượt tương ứng.
4. Câu mẫu về năm 2026 minh họa giới hạn phạm vi: dữ liệu không bao phủ năm tương lai đó, hệ thống cần từ chối hoặc trả kết quả rỗng thay vì tự tạo số liệu.

## 8. LLM, tốc độ và dữ liệu gửi đi

- Groq dùng OpenAI-compatible SDK qua `https://api.groq.com/openai/v1`; model mặc định là `openai/gpt-oss-120b`. Gemini dùng `google-genai`; model mặc định là `gemini-2.5-flash-lite`.
- Ứng dụng giới hạn kết nối API LLM ở IPv4 cho `api.groq.com` và `generativelanguage.googleapis.com`; không thay đổi phân giải mạng của `localhost`/PostgreSQL.
- Timeout HTTP/LLM hiện là 15 giây; kết nối PostgreSQL có connect timeout 5 giây, mỗi truy vấn có `statement_timeout = 10s`.
- Tab 2 gửi tối đa 20 dòng mỗi biểu đồ. Text-to-SQL gửi tối đa 30 dòng truy vấn cho AI diễn giải; toàn bộ bảng kết quả vẫn được trả về giao diện.
- Dữ liệu/kết quả được gửi tới nhà cung cấp LLM đã chọn khi người dùng yêu cầu tóm tắt, phân tích hoặc hỏi đáp. Không dùng với dữ liệu bí mật hoặc thông tin cá nhân; không đưa API key vào câu hỏi, log hay mã nguồn.
- Thời gian phản hồi thực tế phụ thuộc mạng, tải và hạn mức nhà cung cấp; cấu hình IPv4 tránh chờ IPv6 trên mạng không hỗ trợ nhưng không đảm bảo một mốc TTFT cố định.

## 9. An toàn và READ ONLY

Mọi truy vấn qua `db.run_query()` chạy trong một transaction PostgreSQL với `autocommit=False`, `SET TRANSACTION READ ONLY`, `SET LOCAL statement_timeout = '10s'` và `ROLLBACK` sau truy vấn. Ứng dụng không tạo bảng hoặc ghi dữ liệu.

SQL do Text-to-SQL sinh ra tiếp tục qua `validate_readonly_sql()` trước khi thực thi:

- Chỉ chấp nhận một câu bắt đầu bằng `SELECT` hoặc `WITH`; bỏ comment và dấu chấm phẩy cuối, chặn dấu chấm phẩy ở giữa.
- Chặn các lệnh ghi/thay đổi như `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `TRUNCATE`, `CREATE`, `GRANT`, `REVOKE`, `COPY`, `EXECUTE`, `CALL`, `PG_SLEEP`, cùng một số từ khóa/hàm truy cập tệp hoặc điều khiển backend.
- Chặn truy cập catalog/schema hệ thống như `pg_catalog`, `pg_roles`, `pg_shadow` và `information_schema`; yêu cầu câu lệnh tham chiếu schema `dds`.
- Nếu PostgreSQL báo lỗi khi chạy SQL do AI sinh, cho phép tự sửa tối đa một lần; truy vấn đã sửa vẫn phải qua kiểm duyệt. Yêu cầu ghi/xóa dữ liệu bị chặn; ngoài phạm vi TMDB được trả lời theo trạng thái phù hợp.

Các lớp này là bảo vệ ở cấp ứng dụng và transaction; vẫn nên dùng tài khoản PostgreSQL chỉ có quyền đọc đối với schema cần thiết.

## 10. Đối chiếu thủ công

Kịch bản SQL đối chiếu của AI Companion nằm tại [`test/manual test/verify_ai_manual.sql`](../test/manual%20test/verify_ai_manual.sql). Với Docker Compose mặc định của project, chạy từ thư mục gốc:

```powershell
Get-Content '.\test\manual test\verify_ai_manual.sql' |
    docker compose exec -T postgres psql -U labuser -d warehouse
```

Nếu database/user khác cấu hình mặc định, thay các tham số `psql` tương ứng. Kịch bản gồm KPI toàn cầu, lọc đa chọn, so sánh phân bổ Genre/Company, các ngưỡng Budget/Rating và truy vấn mẫu Text-to-SQL.
Để đối chiếu riêng logic bộ lọc với Power BI, tham khảo thêm [`verify_powerbi_filters.sql`](<../test/manual test/verify_powerbi_filters.sql>).

Các mốc ghi trong kịch bản cho snapshot gốc:

| KPI toàn cầu | Giá trị tham chiếu |
|---|---:|
| Movies | 4.803 |
| Valid movies | 3.229 |
| Valid Revenue | khoảng 391,49 tỷ USD |
| Profit | khoảng 260,22 tỷ USD |
| Median ROI | 130,0% |
| Pct Over Budget | 75,5% |

Để đối chiếu với bộ lọc đơn lẻ **Year = 2014**, **Genre = Action**, **Country = United States of America**, **Full**, giá trị tham chiếu đã dùng trong project là **Valid Revenue = 13.838.380.577 USD** và **Profit = 9.874.580.577 USD**. Giá trị có thể khác nếu snapshot DDS đã thay đổi; luôn đối chiếu trên cùng nguồn và cùng bộ lọc.

## 11. Xử lý sự cố

| Hiện tượng | Kiểm tra / xử lý |
|---|---|
| Sidebar báo dữ liệu chưa sẵn sàng hoặc KPI không tải được | Kiểm tra PostgreSQL đang chạy, schema `dds` đã được dbt build, thông tin `POSTGRES_*` đúng; thử **Làm mới**. |
| Thiếu khóa LLM hoặc nút AI bị vô hiệu hóa | Kiểm tra `GROQ_API_KEY`/`GEMINI_API_KEY` trong `.env` ở thư mục gốc; khởi động lại Streamlit. |
| Groq báo 404 / model không hợp lệ | Kiểm tra model được API key hiện tại cho phép, đặt `GROQ_MODEL` phù hợp hoặc chọn Gemini qua `LLM_PROVIDER=gemini`. |
| Lỗi 401/403 | Kiểm tra khóa và quyền API trong `.env`; không in hoặc gửi khóa qua chat/log. |
| Lỗi 429 / quota | Kiểm tra hạn mức nhà cung cấp, chờ rồi thử lại hoặc dùng nhà cung cấp/model khác đã cấu hình. |
| Timeout / lỗi kết nối LLM | Kiểm tra Internet, firewall/proxy và quyền truy cập API. Cơ chế IPv4 chỉ xử lý hai hostname LLM được cấu hình; không khắc phục được chặn mạng toàn phần. |
| Truy vấn PostgreSQL timeout | Xem lại khả năng đáp ứng của server và bộ lọc; mỗi truy vấn bị giới hạn 10 giây. |
| `ModuleNotFoundError` | Dùng đúng `.venv_ai`, cài lại `.\ai_assistant\requirements.txt` bằng interpreter trong môi trường đó. |
| Theme không được áp dụng | Chạy Streamlit từ repository root để Streamlit nhận `.\.streamlit\config.toml`. |

## 12. Tài liệu liên quan

- [README tổng dự án](../README.md) — khởi chạy PostgreSQL, Mage, dbt và Power BI.
- [README dbt](../dbt_transform/README.md) — DDS, Data Contract và quy trình build.
- [README Power BI](../powerbi_dashboard/README.md) — Semantic Model, định nghĩa chỉ số và Refresh.
- [SQL đối chiếu AI Companion](<../test/manual test/verify_ai_manual.sql>) — truy vấn tham chiếu cho các tính năng AI.

