"""Groq/Gemini streaming explanations and guarded, read-only Text-to-SQL."""

from __future__ import annotations

import json
import os
import re
import socket
import time
from pathlib import Path
from typing import Any

import httpx
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from google import genai
from google.genai import types

try:  # chạy bằng `streamlit run ai_assistant/app.py` (thư mục ai_assistant nằm trong sys.path)
    from db import df_to_clean_records, run_query, validate_readonly_sql
except ImportError:  # chạy dạng package: python -m ai_assistant...
    from ai_assistant.db import df_to_clean_records, run_query, validate_readonly_sql

# --------------------------------------------------------------------------------------
# Cấu hình
# --------------------------------------------------------------------------------------
_ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT_DIR / ".env")
load_dotenv()  # dự phòng: tìm .env từ thư mục làm việc hiện tại

DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash-lite"
MAX_ROWS_TO_LLM = 30          # số dòng kết quả tối đa gửi cho model ở bước diễn giải
MAX_DIAG_ROWS = 30            # số dòng tối đa gửi cho model ở chế độ chẩn đoán
MAX_QUESTION_CHARS = 1000

_clients: dict[str, OpenAI | genai.Client] = {}


class LLMError(RuntimeError):
    """Lỗi cấu hình hoặc gọi dịch vụ LLM, trình bày bằng tiếng Việt."""


_LLM_API_HOSTS = frozenset(
    {"api.groq.com", "generativelanguage.googleapis.com"}
)
_ORIGINAL_GETADDRINFO = socket.getaddrinfo
_IPV4_ENABLED = False


def _enable_ipv4_for_llm() -> None:
    """Use IPv4 only for remote LLM API hosts; leave local/database DNS untouched."""
    global _IPV4_ENABLED
    if _IPV4_ENABLED:
        return

    def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
        if isinstance(host, bytes):
            normalized_host = host.decode("ascii", errors="ignore").lower().rstrip(".")
        elif isinstance(host, str):
            normalized_host = host.lower().rstrip(".")
        else:
            normalized_host = ""
        if normalized_host in _LLM_API_HOSTS:
            family = socket.AF_INET
        return _ORIGINAL_GETADDRINFO(host, port, family, type, proto, flags)

    socket.getaddrinfo = getaddrinfo_ipv4
    _IPV4_ENABLED = True


def get_provider() -> str:
    requested = os.getenv("LLM_PROVIDER", "").strip().lower()
    if requested:
        if requested not in {"groq", "gemini"}:
            raise LLMError("LLM_PROVIDER chỉ nhận 'groq' hoặc 'gemini'.")
        return requested
    if os.getenv("GROQ_API_KEY", "").strip():
        return "groq"
    return "gemini"


def get_model_name() -> str:
    if get_provider() == "groq":
        return os.getenv("GROQ_MODEL", "").strip() or DEFAULT_GROQ_MODEL
    return os.getenv("GEMINI_MODEL", "").strip() or DEFAULT_GEMINI_MODEL


def is_configured() -> bool:
    return any(os.getenv(key, "").strip() for key in ("GROQ_API_KEY", "GEMINI_API_KEY"))


def _get_client(provider: str | None = None) -> OpenAI | genai.Client:
    provider = provider or get_provider()
    _enable_ipv4_for_llm()
    if provider not in _clients:
        if provider == "groq":
            api_key = os.getenv("GROQ_API_KEY", "").strip()
            if not api_key:
                raise LLMError("Thiếu GROQ_API_KEY. Thêm khóa vào file .env hoặc chọn LLM_PROVIDER=gemini.")
            http_client = httpx.Client(
                transport=httpx.HTTPTransport(local_address="0.0.0.0"),
                timeout=15.0,
            )
            _clients[provider] = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key,
                timeout=15.0,
                max_retries=1,
                http_client=http_client,
            )
        else:
            api_key = os.getenv("GEMINI_API_KEY", "").strip()
            if not api_key:
                raise LLMError("Thiếu GEMINI_API_KEY. Thêm khóa vào file .env hoặc chọn LLM_PROVIDER=groq.")
            _clients[provider] = genai.Client(
                api_key=api_key,
                http_options=types.HttpOptions(timeout=15_000),
            )
    return _clients[provider]


