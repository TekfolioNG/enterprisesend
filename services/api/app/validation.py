"""Parse and validate a billing file against the EnterpriseSend template.
A file with ANY problem is rejected before it is stored or sent to the AI check."""
import csv
import io
import re
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from zoneinfo import ZoneInfo

COLUMNS = ["account_id", "recipient_name", "primary_email", "phone_whatsapp",
           "invoice_amount", "bill_due_date", "scheduled_send_date", "description"]
LAGOS = ZoneInfo("Africa/Lagos")
MAX_ROWS = 5000
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NAME_RE = re.compile(r"^[\w .,'\-]{1,80}$")
PHONE_RE = re.compile(r"^234\d{10}$")


def _cell(value, column):
    if value is None:
        return ""
    if isinstance(value, datetime):
        fmt = "%Y-%m-%d" if column == "bill_due_date" else "%Y-%m-%d %H:%M:%S"
        return value.strftime(fmt)
    if isinstance(value, float) and value.is_integer() and column != "invoice_amount":
        return str(int(value))
    return str(value).strip()


def parse_file(filename: str, data: bytes) -> list:
    name = filename.lower()
    if name.endswith(".csv"):
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ValueError("CSV must be saved as UTF-8")
        reader = csv.reader(io.StringIO(text))
        table = [r for r in reader]
    elif name.endswith(".xlsx"):
        from openpyxl import load_workbook
        try:
            ws = load_workbook(io.BytesIO(data), read_only=True, data_only=True).worksheets[0]
        except Exception:
            raise ValueError("Could not read the Excel file")
        header = None
        table = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                header = [str(c or "").strip().lower() for c in row]
                table.append(header)
            else:
                table.append([_cell(v, header[j] if j < len(header) else "") for j, v in enumerate(row)])
    else:
        raise ValueError("Upload a .csv or .xlsx file")

    if not table:
        raise ValueError("The file is empty")
    header = [h.strip().lower() for h in table[0]]
    missing = [c for c in COLUMNS if c not in header]
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}. Download the template and use it as is.")
    body = [r for r in table[1:] if any(str(c).strip() for c in r)]
    if not body:
        raise ValueError("The file has no billing rows")
    if len(body) > MAX_ROWS:
        raise ValueError(f"Too many rows (limit {MAX_ROWS} per batch)")
    idx = {c: header.index(c) for c in COLUMNS}
    return [{c: (str(r[idx[c]]).strip() if idx[c] < len(r) else "") for c in COLUMNS} for r in body]


def validate_rows(rows: list, now: datetime | None = None):
    now = now or datetime.now(timezone.utc)
    errors, clean, seen = [], [], set()

    for n, r in enumerate(rows, start=2):  # spreadsheet row number (row 1 is the header)
        def bad(col, msg):
            errors.append({"row": n, "column": col, "message": msg})

        acc = r["account_id"]
        if not acc:
            bad("account_id", "Required")
        elif acc in seen:
            bad("account_id", f"Duplicate account ID '{acc}'")
        seen.add(acc)

        if not NAME_RE.match(r["recipient_name"]):
            bad("recipient_name", "Required, letters and numbers only, up to 80 characters")

        email = r["primary_email"].lower()
        if not EMAIL_RE.match(email):
            bad("primary_email", "Not a valid email address")

        phone = re.sub(r"[\s+\-]", "", r["phone_whatsapp"])
        if not PHONE_RE.match(phone):
            bad("phone_whatsapp", "Use international format starting 234, for example 2348012345678")

        kobo = None
        try:
            amount = Decimal(r["invoice_amount"].replace(",", ""))
            if amount <= 0 or amount != amount.quantize(Decimal("0.01")):
                raise InvalidOperation
            kobo = int(amount * 100)
        except (InvalidOperation, ValueError):
            bad("invoice_amount", "Must be a number greater than 0, with at most 2 decimals")

        due = None
        try:
            due = datetime.strptime(r["bill_due_date"], "%Y-%m-%d").date().isoformat()
        except ValueError:
            bad("bill_due_date", "Use YYYY-MM-DD")

        send_at = None
        try:
            local = datetime.strptime(r["scheduled_send_date"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=LAGOS)
            send_at = local.astimezone(timezone.utc)
            if send_at < now - timedelta(minutes=5):
                bad("scheduled_send_date", "Send time is in the past. Choose a time a few minutes from now or later")
        except ValueError:
            bad("scheduled_send_date", "Use YYYY-MM-DD HH:MM:SS (Lagos time)")

        if len(r["description"]) > 150:
            bad("description", "Up to 150 characters")

        if not any(e["row"] == n for e in errors):
            clean.append({"row": n, "account_id": acc, "recipient_name": r["recipient_name"],
                          "primary_email": email, "phone": phone, "amount_kobo": kobo,
                          "bill_due_date": due, "send_at": send_at.isoformat(),
                          "description": r["description"], "status": "pending"})
    return clean, errors


def build_template_xlsx() -> bytes:
    """Text-formatted cells so Excel keeps leading digits and date formats."""
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Billing"
    ws.append(COLUMNS)
    tomorrow = (datetime.now(LAGOS) + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
    ws.append(["A-001", "Ada Obi", "ada@example.com", "2348012345678", 50000,
               "2026-12-31", tomorrow, "First Term Tuition"])
    for col, letter in zip(COLUMNS, "ABCDEFGH"):
        fmt = "#,##0.00" if col == "invoice_amount" else "@"
        for cell in ws[letter][1:]:
            cell.number_format = fmt
        ws.column_dimensions[letter].width = 22
    guide = wb.create_sheet("Rules")
    for line in [
        "account_id: unique in the file", "recipient_name: letters and numbers, up to 80 characters",
        "primary_email: valid email address", "phone_whatsapp: international format starting 234",
        "invoice_amount: greater than 0, at most 2 decimals", "bill_due_date: YYYY-MM-DD",
        "scheduled_send_date: YYYY-MM-DD HH:MM:SS, Lagos time", "description: up to 150 characters",
        "Delete the example row before uploading. Do not rename or reorder the headings."]:
        guide.append([line])
    guide.column_dimensions["A"].width = 70
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
