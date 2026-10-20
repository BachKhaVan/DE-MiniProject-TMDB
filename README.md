# TMDB 5000 Movie Data Warehouse & BI Analytics System

Dự án xây dựng hệ thống Kho dữ liệu (Data Warehouse), đường ống xử lý dữ liệu (ELT Pipeline), Báo cáo thông minh (BI Dashboard) và Trợ lý phân tích AI (Generative AI) cho bộ dữ liệu **TMDB 5000 Movie Dataset**.

## 1. Kiến trúc Kỹ thuật (Technical Stack)

Hệ thống được thiết kế theo mô hình **Modern Data Stack** kết hợp kiến trúc 3 tầng (**Source → Staging → DDS / Star Schema**):

| Tầng xử lý | Công cụ | Vai trò trong dự án |
| :--- | :--- | :--- |
| **Data Sources** | CSV / Kaggle | 2 tệp dữ liệu chính từ Kaggle: `tmdb_5000_movies.csv` và `tmdb_5000_credits.csv` (~4.800 bộ phim). |
| **Data Ingestion & Orchestration** | **Mage.ai** | Điều phối luồng đọc dữ liệu thô từ CSV, kiểm tra chất lượng ban đầu, nạp Full Load / Incremental Load vào PostgreSQL Staging và ghi log thực thi. |
| **Staging Database** | **PostgreSQL** | Lưu trữ dữ liệu bảng tạm ở schema `stage` (`stg_tmdb_movies`, `stg_tmdb_credits`) và bảng ghi nhận trạng thái điều phối ở schema `control`. |
| **Data Transformation & Testing** | **dbt (`dbt-postgres`)** | Kết nối PostgreSQL Staging, chuẩn hóa dữ liệu (đổi 0 thành NULL), bóc tách mảng JSON phức tạp, tính trọng số `WeightFactor`, sinh Surrogate Key, xây dựng Dimension/Bridge/Fact và chạy `dbt test`. |
| **Data Warehouse (DDS & OLAP)** | **PostgreSQL** | Lưu trữ mô hình **Star Schema** mở rộng tại schema `dds` gồm `FactMovie`, 3 bảng Dim đơn trị, 4 bảng Dim đa trị và 4 bảng Bridge xử lý quan hệ nhiều - nhiều. |
| **BI & Visualization** | **Power BI (`.pbip` / `.pbix`)** | Thiết lập Semantic Model, định nghĩa các chỉ số đo lường bằng DAX (`Profit`, `ROI`, `AvgRating`,...) và trực quan hóa 02 trang Dashboard (Overview & Diagnostic). |
| **Generative AI** | **LLM / API** | Tự động tổng hợp bản tóm tắt KPI (AI Summary), diễn giải xu hướng/biến động tài chính và giải đáp câu hỏi tự nhiên dựa trên dữ liệu đã tính toán. |

---

## 2. Cấu trúc Cây Thư mục

```text
DE-MiniProject-TMDB/
├── README.md                                        # Tài liệu hướng dẫn quy trình làm việc và sử dụng Git
├── compose.yaml                                     # Khởi chạy Docker chứa Mage.ai + PostgreSQL 17
├── Dockerfile                                       # Docker Image cấu hình Mage.ai tích hợp dbt-postgres
├── .env                                             # [Git Ignore] Biến môi trường mật khẩu & kết nối
├── .gitignore                                       # Chặn file cấu hình bảo mật và file dữ liệu thô
├── io_config.yaml                                   # [Git Ignore] Cấu hình profile kết nối Postgres cho Mage.ai
├── profiles.yml                                     # [Git Ignore] Cấu hình profile kết nối Postgres cho dbt
│
├── data/                                            # Quản lý dữ liệu nguồn
│   └── raw/                                         # [Git Ignore] File tmdb_5000_movies.csv & credits.csv tại máy cá nhân
│
├── postgres/                                        # [Người 1 - Khoa] DDL SQL khởi tạo các Schema
│   └── init/                                        # File 01_init.sql tạo schema stage, dds, control
│
├── mage_pipeline/                                   # [Người 1 - Khoa & Người 4 - Vân] Pipeline Ingestion & Orchestration
│   ├── pipelines/                                   # Flow điều phối công việc
│   ├── data_loaders/                                # Block đọc file CSV nguồn
│   ├── transformers/                                # Block lọc dữ liệu incremental & chuẩn hóa
│   └── data_exporters/                              # Block nạp dữ liệu vào Postgres Staging
│
├── dbt_transform/                                   # [Tuấn, Thịnh, Vân] Transformation & Data Quality Tests
│   ├── dbt_project.yml
│   ├── packages.yml
│   ├── seeds/                                       # [Người 3 - Thịnh] Seed file ánh xạ ThemeGroup cho Keyword
│   ├── models/
│   │   ├── staging/                                 # [Người 2 - Tuấn] Staging views đổi 0 thành NULL & làm sạch
│   │   ├── dimensions/                              # [Người 2 - Tuấn] DimDate, DimMovie, DimLanguage
│   │   ├── bridge/                                  # [Người 3 - Thịnh] DimGenre, DimCompany, DimCountry, DimKeyword & 4 Bridge tables
│   │   └── facts/                                   # [Người 4 - Vân] FactMovie & các chỉ số đo lường
│   └── tests/                                       # [Người 4 - Vân] Bộ kiểm thử chất lượng dữ liệu (dbt tests)
│
├── powerbi_dashboard/                               # [Cả nhóm] File Power BI Project (.pbip/.pbix) & công thức DAX
└── docs/                                            # Tài liệu sơ đồ thiết kế, kiểm thử và báo cáo đồ án
    ├── diagrams/                                    # Sơ đồ ERD, Star Schema, Lineage DAG Diagram
    └── reports/                                     # Báo cáo PDF cá nhân và tổng hợp dự án
```

