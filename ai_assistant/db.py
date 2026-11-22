"""
db.py — Kết nối PostgreSQL CHỈ ĐỌC (READ ONLY) cho TMDB BI — AI Companion.

- Tự tìm và nạp file .env ở thư mục gốc dự án (python-dotenv).
- Dùng psycopg (psycopg3), autocommit=False; mỗi truy vấn chạy trong transaction
  `SET TRANSACTION READ ONLY` + `SET LOCAL statement_timeout = '10s'`, và luôn ROLLBACK khi kết thúc.
- validate_readonly_sql(): lớp kiểm duyệt SQL (đặc biệt cho SQL do LLM sinh ra).
- df_to_clean_records(): chuyển DataFrame sang list[dict] thuần Python/JSON để gửi cho LLM.
"""

from __future__ import annotations

import math
import os
import re
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pandas as pd
import psycopg
from dotenv import find_dotenv, load_dotenv

# --------------------------------------------------------------------------------------
# Nạp .env (thư mục gốc dự án = cha của ai_assistant/)
# --------------------------------------------------------------------------------------
_ROOT_DIR = Path(__file__).resolve().parent.parent
_ENV_PATH = _ROOT_DIR / ".env"
if _ENV_PATH.exists():
    load_dotenv(_ENV_PATH)
else:
    _found = find_dotenv(usecwd=True)  # dự phòng: tìm ngược từ thư mục đang chạy
    if _found:
        load_dotenv(_found)

STATEMENT_TIMEOUT = "10s"


class SQLValidationError(ValueError):
    """SQL bị lớp kiểm duyệt chặn (không phải câu lệnh chỉ-đọc hợp lệ trên schema dds)."""


# --------------------------------------------------------------------------------------
# Kết nối
# --------------------------------------------------------------------------------------
def _connection_kwargs() -> dict:
    dbname = os.getenv("POSTGRES_DB", "").strip()
    user = os.getenv("POSTGRES_USER", "").strip()
    password = os.getenv("POSTGRES_PASSWORD", "")
    if not dbname or not user:
        raise RuntimeError(
            "Thiếu POSTGRES_DB hoặc POSTGRES_USER trong file .env ở thư mục gốc dự án "
            "(cần POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD; tùy chọn POSTGRES_HOST, POSTGRES_PORT)."
        )
    return {
        "dbname": dbname,
        "user": user,
        "password": password,
        "host": os.getenv("POSTGRES_HOST", "").strip() or "localhost",
        "port": int(os.getenv("POSTGRES_PORT", "").strip() or 5432),
        "connect_timeout": 5,
        "autocommit": False,
    }


def _connect() -> psycopg.Connection:
    return psycopg.connect(**_connection_kwargs())


# --------------------------------------------------------------------------------------
# Kiểm duyệt SQL
# --------------------------------------------------------------------------------------
_FORBIDDEN_KEYWORDS = (
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "GRANT", "REVOKE",
    "COPY", "EXECUTE", "CALL", "PG_SLEEP",
    # chặn thêm các hàm/cú pháp nguy hiểm khác
    "INTO", "PG_READ_FILE", "PG_LS_DIR", "LO_IMPORT", "LO_EXPORT", "DBLINK", "SET_CONFIG",
    "PG_TERMINATE_BACKEND", "PG_CANCEL_BACKEND",
)
_FORBIDDEN_RE = re.compile(r"\b(" + "|".join(_FORBIDDEN_KEYWORDS) + r")\b", re.IGNORECASE)
_SYSTEM_TABLE_RE = re.compile(
    r"\b(pg_catalog|pg_shadow|pg_roles|pg_authid|pg_user|pg_stat_activity|information_schema)\b", re.IGNORECASE
)
_DDS_REF_RE = re.compile(r"\bdds\s*\.", re.IGNORECASE)
_STRING_LITERAL_RE = re.compile(r"'(?:[^']|'')*'")


def _strip_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    sql = re.sub(r"--[^\n]*", " ", sql)
    return sql