def _friendly_llm_error(exc: Exception, provider: str) -> str:
    msg = str(exc)
    for key in ("GROQ_API_KEY", "GEMINI_API_KEY"):
        api_key = os.getenv(key, "").strip()
        if api_key:
            msg = msg.replace(api_key, "[đã ẩn]")
    low = msg.lower()
    provider_name = "Groq" if provider == "groq" else "Gemini"
    key_name = "GROQ_API_KEY" if provider == "groq" else "GEMINI_API_KEY"
    if "429" in msg or "resource_exhausted" in low or "quota" in low or "rate limit" in low:
        return f"{provider_name} API đang giới hạn yêu cầu. Hãy đợi rồi thử lại hoặc kiểm tra hạn mức."
    if "404" in msg or "not_found" in low or "model_not_found" in low:
        return (
            f"{provider_name} không tìm thấy model '{get_model_name()}' hoặc khóa không có quyền dùng model đó. "
            f"Hãy kiểm tra {('GROQ_MODEL' if provider == 'groq' else 'GEMINI_MODEL')} và quyền truy cập."
        )
    if "api key" in low or "api_key" in low or "401" in msg or "403" in msg or "permission" in low:
        return f"{key_name} không hợp lệ hoặc không có quyền truy cập model. Hãy kiểm tra file .env."
    if "503" in msg or "unavailable" in low or "overloaded" in low:
        return f"Dịch vụ {provider_name} đang quá tải tạm thời. Vui lòng thử lại sau."
    if "timeout" in low or "timed out" in low or "connection" in low:
        return f"Không kết nối được tới {provider_name} API (lỗi mạng/timeout). Hãy kiểm tra Internet."
    return f"Lỗi khi gọi {provider_name} API: {msg[:300]}"


def _gemini_generation_config(
    *,
    system_instruction: str,
    temperature: float,
    json_mode: bool,
) -> types.GenerateContentConfig:
    config_values: dict[str, Any] = {
        "system_instruction": system_instruction,
        "temperature": temperature,
        "response_mime_type": "application/json" if json_mode else "text/plain",
        "max_output_tokens": 1200 if json_mode else 1000,
    }
    thinking_config_type = getattr(types, "ThinkingConfig", None)
    if thinking_config_type is not None:
        config_values["thinking_config"] = thinking_config_type(thinking_budget=0)
    try:
        return types.GenerateContentConfig(**config_values)
    except (TypeError, ValueError):
        config_values.pop("thinking_config", None)
        return types.GenerateContentConfig(**config_values)


def _groq_reasoning_options() -> dict[str, str]:
    if get_model_name().startswith("openai/gpt-oss-"):
        return {"reasoning_effort": "low"}
    return {}


def _generate(
    prompt: str,
    *,
    system_instruction: str,
    temperature: float = 0.2,
    json_mode: bool = False,
) -> str:
    """Generate one response using the configured provider."""
    provider = get_provider()
    client = _get_client(provider)
    last_exc: Exception | None = None
    for attempt in range(2 if provider == "gemini" else 1):
        try:
            if provider == "groq":
                request: dict[str, Any] = {
                    "model": get_model_name(),
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": temperature,
                    "max_tokens": 1500 if json_mode else 1200,
                    **_groq_reasoning_options(),
                }
                if json_mode:
                    request["response_format"] = {"type": "json_object"}
                try:
                    response = client.chat.completions.create(**request)
                except Exception as groq_exc:  # noqa: BLE001
                    err_low = str(groq_exc).lower()
                    if json_mode and ("failed_generation" in err_low or "json" in err_low):
                        request.pop("response_format", None)
                        response = client.chat.completions.create(**request)
                    else:
                        raise
                text = (response.choices[0].message.content or "").strip()
            else:
                response = client.models.generate_content(
                    model=get_model_name(),
                    contents=prompt,
                    config=_gemini_generation_config(
                        system_instruction=system_instruction,
                        temperature=temperature,
                        json_mode=json_mode,
                    ),
                )
                text = (response.text or "").strip()
            if not text:
                raise LLMError(f"{provider.title()} không trả về nội dung. Vui lòng thử lại.")
            return text
        except LLMError:
            raise
        except Exception as exc:  # noqa: BLE001 — SDK ném nhiều loại lỗi khác nhau
            last_exc = exc
            transient = "503" in str(exc) or "UNAVAILABLE" in str(exc).upper()
            if provider == "gemini" and transient and attempt == 0:
                time.sleep(2)
                continue
            break
    raise LLMError(_friendly_llm_error(last_exc or Exception("unknown"), provider)) from last_exc


