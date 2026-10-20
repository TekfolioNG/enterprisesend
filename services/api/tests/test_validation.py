import io
from datetime import datetime, timezone

import pytest
from openpyxl import Workbook

from app.validation import COLUMNS, build_template_xlsx, parse_file, validate_rows

NOW = datetime(2026, 11, 1, tzinfo=timezone.utc)
GOOD = ["A-1", "Ada Obi", "ada@example.com", "2348012345678", "50,000.00",
        "2026-12-31", "2026-12-01 09:00:00", "First Term Tuition"]


def csv_bytes(*rows):
    lines = [",".join(COLUMNS)] + [",".join(f'"{c}"' for c in r) for r in rows]
    return "\n".join(lines).encode()


def test_template_roundtrip_is_valid():
    rows = parse_file("t.xlsx", build_template_xlsx())
    clean, errors = validate_rows(rows)
    assert errors == [] and clean[0]["amount_kobo"] == 5_000_000


def test_good_csv_converts_amount_and_time_to_utc():
    clean, errors = validate_rows(parse_file("a.csv", csv_bytes(GOOD)), NOW)
    assert not errors
    assert clean[0]["amount_kobo"] == 5_000_000
    assert clean[0]["send_at"].startswith("2026-12-01T08:00:00")  # Lagos is UTC+1


def test_problems_are_reported_by_row_and_column():
    bad = list(GOOD); bad[0] = "A-2"; bad[3] = "08012345678"; bad[4] = "-5"
    dup = list(GOOD)
    _, errors = validate_rows(parse_file("a.csv", csv_bytes(GOOD, bad, dup)), NOW)
    found = {(e["row"], e["column"]) for e in errors}
    assert {(3, "phone_whatsapp"), (3, "invoice_amount"), (4, "account_id")} <= found


def test_past_send_time_rejected():
    old = list(GOOD); old[6] = "2026-10-01 09:00:00"
    _, errors = validate_rows(parse_file("a.csv", csv_bytes(old)), NOW)
    assert errors and errors[0]["column"] == "scheduled_send_date"


def test_excel_numeric_phone_survives():
    wb = Workbook(); ws = wb.active
    ws.append(COLUMNS)
    ws.append(["A-1", "Ada Obi", "ada@example.com", 2348012345678, 50000,
               "2026-12-31", "2026-12-01 09:00:00", "Fees"])
    buf = io.BytesIO(); wb.save(buf)
    clean, errors = validate_rows(parse_file("a.xlsx", buf.getvalue()), NOW)
    assert not errors and clean[0]["phone"] == "2348012345678"


def test_missing_column_and_bad_type():
    with pytest.raises(ValueError):
        parse_file("a.csv", b"account_id,recipient_name\nA,B")
    with pytest.raises(ValueError):
        parse_file("a.pdf", b"x")