def validate_readonly_sql(sql: str) -> str:
    """
    Kiểm tra chặt một câu SQL chỉ-đọc. Trả về câu SQL đã làm sạch (bỏ comment và dấu ';' ở cuối).
    Ném SQLValidationError (là ValueError) với thông báo tiếng Việt nếu vi phạm.
    """
    if not isinstance(sql, str) or not sql.strip():
        raise SQLValidationError("Câu SQL rỗng.")

    cleaned = _strip_comments(sql).strip()
    cleaned = re.sub(r"[;\s]+$", "", cleaned)  # bỏ dấu ';' (và khoảng trắng) ở cuối
    if not cleaned:
        raise SQLValidationError("Câu SQL rỗng.")

    # Quét trên bản đã loại chuỗi ký tự để không báo nhầm từ khóa/dấu ';' nằm trong giá trị lọc (ví dụ tên phim).
    scan = _STRING_LITERAL_RE.sub("''", cleaned)

    if ";" in scan:
        raise SQLValidationError("Chỉ cho phép MỘT câu lệnh duy nhất (phát hiện dấu ';' ở giữa câu SQL).")

    if not re.match(r"^(SELECT|WITH)\b", scan, flags=re.IGNORECASE):
        raise SQLValidationError("Chỉ cho phép câu lệnh bắt đầu bằng SELECT hoặc WITH.")

    bad = _FORBIDDEN_RE.search(scan)
    if bad:
        raise SQLValidationError(f"Phát hiện từ khóa bị cấm: {bad.group(1).upper()}.")

    sysref = _SYSTEM_TABLE_RE.search(scan)
    if sysref:
        raise SQLValidationError(f"Không được truy cập bảng/schema hệ thống: {sysref.group(1).lower()}.")

    if not _DDS_REF_RE.search(scan):
        raise SQLValidationError("Câu SQL phải tham chiếu tới schema `dds.` (ví dụ dds.fact_movie).")

    return cleaned


# --------------------------------------------------------------------------------------
# Thực thi
# --------------------------------------------------------------------------------------
def _decimals_to_float(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        if df[col].dtype == object:
            non_null = df[col].dropna()
            if len(non_null) and non_null.map(lambda v: isinstance(v, Decimal)).all():
                df[col] = df[col].map(lambda v: float(v) if isinstance(v, Decimal) else v).astype("float64")
    return df


def run_query(sql: str, params=None) -> pd.DataFrame:
    """
    Chạy một câu truy vấn chỉ-đọc và trả về DataFrame.
    Mọi truy vấn đều chạy trong transaction READ ONLY với statement_timeout = 10s, kết thúc bằng ROLLBACK.
    Cột Decimal được đổi sang float64 để dễ tính toán/hiển thị.
    """
    with _connect() as conn:
        try:
            with conn.cursor() as cur:
                cur.execute("SET TRANSACTION READ ONLY")
                cur.execute(f"SET LOCAL statement_timeout = '{STATEMENT_TIMEOUT}'")
                cur.execute(sql, params)
                if cur.description is None:
                    df = pd.DataFrame()
                else:
                    columns = [c.name for c in cur.description]
                    df = pd.DataFrame(cur.fetchall(), columns=columns)
        finally:
            conn.rollback()
    return _decimals_to_float(df)


def test_connection() -> dict:
    """
    Kiểm tra kết nối và đếm số dòng dds.fact_movie.
    Trả về: {"connected": bool, "status": "ok"|"error", "fact_movie_rows": int|None,
             "database": str, "host": str, "port": int, "error": str|None}
    """
    info: dict[str, Any] = {
        "connected": False, "status": "error", "fact_movie_rows": None,
        "database": os.getenv("POSTGRES_DB", ""), "host": os.getenv("POSTGRES_HOST", "") or "localhost",
        "port": int(os.getenv("POSTGRES_PORT", "") or 5432), "error": None,
    }
    try:
        df = run_query("SELECT COUNT(*) AS n FROM dds.fact_movie")
        info.update(connected=True, status="ok", fact_movie_rows=int(df.iloc[0, 0]))
    except Exception as exc:  # noqa: BLE001
        info["error"] = str(exc).strip()[:300] or exc.__class__.__name__
    return info


# --------------------------------------------------------------------------------------
# Làm sạch dữ liệu để gửi cho LLM / JSON
# --------------------------------------------------------------------------------------
def _clean_value(v: Any) -> Any:
    if v is None or v is pd.NA or v is pd.NaT:
        return None
    if isinstance(v, bool):
        return v
    if isinstance(v, Decimal):
        if not v.is_finite():
            return None
        f = float(v)
        return int(f) if f.is_integer() and abs(f) < 1e15 else round(f, 6)
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return None if (math.isnan(v) or math.isinf(v)) else round(v, 6)
    if isinstance(v, (pd.Timestamp, datetime, date)):
        return None if v is pd.NaT else v.isoformat()
    if hasattr(v, "item") and not isinstance(v, (str, bytes)):  # numpy scalar
        try:
            return _clean_value(v.item())
        except (ValueError, AttributeError):
            pass
    if isinstance(v, (list, tuple)):
        return [_clean_value(x) for x in v]
    if isinstance(v, dict):
        return {str(k): _clean_value(x) for k, x in v.items()}
    return str(v)


def df_to_clean_records(df: pd.DataFrame) -> list[dict]:
    """DataFrame -> list[dict] chỉ gồm kiểu Python/JSON (Decimal, Timestamp, NaN/NA đã được xử lý)."""
    if df is None or len(df) == 0:
        return []
    records = []
    for row in df.to_dict(orient="records"):
        records.append({str(k): _clean_value(v) for k, v in row.items()})
    return records