def _generate_stream(
    prompt: str,
    *,
    system_instruction: str,
    temperature: float = 0.2,
) -> Any:
    """Yield visible text chunks; retry Gemini only before the first chunk."""
    provider = get_provider()
    client = _get_client(provider)
    attempts = 2 if provider == "gemini" else 1
    for attempt in range(attempts):
        yielded = False
        try:
            if provider == "groq":
                stream = client.chat.completions.create(
                    model=get_model_name(),
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                    max_tokens=1200,
                    stream=True,
                    **_groq_reasoning_options(),
                )
                for chunk in stream:
                    text = chunk.choices[0].delta.content
                    if isinstance(text, str) and text:
                        yielded = True
                        yield text
            else:
                config = _gemini_generation_config(
                    system_instruction=system_instruction,
                    temperature=temperature,
                    json_mode=False,
                )
                for response in client.models.generate_content_stream(
                    model=get_model_name(),
                    contents=prompt,
                    config=config,
                ):
                    text = response.text or ""
                    if text:
                        yielded = True
                        yield text
            if not yielded:
                raise LLMError(f"{provider.title()} không trả về nội dung. Vui lòng thử lại.")
            return
        except LLMError:
            raise
        except Exception as exc:  # noqa: BLE001 — SDK ném nhiều loại lỗi khác nhau
            transient = "503" in str(exc) or "UNAVAILABLE" in str(exc).upper()
            if provider == "gemini" and not yielded and transient and attempt == 0:
                time.sleep(1)
                continue
            raise LLMError(_friendly_llm_error(exc, provider)) from exc


def _to_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str, indent=None)


# --------------------------------------------------------------------------------------
# System instruction & Schema context
# --------------------------------------------------------------------------------------
BASE_SYSTEM_INSTRUCTION = """
Bạn là chuyên viên BI cho TMDB 5000, trả lời bằng TIẾNG VIỆT, khách quan và thận trọng.
- Chỉ dùng số có trong JSON đầu vào; không bịa, suy đoán hay tự tính tổng, chênh lệch hoặc tỷ lệ. Chỉ đổi cách trình bày/đơn vị và so sánh thứ hạng hiển nhiên; thiếu dữ liệu thì nói rõ.
- Mô tả quan sát/tương quan, không khẳng định nhân quả; không tư vấn đầu tư, dự báo hay kết luận ngoài phạm vi. Payload rỗng thì không có số để nêu.
- USD: số phim có phân cách hàng nghìn; phần trăm 1–2 chữ số. `roi`/`roi_median` là thập phân (0.5 = 50%), cần nhân 100 khi trình bày; `pct_*`/`*_pct` đã là %, không nhân thêm. Điểm rating theo thang 10.
- Giữ nguyên tên phim/hãng/thể loại. Doanh thu, lợi nhuận, ROI chỉ phản ánh phim `is_finance_valid = 1`; dữ liệu 2016–2017 chưa đầy đủ.
- Full Credit ghi nhận toàn bộ phim ở mỗi nhóm; Weighted chia theo `weight_factor`. Giá trị theo nhóm là phân bổ, không phải kết quả kế toán riêng của nhóm. ROI trung vị là trung vị ROI từng phim.
""".strip()

