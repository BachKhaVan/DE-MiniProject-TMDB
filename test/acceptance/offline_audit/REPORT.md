# TMDB — Acceptance test report

- Run ID: `20261115T144515Z_ac7308`
- UTC: `2026-11-15T14:45:18.085155+00:00`
- Mode: **readonly**; Section: **all**
- Branch/commit: `n/a` / `n/a`; dirty=None
- **PASS 22 / FAIL 4 / BLOCKED 100 / SKIPPED 13**

## Bảng toàn bộ test (requirement → evidence → kết luận)

| Test ID | Mục | Loại | Tên | Kết quả | Bằng chứng |
|---|---|---|---|---|---|
| MG01 | 3.1 | Yêu cầu bắt buộc | test_csv_headers[MG01] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG02 | 3.1 | Yêu cầu bắt buộc | test_csv_headers[MG02] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG03 | 3.1 | Yêu cầu bắt buộc | test_csv_headers[MG03] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG04 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG04] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG05 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG05] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG06 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG06] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG07 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG07] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG08 | 3.1 | Kiểm tra độ bền | test_source_profiles[MG08] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG09 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG09] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG10 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG10] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG11 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG11] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG12 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG12] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG13 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG13] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG14 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG14] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG15 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG15] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG16 | 3.1 | Yêu cầu bắt buộc | test_mage_implementation[MG16] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG17 | 3.1 | Yêu cầu bắt buộc | test_pipeline_risks[MG17] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| MG18 | 3.1 | Kiểm tra độ bền | test_pipeline_risks[MG18] | **FAIL** | `junit.xml; pytest_output.txt` |
| MG19 | 3.1 | Kiểm tra độ bền | test_pipeline_risks[MG19] | **FAIL** | `junit.xml; pytest_output.txt` |
| MG20 | 3.1 | Kiểm tra độ bền | test_pipeline_risks[MG20] | **FAIL** | `junit.xml; pytest_output.txt` |
| MG21 | 3.1 | Yêu cầu bắt buộc | test_mage_stage[MG21] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG22 | 3.1 | Yêu cầu bắt buộc | test_mage_stage[MG22] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG23 | 3.1 | Yêu cầu bắt buộc | test_mage_stage[MG23] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MG24 | 3.1 | Kiểm tra độ bền | test_mage_stage[MG24] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| MI01 | 3.1 | Yêu cầu bắt buộc | test_real_pipeline_scenarios[MI01] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| MI02 | 3.1 | Yêu cầu bắt buộc | test_real_pipeline_scenarios[MI02] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| MI03 | 3.1 | Yêu cầu bắt buộc | test_real_pipeline_scenarios[MI03] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| MI04 | 3.1 | Kiểm tra độ bền | test_real_pipeline_scenarios[MI04] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| MI05 | 3.1 | Kiểm tra độ bền | test_real_pipeline_scenarios[MI05] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| MI06 | 3.1 | Kiểm tra độ bền | test_real_pipeline_scenarios[MI06] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| MI07 | 3.1 | Kiểm tra độ bền | test_real_pipeline_scenarios[MI07] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| MI08 | 3.1 | Yêu cầu bắt buộc | test_real_pipeline_scenarios[MI08] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| DB01 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB01] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB02 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB02] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB03 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB03] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB04 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB04] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB05 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB05] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB06 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB06] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB07 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB07] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)` |
| DB08 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB08] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DB09 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB09] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DB10 | 3.2 | Yêu cầu bắt buộc | test_dbt_structure[DB10] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DB11 | 3.2 | Kiểm tra độ bền | test_dbt_structure[DB11] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DB12 | 3.2 | Kiểm tra độ bền | test_dbt_structure[DB12] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DB13 | 3.2 | Kiểm tra độ bền | test_dbt_structure[DB13] | **FAIL** | `junit.xml; pytest_output.txt` |
| DW32 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW32] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW33 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW33] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW34 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW34] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW35 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW35] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW36 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW36] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW37 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW37] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW38 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW38] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW41 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW41] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW42 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW42] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW43 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW43] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW44 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW44] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW45 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW45] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW46 | 3.2 | Yêu cầu bắt buộc | test_transformation_invariant[DW46] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| NC01 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC01] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| NC02 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC02] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| NC03 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC03] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| NC04 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC04] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| NC05 | 3.3 | Kiểm tra độ bền | test_negative_controls[NC05] | **SKIPPED** | `junit.xml; pytest_output.txt` |
| DW01 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW01] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW02 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW02] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW03 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW03] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW04 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW04] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW05 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW05] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW06 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW06] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW07 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW07] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW08 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW08] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW09 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW09] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW10 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW10] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW11 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW11] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW12 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW12] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW13 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW13] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW14 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW14] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW15 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW15] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW16 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW16] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW17 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW17] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW18 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW18] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW19 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW19] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW20 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW20] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW21 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW21] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW22 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW22] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW23 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW23] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW24 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW24] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW25 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW25] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW26 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW26] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW27 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW27] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW28 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW28] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW29 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW29] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW30 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW30] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW31 | 3.3 | Kiểm tra độ bền | test_warehouse_invariant[DW31] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW39 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW39] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW40 | 3.3 | Kiểm tra độ bền | test_warehouse_invariant[DW40] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW47 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW47] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW48 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW48] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| DW49 | 3.3 | Yêu cầu bắt buộc | test_warehouse_invariant[DW49] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB01 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB01] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB02 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB02] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB03 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB03] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB04 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB04] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB05 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB05] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB06 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB06] | **PASS** | `junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)` |
| PB07 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB07] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB08 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB08] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB09 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB09] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB10 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB10] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB11 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB11] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB12 | 3.4 | Yêu cầu bắt buộc | test_powerbi_metadata_and_manual[PB12] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB13 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[PB13] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| PB14 | 3.4 | Quy tắc project | test_powerbi_metadata_and_manual[PB14] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_powerbi_metadata_and_manual[Q1] | ? | ? | test_powerbi_metadata_and_manual[Q1] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_powerbi_metadata_and_manual[Q2] | ? | ? | test_powerbi_metadata_and_manual[Q2] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_powerbi_metadata_and_manual[Q3] | ? | ? | test_powerbi_metadata_and_manual[Q3] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_powerbi_metadata_and_manual[Q4] | ? | ? | test_powerbi_metadata_and_manual[Q4] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_powerbi_metadata_and_manual[Q5] | ? | ? | test_powerbi_metadata_and_manual[Q5] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_powerbi_metadata_and_manual[Q6] | ? | ? | test_powerbi_metadata_and_manual[Q6] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_powerbi_metadata_and_manual[Q7] | ? | ? | test_powerbi_metadata_and_manual[Q7] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_powerbi_metadata_and_manual[Q8] | ? | ? | test_powerbi_metadata_and_manual[Q8] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI01 | 3.4 | Quy tắc project | test_independent_bi_sql[BI01] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI02 | 3.4 | Quy tắc project | test_independent_bi_sql[BI02] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI03 | 3.4 | Quy tắc project | test_independent_bi_sql[BI03] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI04 | 3.4 | Quy tắc project | test_independent_bi_sql[BI04] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI05 | 3.4 | Quy tắc project | test_independent_bi_sql[BI05] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI06 | 3.4 | Quy tắc project | test_independent_bi_sql[BI06] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_independent_bi_sql[Q1SQL] | ? | ? | test_independent_bi_sql[Q1SQL] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_independent_bi_sql[Q2SQL] | ? | ? | test_independent_bi_sql[Q2SQL] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_independent_bi_sql[Q3SQL] | ? | ? | test_independent_bi_sql[Q3SQL] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_independent_bi_sql[Q4SQL] | ? | ? | test_independent_bi_sql[Q4SQL] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_independent_bi_sql[Q5SQL] | ? | ? | test_independent_bi_sql[Q5SQL] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_independent_bi_sql[Q6SQL] | ? | ? | test_independent_bi_sql[Q6SQL] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_independent_bi_sql[Q7SQL] | ? | ? | test_independent_bi_sql[Q7SQL] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| test_independent_bi_sql[Q8SQL] | ? | ? | test_independent_bi_sql[Q8SQL] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI07 | 3.4 | Quy tắc project | test_independent_bi_sql[BI07] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI08 | 3.4 | Quy tắc project | test_independent_bi_sql[BI08] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI09 | 3.4 | Quy tắc project | test_independent_bi_sql[BI09] | **BLOCKED** | `junit.xml; pytest_output.txt` |
| BI10 | 3.4 | Quy tắc project | test_independent_bi_sql[BI10] | **BLOCKED** | `junit.xml; pytest_output.txt` |

## Chi tiết FAIL/BLOCKED và test được chọn cho demo


### MG01 — test_csv_headers[MG01]
- **1. Test ID:** MG01
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** CSV tmdb_5000_movies.csv tồn tại và có header
- **5. Đầu vào:** data/raw/tmdb_5000_movies.csv
- **6. Các bước:** csv.DictReader, đối chiếu cột thực tế
- **7. Expected:** CSV có đủ 20 cột bắt buộc, không trùng header
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu data/raw/tmdb_5000_movies.csv trong bản ZIP; thêm CSV TMDB của project
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG02 — test_csv_headers[MG02]
- **1. Test ID:** MG02
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** CSV tmdb_5000_credits.csv tồn tại và có header
- **5. Đầu vào:** data/raw/tmdb_5000_credits.csv
- **6. Các bước:** csv.DictReader, đối chiếu cột thực tế
- **7. Expected:** CSV có đủ 4 cột bắt buộc, không trùng header
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu data/raw/tmdb_5000_credits.csv trong bản ZIP; thêm CSV TMDB của project
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG03 — test_csv_headers[MG03]
- **1. Test ID:** MG03
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** CSV tmdb_new_batch.csv tồn tại và có header
- **5. Đầu vào:** data/raw/tmdb_new_batch.csv
- **6. Các bước:** csv.DictReader, đối chiếu cột thực tế
- **7. Expected:** CSV có đủ 20 cột bắt buộc, không trùng header
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu data/raw/tmdb_new_batch.csv trong bản ZIP; thêm CSV TMDB của project
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG04 — test_source_profiles[MG04]
- **1. Test ID:** MG04
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Movies: khóa id không null hoặc trùng trong file nguồn
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Đọc CSV nguồn, thống kê và lấy tối đa 10 mẫu có thứ tự
- **7. Expected:** Phân tích nguồn và ghi lại số liệu/bất thường; không giả định dữ liệu hoàn hảo
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu data/raw/tmdb_5000_movies.csv trong bản ZIP; thêm CSV TMDB của project
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG05 — test_source_profiles[MG05]
- **1. Test ID:** MG05
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Credits: khóa movie_id không null hoặc trùng trong file nguồn
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Đọc CSV nguồn, thống kê và lấy tối đa 10 mẫu có thứ tự
- **7. Expected:** Phân tích nguồn và ghi lại số liệu/bất thường; không giả định dữ liệu hoàn hảo
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu data/raw/tmdb_5000_credits.csv trong bản ZIP; thêm CSV TMDB của project
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG06 — test_source_profiles[MG06]
- **1. Test ID:** MG06
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Movie release_date parse được hoặc được ghi nhận coerce
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Đọc CSV nguồn, thống kê và lấy tối đa 10 mẫu có thứ tự
- **7. Expected:** Phân tích nguồn và ghi lại số liệu/bất thường; không giả định dữ liệu hoàn hảo
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu data/raw/tmdb_5000_movies.csv trong bản ZIP; thêm CSV TMDB của project
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG07 — test_source_profiles[MG07]
- **1. Test ID:** MG07
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Các trường JSON phim đúng cú pháp hoặc ghi nhận bất thường
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Đọc CSV nguồn, thống kê và lấy tối đa 10 mẫu có thứ tự
- **7. Expected:** Phân tích nguồn và ghi lại số liệu/bất thường; không giả định dữ liệu hoàn hảo
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu data/raw/tmdb_5000_movies.csv trong bản ZIP; thêm CSV TMDB của project
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG08 — test_source_profiles[MG08]
- **1. Test ID:** MG08
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Quan hệ CSV movies và credits hai chiều
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Đọc CSV nguồn, thống kê và lấy tối đa 10 mẫu có thứ tự
- **7. Expected:** Phân tích nguồn và ghi lại số liệu/bất thường; không giả định dữ liệu hoàn hảo
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Thiếu data/raw/tmdb_5000_movies.csv trong bản ZIP; thêm CSV TMDB của project
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG18 — test_pipeline_risks[MG18]
- **1. Test ID:** MG18
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Watermark phụ thuộc vào thành công export incremental
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** update_watermark có upstream export_incremental_stage
- **8. Actual:** {"pipeline": "tmdb_incremental", "errors": ["upstream hiện tại = ['get_watermark'], thiếu exporter"]}
- **9. Trạng thái:** FAIL
- **10. Nguyên nhân kết quả:** Đã quan sát vi phạm; AssertionError: upstream hiện tại = ['get_watermark'], thiếu exporter
assert not ["upstream hiện tại = ['get_watermark'], thiếu exporter"]
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG19 — test_pipeline_risks[MG19]
- **1. Test ID:** MG19
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Loader incremental lọc batch qua LSET/CET
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Batch mới được so với lset/cet trước export
- **8. Actual:** {"loader_uses_lset_or_cet": false}
- **9. Trạng thái:** FAIL
- **10. Nguyên nhân kết quả:** Đã quan sát vi phạm; AssertionError: Loader chỉ đọc nguyên batch CSV, không dùng LSET/CET
assert None
 +  where None = <function search at 0x7f748e734720>('\\b(lset|cet)\\b', 'import pandas as pd\n\nif \'data_loader\' not in globals():\n    from mage_ai.data_preparation.decorators import data...    df = pd.read_csv(\'data/raw/tmdb_new_batch.csv\')\n    print(f"Đã đọc {len(df)} dòng dữ liệu mới.")\n    return df', re.IGNORECASE)
 +    where <function search at 0x7f748e734720> = re.search
 +    and   re.IGNORECASE = re.I
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG20 — test_pipeline_risks[MG20]
- **1. Test ID:** MG20
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Exporter incremental xử lý ID trùng khi replay
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có logic upsert/deduplicate hoặc unique key, không tạo bản ghi trùng
- **8. Actual:** {"deduplication_in_exporter": false}
- **9. Trạng thái:** FAIL
- **10. Nguyên nhân kết quả:** Đã quan sát vi phạm; AssertionError: Exporter append không thấy cơ chế chống trùng ở cấp exporter; cần thực nghiệm replay isolated
assert False
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG21 — test_mage_stage[MG21]
- **1. Test ID:** MG21
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Full load rowcount stage so với CSV sau làm sạch
- **5. Đầu vào:** CSV nguồn + database stage
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Số hàng stage bằng số hàng drop_duplicates + dropna của transformer
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG22 — test_mage_stage[MG22]
- **1. Test ID:** MG22
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Quan hệ hai bảng stage và khóa null/trùng
- **5. Đầu vào:** PostgreSQL stage
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Stage không mất tham chiếu / khóa sau load sạch
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG23 — test_mage_stage[MG23]
- **1. Test ID:** MG23
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bảng watermark tồn tại và có dòng incremental
- **5. Đầu vào:** PostgreSQL control
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có một dòng tmdb_incremental và LSET không null
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MG24 — test_mage_stage[MG24]
- **1. Test ID:** MG24
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Metadata Mage có log run thực và rowcount
- **5. Đầu vào:** Mage runtime log
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Phải có log run mới có thể khẳng định các pipeline thực thi thành công
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Mage UI, chạy trong isolated, cung cấp run ID/log block

### MI01 — test_real_pipeline_scenarios[MI01]
- **1. Test ID:** MI01
- **2. Mục:** 3.1
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Full Load chạy lại giữ nguyên dữ liệu
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py full_repeat before → Mage UI run thật → scenario.py full_repeat after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** SKIPPED
- **10. Nguyên nhân kết quả:** SKIPPED: Chỉ chạy với --mode integration
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MI04 — test_real_pipeline_scenarios[MI04]
- **1. Test ID:** MI04
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Incremental cùng batch replay không tạo trùng
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py batch_replay before → Mage UI run thật → scenario.py batch_replay after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** SKIPPED
- **10. Nguyên nhân kết quả:** SKIPPED: Chỉ chạy với --mode integration
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### MI07 — test_real_pipeline_scenarios[MI07]
- **1. Test ID:** MI07
- **2. Mục:** 3.1
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Export thất bại không cập nhật watermark
- **5. Đầu vào:** DB isolated và log Mage của run thật
- **6. Các bước:** scenario.py export_failure before → Mage UI run thật → scenario.py export_failure after --mage-run-id <ID>
- **7. Expected:** Đối chiếu 2 snapshot before/after của lần Mage run thực
- **8. Actual:** None
- **9. Trạng thái:** SKIPPED
- **10. Nguyên nhân kết quả:** SKIPPED: Chỉ chạy với --mode integration
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.1 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DB05 — test_dbt_structure[DB05]
- **1. Test ID:** DB05
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** dbt refs/sources hình thành DAG hợp lệ
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** manifest hiện có đọc được, DAG không có cycle và bao phủ các SQL models
- **8. Actual:** {"models_in_old_manifest": 18, "source_node_count": 2}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** Đồ thị của artifact cũ, không phải build mới
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Phát hiện tĩnh trong code)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DB08 — test_dbt_structure[DB08]
- **1. Test ID:** DB08
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** dbt executable có thể khởi tạo
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có dbt trên máy hiện tại (chưa tuyên bố debug thành công)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có dbt Core trên PATH môi trường đang chạy
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DB09 — test_dbt_structure[DB09]
- **1. Test ID:** DB09
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** dbt model test được chạy trên snapshot hiện tại
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Có run_results của lần chạy này và DB quyền chỉ đọc
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa thực hiện dbt build mới có provenance trong isolated; xem isolation.py dbt-build
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DB10 — test_dbt_structure[DB10]
- **1. Test ID:** DB10
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** dbt docs được sinh từ model hiện tại
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** docs generate trên máy người dùng mới là bằng chứng hiện hành
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa thực hiện dbt build mới có provenance trong isolated; xem isolation.py dbt-build
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DB11 — test_dbt_structure[DB11]
- **1. Test ID:** DB11
- **2. Mục:** 3.2
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Thực thi dbt build/rebuild trong database cô lập
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Không chạy trên warehouse demo; có bằng chứng mới sau isolated build
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa thực hiện dbt build mới có provenance trong isolated; xem isolation.py dbt-build
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DB12 — test_dbt_structure[DB12]
- **1. Test ID:** DB12
- **2. Mục:** 3.2
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Surrogate key ổn định theo natural key sau rebuild
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** So sánh natural key và quan hệ, không giả định SK luôn cố định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: DB12: cần 2 snapshots natural key quanh rebuild và tái kiểm tra các FK; chưa có bằng chứng
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DB13 — test_dbt_structure[DB13]
- **1. Test ID:** DB13
- **2. Mục:** 3.2
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Mức độ bao phủ model trong schema.yml
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cả 18 models được mô tả riêng trong schema.yml (mức mong muốn, không phải điều kiện tối thiểu của đề)
- **8. Actual:** {"models_sql": 18, "documented": 14, "missing_models": ["stg_movie_companies", "stg_movie_countries", "stg_movie_genres", "stg_movie_keywords"]}
- **9. Trạng thái:** FAIL
- **10. Nguyên nhân kết quả:** Đã quan sát vi phạm; AssertionError: Các model chưa được mô tả riêng: stg_movie_companies, stg_movie_countries, stg_movie_genres, stg_movie_keywords
assert not ['stg_movie_companies', 'stg_movie_countries', 'stg_movie_genres', 'stg_movie_keywords']
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Chạy dbt bằng profiles-dir riêng trên DB cô lập và lưu artifacts mới

### DW32 — test_transformation_invariant[DW32]
- **1. Test ID:** DW32
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Staging chuẩn hóa budget/revenue 0 thành NULL
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW33 — test_transformation_invariant[DW33]
- **1. Test ID:** DW33
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Staging chuẩn hóa vote_average khi vote_count<=0
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW34 — test_transformation_invariant[DW34]
- **1. Test ID:** DW34
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Staging phim có natural key/title và không trùng phim
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW35 — test_transformation_invariant[DW35]
- **1. Test ID:** DW35
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Language fallback giữ mã và Unknown hợp lệ
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW36 — test_transformation_invariant[DW36]
- **1. Test ID:** DW36
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Country region không được NULL khi chưa map
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW37 — test_transformation_invariant[DW37]
- **1. Test ID:** DW37
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Keyword theme_group không được NULL
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW38 — test_transformation_invariant[DW38]
- **1. Test ID:** DW38
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact không có finance-valid khi budget/revenue NULL
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW41 — test_transformation_invariant[DW41]
- **1. Test ID:** DW41
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Country region chính xác theo seed, fallback Unknown
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW42 — test_transformation_invariant[DW42]
- **1. Test ID:** DW42
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Keyword theme chính xác theo seed, fallback Other
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW43 — test_transformation_invariant[DW43]
- **1. Test ID:** DW43
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Language label fallback giữ code khi không có tên
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW44 — test_transformation_invariant[DW44]
- **1. Test ID:** DW44
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** RuntimeBand trong dim_movie đúng theo staging
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW45 — test_transformation_invariant[DW45]
- **1. Test ID:** DW45
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** BudgetBand trong dim_movie đúng theo staging
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW46 — test_transformation_invariant[DW46]
- **1. Test ID:** DW46
- **2. Mục:** 3.2
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** CountryType và country_count từ quan hệ stage
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.2 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### NC01 — test_negative_controls[NC01]
- **1. Test ID:** NC01
- **2. Mục:** 3.3
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Bridge weight_factor phải bắt được sai lệch
- **5. Đầu vào:** Chỉ tmdb_test_warehouse ở localhost:55432
- **6. Các bước:** BEGIN → injection có chủ đích → chạy nguyên assertion DW → ROLLBACK
- **7. Expected:** Tạo lỗi trong isolated, SQL DW18 bắt được, sau đó rollback
- **8. Actual:** None
- **9. Trạng thái:** SKIPPED
- **10. Nguyên nhân kết quả:** SKIPPED: Chỉ chạy với --mode integration
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW01 — test_warehouse_invariant[DW01]
- **1. Test ID:** DW01
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Có đúng 12 bảng fact/dim/bridge
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW02 — test_warehouse_invariant[DW02]
- **1. Test ID:** DW02
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** 12 bảng có khóa chính vật lý
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW03 — test_warehouse_invariant[DW03]
- **1. Test ID:** DW03
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** UNIQUE vật lý cho các natural key
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW04 — test_warehouse_invariant[DW04]
- **1. Test ID:** DW04
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** 11 FK vật lý trỏ đúng bảng cha (confrelid)
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW05 — test_warehouse_invariant[DW05]
- **1. Test ID:** DW05
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Grain Fact = dim_movie = số movie_sk distinct
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW06 — test_warehouse_invariant[DW06]
- **1. Test ID:** DW06
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** fact_movie không có movie_sk trùng
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW07 — test_warehouse_invariant[DW07]
- **1. Test ID:** DW07
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact SK và cờ không NULL
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW08 — test_warehouse_invariant[DW08]
- **1. Test ID:** DW08
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact → dim_movie 1:1 logic
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW09 — test_warehouse_invariant[DW09]
- **1. Test ID:** DW09
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact không có FK logic mồ côi
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW10 — test_warehouse_invariant[DW10]
- **1. Test ID:** DW10
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge genre không có orphan
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW11 — test_warehouse_invariant[DW11]
- **1. Test ID:** DW11
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge company không có orphan
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW12 — test_warehouse_invariant[DW12]
- **1. Test ID:** DW12
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge country không có orphan
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW13 — test_warehouse_invariant[DW13]
- **1. Test ID:** DW13
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge keyword không có orphan
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW14 — test_warehouse_invariant[DW14]
- **1. Test ID:** DW14
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge genre không trùng cặp khóa
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW15 — test_warehouse_invariant[DW15]
- **1. Test ID:** DW15
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge company không trùng cặp khóa
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW16 — test_warehouse_invariant[DW16]
- **1. Test ID:** DW16
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge country không trùng cặp khóa
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW17 — test_warehouse_invariant[DW17]
- **1. Test ID:** DW17
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge keyword không trùng cặp khóa
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW18 — test_warehouse_invariant[DW18]
- **1. Test ID:** DW18
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge genre weight_factor dương, sum=1
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW19 — test_warehouse_invariant[DW19]
- **1. Test ID:** DW19
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge company weight_factor dương, sum=1
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW20 — test_warehouse_invariant[DW20]
- **1. Test ID:** DW20
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge country weight_factor dương, sum=1
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW21 — test_warehouse_invariant[DW21]
- **1. Test ID:** DW21
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Keyword bridge không có cột weight_factor
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW22 — test_warehouse_invariant[DW22]
- **1. Test ID:** DW22
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** 6 dimension (trừ dim_movie) có đúng 1 Unknown SK=-1
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW23 — test_warehouse_invariant[DW23]
- **1. Test ID:** DW23
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Các bridge genre/company/country bao phủ mọi phim
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW24 — test_warehouse_invariant[DW24]
- **1. Test ID:** DW24
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** dim_date có đủ chuỗi ngày liên tục (trừ Unknown)
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW25 — test_warehouse_invariant[DW25]
- **1. Test ID:** DW25
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** dim_date month_name English, decade dạng 1980s
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW26 — test_warehouse_invariant[DW26]
- **1. Test ID:** DW26
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact profit=revenue-budget; ROI thập phân
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW27 — test_warehouse_invariant[DW27]
- **1. Test ID:** DW27
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Cờ is_finance_valid và is_revenue_over_budget đúng
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW28 — test_warehouse_invariant[DW28]
- **1. Test ID:** DW28
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact vote_count mặc định 0 và NOT NULL
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW29 — test_warehouse_invariant[DW29]
- **1. Test ID:** DW29
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Fact movie_count luôn bằng 1
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW30 — test_warehouse_invariant[DW30]
- **1. Test ID:** DW30
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Votes không dương thì vote_average NULL
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW31 — test_warehouse_invariant[DW31]
- **1. Test ID:** DW31
- **2. Mục:** 3.3
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Profit không âm/âm đều được, không loại phim không hợp lệ
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW39 — test_warehouse_invariant[DW39]
- **1. Test ID:** DW39
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Weighted profit across each bridge = fact profit for covered movies
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW40 — test_warehouse_invariant[DW40]
- **1. Test ID:** DW40
- **2. Mục:** 3.3
- **3. Phân loại:** Kiểm tra độ bền
- **4. Mục đích:** Vote-count, ROI và finance được dùng nhất quán khi tổng hợp
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW47 — test_warehouse_invariant[DW47]
- **1. Test ID:** DW47
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge genre phải có đúng weight_factor = 1/k mỗi link
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW48 — test_warehouse_invariant[DW48]
- **1. Test ID:** DW48
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge company phải có đúng weight_factor = 1/k mỗi link
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### DW49 — test_warehouse_invariant[DW49]
- **1. Test ID:** DW49
- **2. Mục:** 3.3
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Bridge country phải có đúng weight_factor = 1/k mỗi link
- **5. Đầu vào:** PostgreSQL warehouse.dds (snapshot hiện tại)
- **6. Các bước:** Chạy SELECT đếm toàn bộ vi phạm và lưu tối đa 10 mẫu có thứ tự
- **7. Expected:** Số dòng vi phạm = 0 (NULL được xét tường minh, lấy 10 mẫu)
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.3 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### PB02 — test_powerbi_metadata_and_manual[PB02]
- **1. Test ID:** PB02
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Có tối thiểu hai trang Dashboard
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Chính xác 4 trang được liệt kê trong report pages metadata
- **8. Actual:** {"page_count": 4, "names": ["Overview", "Financial drivers", "Companies & Countries", "Audience & Ratings"]}
- **9. Trạng thái:** PASS
- **10. Nguyên nhân kết quả:** Assertion đạt trên dữ liệu/mã hiện tại.
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt (Phát hiện tĩnh trong PBIX)
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB07 — test_powerbi_metadata_and_manual[PB07]
- **1. Test ID:** PB07
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Drill-down thời gian hoạt động
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Dùng giao diện Power BI Desktop để mở và thao tác drill-down
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB08 — test_powerbi_metadata_and_manual[PB08]
- **1. Test ID:** PB08
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Relationships đúng cardinality và cross-filter
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Truy vấn semantic model hoặc TMDL; DataModel nén không thể xác minh tĩnh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB09 — test_powerbi_metadata_and_manual[PB09]
- **1. Test ID:** PB09
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** DAX measures tính đúng với SQL
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Phải đọc DAX expression và cùng filter-context rồi mới kết luận
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB10 — test_powerbi_metadata_and_manual[PB10]
- **1. Test ID:** PB10
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Top N được sort theo measure hiển thị
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cần truy vấn/mở visual và xem sortBy hay ranking filter
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB11 — test_powerbi_metadata_and_manual[PB11]
- **1. Test ID:** PB11
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Ngưỡng Min Movies, Min Votes dùng đúng measure
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Kiểm tra khi đổi các tham số trong Desktop và truy vấn SQL
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB12 — test_powerbi_metadata_and_manual[PB12]
- **1. Test ID:** PB12
- **2. Mục:** 3.4
- **3. Phân loại:** Yêu cầu bắt buộc
- **4. Mục đích:** Refresh Import thành công và khớp DDS
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cần refresh thật, thời điểm refresh, các KPI sau refresh
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB13 — test_powerbi_metadata_and_manual[PB13]
- **1. Test ID:** PB13
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Allocation Weighted và Full đổi thứ hạng
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cần quan sát report + đối chiếu SQL cùng snapshot
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### PB14 — test_powerbi_metadata_and_manual[PB14]
- **1. Test ID:** PB14
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Country=USA, Year=2014, Genre=Action
- **5. Đầu vào:** Source/DB tương ứng của project
- **6. Các bước:** Thực hiện assertion mô tả trong mã test.
- **7. Expected:** Cần cùng filter context tại Desktop và số liệu SQL độc lập
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Mở Power BI Desktop và điền checklist bằng bằng chứng thật (ảnh/giá trị/refresh)

### test_powerbi_metadata_and_manual[Q1] — test_powerbi_metadata_and_manual[Q1]
- **1. Test ID:** test_powerbi_metadata_and_manual[Q1]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_powerbi_metadata_and_manual[Q1]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_powerbi_metadata_and_manual[Q2] — test_powerbi_metadata_and_manual[Q2]
- **1. Test ID:** test_powerbi_metadata_and_manual[Q2]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_powerbi_metadata_and_manual[Q2]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_powerbi_metadata_and_manual[Q3] — test_powerbi_metadata_and_manual[Q3]
- **1. Test ID:** test_powerbi_metadata_and_manual[Q3]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_powerbi_metadata_and_manual[Q3]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_powerbi_metadata_and_manual[Q4] — test_powerbi_metadata_and_manual[Q4]
- **1. Test ID:** test_powerbi_metadata_and_manual[Q4]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_powerbi_metadata_and_manual[Q4]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_powerbi_metadata_and_manual[Q5] — test_powerbi_metadata_and_manual[Q5]
- **1. Test ID:** test_powerbi_metadata_and_manual[Q5]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_powerbi_metadata_and_manual[Q5]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_powerbi_metadata_and_manual[Q6] — test_powerbi_metadata_and_manual[Q6]
- **1. Test ID:** test_powerbi_metadata_and_manual[Q6]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_powerbi_metadata_and_manual[Q6]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_powerbi_metadata_and_manual[Q7] — test_powerbi_metadata_and_manual[Q7]
- **1. Test ID:** test_powerbi_metadata_and_manual[Q7]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_powerbi_metadata_and_manual[Q7]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_powerbi_metadata_and_manual[Q8] — test_powerbi_metadata_and_manual[Q8]
- **1. Test ID:** test_powerbi_metadata_and_manual[Q8]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_powerbi_metadata_and_manual[Q8]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Không có semantic model/Power BI Desktop đang kết nối; dùng CHECKLIST_POWERBI.md, không suy từ PBIX Import
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### BI01 — test_independent_bi_sql[BI01]
- **1. Test ID:** BI01
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** KPI toàn danh mục, cùng tập phim finance-valid
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI02 — test_independent_bi_sql[BI02]
- **1. Test ID:** BI02
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Country USA + Year 2014 + Genre Action (không nhân đôi phim)
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI03 — test_independent_bi_sql[BI03]
- **1. Test ID:** BI03
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Weighted và Full: profit theo hãng, kiểm tra phân bổ
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI04 — test_independent_bi_sql[BI04]
- **1. Test ID:** BI04
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** SQL kiểm tra phân nhóm ít hơn 5 valid movies
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI05 — test_independent_bi_sql[BI05]
- **1. Test ID:** BI05
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Một phim nhiều genre, minh họa 1/k từ dữ liệu thật
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI06 — test_independent_bi_sql[BI06]
- **1. Test ID:** BI06
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Phim có budget/revenue NULL, ví dụ dữ liệu thật
- **5. Đầu vào:** Read-only PostgreSQL dds, cùng snapshot với PBIX chỉ sau Refresh
- **6. Các bước:** SELECT độc lập vào dds, lưu rows có thứ tự (tối đa 30 mẫu) và tổng số dòng
- **7. Expected:** SQL độc lập chạy thành công và lưu actual chưa làm tròn; KHÔNG thay thế đối chiếu DAX/UI
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### test_independent_bi_sql[Q1SQL] — test_independent_bi_sql[Q1SQL]
- **1. Test ID:** test_independent_bi_sql[Q1SQL]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_independent_bi_sql[Q1SQL]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_independent_bi_sql[Q2SQL] — test_independent_bi_sql[Q2SQL]
- **1. Test ID:** test_independent_bi_sql[Q2SQL]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_independent_bi_sql[Q2SQL]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_independent_bi_sql[Q3SQL] — test_independent_bi_sql[Q3SQL]
- **1. Test ID:** test_independent_bi_sql[Q3SQL]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_independent_bi_sql[Q3SQL]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_independent_bi_sql[Q4SQL] — test_independent_bi_sql[Q4SQL]
- **1. Test ID:** test_independent_bi_sql[Q4SQL]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_independent_bi_sql[Q4SQL]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_independent_bi_sql[Q5SQL] — test_independent_bi_sql[Q5SQL]
- **1. Test ID:** test_independent_bi_sql[Q5SQL]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_independent_bi_sql[Q5SQL]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_independent_bi_sql[Q6SQL] — test_independent_bi_sql[Q6SQL]
- **1. Test ID:** test_independent_bi_sql[Q6SQL]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_independent_bi_sql[Q6SQL]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_independent_bi_sql[Q7SQL] — test_independent_bi_sql[Q7SQL]
- **1. Test ID:** test_independent_bi_sql[Q7SQL]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_independent_bi_sql[Q7SQL]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### test_independent_bi_sql[Q8SQL] — test_independent_bi_sql[Q8SQL]
- **1. Test ID:** test_independent_bi_sql[Q8SQL]
- **2. Mục:** ?
- **3. Phân loại:** ?
- **4. Mục đích:** test_independent_bi_sql[Q8SQL]
- **5. Đầu vào:** Không xác định
- **6. Các bước:** Mở pytest output
- **7. Expected:** Không xác định
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi ? của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đọc pytest_output.txt để xem lỗi

### BI07 — test_independent_bi_sql[BI07]
- **1. Test ID:** BI07
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Q2 bổ sung: popularity/rating theo genre và language
- **5. Đầu vào:** Read-only dds (current snapshot)
- **6. Các bước:** SELECT theo filter; ghi đầy đủ kết quả vào queries/<ID>.json
- **7. Expected:** SQL độc lập tính được giá trị tham chiếu cho UI; chưa chứng minh DAX đúng
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI08 — test_independent_bi_sql[BI08]
- **1. Test ID:** BI08
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Q4 bổ sung: budget-revenue từng phim hợp lệ để đối chiếu scatter
- **5. Đầu vào:** Read-only dds (current snapshot)
- **6. Các bước:** SELECT theo filter; ghi đầy đủ kết quả vào queries/<ID>.json
- **7. Expected:** SQL độc lập tính được giá trị tham chiếu cho UI; chưa chứng minh DAX đúng
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI09 — test_independent_bi_sql[BI09]
- **1. Test ID:** BI09
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Q5 bổ sung: revenue/ROI của hãng Weighted và Full
- **5. Đầu vào:** Read-only dds (current snapshot)
- **6. Các bước:** SELECT theo filter; ghi đầy đủ kết quả vào queries/<ID>.json
- **7. Expected:** SQL độc lập tính được giá trị tham chiếu cho UI; chưa chứng minh DAX đúng
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

### BI10 — test_independent_bi_sql[BI10]
- **1. Test ID:** BI10
- **2. Mục:** 3.4
- **3. Phân loại:** Quy tắc project
- **4. Mục đích:** Ngưỡng Min Votes 100 và 1000 theo LanguageGroup
- **5. Đầu vào:** Read-only dds (current snapshot)
- **6. Các bước:** SELECT theo filter; ghi đầy đủ kết quả vào queries/<ID>.json
- **7. Expected:** SQL độc lập tính được giá trị tham chiếu cho UI; chưa chứng minh DAX đúng
- **8. Actual:** None
- **9. Trạng thái:** BLOCKED
- **10. Nguyên nhân kết quả:** Thiếu điều kiện kiểm chứng; BLOCKED: Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt
- **11. Ý nghĩa:** Chỉ xác nhận phạm vi 3.4 của test này; không suy rộng sang toàn project.
- **12. Bằng chứng và loại:** junit.xml; pytest_output.txt
- **13. Tái hiện:** .\test\run_acceptance.ps1 -Section all -Mode readonly
- **14. Hướng xử lý:** Đối chiếu bằng chứng, kiểm tra nguồn dữ liệu và sửa trong nhiệm vụ riêng.

## Giới hạn

- Kết quả tĩnh chỉ chứng minh nội dung các file trong repository; không chứng minh runtime đã chạy.
- Các hiện tượng Power BI chưa truy vấn được DAX expression / refresh trực tiếp được ghi BLOCKED.
- Kết quả từ `dbt_transform/target/` là artifacts cũ, không phải lần build mới.
- Đây không phải kết luận tổng thể thành công khi còn BLOCKED.

## Môi trường và snapshot (không chứa credentials)

```json
{
  "versions": {
    "python": "3.13.5",
    "pytest": "pytest 9.0.2",
    "dbt": "Không có trên PATH",
    "docker": "Không có trên PATH",
    "compose": "Không có trên PATH",
    "mage": "Không có trên PATH",
    "powerbi_desktop": "Không thể kiểm tra từ môi trường CLI này"
  },
  "sources": {
    "tmdb_5000_movies.csv": {
      "available": false
    },
    "tmdb_5000_credits.csv": {
      "available": false
    },
    "tmdb_new_batch.csv": {
      "available": false
    }
  },
  "target": {
    "host": "127.0.0.1",
    "port": 5432,
    "dbname": "warehouse",
    "user": "labuser"
  },
  "db_snapshot": {
    "status": "BLOCKED",
    "reason": "Chưa cài psycopg: python -m pip install -r test/acceptance/requirements.txt"
  }
}
```