---

## 3. Phân công Nhiệm vụ & Vùng Làm việc trên Git

Để tránh xung đột khi gộp nhánh (Merge Conflict), mỗi thành viên chỉ chỉnh sửa trực tiếp các thư mục thuộc phạm vi phụ trách của mình:

| Thành viên | Vai trò chính | Nhánh làm việc (`Feature Branch`) | Thư mục phụ trách chính | Người Review & Chạy thử chéo |
| :--- | :--- | :--- | :--- | :--- |
| **Người 1 (Khoa)** | **Data Ingestion & Staging** (Source CSV → Postgres Stage; Mage Pipeline & Control Logs) | `feat/ingestion-khoa` | `mage_pipeline/`, `postgres/init/`, `docs/reports/` | **Tuấn** |
| **Người 2 (Tuấn)** | **Single-value Dimensions** (Staging → DimDate, DimMovie, DimLanguage; Ép kiểu & Surrogate Key) | `feat/dim-tuan` | `dbt_transform/models/staging/`, `dbt_transform/models/dimensions/` | **Thịnh** |
| **Người 3 (Thịnh)** | **JSON Parsing & Bridge Tables** (Bóc tách chuỗi JSON → Dim & Bridge Genre, Company, Country, Keyword) | `feat/bridge-thinh` | `dbt_transform/models/bridge/`, `dbt_transform/seeds/` | **Vân** |
| **Người 4 (Vân)** | **Fact, Testing, BI & AI** (Xây dựng `FactMovie`, dbt tests, Power BI Dashboard, tích hợp GenAI & Báo cáo) | `feat/fact-van` | `dbt_transform/models/facts/`, `dbt_transform/tests/`, `powerbi_dashboard/`, `docs/` | **Khoa** |

---

## 4. Hướng dẫn Khởi chạy Nhanh (Local Setup)

### Bước 1: Chuẩn bị môi trường & Dữ liệu
1. Sao chép và tạo các file cấu hình môi trường cục bộ từ mẫu:
   ```bash
   cp .env.example .env
   ```
2. Tải tệp `tmdb_5000_movies.csv` và `tmdb_5000_credits.csv` từ Kaggle đặt vào thư mục `data/raw/` (thư mục này đã bị `.gitignore` chặn nên không lo push nhầm lên Git).

### Bước 2: Khởi động PostgreSQL và Mage.ai bằng Docker
Chạy lệnh khởi động các container dịch vụ:
```bash
docker compose up -d
```
* Giao diện **Mage.ai**: Truy cập tại `http://localhost:6789`
* CSDL **PostgreSQL**: Kết nối qua `localhost:5432` (Database: `warehouse`, User: `labuser`)