DDS_SCHEMA_CONTEXT = """
=== Schema DDS: chỉ dùng 12 bảng, luôn ghi tiền tố dds. ===
fact_movie (1 dòng/phim): movie_sk int, date_sk int, language_sk int, budget numeric, revenue numeric, profit numeric, roi numeric (thập phân), runtime numeric (phút), popularity numeric, vote_average numeric (thang 10), vote_count int, is_finance_valid int, is_revenue_over_budget int, movie_count int.
dim_movie: movie_sk, movie_nk, title, original_title, status, runtime_band, budget_band, country_count, country_type (không có SK -1).
dim_date: date_sk, full_date, day, month (1–12), month_name, quarter, year, decade.
dim_genre: genre_sk, genre_nk, genre_name.
dim_company: company_sk, company_nk, company_name.
dim_country: country_sk, country_code, country_name, region.
dim_language: language_sk, language_nk, language_name, language_group.
dim_keyword: keyword_sk, keyword_nk, keyword_name, theme_group (Adaptation, Sequel, Superhero, Other, Unknown).
bridge_movie_genre: movie_sk, genre_sk, weight_factor numeric.
bridge_movie_company: movie_sk, company_sk, weight_factor numeric.
bridge_movie_country: movie_sk, country_sk, weight_factor numeric.
bridge_movie_keyword: movie_sk, keyword_sk (không có weight_factor).
Nối fact/dim movie/bridge theo movie_sk; fact.date_sk→dim_date.date_sk; fact.language_sk→dim_language.language_sk; bridge *_sk→SK của dim tương ứng.

=== Data Contract bắt buộc ===
1. Một câu SELECT hoặc WITH ... SELECT; không dấu `;` giữa câu lệnh. Cấm INSERT/UPDATE/DELETE/DROP/ALTER/TRUNCATE/CREATE/GRANT/REVOKE/COPY/EXECUTE/CALL/PG_SLEEP và pg_catalog/pg_shadow/pg_roles.
2. Tài chính dùng `f.is_finance_valid = 1` (budget > 0 và revenue > 0). `roi` thập phân: không `AVG(roi)`/`SUM(roi)`; dùng median `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY f.roi)` hoặc ROI gộp `SUM(profit) / NULLIF(SUM(budget), 0)`. Rating median dùng `PERCENTILE_CONT` và `vote_count > 0`.
3. Năm/tháng lấy từ `dim_date` qua `f.date_sk`, dùng bí danh `d.year`, `d.month`. Lọc thuộc tính bridge mà không nhân dòng fact bằng `EXISTS`; không JOIN nhiều bridge rồi SUM trực tiếp.
4. Full Credit mặc định, không nhân `weight_factor`. Weighted chỉ nhân revenue/profit theo bridge đang nhóm; không nhân ROI, rating hay số đếm. Kết quả theo nhóm là giá trị phân bổ.
5. Keyword không có trọng số; đếm `COUNT(DISTINCT movie_sk)`, và loại trùng `(movie_sk, theme_group)` trước khi tính thống kê theo theme.
6. Các dim có Unknown SK = -1 (ngoại trừ dim_movie); loại Unknown khi nhóm/xếp hạng. Danh sách/top phải có ORDER BY và LIMIT tối đa 50.
7. Tên phim lấy từ `dim_movie.title`; đặt alias rõ nghĩa. Tiền trong DB là USD, có thể đổi sang triệu/tỷ với alias `_m`/`_bn`.
8. Dữ liệu kết thúc khoảng 2017, 2016–2017 chưa đầy đủ; vẫn truy vấn năm người dùng hỏi. Nguồn ngoài TMDB, dự báo, hay yêu cầu ghi/sửa/xóa dữ liệu: `can_answer=false`.
9. Lọc quốc gia qua `dds.dim_country`: ưu tiên `country_code` ISO-2 (Mỹ='US', Nhật='JP', Anh='GB', Pháp='FR', Đức='DE', Trung Quốc='CN', Hàn Quốc='KR', Ấn Độ='IN') hoặc tên đầy đủ (`'United States of America'`, `'Japan'`). Khi hỏi phim "cùng sản xuất" giữa 2 quốc gia A và B, dùng 2 điều kiện `EXISTS` riêng biệt trên `dds.bridge_movie_country` JOIN `dds.dim_country`.
""".strip()

_SQL_JSON_FORMAT = """
Trả về DUY NHẤT một đối tượng JSON hợp lệ với đúng 3 khóa sau (không thêm văn bản nào khác, không markdown):
{"can_answer": true|false, "sql": "<câu SELECT/WITH trên 1 dòng hoặc chuỗi rỗng>", "reason": "<giải thích ngắn bằng tiếng Việt>"}
- can_answer = true: "sql" là MỘT câu SELECT/WITH hợp lệ cho PostgreSQL, viết trên MỘT dòng duy nhất (dùng dấu cách thay cho xuống dòng để không vỡ JSON); "reason" mô tả ngắn cách tính.
- can_answer = false: "sql" là chuỗi rỗng; "reason" là lời giải thích lịch sự bằng tiếng Việt vì sao không thể trả lời
  (nguồn ngoài TMDB, dự báo tương lai, hoặc yêu cầu thay đổi dữ liệu).
""".strip()

_SQL_SYSTEM_INSTRUCTION = (
    "Bạn là kỹ sư dữ liệu PostgreSQL chuyên viết truy vấn chỉ-đọc cho Data Warehouse TMDB 5000 Movies. "
    "Bạn tuyệt đối tuân thủ schema và Data Contract bên dưới, không bịa tên bảng/cột.\n\n"
    + DDS_SCHEMA_CONTEXT
)

_WRITE_INTENT = re.compile(
    r"\b(drop|delete|truncate|alter|insert|update|create|grant|revoke)\b"
    r"|\b(xóa|xoá|sửa|cập nhật|thêm|chèn|ghi đè)\s+(dữ liệu|bảng|dòng|bản ghi|phim|cột|database|csdl)",
    re.IGNORECASE,
)

