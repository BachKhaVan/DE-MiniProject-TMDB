#!/usr/bin/env python3
"""Read-only validation for the TMDB source files and Mage pipelines."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple


ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "test" / "results"
MOVIES_CSV = ROOT / "data" / "raw" / "tmdb_5000_movies.csv"
CREDITS_CSV = ROOT / "data" / "raw" / "tmdb_5000_credits.csv"
BATCH_CSV = ROOT / "data" / "raw" / "tmdb_new_batch.csv"
NULL_VALUES = {
    "",
    "#N/A",
    "#N/A N/A",
    "#NA",
    "-1.#IND",
    "-1.#QNAN",
    "-NaN",
    "-nan",
    "1.#IND",
    "1.#QNAN",
    "<NA>",
    "N/A",
    "NA",
    "NaN",
    "NULL",
    "None",
    "n/a",
    "nan",
    "null",
}
ID_PATTERN = re.compile(r"^[+-]?\d+$")


@dataclass
class Check:
    status: str
    name: str
    expected: str
    actual: str
    details: str = ""
    remediation: str = ""


@dataclass
class CsvStats:
    path: Path
    header: List[str] = field(default_factory=list)
    rows: List[List[Optional[str]]] = field(default_factory=list)
    error: str = ""
    malformed_rows: int = 0
    duplicate_rows: int = 0
    key_nulls: int = 0
    key_duplicates: int = 0
    invalid_ids: int = 0
    missing_required_rows: int = 0
    clean_rows: Optional[int] = None
    clean_ids: Set[str] = field(default_factory=set)
    ids: Set[str] = field(default_factory=set)
    release_date_invalid: int = 0

    @property
    def row_count(self) -> int:
        return len(self.rows)

    @property
    def column_count(self) -> int:
        return len(self.header)


@dataclass
class ComposeConfig:
    service: str
    database: str
    user: str


def is_null(value: Optional[str]) -> bool:
    return value is None or value in NULL_VALUES


def canonical_number(value: str) -> Optional[str]:
    try:
        number = Decimal(value)
    except InvalidOperation:
        return None
    if not number.is_finite():
        return None
    normalized = number.normalize()
    if normalized == normalized.to_integral_value():
        return str(normalized.quantize(Decimal(1)))
    return format(normalized, "f")


def normalize_id(value: Optional[str]) -> Optional[str]:
    if is_null(value):
        return None
    text = value or ""
    numeric = canonical_number(text)
    if numeric is not None and Decimal(numeric) == Decimal(numeric).to_integral_value():
        return str(int(Decimal(numeric)))
    return None


def parse_release_date(value: Optional[str]) -> bool:
    if is_null(value):
        return False
    text = (value or "").strip()
    for format_string in (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S",
    ):
        try:
            datetime.strptime(text, format_string)
            return True
        except ValueError:
            pass
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def read_csv_stats(path: Path, key_column: str, clean_columns: Sequence[str]) -> CsvStats:
    stats = CsvStats(path=path)
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as source:
            reader = csv.reader(source)
            stats.header = next(reader, [])
            if not stats.header:
                stats.error = "CSV không có header hoặc file rỗng."
                return stats

            for row in reader:
                if len(row) != len(stats.header):
                    stats.malformed_rows += 1
                padded = list(row[: len(stats.header)])
                padded.extend([None] * (len(stats.header) - len(padded)))
                stats.rows.append(
                    [None if is_null(value) else value for value in padded]
                )
    except FileNotFoundError:
        stats.error = "Không tìm thấy file."
        return stats
    except (OSError, UnicodeError, csv.Error) as error:
        stats.error = "{}: {}".format(type(error).__name__, error)
        return stats

    if key_column not in stats.header:
        stats.error = "Thiếu cột khóa {!r} trong header.".format(key_column)
        return stats

    key_index = stats.header.index(key_column)
    stats.key_nulls = sum(1 for row in stats.rows if row[key_index] is None)

    key_counts: Dict[str, int] = {}
    for row in stats.rows:
        normalized = normalize_id(row[key_index])
        if row[key_index] is not None and normalized is None:
            stats.invalid_ids += 1
        if normalized is not None:
            stats.ids.add(normalized)
            key_counts[normalized] = key_counts.get(normalized, 0) + 1
    stats.key_duplicates = sum(count - 1 for count in key_counts.values() if count > 1)

    numeric_columns: Set[int] = set()
    for index in range(len(stats.header)):
        non_null = [row[index] for row in stats.rows if row[index] is not None]
        if non_null and all(canonical_number(value or "") is not None for value in non_null):
            numeric_columns.add(index)

    def canonical_row(row: Sequence[Optional[str]]) -> Tuple[Optional[str], ...]:
        values: List[Optional[str]] = []
        for index, value in enumerate(row):
            if value is None:
                values.append(None)
            elif index in numeric_columns:
                values.append(canonical_number(value))
            else:
                values.append(value)
        return tuple(values)

    unique_rows: List[List[Optional[str]]] = []
    seen_rows: Set[Tuple[Optional[str], ...]] = set()
    for row in stats.rows:
        normalized = canonical_row(row)
        if normalized not in seen_rows:
            seen_rows.add(normalized)
            unique_rows.append(row)
    stats.duplicate_rows = len(stats.rows) - len(unique_rows)

    key_name = key_column
    required_indices = [stats.header.index(name) for name in clean_columns if name in stats.header]
    if len(required_indices) != len(clean_columns):
        stats.error = "Thiếu cột cần thiết để tính số dòng sau làm sạch."
        return stats

    cleaned = [
        row
        for row in unique_rows
        if all(row[index] is not None for index in required_indices)
    ]
    stats.missing_required_rows = len(unique_rows) - len(cleaned)
    stats.clean_rows = None if stats.malformed_rows else len(cleaned)
    stats.clean_ids = {
        normalized
        for row in cleaned
        if (normalized := normalize_id(row[stats.header.index(key_name)])) is not None
    }

    if "release_date" in stats.header:
        release_index = stats.header.index("release_date")
        stats.release_date_invalid = sum(
            1 for row in cleaned if not parse_release_date(row[release_index])
        )
    return stats


def load_dotenv(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except FileNotFoundError:
        return values
    except (OSError, UnicodeError):
        return values

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped[7:].lstrip()
        key, separator, value = stripped.partition("=")
        if not separator:
            continue
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        else:
            value = value.split("#", 1)[0].rstrip()
        values[key] = value
    return values


def strip_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def resolve_compose_value(
    raw_value: str, dotenv: Dict[str, str]
) -> Optional[str]:
    value = strip_yaml_scalar(raw_value)
    match = re.fullmatch(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?:(:-|-)(.*))?\}", value)
    if match is None:
        return value or None
    variable, operator, default = match.groups()
    resolved = os.environ.get(variable)
    if resolved is None:
        resolved = dotenv.get(variable)
    if resolved is not None and (resolved != "" or operator not in {":-", "-"}):
        return resolved
    if operator in {":-", "-"}:
        return default or None
    return None


def read_compose_config(compose_path: Path, dotenv_path: Path) -> ComposeConfig:
    text = compose_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    try:
        services_index = next(
            index for index, line in enumerate(lines) if re.match(r"^services:\s*$", line)
        )
    except StopIteration as error:
        raise ValueError("compose.yaml không có mục services.") from error

    service_blocks: List[Tuple[str, List[str]]] = []
    current_name: Optional[str] = None
    current_lines: List[str] = []
    for line in lines[services_index + 1 :]:
        if line.strip() and not line.startswith(" "):
            break
        match = re.match(r"^  ([A-Za-z0-9_-]+):\s*$", line)
        if match:
            if current_name is not None:
                service_blocks.append((current_name, current_lines))
            current_name = match.group(1)
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)
    if current_name is not None:
        service_blocks.append((current_name, current_lines))

    dotenv = load_dotenv(dotenv_path)
    for service_name, block in service_blocks:
        values: Dict[str, str] = {}
        in_environment = False
        for line in block:
            if re.match(r"^    environment:\s*$", line):
                in_environment = True
                continue
            if in_environment and line.strip() and len(line) - len(line.lstrip()) < 6:
                in_environment = False
            if in_environment:
                match = re.match(
                    r"^\s{6}(POSTGRES_DB|POSTGRES_USER):\s*(.*?)\s*$", line
                )
                if match:
                    values[match.group(1)] = match.group(2)
        if "POSTGRES_DB" in values and "POSTGRES_USER" in values:
            database = resolve_compose_value(values["POSTGRES_DB"], dotenv)
            user = resolve_compose_value(values["POSTGRES_USER"], dotenv)
            if database and user:
                return ComposeConfig(service=service_name, database=database, user=user)
            raise ValueError(
                "Không xác định được POSTGRES_DB/POSTGRES_USER từ compose.yaml và .env."
            )
    raise ValueError(
        "Không tìm thấy service PostgreSQL có POSTGRES_DB và POSTGRES_USER "
        "trong compose.yaml."
    )


def read_password_secrets(dotenv_path: Path) -> List[str]:
    secrets: List[str] = []
    for key, value in load_dotenv(dotenv_path).items():
        if "PASSWORD" in key.upper() and value:
            secrets.append(value)
    value = os.environ.get("POSTGRES_PASSWORD")
    if value:
        secrets.append(value)
    return secrets


def redact(text: str, secrets: Sequence[str]) -> str:
    cleaned = text
    for secret in secrets:
        cleaned = cleaned.replace(secret, "[REDACTED]")
    return cleaned.strip()


class Validator:
    def __init__(self, flow: str) -> None:
        self.flow = flow
        self.started = time.monotonic()
        self.checks: List[Check] = []
        self.csv_stats: Dict[str, CsvStats] = {}
        self.db_context = "Chưa kết nối"
        self.db_counts: Dict[str, Optional[int]] = {
            "movies": None,
            "credits": None,
        }
        self.db_key_duplicates: Dict[str, Optional[int]] = {
            "movies": None,
            "credits": None,
        }
        self.db_ids: Dict[str, Set[str]] = {"movies": set(), "credits": set()}
        self.watermark = "Chưa kiểm tra"
        self.db_config: Optional[ComposeConfig] = None
        self.secrets = read_password_secrets(ROOT / ".env")
        self.db_connected = False

    def add(
        self,
        status: str,
        name: str,
        expected: str,
        actual: str,
        details: str = "",
        remediation: str = "",
    ) -> None:
        self.checks.append(
            Check(status, name, expected, actual, details, remediation)
        )

    def inspect_csv(
        self,
        label: str,
        path: Path,
        key_column: str,
        clean_columns: Sequence[str],
        required_header: Sequence[str],
    ) -> Optional[CsvStats]:
        stats = read_csv_stats(path, key_column, clean_columns)
        self.csv_stats[label] = stats
        if stats.error:
            self.add(
                "FAIL",
                "{} CSV đọc được".format(label),
                "File hợp lệ tại {}".format(path.relative_to(ROOT)),
                stats.error,
                remediation="Đặt đúng CSV nguồn/batch và kiểm tra encoding, header, định dạng.",
            )
            return None

        missing = [name for name in required_header if name not in stats.header]
        duplicate_headers = len(stats.header) != len(set(stats.header))
        header_status = "PASS" if not missing and not duplicate_headers else "FAIL"
        header_details = ""
        if missing:
            header_details += "Thiếu cột: {}. ".format(", ".join(missing))
        if duplicate_headers:
            header_details += "Header có tên cột bị trùng."
        self.add(
            header_status,
            "{} CSV header".format(label),
            "Có các cột {}".format(", ".join(required_header)),
            "{} cột: {}".format(stats.column_count, ", ".join(stats.header)),
            header_details,
            "Đối chiếu header với CSV TMDB tương ứng." if header_details else "",
        )

        shape_status = "PASS" if stats.malformed_rows == 0 else "FAIL"
        self.add(
            shape_status,
            "{} CSV số dòng/cột".format(label),
            "Mỗi dòng có {} cột".format(stats.column_count),
            "{} dòng dữ liệu, {} cột; {} dòng sai số cột".format(
                stats.row_count, stats.column_count, stats.malformed_rows
            ),
            remediation="Sửa các dòng CSV không khớp số cột." if stats.malformed_rows else "",
        )
        self.add(
            "FAIL" if stats.row_count == 0 else "PASS",
            "{} CSV có dữ liệu".format(label),
            "Ít nhất một dòng dữ liệu",
            str(stats.row_count),
            remediation="Khôi phục CSV nguồn/batch có dữ liệu."
            if stats.row_count == 0
            else "",
        )
        key_status = (
            "FAIL"
            if label == "Incremental batch" and stats.key_nulls
            else ("WARN" if stats.key_nulls else "PASS")
        )
        self.add(
            key_status,
            "{} CSV khóa null".format(label),
            "Không có null ở {}".format(key_column),
            str(stats.key_nulls),
            "Full Load loại dòng thiếu khóa; incremental append không tự làm sạch."
            if stats.key_nulls
            else "",
        )
        key_duplicate_status = (
            "FAIL"
            if label == "Incremental batch" and stats.key_duplicates
            else ("WARN" if stats.key_duplicates else "PASS")
        )
        self.add(
            key_duplicate_status,
            "{} CSV khóa trùng".format(label),
            "Không có ID khóa lặp",
            str(stats.key_duplicates),
            "Full Load chỉ loại dòng trùng toàn bộ; hai dòng có cùng khóa nhưng nội dung khác nhau vẫn có thể còn."
            if stats.key_duplicates
            else "",
        )
        self.add(
            "FAIL" if stats.invalid_ids else "PASS",
            "{} CSV ID hợp lệ".format(label),
            "ID khóa là số nguyên hoặc null",
            str(stats.invalid_ids),
            remediation="Sửa ID không phải số nguyên." if stats.invalid_ids else "",
        )
        duplicate_status = (
            "FAIL"
            if label == "Incremental batch" and stats.duplicate_rows
            else ("WARN" if stats.duplicate_rows else "PASS")
        )
        duplicate_expected = (
            "Không có dòng trùng vì incremental exporter append nguyên batch"
            if label == "Incremental batch"
            else "Không có dòng trùng hoặc Full Load loại theo drop_duplicates"
        )
        self.add(
            duplicate_status,
            "{} CSV dòng trùng hoàn toàn".format(label),
            duplicate_expected,
            str(stats.duplicate_rows),
            "Incremental exporter không loại dòng trùng."
            if label == "Incremental batch" and stats.duplicate_rows
            else "",
            "Loại dòng batch trùng trước khi chạy exporter."
            if label == "Incremental batch" and stats.duplicate_rows
            else "",
        )
        if label == "Incremental batch":
            self.add(
                "PASS",
                "Incremental batch số dòng được append",
                "Exporter append nguyên các dòng CSV",
                str(stats.row_count),
            )
        elif stats.clean_rows is not None:
            self.add(
                "PASS",
                "{} số dòng sau quy tắc làm sạch Full Load".format(label),
                "drop_duplicates rồi bỏ dòng thiếu {}".format(
                    ", ".join(clean_columns)
                ),
                str(stats.clean_rows),
                "release_date không hợp lệ/null: {}; transformer chỉ coerce, không loại dòng."
                .format(stats.release_date_invalid)
                if "release_date" in stats.header
                else "",
            )
            if label != "Incremental batch":
                self.add(
                    "WARN" if stats.missing_required_rows else "PASS",
                    "{} dòng thiếu cột khóa bắt buộc".format(label),
                    "0 hoặc được loại theo transformer Full Load",
                    str(stats.missing_required_rows),
                    remediation="Full Load sẽ bỏ dòng thiếu khóa/cột bắt buộc."
                    if stats.missing_required_rows
                    else "",
                )
        return stats

    def inspect_sources(self) -> None:
        movies = self.inspect_csv(
            "Movies",
            MOVIES_CSV,
            "id",
            ("id", "title"),
            ("id", "title"),
        )
        credits = self.inspect_csv(
            "Credits",
            CREDITS_CSV,
            "movie_id",
            ("movie_id",),
            ("movie_id",),
        )

        if self.flow in {"incremental", "all"}:
            batch = self.inspect_csv(
                "Incremental batch",
                BATCH_CSV,
                "id",
                ("id",),
                ("id", "title"),
            )
            if batch is not None and movies is not None:
                compatible = set(batch.header) == set(movies.header)
                self.add(
                    "PASS" if compatible else "FAIL",
                    "Batch header tương thích movies",
                    "Cùng tập cột với tmdb_5000_movies.csv",
                    "Tương thích" if compatible else "Không tương thích",
                    "Thứ tự cột có thể khác nhau." if compatible else "Header batch phải cùng tập cột với movies.",
                    "Sửa header batch theo CSV movies." if not compatible else "",
                )
        if movies is None or credits is None:
            return
        if movies.clean_rows is None or credits.clean_rows is None:
            self.add(
                "FAIL",
                "Tính baseline Full Load",
                "CSV baseline có cấu trúc hợp lệ",
                "Không thể tính chính xác do dòng sai số cột.",
                remediation="Sửa CSV rồi chạy lại script.",
            )

    def psql_query(self, sql: str) -> Any:
        if self.db_config is None:
            raise RuntimeError("Chưa đọc được cấu hình PostgreSQL từ compose.yaml.")
        wrapped = (
            "SELECT COALESCE(json_agg(row_to_json(validation_rows)), '[]'::json)::text "
            "FROM ({}) AS validation_rows".format(sql)
        )
        command = [
            "docker",
            "compose",
            "exec",
            "-T",
            self.db_config.service,
            "psql",
            "-X",
            "-A",
            "-t",
            "-v",
            "ON_ERROR_STOP=1",
            "-U",
            self.db_config.user,
            "-d",
            self.db_config.database,
            "-c",
            wrapped,
        ]
        try:
            result = subprocess.run(
                command,
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=35,
                check=False,
            )
        except FileNotFoundError as error:
            raise RuntimeError("Không tìm thấy lệnh docker trong PATH.") from error
        except subprocess.TimeoutExpired as error:
            raise RuntimeError("Lệnh psql vượt quá thời gian chờ 35 giây.") from error
        if result.returncode != 0:
            message = result.stderr or result.stdout or "psql trả exit code khác 0."
            raise RuntimeError(redact(message[-2000:], self.secrets))
        output = result.stdout.strip()
        if not output:
            return []
        try:
            return json.loads(output.splitlines()[-1])
        except json.JSONDecodeError as error:
            raise RuntimeError(
                "Không đọc được kết quả JSON từ psql: {}".format(
                    redact(output[-500:], self.secrets)
                )
            ) from error

    def query_check(
        self, name: str, sql: str, remediation: str = ""
    ) -> Optional[Any]:
        try:
            return self.psql_query(sql)
        except (RuntimeError, OSError) as error:
            self.add(
                "FAIL",
                name,
                "Truy vấn chỉ đọc chạy thành công",
                str(error),
                remediation=remediation or "Kiểm tra Docker Engine, container PostgreSQL và cấu hình .env.",
            )
            return None

    @staticmethod
    def first_row(result: Any) -> Optional[Dict[str, Any]]:
        if isinstance(result, list) and result and isinstance(result[0], dict):
            return result[0]
        return None

    def inspect_database(self) -> None:
        try:
            self.db_config = read_compose_config(
                ROOT / "compose.yaml", ROOT / ".env"
            )
            self.db_context = "service={}, database={}, configured user={}".format(
                self.db_config.service,
                self.db_config.database,
                self.db_config.user,
            )
            self.add(
                "PASS",
                "Đọc cấu hình PostgreSQL từ Compose",
                "Service/database/user xác định từ compose.yaml và .env",
                self.db_context,
            )
        except (OSError, UnicodeError, ValueError) as error:
            self.add(
                "FAIL",
                "Đọc cấu hình PostgreSQL từ Compose",
                "Cấu hình service/database/user rõ ràng",
                str(error),
                remediation="Kiểm tra compose.yaml và POSTGRES_DB/POSTGRES_USER trong .env.",
            )
            return

        configured_password = bool(
            os.environ.get("POSTGRES_PASSWORD")
            or load_dotenv(ROOT / ".env").get("POSTGRES_PASSWORD")
        )
        self.add(
            "PASS" if configured_password else "WARN",
            "POSTGRES_PASSWORD đã cấu hình",
            "Compose có giá trị POSTGRES_PASSWORD (không ghi giá trị vào báo cáo)",
            "Đã có" if configured_password else "Chưa tìm thấy trong môi trường hoặc .env",
            remediation="Tạo .env từ .env.example và đặt mật khẩu cục bộ."
            if not configured_password
            else "",
        )

        connection = self.query_check(
            "Kết nối PostgreSQL qua docker compose exec -T",
            "SELECT current_database() AS database, current_user AS username",
        )
        row = self.first_row(connection)
        if row is None:
            return
        actual_database = str(row.get("database", ""))
        actual_user = str(row.get("username", ""))
        connection_matches = (
            actual_database == self.db_config.database
            and actual_user == self.db_config.user
        )
        self.db_connected = True
        self.add(
            "PASS" if connection_matches else "FAIL",
            "Database/user kết nối thực tế",
            "{}/{}".format(self.db_config.database, self.db_config.user),
            "{}/{}".format(actual_database, actual_user),
            remediation="Đồng nhất POSTGRES_DB/POSTGRES_USER trong .env với cấu hình Compose."
            if not connection_matches
            else "",
        )

        columns = self.query_check(
            "Schema cột và kiểu dữ liệu Stage",
            """
            SELECT table_name, column_name, data_type, udt_name, ordinal_position
            FROM information_schema.columns
            WHERE table_schema = 'stage'
              AND table_name IN ('stg_tmdb_movies', 'stg_tmdb_credits')
            ORDER BY table_name, ordinal_position
            """,
            remediation="Chạy Full Load để tạo lại bảng staging hoặc kiểm tra schema stage.",
        )
        if columns is not None:
            column_report: Dict[str, List[str]] = {
                "stg_tmdb_movies": [],
                "stg_tmdb_credits": [],
            }
            for item in columns:
                table = str(item.get("table_name", ""))
                if table in column_report:
                    column_report[table].append(
                        "{}:{} ({}/{})".format(
                            item.get("column_name"),
                            item.get("ordinal_position"),
                            item.get("data_type"),
                            item.get("udt_name"),
                        )
                    )
            missing_keys = []
            for table, key in (
                ("stg_tmdb_movies", "id"),
                ("stg_tmdb_credits", "movie_id"),
            ):
                names = {
                    str(item.get("column_name"))
                    for item in columns
                    if item.get("table_name") == table
                }
                if key not in names:
                    missing_keys.append("{}.{}".format(table, key))
            self.add(
                "FAIL" if missing_keys else "PASS",
                "Cột khóa Stage tồn tại; kiểu dữ liệu được liệt kê",
                "movies.id và credits.movie_id",
                "movies [{}]; credits [{}]".format(
                    ", ".join(column_report["stg_tmdb_movies"]) or "bảng/cột không thấy",
                    ", ".join(column_report["stg_tmdb_credits"]) or "bảng/cột không thấy",
                ),
                "Thiếu: {}".format(", ".join(missing_keys)) if missing_keys else "",
                "Chạy Full Load hoặc kiểm tra schema." if missing_keys else "",
            )

        for label, table, key in (
            ("movies", "stg_tmdb_movies", "id"),
            ("credits", "stg_tmdb_credits", "movie_id"),
        ):
            rows = self.query_check(
                "Row count Stage {}".format(label),
                "SELECT COUNT(*) AS row_count FROM stage.{}".format(table),
                remediation="Chạy Full Load hoặc kiểm tra bảng stage.{}".format(table),
            )
            row = self.first_row(rows)
            if row is not None:
                self.db_counts[label] = int(row["row_count"])
                self.add(
                    "PASS",
                    "Đếm dòng stage.{}".format(table),
                    "Truy vấn COUNT(*) thành công",
                    str(self.db_counts[label]),
                )

            metrics = self.query_check(
                "Khóa null/trùng Stage {}".format(label),
                """
                SELECT
                    COUNT(*) FILTER (WHERE {key} IS NULL) AS null_keys,
                    COALESCE((
                        SELECT SUM(key_count - 1)
                        FROM (
                            SELECT COUNT(*) AS key_count
                            FROM stage.{table}
                            WHERE {key} IS NOT NULL
                            GROUP BY {key}
                            HAVING COUNT(*) > 1
                        ) AS duplicate_keys
                    ), 0) AS duplicate_keys
                FROM stage.{table}
                """.format(key=key, table=table),
                remediation="Kiểm tra batch trùng và quy tắc làm sạch của pipeline.",
            )
            row = self.first_row(metrics)
            if row is not None:
                null_keys = int(row["null_keys"])
                duplicate_keys = int(row["duplicate_keys"])
                self.db_key_duplicates[label] = duplicate_keys
                self.add(
                    "FAIL" if null_keys else "PASS",
                    "Stage {} không có khóa null".format(label),
                    "0",
                    str(null_keys),
                )
                self.add(
                    "FAIL" if duplicate_keys else "PASS",
                    "Stage {} không có khóa trùng".format(label),
                    "0",
                    str(duplicate_keys),
                    remediation="Không append lại incremental batch; reload baseline và dùng ID mới."
                    if duplicate_keys
                    else "",
                )

            identifiers = self.query_check(
                "Đọc ID Stage {}".format(label),
                "SELECT DISTINCT {key} AS id FROM stage.{table} WHERE {key} IS NOT NULL".format(
                    key=key, table=table
                ),
            )
            if identifiers is not None:
                self.db_ids[label] = {
                    normalized
                    for item in identifiers
                    if (normalized := normalize_id(str(item.get("id")))) is not None
                }

        relation = self.query_check(
            "Đối chiếu khóa movies/credits",
            """
            SELECT
                (SELECT COUNT(*) FROM (
                    SELECT DISTINCT m.id
                    FROM stage.stg_tmdb_movies AS m
                    INNER JOIN stage.stg_tmdb_credits AS c ON c.movie_id = m.id
                    WHERE m.id IS NOT NULL
                ) AS matched_movies) AS matched_movie_ids,
                (SELECT COUNT(*) FROM (
                    SELECT DISTINCT c.movie_id
                    FROM stage.stg_tmdb_credits AS c
                    LEFT JOIN stage.stg_tmdb_movies AS m ON m.id = c.movie_id
                    WHERE c.movie_id IS NOT NULL AND m.id IS NULL
                ) AS orphan_credit_ids) AS orphan_credit_ids,
                (SELECT COUNT(*) FROM (
                    SELECT DISTINCT m.id
                    FROM stage.stg_tmdb_movies AS m
                    LEFT JOIN stage.stg_tmdb_credits AS c ON c.movie_id = m.id
                    WHERE m.id IS NOT NULL AND c.movie_id IS NULL
                ) AS movies_without_credits) AS movies_without_credits
            """,
            remediation="Đối chiếu ID của hai CSV nguồn và các bảng staging.",
        )
        row = self.first_row(relation)
        if row is not None:
            orphans = int(row["orphan_credit_ids"])
            self.add(
                "WARN" if orphans else "PASS",
                "Credits mồ côi và movies khớp credits",
                "Không có credit ID không thuộc movies; phim không có credits có thể hợp lệ",
                "Khớp {} ID; {} credit ID mồ côi; {} phim không có credits".format(
                    row["matched_movie_ids"],
                    orphans,
                    row["movies_without_credits"],
                ),
                "Batch incremental hiện không cung cấp file credits; phim mới không có credits không bị coi là lỗi."
                if row["movies_without_credits"]
                else "",
            )

        table_exists = self.query_check(
            "Kiểm tra bảng control.etl_watermark",
            "SELECT to_regclass('control.etl_watermark') IS NOT NULL AS exists",
        )
        row = self.first_row(table_exists)
        if row is None:
            return
        if not row.get("exists"):
            self.watermark = "Bảng không tồn tại"
            self.add(
                "WARN",
                "Watermark tồn tại",
                "control.etl_watermark có sẵn",
                self.watermark,
                "Project hiện không khởi tạo bảng này trong postgres/init.",
                "Nếu cần demo watermark, tạo/cấu hình bảng theo hướng dẫn nhóm trước khi chạy block.",
            )
            return
        watermark_rows = self.query_check(
            "Đọc watermark tmdb_incremental",
            """
            SELECT pipeline_name, lset
            FROM control.etl_watermark
            WHERE pipeline_name = 'tmdb_incremental'
            """,
        )
        row = self.first_row(watermark_rows)
        if row is None:
            self.watermark = "Không có dòng tmdb_incremental"
            self.add(
                "WARN",
                "Watermark có giá trị lset",
                "Có một dòng tmdb_incremental",
                self.watermark,
                "LSET không chứng minh exporter đã chạy thành công.",
                "Tạo/khởi tạo watermark trước khi chạy block get_watermark.",
            )
        else:
            self.watermark = str(row.get("lset"))
            self.add(
                "PASS",
                "Watermark quan sát được",
                "Ghi nhận giá trị hiện tại, không dùng làm bằng chứng export",
                "pipeline_name={}, lset={}".format(
                    row.get("pipeline_name"), row.get("lset")
                ),
                "Metadata hiện không nối update_watermark sau export_incremental_stage.",
            )

    def compare_full_counts(self) -> None:
        if self.flow == "all":
            self.add(
                "PASS",
                "Full Load baseline dự kiến",
                "Nguồn sau quy tắc làm sạch được tính từ CSV",
                "Movies={}, credits={}".format(
                    self.csv_stats["Movies"].clean_rows
                    if self.csv_stats.get("Movies")
                    else "không có",
                    self.csv_stats["Credits"].clean_rows
                    if self.csv_stats.get("Credits")
                    else "không có",
                ),
                "Flow all bao gồm batch append nên so sánh stage chính ở kiểm tra incremental.",
            )
            return
        for label in ("Movies", "Credits"):
            stats = self.csv_stats.get(label)
            table = "movies" if label == "Movies" else "credits"
            expected = stats.clean_rows if stats else None
            actual = self.db_counts[table]
            if expected is None or actual is None:
                continue
            matches = expected == actual
            self.add(
                "PASS" if matches else "FAIL",
                "Full Load row count {}".format(label),
                str(expected),
                str(actual),
                "Movies clean rule: drop_duplicates + non-null id/title; credits: drop_duplicates + non-null movie_id."
                if label == "Movies"
                else "Credits clean rule: drop_duplicates + non-null movie_id.",
                "Chạy tmdb_ingestion; kiểm tra CSV và bảng stage."
                if not matches
                else "",
            )

    def compare_incremental(self) -> None:
        movies = self.csv_stats.get("Movies")
        credits = self.csv_stats.get("Credits")
        batch = self.csv_stats.get("Incremental batch")
        if batch is None or batch.error:
            return
        if movies is None or movies.clean_rows is None:
            self.add(
                "FAIL",
                "Incremental baseline movies",
                "Movies baseline tính được",
                "Không có baseline CSV hợp lệ",
                remediation="Đặt CSV nguồn và sửa lỗi header/định dạng trước.",
            )
            return

        overlapping_ids = batch.ids & movies.clean_ids
        self.add(
            "FAIL" if overlapping_ids else "PASS",
            "Incremental batch ID mới so với baseline",
            "Không trùng ID movies nguồn",
            "{} ID trùng".format(len(overlapping_ids)),
            "ID trùng mẫu: {}".format(", ".join(sorted(overlapping_ids)[:10]))
            if overlapping_ids
            else "",
            "Dùng batch ID mới và reload baseline trước khi thử lại."
            if overlapping_ids
            else "",
        )
        invalid_batch_ids = [
            row[batch.header.index("id")]
            for row in batch.rows
            if row[batch.header.index("id")] is not None
            and normalize_id(row[batch.header.index("id")]) is None
        ]
        if invalid_batch_ids:
            self.add(
                "FAIL",
                "Incremental batch ID dạng số nguyên",
                "ID số nguyên",
                "{} ID không hợp lệ".format(len(invalid_batch_ids)),
            )
        batch_ids = {
            normalize_id(row[batch.header.index("id")])
            for row in batch.rows
            if row[batch.header.index("id")] is not None
        }
        batch_ids.discard(None)
        missing_ids = batch_ids - self.db_ids["movies"]
        self.add(
            "FAIL" if missing_ids else "PASS",
            "Incremental ID xuất hiện trong stage.movies",
            "{} ID batch hợp lệ".format(len(batch_ids)),
            "{} ID chưa có trong stage".format(len(missing_ids)),
            "Thiếu ID mẫu: {}".format(", ".join(sorted(missing_ids)[:10]))
            if missing_ids
            else "",
            "Chạy các block load/export theo thứ tự rồi kiểm tra log exporter."
            if missing_ids
            else "",
        )

        duplicate_count = self.db_key_duplicates["movies"]
        self.add(
            "FAIL" if duplicate_count is None or duplicate_count else "PASS",
            "Incremental không tạo khóa trùng trong stage.movies",
            "0 khóa trùng",
            "Chưa truy vấn được" if duplicate_count is None else str(duplicate_count),
            remediation="Không chạy lặp exporter; reload Full Load baseline trước lần test kế tiếp."
            if duplicate_count
            else "",
        )

        actual_movies = self.db_counts["movies"]
        expected_movies = movies.clean_rows + batch.row_count
        if actual_movies is not None:
            self.add(
                "PASS" if actual_movies == expected_movies else "FAIL",
                "Incremental row count movies",
                "{} (baseline {} + {} dòng CSV được append)".format(
                    expected_movies, movies.clean_rows, batch.row_count
                ),
                str(actual_movies),
                "Exporter append trực tiếp; dự kiến đếm toàn bộ dòng batch, kể cả dòng không hợp lệ."
                if batch.key_nulls or batch.key_duplicates or batch.malformed_rows
                else "",
                "Đảm bảo đã chạy Full Load đúng baseline và export batch đúng một lần."
                if actual_movies != expected_movies
                else "",
            )

        actual_credits = self.db_counts["credits"]
        expected_credits = credits.clean_rows if credits else None
        if actual_credits is not None and expected_credits is not None:
            matches = actual_credits == expected_credits
            self.add(
                "PASS" if matches else "WARN",
                "Incremental row count credits",
                "{} (batch hiện không có CSV credits)".format(expected_credits),
                str(actual_credits),
                "Movies mới không có credits không bị coi là lỗi theo thiết kế batch hiện tại.",
                "Nếu credits thay đổi, xác minh có chạy Full Load hoặc tác vụ khác không."
                if not matches
                else "",
            )

    def run(self) -> None:
        self.inspect_sources()
        self.inspect_database()
        if self.flow in {"full", "all"}:
            self.compare_full_counts()
        if self.flow in {"incremental", "all"}:
            self.compare_incremental()

    @staticmethod
    def markdown_cell(value: str) -> str:
        return str(value).replace("|", "\\|").replace("\n", "<br>")

    def render_report(self) -> str:
        elapsed = time.monotonic() - self.started
        lines = [
            "# Báo cáo kiểm tra TMDB",
            "",
            "- Thời gian chạy: `{}`".format(datetime.now().astimezone().isoformat(timespec="seconds")),
            "- Luồng: `{}`".format(self.flow),
            "- Thời lượng: `{:.2f}s`".format(elapsed),
            "- Kết nối: `{}`".format(self.db_context),
            "- Mật khẩu: không được đọc/ghi vào báo cáo.",
            "",
            "## Kết quả kiểm tra",
            "",
            "| Trạng thái | Kiểm tra | Mong đợi | Thực tế | Chi tiết / cách xử lý |",
            "|---|---|---|---|---|",
        ]
        if not self.checks:
            lines.append("| WARN | Chưa có kiểm tra | Có kết quả | Không có | Xem lại cấu hình chạy script. |")
        for check in self.checks:
            detail = " ".join(
                part for part in (check.details, check.remediation) if part
            )
            lines.append(
                "| {} | {} | {} | {} | {} |".format(
                    self.markdown_cell(check.status),
                    self.markdown_cell(check.name),
                    self.markdown_cell(check.expected),
                    self.markdown_cell(check.actual),
                    self.markdown_cell(detail),
                )
            )

        lines.extend(
            [
                "",
                "## Tóm tắt CSV",
                "",
                "| Tệp | Dòng dữ liệu | Số cột | Dòng trùng hoàn toàn | Khóa null | Khóa trùng | Dòng dự kiến sau Full Load |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        if not self.csv_stats:
            lines.append("| Không đọc được CSV | - | - | - | - | - | - |")
        for label, stats in self.csv_stats.items():
            lines.append(
                "| {} (`{}`) | {} | {} | {} | {} | {} | {} |".format(
                    self.markdown_cell(label),
                    self.markdown_cell(str(stats.path.relative_to(ROOT))),
                    stats.row_count if not stats.error else "-",
                    stats.column_count if stats.header else "-",
                    stats.duplicate_rows if not stats.error else "-",
                    stats.key_nulls if not stats.error else "-",
                    stats.key_duplicates if not stats.error else "-",
                    (
                        "— (append nguyên batch)"
                        if label == "Incremental batch"
                        else (stats.clean_rows if stats.clean_rows is not None else "-")
                    ),
                )
            )

        failed = sum(1 for check in self.checks if check.status == "FAIL")
        warned = sum(1 for check in self.checks if check.status == "WARN")
        passed = sum(1 for check in self.checks if check.status == "PASS")
        conclusion = "FAIL" if failed else ("WARN" if warned else "PASS")
        lines.extend(
            [
                "",
                "## Kết luận",
                "",
                "**{}** — PASS: {}, WARN: {}, FAIL: {}.".format(
                    conclusion, passed, warned, failed
                ),
                "",
                "Watermark quan sát: `{}`. Giá trị watermark không chứng minh "
                "export thành công hoặc batch đã được lọc theo LSET.".format(
                    self.markdown_cell(self.watermark)
                ),
                "",
            ]
        )
        return "\n".join(lines)


def new_report_path() -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stem = "validation_{}".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    candidate = RESULTS_DIR / (stem + ".md")
    suffix = 1
    while candidate.exists():
        candidate = RESULTS_DIR / "{}_{}.md".format(stem, suffix)
        suffix += 1
    return candidate


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only checks for TMDB CSV sources and Mage pipeline results."
    )
    parser.add_argument(
        "--flow",
        choices=("full", "incremental", "all"),
        default="all",
        help="Chọn luồng kiểm tra (mặc định: all).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    validator = Validator(args.flow)
    try:
        validator.run()
    except (OSError, UnicodeError, csv.Error, ValueError, RuntimeError) as error:
        validator.add(
            "FAIL",
            "Lỗi khi chạy kiểm tra",
            "Tạo báo cáo kết quả",
            redact("{}: {}".format(type(error).__name__, error), validator.secrets),
            remediation="Xem lại cấu hình/file đầu vào; script không sửa database.",
        )

    try:
        report_path = new_report_path()
        report_path.write_text(validator.render_report(), encoding="utf-8")
    except OSError as error:
        print(
            "Không thể tạo báo cáo trong test/results: {}".format(error),
            file=sys.stderr,
        )
        return 2

    failed = any(check.status == "FAIL" for check in validator.checks)
    print("Báo cáo: {}".format(report_path.relative_to(ROOT)))
    print(
        "Kết quả: {} PASS, {} WARN, {} FAIL".format(
            sum(check.status == "PASS" for check in validator.checks),
            sum(check.status == "WARN" for check in validator.checks),
            sum(check.status == "FAIL" for check in validator.checks),
        )
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