### Bước 3: Chạy Pipeline Ingestion & dbt Transformations
1. Truy cập giao diện Mage.ai, chạy pipeline `tmdb_ingestion` để đọc CSV và nạp vào schema `stage`.
2. Chuyển vào thư mục `dbt_transform` (hoặc mở Terminal bên trong container Mage) để chạy chuyển đổi dữ liệu:
```bash
cd dbt_transform
dbt deps                              # Cài đặt gói mở rộng dbt_utils
dbt seed                              # Nạp bảng danh mục tĩnh ánh xạ Keyword -> ThemeGroup
dbt run --select staging              # Tạo các staging views chuẩn hóa dữ liệu
dbt run --select dimensions           # Tạo các bảng Dimension đơn trị (DimDate, DimMovie, DimLanguage)
dbt run --select bridge               # Bóc tách JSON, tạo các bảng Dim đa trị và Bridge tables
dbt run --select facts                # Tạo bảng FactMovie
dbt test                              # Chạy toàn bộ bộ kiểm thử chất lượng dữ liệu
dbt docs generate                     # Sinh tài liệu và sơ đồ phụ thuộc Lineage DAG
```

---

## 5. Quy trình Làm việc với Git (Git Workflow)

Nhóm sử dụng mô hình **3 tầng nhánh** để đảm bảo nhánh nộp bài luôn chạy ổn định:
* **`main`**: Nhánh chính thức, chỉ chứa code đã kiểm thử hoàn chỉnh để đóng gói nộp bài. Không ai được push trực tiếp lên `main`.
* **`develop`**: Nhánh tích hợp chung của cả 4 thành viên. Khi hoàn thành một phần việc, thành viên tạo Pull Request (PR) gộp vào `develop`.
* **`feat/<ten-phan-viec>-<ten-thanh-vien>`**: Nhánh làm việc cá nhân của từng người (ví dụ: `feat/ingestion-khoa`, `feat/dim-tuan`, `feat/bridge-thinh`, `feat/fact-van`).

### Các bước thao tác Git hàng ngày

#### 1. Lần đầu tiên lấy dự án về máy
```bash
git clone https://github.com/BachKhaVan/DE-MiniProject-TMDB.git
cd DE-MiniProject-TMDB
git checkout develop
git checkout -b feat/ingestion-khoa        # Thay bằng tên nhánh cá nhân của bạn
```

#### 2. Trước khi bắt đầu code mỗi ngày (Cập nhật code mới nhất từ nhóm)
Luôn kéo code mới nhất từ nhánh `develop` về nhánh cá nhân trước khi làm việc để tránh lệch cấu trúc bảng:
```bash
git checkout develop
git pull origin develop
git checkout feat/ingestion-khoa           # Quay lại nhánh cá nhân
git merge develop                          # Gộp cập nhật mới nhất từ develop vào nhánh của mình
```

#### 3. Khi code xong một tính năng / script và muốn lưu lên Git
```bash
# 1. Kiểm tra những file nào vừa bị thay đổi (đảm bảo không dính file dữ liệu nặng hay mật khẩu)
git status

# 2. Đưa các file cần lưu vào vùng chờ (Staging Area)
git add <duong-dan-thu-muc-cua-ban>
# Ví dụ: git add dbt_transform/models/dimensions/

# 3. Tạo commit với nội dung rõ ràng theo chuẩn quy ước của nhóm
git commit -m "feat(dim): implement dim_movie with runtime_band and budget_band"

# 4. Đẩy code từ máy cá nhân lên GitHub
git push origin feat/ingestion-khoa
```

#### 4. Tạo Pull Request (PR) để ghép code vào `develop`
1. Lên trang GitHub của nhóm, bấm **Compare & pull request** từ nhánh cá nhân (`feat/...`) vào nhánh **`develop`**.
2. Điền ngắn gọn trong phần mô tả PR:
   * **Input nhận vào**: (ví dụ: bảng `stg_tmdb_movies` từ PostgreSQL Stage).
   * **Output tạo ra**: (ví dụ: bảng `dim_movie`, `dim_date` trong schema `dds`).
   * **Cách chạy thử**: (ví dụ: `dbt run --select dim_movie`).
3. Gắn thẻ (**Assign Reviewer**) thành viên phụ trách kiểm thử chéo theo bảng phân công ở Mục 3 để duyệt và nhấn **Merge pull request**.

---

## 6. Quy ước Đặt tên Commit (Commit Message Convention)

Toàn bộ thành viên thống nhất cấu trúc commit như sau để lịch sử Git sạch đẹp, dễ tra cứu:

```text
<loại_thay_đổi>(<phạm_vi>): <mô_tả_ngắn_gọn_việc_đã_làm>
```