_ALLOCATION_LABELS = {"full": "Full Credit (không chia trọng số)", "weighted": "Weighted (chia 1/k theo weight_factor)"}


# --------------------------------------------------------------------------------------
# 1) Tóm tắt KPI điều hành
# --------------------------------------------------------------------------------------
def stream_kpi_summary(filters: dict, kpi_records: list, top_movies: list) -> Any:
    """Stream an executive summary grounded only in supplied KPI rows."""
    payload = {
        "bo_loc_hien_tai": filters,
        "kpi": kpi_records,
        "top_5_phim_loi_nhuan_cao_nhat": top_movies,
    }
    prompt = (
        "Dưới đây là payload JSON gồm bộ lọc hiện tại, các KPI đã được tính từ PostgreSQL và Top 5 phim có lợi nhuận cao nhất "
        "trong phạm vi lọc.\n\n"
        f"PAYLOAD:\n{_to_json(payload)}\n\n"
        "NHIỆM VỤ: Viết tóm tắt tiếng Việt gồm ĐÚNG 4–5 gạch đầu dòng Markdown, súc tích:\n"
        "- Gạch 1: Phạm vi lọc (năm, thể loại, chế độ phân bổ) và quy mô: tổng số phim, số phim hợp lệ tài chính.\n"
        "- Gạch 2: Doanh thu và lợi nhuận tổng (in đậm số liệu chính bằng **...**).\n"
        "- Gạch 3: ROI trung vị và tỷ lệ phim có doanh thu vượt ngân sách (in đậm), kèm điểm đánh giá trung vị nếu có.\n"
        "- Gạch 4: Phim nổi bật trong Top 5 (nêu tên phim và lợi nhuận, in đậm tên/số chính).\n"
        "- Gạch 5 (tùy chọn): Một lưu ý ngắn về giới hạn phương pháp luận liên quan đến bộ lọc hiện tại.\n"
        "Không viết tiêu đề, không lời chào, không thêm đoạn văn ngoài các gạch đầu dòng. Chỉ dùng số trong payload."
    )
    return _generate_stream(prompt, system_instruction=BASE_SYSTEM_INSTRUCTION, temperature=0.2)


def generate_kpi_summary(filters: dict, kpi_records: list, top_movies: list) -> str:
    """Synchronous compatibility wrapper for consumers that do not stream."""
    return "".join(stream_kpi_summary(filters, kpi_records, top_movies))


# --------------------------------------------------------------------------------------
# 2) Giải thích xu hướng chẩn đoán
# --------------------------------------------------------------------------------------
def stream_business_question_explanation(
    topic_title: str,
    allocation_mode: str,
    data_records: Any,
) -> Any:
    """Stream a grounded explanation for one business question and its basis tables."""
    if (
        isinstance(data_records, dict)
        and isinstance(data_records.get("tables"), dict)
    ):
        limited_records = {
            "filters": data_records.get("filters"),
            "tables": {
                table: rows[:MAX_DIAG_ROWS]
                for table, rows in data_records["tables"].items()
            },
        }
    elif isinstance(data_records, dict):
        limited_records = {
            table: rows[:MAX_DIAG_ROWS]
            for table, rows in data_records.items()
        }
    else:
        limited_records = data_records[:MAX_DIAG_ROWS]
    payload = {
        "chu_de": topic_title,
        "che_do_phan_bo": _ALLOCATION_LABELS.get(str(allocation_mode).lower(), str(allocation_mode)),
        "bang_du_lieu": limited_records,
    }
    prompt = (
        "Dưới đây là bảng dữ liệu chẩn đoán đã được PostgreSQL tính sẵn.\n\n"
        f"PAYLOAD:\n{_to_json(payload)}\n\n"
        "NHIỆM VỤ: Viết phần giải thích ngắn bằng tiếng Việt theo đúng ba mục Markdown:\n"
        "### Xu hướng chính\n- 1–3 gạch đầu dòng, chỉ nêu xu hướng thấy trực tiếp trong các bảng.\n"
        "### Điểm nổi bật / Nghịch lý\n- Nêu điểm đáng chú ý nếu dữ liệu thể hiện; nếu không có, nói rõ chưa thấy điểm nổi bật.\n"
        "### Lưu ý phương pháp luận\n- Nêu một giới hạn phù hợp (phân bổ, nhóm chồng lấn, ngưỡng lượt bình chọn, dữ liệu 2016–2017 hoặc cỡ mẫu).\n"
        "Chỉ dùng số trong bảng; chỉ mô tả tương quan/xu hướng, không khẳng định nhân quả. Không lời chào, không tiêu đề."
    )
    return _generate_stream(prompt, system_instruction=BASE_SYSTEM_INSTRUCTION, temperature=0.2)


