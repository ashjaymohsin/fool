#!/usr/bin/env python3
"""Write posts/comments to the correct platform sheet tab."""

import json
import sys
from datetime import datetime
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1XVkN3dyk1Xj-UNFj2kVRMe8APBDNTlCj2oY9car8Xzk"

PLATFORM_MAP = {
    "reddit": "Reddit",
    "quora": "Quora",
    "youtube": "YouTube",
    "facebook": "Facebook Groups",
    "x": "X Communities",
    "twitter": "X Communities",
}

# Column layout per sheet (0-indexed)
# Quora:       Date(0) Platform(1) Title(2) Post(3) Comment(4) PostLink(5) CommentLink(6) Notes(7)
# All others:  Date(0) Title(1)    Post(2)  Comment(3) PostLink(4) CommentLink(5) Notes(6)
QUORA_COLS = {"date": 0, "title": 2, "post": 3, "comment": 4, "post_link": 5}
DEFAULT_COLS = {"date": 0, "title": 1, "post": 2, "comment": 3, "post_link": 4}

_sheet_id_cache: dict[str, int] = {}


def get_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def col_letter(idx: int) -> str:
    result = ""
    while True:
        result = chr(ord("A") + idx % 26) + result
        idx = idx // 26 - 1
        if idx < 0:
            break
    return result


def get_sheet_id(service, sheet_name: str) -> int:
    if sheet_name not in _sheet_id_cache:
        meta = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        for s in meta["sheets"]:
            _sheet_id_cache[s["properties"]["title"]] = s["properties"]["sheetId"]
    return _sheet_id_cache[sheet_name]


def find_first_empty_row(service, sheet_name: str) -> int:
    """Return the 1-indexed row number of the first row where the Date column is empty."""
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{sheet_name}'!A:A",
    ).execute()
    values = result.get("values", [])
    for i, row in enumerate(values):
        if i == 0:
            continue  # skip header
        if not row or not row[0].strip():
            return i + 1  # 1-indexed
    return len(values) + 1  # append after last row


def format_row(service, sheet_name: str, row: int):
    """Apply Calibri 10pt + wrap to the written row."""
    sid = get_sheet_id(service, sheet_name)
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"requests": [{
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": row - 1,
                    "endRowIndex": row,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"fontFamily": "Calibri", "fontSize": 10},
                        "wrapStrategy": "WRAP",
                    }
                },
                "fields": "userEnteredFormat(textFormat,wrapStrategy)",
            }
        }]},
    ).execute()


def write_entry(platform: str, post: str = "", comment: str = "",
                title: str = "", post_link: str = ""):
    platform_key = platform.lower().strip()
    sheet_name = PLATFORM_MAP.get(platform_key)
    if not sheet_name:
        raise ValueError(f"Unknown platform: {platform}. Choose from: {', '.join(PLATFORM_MAP)}")

    cols = QUORA_COLS if sheet_name == "Quora" else DEFAULT_COLS
    service = get_service()
    row = find_first_empty_row(service, sheet_name)
    today = datetime.now().strftime("%d/%m/%y")

    updates = []

    def add(col_idx, value):
        if value:
            updates.append({
                "range": f"'{sheet_name}'!{col_letter(col_idx)}{row}",
                "values": [[value]],
            })

    add(cols["date"], today)
    if title:
        add(cols["title"], title)
    if post:
        add(cols["post"], post)
    if comment:
        add(cols["comment"], comment)
    if post_link:
        add(cols["post_link"], post_link)

    if not updates:
        print("Nothing to write.")
        return

    service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"valueInputOption": "USER_ENTERED", "data": updates},
    ).execute()

    format_row(service, sheet_name, row)

    kind = "post" if post else "comment"
    print(f"[{sheet_name}] Row {row}: wrote {kind} ({today})")


def process_batch(entries: list[dict]):
    for e in entries:
        write_entry(
            platform=e.get("platform", ""),
            post=e.get("post", ""),
            comment=e.get("comment", ""),
            title=e.get("title", ""),
            post_link=e.get("post_link", ""),
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python write_sheet.py '<json>'")
        print("JSON format (single): {\"platform\": \"reddit\", \"post\": \"...\", \"post_link\": \"...\"}")
        print("JSON format (batch):  [{\"platform\": \"reddit\", ...}, {\"platform\": \"quora\", ...}]")
        sys.exit(1)

    payload = json.loads(sys.argv[1])
    if isinstance(payload, list):
        process_batch(payload)
    else:
        write_entry(**{k: v for k, v in payload.items()})
