"""Compare six exported DAX KPIs against BI01/BI02 SQL evidence; no rounding of input."""
import argparse,csv,datetime,decimal,json,sys
from pathlib import Path

TOLERANCE={'movies':'0','valid_movies':'0','valid_revenue':'0.01','total_profit':'0.01',
           'roi_median':'0.000001','pct_over_budget':'0.000001'}


def compare(expected,actual):
    results=[]
    for name,tolerance in TOLERANCE.items():
        if name not in expected or name not in actual:
            results.append({'metric':name,'status':'FAIL','reason':'Missing column'});continue
        left,right=expected[name],actual[name]
        if left is None and (right is None or str(right).strip()==''):
            results.append({'metric':name,'status':'PASS','sql':None,'dax':None});continue
        try:
            a=decimal.Decimal(str(left));b=decimal.Decimal(str(right))
            if not a.is_finite() or not b.is_finite():raise ValueError('Non-finite value')
            difference=abs(a-b)
            ok=difference<=decimal.Decimal(tolerance)
            results.append({'metric':name,'status':'PASS' if ok else 'FAIL','sql':str(a),'dax':str(b),
                            'absolute_difference':str(difference),'tolerance':tolerance})
        except (decimal.InvalidOperation,ValueError):
            results.append({'metric':name,'status':'FAIL','reason':'Use raw numeric values: no %, currency, thousands separators or K/M/bn'})
    return results


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--reference',required=True,type=Path,help='queries/BI01.json or BI02.json from run.py')
    ap.add_argument('--actual',required=True,type=Path,help='CSV exported from DAX query view with six named columns')
    ap.add_argument('--confirm-same-snapshot',action='store_true')
    args=ap.parse_args()
    if not args.confirm_same_snapshot:
        print('BLOCKED: refresh PBIX, match filters, stop data changes, then use --confirm-same-snapshot');return 2
    try:
        reference=json.loads(args.reference.read_text(encoding='utf8'))
        if reference.get('id') not in ('BI01','BI02') or len(reference.get('rows',[]))!=1:
            raise ValueError('Reference must be one-row BI01/BI02 evidence')
        with args.actual.open(encoding='utf-8-sig',newline='') as handle:
            rows=list(csv.DictReader(handle))
        if len(rows)!=1:raise ValueError('DAX CSV must have exactly one data row')
        row={key.strip().strip('[]'):value for key,value in rows[0].items()}
        checks=compare(reference['rows'][0],row)
    except (OSError,ValueError,TypeError) as exc:
        print('BLOCKED:',str(exc));return 2
    result={'reference':str(args.reference.resolve()),'actual':str(args.actual.resolve()),
            'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,
            'scope':'Six numeric KPIs only. Snapshot/filter/refresh confirmation supplied by user; not UI or all DAX validation.'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if any(item['status']=='FAIL' for item in checks) else 0

if __name__=='__main__':raise SystemExit(main())