def explain_diagnostic_trend(topic_title: str, allocation_mode: str, data_records: Any) -> str:
    """Synchronous compatibility wrapper for diagnostic explanations."""
    return "".join(
        stream_business_question_explanation(topic_title, allocation_mode, data_records)
    )


def stream_dashboard_charts_explanation(
    scope_text: str,
    allocation_mode: str,
    charts_payload: list[dict],
    user_focus: str = "",
) -> Any:
    """Stream a cross-chart explanation grounded in at most 20 rows per selected chart."""
    if not 1 <= len(charts_payload) <= 4:
        raise ValueError("Chọn từ 1 đến 4 biểu đồ để phân tích.")

    chart_records = []
    for chart in charts_payload:
        frame = chart.get("df")
        if not isinstance(frame, pd.DataFrame):
            raise TypeError(f"Dữ liệu biểu đồ {chart.get('chart_id', '')} không phải DataFrame.")
        chart_records.append(
            {
                "chart_id": chart["chart_id"],
                "page": chart["page"],
                "title": chart["title"],
                "description": chart["description"],
                "total_rows": len(frame),
                "rows_sent": df_to_clean_records(frame.head(20)),
            }
        )

    focus = (user_focus or "").strip()
    payload = {
        "filters": scope_text,
        "allocation_mode": _ALLOCATION_LABELS.get(
            str(allocation_mode).lower(), str(allocation_mode)
        ),
        "user_focus": focus,
        "charts": chart_records,
    }
    if len(chart_records) == 1:
        output_requirements = (
            "Chỉ phân tích biểu đồ đã chọn, theo đúng ba mục:\n"
            "### Xu hướng chính\n### Biến động / Điểm bất thường nổi bật\n### Lưu ý dữ liệu"
        )
    else:
        output_requirements = (
            "Phân tích từng biểu đồ đã chọn, sau đó liên kết các xu hướng/điểm khác biệt "
            "có thể quan sát giữa chúng. Dùng đúng các mục:\n"
            "### Điểm đáng chú ý theo biểu đồ\n"
            "### Mối liên hệ giữa các biểu đồ\n"
            "### Lưu ý dữ liệu"
        )
    focus_instruction = (
        f"Ưu tiên trả lời thẳng nghi vấn này bằng số liệu đã gửi: {focus}\n"
        if focus
        else ""
    )
    prompt = (
        "Dữ liệu dưới đây là kết quả thật do PostgreSQL tính cho các biểu đồ Power BI được chọn. "
        "Mỗi biểu đồ chỉ gửi tối đa 20 dòng; không suy rộng từ các dòng đã lược bỏ.\n\n"
        f"PAYLOAD:\n{_to_json(payload)}\n\n"
        f"{focus_instruction}"
        f"NHIỆM VỤ: {output_requirements}\n"
        "- Chỉ nêu số xuất hiện trong payload; không tự tính thêm, không bịa và giữ nguyên tên biểu đồ/nhóm.\n"
        "- Chỉ mô tả quan sát hoặc mối liên hệ; không khẳng định nhân quả tuyệt đối.\n"
        "- Nếu dữ liệu không cho thấy nghi vấn, nói rõ chưa đủ căn cứ. Kết luận gọn, không lời chào."
    )
    return _generate_stream(prompt, system_instruction=BASE_SYSTEM_INSTRUCTION, temperature=0.2)


# --------------------------------------------------------------------------------------
# 3) Text-to-SQL có kiểm duyệt
# --------------------------------------------------------------------------------------
def _strip_code_fence(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json|sql)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _parse_plan(raw: str) -> dict:
    """Parse JSON {can_answer, sql, reason}; chịu lỗi nếu model bọc thêm markdown/văn bản."""
    cleaned = _strip_code_fence(raw)
    data: Any = None
    try:
        data = json.loads(cleaned, strict=False)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(0), strict=False)
            except json.JSONDecodeError:
                data = None
    if not isinstance(data, dict):
        raise LLMError("Model trả về định dạng không hợp lệ khi sinh SQL. Vui lòng thử lại hoặc diễn đạt lại câu hỏi.")
    can_answer = data.get("can_answer")
    if isinstance(can_answer, str):
        can_answer = can_answer.strip().lower() == "true"
    sql = _strip_code_fence(str(data.get("sql") or "")).strip()
    return {
        "can_answer": bool(can_answer) and bool(sql),
        "sql": sql,
        "reason": str(data.get("reason") or "").strip(),
    }


