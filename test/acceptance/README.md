# TMDB acceptance tests

Hướng dẫn chính: [HUONG_DAN_CHAY_TEST.md](../HUONG_DAN_CHAY_TEST.md).

Đối chiếu đề 2627.Yêu cầu_unlocked.pdf và báo cáo tổng hợp TMDB 88 trang. Bao phủ kiểm tra tự động 3.1–3.4 và ghi rõ khoảng trống AI 3.5. [MATRIX.md](MATRIX.md) liệt kê case và loại bằng chứng.

```powershell
.\.venv\Scripts\python.exe test/acceptance/preflight.py --mode readonly --env-file .env
.\.venv\Scripts\python.exe test/acceptance/run.py --mode readonly --section all --env-file .env
```

Section: 31, 32, 33, 34, 35, all. Thêm --snapshot full chỉ khi stage vừa Full Load, chưa append. Integration dùng DB test 55432, Mage test 16789 và --approved; đọc hướng dẫn chính trước khi chạy.

Mỗi lượt tạo REPORT.md/result.json/JUnit/log dưới test/results. PASS/FAIL/BLOCKED/SKIPPED/INFO được tách riêng. INFO không phải nghiệm thu đạt. SQL tham chiếu không thay DAX; compare_powerbi.py so 6 KPI từ CSV DAX khi cùng snapshot/filter.

Kiểm tra hồi quy harness:

```powershell
.\.venv\Scripts\python.exe -m pytest -c test/acceptance/pytest.ini test/unit -q
```

Trạng thái và liên kết các report integration gần nhất: [README tổng](../../README.md). Dùng cùng venv đã cài dependencies; nếu dùng `.venv_test` thì thay đường dẫn Python tương ứng. FAIL còn lại của source, thiếu AI và thiếu evidence Desktop phải được ghi nhận trung thực.