### Danh sách `<loại_thay_đổi>` (Type)
* **`feat`**: Thêm mới bảng, pipeline Mage, model dbt, chỉ số DAX hoặc biểu đồ Power BI.
* **`fix`**: Sửa lỗi kiểu dữ liệu, lỗi parse JSON, lỗi khóa ngoại hoặc lỗi logic tính toán.
* **`test`**: Thêm hoặc cập nhật dbt test, schema test (`.yml`) hoặc singular test (`.sql`).
* **`docs`**: Cập nhật tài liệu mapping, sơ đồ ERD, báo cáo cá nhân hoặc `README.md`.
* **`chore`**: Cập nhật file cấu hình `compose.yaml`, `.gitignore`, `profiles.yml` hoặc `dbt_project.yml`.
* **`refactor`**: Tối ưu lại câu truy vấn SQL/dbt cho chạy nhanh hơn mà không làm đổi kết quả.

### Danh sách `<phạm_vi>` (Scope) theo từng phần việc
* **`staging`** hoặc **`mage`**: Phần nạp dữ liệu nguồn và tạo PostgreSQL Stage (Khoa).
* **`dim`**: Phần các bảng Dimension đơn trị (Tuấn).
* **`bridge`**: Phần parse JSON, tạo Dim đa trị và Bridge tables (Thịnh).
* **`fact`**: Phần bảng `FactMovie` và các đo lường tài chính (Vân).
* **`test`**: Phần kiểm thử chất lượng dữ liệu và ràng buộc mối quan hệ (Vân).
* **`pbi`**: Phần mô hình DAX, Semantic Model và Power BI Dashboard (Cả nhóm).
* **`genai`**: Phần tích hợp mô hình AI tóm tắt & diễn giải insight (Vân).
* **`report`**: Phần tổng hợp báo cáo đồ án PDF (Cả nhóm).

### Ví dụ Commit chuẩn cho từng thành viên
* **Người 1 (Khoa)**:
  * `feat(staging): create postgres init DDL for stage, dds, control schemas`
  * `feat(mage): build csv data loader and postgres exporter blocks`
  * `docs(report): add data ingestion architecture section`
* **Người 2 (Tuấn)**:
  * `feat(dim): build stg_tmdb_movies model converting 0 budget to null`
  * `feat(dim): implement dim_date and dim_language models with surrogate keys`
  * `fix(dim): handle missing release_date with unknown surrogate key -1`
* **Người 3 (Thịnh)**:
  * `feat(bridge): parse json string for genres and create bridge_movie_genre`
  * `feat(bridge): calculate weight_factor for multi-valued dimensions`
  * `feat(bridge): add seed file mapping keywords to theme_groups`
* **Người 4 (Vân)**:
  * `feat(fact): construct fact_movie model with profit and roi measures`
  * `test(fact): add primary key and foreign key relationship dbt tests`
  * `feat(pbi): design overview dashboard page with descriptive analytics`
  * `feat(genai): integrate llm summary generator for dashboard kpis`

---

## 7. Năm Nguyên tắc Khi Dùng Git Trong Nhóm

1. **Tuyệt đối không commit dữ liệu thô (`data/raw/`) và file chứa mật khẩu (`.env`, `profiles.yml`, `io_config.yaml`)**: Trước khi gõ `git commit`, luôn chạy `git status` để chắc chắn không dính file `.csv` nặng hay file cấu hình tài khoản.
2. **Không dùng `git add .` một cách mù quáng**: Hãy dùng `git status` rồi `git add <đường_dẫn_thư_mục_của_bạn>` để tránh vô tình đẩy các file cấu hình tạm trên máy cá nhân lên kho chung.
3. **Kiểm tra kỹ chỉ số `WeightFactor` trên các bảng Bridge**: Khi tổng hợp chỉ số tài chính (`Revenue`, `Profit`) qua chiều đa trị (Thể loại, Hãng sản xuất, Quốc gia), phải nhân với `WeightFactor` để tránh nhân đôi/nhân ba doanh thu thực tế của bộ phim.
4. **Ghi rõ điều kiện lọc dữ liệu trong tài liệu & commit**: Khi xử lý lọc dữ liệu tài chính chưa hợp lệ (`budget = 0` hoặc `revenue = 0`), cần ghi rõ điều kiện trong file model và báo cáo để số liệu kiểm thử khớp 100%.
5. **Không bao giờ dùng `git push --force` lên nhánh `develop` hoặc `main`**: Mọi xung đột (Conflict) phải được xử lý tại nhánh cá nhân bằng cách `git merge develop` và trao đổi trực tiếp với thành viên liên quan.

---