def _plan_sql(question: str) -> dict:
    prompt = (
        f"CÂU HỎI CỦA NGƯỜI DÙNG (tiếng Việt):\n{question}\n\n"
        "Hãy quyết định có thể trả lời bằng dữ liệu schema dds hay không và sinh SQL nếu được.\n\n" + _SQL_JSON_FORMAT
    )
    raw = _generate(prompt, system_instruction=_SQL_SYSTEM_INSTRUCTION, temperature=0.0, json_mode=True)
    return _parse_plan(raw)


def _repair_sql(question: str, bad_sql: str, error_message: str) -> dict:
    prompt = (
        f"CÂU HỎI CỦA NGƯỜI DÙNG:\n{question}\n\n"
        f"CÂU SQL ĐÃ SINH (bị lỗi khi chạy trên PostgreSQL):\n{bad_sql}\n\n"
        f"THÔNG BÁO LỖI TỪ POSTGRESQL:\n{error_message[:1500]}\n\n"
        "Hãy sửa câu SQL cho đúng cú pháp PostgreSQL và đúng tên bảng/cột theo schema dds, vẫn tuân thủ toàn bộ Data Contract. "
        "Chỉ sửa những gì cần thiết để trả lời đúng câu hỏi ban đầu.\n\n" + _SQL_JSON_FORMAT
    )
    raw = _generate(prompt, system_instruction=_SQL_SYSTEM_INSTRUCTION, temperature=0.0, json_mode=True)
    return _parse_plan(raw)


def stream_text_to_sql_answer(question: str, sql: str, df: pd.DataFrame) -> Any:
    """Stream an answer grounded in the database result already returned to the UI."""
    if df is None or df.empty:
        yield (
            "Kho dữ liệu TMDB không có bản ghi nào thỏa mãn điều kiện của câu hỏi "
            "(truy vấn trả về 0 dòng), nên hệ thống không đưa ra số liệu nào."
        )
        return
    records = df_to_clean_records(df.head(MAX_ROWS_TO_LLM))
    payload = {
        "cau_hoi": question,
        "cau_sql_da_thuc_thi": sql,
        "tong_so_dong_tra_ve": int(len(df)),
        "so_dong_gui_kem": len(records),
        "ket_qua": records,
    }
    prompt = (
        "Dưới đây là kết quả THẬT do PostgreSQL trả về cho câu hỏi của người dùng.\n\n"
        f"PAYLOAD:\n{_to_json(payload)}\n\n"
        "NHIỆM VỤ: Trả lời câu hỏi bằng tiếng Việt, súc tích (2–5 câu hoặc vài gạch đầu dòng), bám sát bảng kết quả, "
        "in đậm các số liệu/tên chính. Chỉ dùng số trong 'ket_qua'. Nếu 'tong_so_dong_tra_ve' lớn hơn 'so_dong_gui_kem', "
        "nói rõ chỉ nhận xét trên các dòng đầu. Nếu truy vấn dùng chế độ Weighted/Full hay có giới hạn dữ liệu liên quan, nhắc ngắn gọn 1 câu. "
        "Nếu kết quả tổng hợp cho biết số phim bằng 0 hoặc giá trị tổng hợp là null, kết luận rõ kho dữ liệu không có bản ghi/giá trị "
        "thỏa điều kiện tương ứng; tuyệt đối không bịa số liệu. Không lặp lại câu SQL, không lời chào."
    )
    yield from _generate_stream(prompt, system_instruction=BASE_SYSTEM_INSTRUCTION, temperature=0.2)


def _interpret_result(question: str, sql: str, df: pd.DataFrame) -> str:
    """Synchronous compatibility wrapper for Text-to-SQL answer generation."""
    return "".join(stream_text_to_sql_answer(question, sql, df))


def _result(status: str, *, sql=None, dataframe=None, answer: str = "", error=None) -> dict:
    return {"status": status, "sql": sql, "dataframe": dataframe, "answer": answer, "error": error}


