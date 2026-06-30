#!/usr/bin/env python3
"""Write posts/comments to the correct platform sheet tab."""

import json
import sys
from datetime import datetime
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Look in ~/.claude/ first, then fall back to script directory
_CLAUDE_DIR = Path.home() / ".claude"
CREDENTIALS_FILE = (
    _CLAUDE_DIR / "credentials.json"
    if (_CLAUDE_DIR / "credentials.json").exists()
    else Path(__file__).parent / "credentials.json"
)

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

QUORA_COLS = {"date": 0, "title": 2, "post": 3, "comment": 4, "post_link": 5}
DEFAULT_COLS = {"date": 0, "title": 1, "post": 2, "comment": 3, "post_link": 4}


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


def find_first_empty_row(service, sheet_name: str) -> int:
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"'{sheet_name}'!A:A",
    ).execute()
    values = result.get("values", [])
    for i, row in enumerate(values):
        if i == 0:
            continue
        if not row or not row[0].strip():
            return i + 1
    return len(values) + 1


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
        sys.exit(1)

    payload = json.loads(sys.argv[1])
    if isinstance(payload, list):
        process_batch(payload)
    else:
        write_entry(**{k: v for k, v in payload.items()})
