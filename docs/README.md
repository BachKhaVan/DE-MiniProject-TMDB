# Tài liệu bàn giao TMDB — Nhóm 5

Điểm bắt đầu và trạng thái triển khai: [README tổng](../README.md).

| Tài liệu | Đường dẫn | Vai trò |
|---|---|---|
| Dashboard PDF | [TMDB_Movie_Dashboard.pdf](diagrams/TMDB_Movie_Dashboard.pdf) | Bản xem tĩnh, không thay PBIX tương tác |
| Phụ lục C | [60 DAX](reports/Phu_luc_C_60_DAX.pdf) | Tài liệu công thức DAX |
| Phụ lục D | [Kiểm chứng PostgreSQL–Power BI](reports/Phu_luc_D_Kiem_chung_PostgreSQL_PowerBI.pdf) | Bằng chứng đối chiếu đã biên soạn |
| Data Contract | [Schema_Report.md](../Schema_Report.md) | Thiết kế mô hình |
| Kiểm chứng DW | [DW_Verification_Report.md](../DW_Verification_Report.md) | Kết quả đã ghi nhận, cần đọc đúng snapshot |
| Hướng dẫn chạy tổng | [HUONG_DAN_CHAY_TONG_QUAT.md](../HUONG_DAN_CHAY_TONG_QUAT.md) | Thứ tự chạy Docker, Mage, dbt, Power BI và test |
| Hướng dẫn test | [HUONG_DAN_CHAY_TEST.md](../test/HUONG_DAN_CHAY_TEST.md) | Quy trình tái chạy và lưu bằng chứng |
| Kịch bản video | [VIDEO_DEMO.md](../test/acceptance/VIDEO_DEMO.md) | Nội dung quay demo |

**Báo cáo tổng hợp bản nộp:** [BaoCao_TongHop_TMDB_Nhom5.pdf](reports/BaoCao_TongHop_TMDB_Nhom5.pdf). Thứ tự đọc và vai trò từng thư mục: [Hướng dẫn đọc tài liệu](../HUONG_DAN_DOC_TAI_LIEU.md).

**Video demo:** [Thư mục video demo trên Google Drive](https://drive.google.com/drive/folders/1x6fNNB01GWwsOE6fa5XxfcngMb8h902G?usp=sharing). Liên kết cũng được ghi tại mục 1 của [README tổng](../README.md).

Trước khi nộp, đối chiếu phiên bản báo cáo/PBIX/phụ lục với nguồn dữ liệu và report kiểm thử đã chọn. PDF dashboard không chứng minh Refresh hoặc tương tác. Không thay số liệu bằng baseline nếu nguồn hiện tại khác snapshot của tài liệu.