def prepare_text_to_sql(user_question: str) -> dict:
    """
    Generate and safely execute a Text-to-SQL plan, returning database results immediately:
        1. Model sinh {"can_answer", "sql", "reason"} (JSON có cấu trúc).
        2. validate_readonly_sql() -> run_query() (READ ONLY, timeout 10s); lỗi SQL => tự sửa đúng 1 lần.

    Trả về: {"status": "ok"|"out_of_scope"|"blocked"|"error",
             "sql": str|None, "dataframe": pd.DataFrame|None, "answer": str, "error": str|None}.
    Call stream_text_to_sql_answer() separately after displaying the returned dataframe.
    """
    question = (user_question or "").strip()
    if not question:
        return _result("error", answer="Vui lòng nhập câu hỏi.", error="empty_question")
    if len(question) > MAX_QUESTION_CHARS:
        question = question[:MAX_QUESTION_CHARS]

    # ---- Bước 1: sinh SQL có cấu trúc -------------------------------------------------
    try:
        plan = _plan_sql(question)
    except LLMError as exc:
        return _result("error", answer=str(exc), error=str(exc))

    if not plan["can_answer"]:
        reason = plan["reason"] or "Câu hỏi nằm ngoài phạm vi dữ liệu TMDB 5000 trong kho dữ liệu."
        status = "blocked" if _WRITE_INTENT.search(question) else "out_of_scope"
        return _result(status, answer=reason)

    # ---- Bước 2: kiểm duyệt & thực thi an toàn ----------------------------------------
    sql = plan["sql"]
    try:
        safe_sql = validate_readonly_sql(sql)
    except Exception as exc:  # noqa: BLE001 — validate_readonly_sql ném ValueError khi vi phạm
        return _result(
            "blocked",
            sql=sql,
            answer="Câu truy vấn do AI sinh ra đã bị lớp kiểm duyệt bảo mật chặn lại (hệ thống chỉ cho phép đọc dữ liệu).",
            error=str(exc),
        )

    df: pd.DataFrame | None = None
    try:
        df = run_query(safe_sql)
    except Exception as first_exc:  # noqa: BLE001 — lỗi cú pháp/tên cột/timeout từ PostgreSQL
        # Self-repair đúng 1 lần
        try:
            repaired = _repair_sql(question, safe_sql, str(first_exc))
        except LLMError as exc:
            return _result("error", sql=safe_sql, answer=str(exc), error=f"{first_exc} | {exc}")

        if not repaired["can_answer"]:
            return _result(
                "error",
                sql=safe_sql,
                answer="Hệ thống chưa thể xây dựng truy vấn phù hợp cho câu hỏi này. Hãy thử diễn đạt cụ thể hơn.",
                error=str(first_exc),
            )
        try:
            safe_sql = validate_readonly_sql(repaired["sql"])
        except Exception as exc:  # noqa: BLE001
            return _result(
                "blocked",
                sql=repaired["sql"],
                answer="Câu truy vấn đã sửa bị lớp kiểm duyệt bảo mật chặn lại.",
                error=str(exc),
            )
        try:
            df = run_query(safe_sql)
        except Exception as second_exc:  # noqa: BLE001
            return _result(
                "error",
                sql=safe_sql,
                answer=("Không thể thực thi truy vấn sau khi đã tự sửa lỗi. Vui lòng diễn đạt lại câu hỏi "
                        "hoặc kiểm tra kết nối PostgreSQL."),
                error=str(second_exc),
            )

    # Return the database result before asking the configured model to interpret it.
    if df is None or df.empty:
        return _result(
            "ok",
            sql=safe_sql,
            dataframe=pd.DataFrame() if df is None else df,
            answer=("Kho dữ liệu TMDB không có bản ghi nào thỏa mãn điều kiện của câu hỏi "
                    "(truy vấn trả về 0 dòng), nên hệ thống không đưa ra số liệu nào."),
        )

    return _result("ok", sql=safe_sql, dataframe=df)


def text_to_sql_and_answer(user_question: str) -> dict:
    """Compatibility API that returns both the read-only result and a complete answer."""
    result = prepare_text_to_sql(user_question)
    if result.get("status") != "ok" or result.get("dataframe") is None:
        return result
    try:
        result["answer"] = _interpret_result(
            (user_question or "").strip(),
            result.get("sql") or "",
            result["dataframe"],
        )
    except LLMError as exc:
        result["answer"] = (
            "Truy vấn đã chạy thành công nhưng chưa thể diễn giải bằng AI. "
            f"{exc} Bảng kết quả bên dưới là dữ liệu thật từ PostgreSQL."
        )
        result["error"] = str(exc)
    return result