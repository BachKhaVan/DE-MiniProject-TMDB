"""Keep required but unimplemented AI visible in overall coverage."""
import pytest
from core import register,blocked

REQUIREMENTS={
 'AI01':'Tích hợp LLM hoặc dịch vụ Generative AI',
 'AI02':'Tự động tạo summary từ KPI và ngữ cảnh lọc',
 'AI03':'Giải thích xu hướng/biến động bằng số liệu',
 'AI04':'Kiểm chứng số liệu và hạn chế suy diễn không có căn cứ',
}
for key,title in REQUIREMENTS.items():
    register(key,'3.5',title,'Có implementation và bằng chứng thực thi AI dựa trên KPI',
        input_data='Đề mục 3.5; báo cáo tổng hợp mục 2.6 và 4.1 (chưa triển khai)',
        fix='Triển khai AI, lưu input KPI/filter, prompt/model/output rồi bổ sung adapter kiểm thử runtime')

@pytest.mark.m35
@pytest.mark.parametrize('case_id',list(REQUIREMENTS))
def test_ai_requirement_gap(case_id):
    blocked('Chưa triển khai AI theo báo cáo; chưa có adapter/runtime evidence. Đây là khoảng trống yêu cầu, không phải đã đạt.')
