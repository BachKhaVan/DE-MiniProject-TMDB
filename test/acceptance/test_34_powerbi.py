"""3.4: parse embedded PBIR JSON and explicitly block unobservable semantic UI checks."""
import json,re,zipfile
from pathlib import Path
import pytest
from core import ROOT,register,record,blocked

DESCRIPTIONS={
 'PB01':('PBIX là file có thể đọc được','PBIX zip hợp lệ và có report definition'),
 'PB02':('Có tối thiểu hai trang Dashboard','Ít nhất 2 trang theo đề; ghi nhận 4 trang là trạng thái báo cáo'),
 'PB03':('Mỗi trang có ít nhất một biểu đồ','Số visual JSON > 0 trên từng trang'),
 'PB04':('Report có tham chiếu measure DAX','Visual query sử dụng measure references, không chứng minh đúng công thức'),
 'PB05':('Overview có các KPI chính','Dấu vết các measure KPI trong visual metadata'),
 'PB06':('Dashboard có khả năng đặt bộ lọc/slicer','Có visualType slicer trong metadata PBIR'),
 'PB07':('Drill-down thời gian hoạt động','Dùng giao diện Power BI Desktop để mở và thao tác drill-down'),
 'PB08':('Relationships đúng cardinality và cross-filter','Truy vấn semantic model hoặc TMDL; DataModel nén không thể xác minh tĩnh'),
 'PB09':('DAX measures tính đúng với SQL','Phải đọc DAX expression và cùng filter-context rồi mới kết luận'),
 'PB10':('Top N được sort theo measure hiển thị','Cần truy vấn/mở visual và xem sortBy hay ranking filter'),
 'PB11':('Ngưỡng Min Movies, Min Votes dùng đúng measure','Kiểm tra khi đổi các tham số trong Desktop và truy vấn SQL'),
 'PB12':('Refresh Import thành công và khớp DDS','Cần refresh thật, thời điểm refresh, các KPI sau refresh'),
 'PB13':('Allocation Weighted và Full đổi thứ hạng','Cần quan sát report + đối chiếu SQL cùng snapshot'),
 'PB14':('Country=USA, Year=2014, Genre=Action','Cần cùng filter context tại Desktop và số liệu SQL độc lập'),
}
for id,(title,exp) in DESCRIPTIONS.items():
 register(id,'3.4',title,exp,category='Quy tắc project' if id in ('PB13','PB14') else 'Yêu cầu bắt buộc',
 evidence='Phát hiện tĩnh trong PBIX' if int(id[2:])<=6 else 'Kết quả chạy mới',
 demo=id in ('PB02','PB07','PB12','PB14'),
 fix='Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)')
for i in range(1,9):
 register(f'Q{i}','3.4',f'Câu hỏi nghiệp vụ Q{i}','Có visual/measure trả lời đủ các vế + SQL cùng snapshot + ảnh xác minh',
 category='Quy tắc project',demo=True,fix=f'Chụp visual trang liên quan đến Q{i}; đối chiếu giá trị SQL với đúng filters')

PBI=ROOT/'powerbi_dashboard/TMDB_Movie_Dashboard.pbix'

def load_pbir():
    if not PBI.exists():blocked('Thiếu PBIX từ project')
    try:
        with zipfile.ZipFile(PBI) as z:
            names=set(z.namelist())
            root='Report/definition/pages/'
            if root+'pages.json' not in names: blocked('PBIX không chứa PBIR JSON; không có extractor DataModel phù hợp')
            order=json.loads(z.read(root+'pages.json'))['pageOrder']
            pages=[]
            for uid in order:
                page=json.loads(z.read(root+uid+'/page.json'))
                prefix=root+uid+'/visuals/'
                visuals=[json.loads(z.read(n)) for n in sorted(names) if n.startswith(prefix) and n.endswith('/visual.json')]
                pages.append({'uid':uid,'name':page.get('displayName',''),'visuals':visuals})
            return pages
    except zipfile.BadZipFile as e:pytest.fail('PBIX archive lỗi')

def walk_measure_refs(node,result):
    if isinstance(node,dict):
        if 'Measure' in node and isinstance(node['Measure'],dict):
            p=node['Measure'].get('Property')
            if p:result.add(p)
        for v in node.values():walk_measure_refs(v,result)
    elif isinstance(node,list):
        for v in node:walk_measure_refs(v,result)

@pytest.mark.m34
@pytest.mark.readonly
@pytest.mark.parametrize('case_id',list(DESCRIPTIONS)+[f'Q{i}' for i in range(1,9)],ids=lambda x:x)
def test_powerbi_metadata_and_manual(case_id,request):
    if case_id not in ('PB01','PB02','PB03','PB04','PB05','PB06'):
        blocked('Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import')
    pages=load_pbir()
    if case_id=='PB01':
        record(request,{'zip_readable':True,'has_pbir':True,'page_count':len(pages)})
    elif case_id=='PB02':
        record(request,{'page_count':len(pages),'names':[p['name'] for p in pages]})
        assert len(pages)>=2,f'Đếm thực tế {len(pages)} trang'
    elif case_id=='PB03':
        decorative={'slicer','textbox','shape','image','actionButton','pageNavigator','bookmarkNavigator'}
        found={p['name']:sum(v.get('visual',{}).get('visualType') not in decorative
                            and bool(v.get('visual',{}).get('visualType')) for v in p['visuals']) for p in pages}
        record(request,found)
        assert found and all(n>0 for n in found.values())
    elif case_id=='PB04':
        measures=set()
        for p in pages:
            for v in p['visuals']:walk_measure_refs(v,measures)
        record(request,{'measure_references_count':len(measures),'measure_references':sorted(measures)[:100]},note='Chỉ thấy tên measures trong visuals; không đọc được DAX expressions trong compressed DataModel')
        assert measures
    elif case_id=='PB05':
        first=pages[0]['visuals'] if pages else []
        measures=set()
        for v in first:walk_measure_refs(v,measures)
        requested={'Movie Count','Valid Movies','Total Revenue','Total Profit','ROI Median','Pct Over Budget'}
        matches=sorted(m for m in measures if any(x in m.lower() for x in ('movie','profit','roi','revenue','budget')))
        record(request,{'overview_name':pages[0]['name'],'matching_measures':matches,'all_measures':sorted(measures)})
        assert requested.issubset(measures),'Thiếu measure KPI Overview: '+str(sorted(requested-measures))
    else:
        slicers={p['name']:sum(v.get('visual',{}).get('visualType')=='slicer' for v in p['visuals']) for p in pages}
        record(request,slicers)
        assert any(n>0 for n in slicers.values()),'Không thấy slicer nào được khai báo trong report'
