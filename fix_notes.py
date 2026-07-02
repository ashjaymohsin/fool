#!/usr/bin/env python3
"""Find cells whose display value looks like a note placeholder and replace with the note text."""

import re
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1XVkN3dyk1Xj-UNFj2kVRMe8APBDNTlCj2oY9car8Xzk"

PLACEHOLDER_RE = re.compile(r"click\s+(this\s+)?box\s+to\s+view\s+note", re.IGNORECASE)


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


def main():
    service = get_service()
    ss = service.spreadsheets()

    # Get all sheet names
    meta = ss.get(spreadsheetId=SPREADSHEET_ID).execute()
    sheets = [s["properties"]["title"] for s in meta["sheets"]]
    print(f"Sheets: {sheets}")

    updates = []

    for sheet_name in sheets:
        # Fetch cell data including notes
        result = ss.get(
            spreadsheetId=SPREADSHEET_ID,
            ranges=[f"'{sheet_name}'"],
            includeGridData=True,
            fields="sheets.data.rowData.values(formattedValue,note)",
        ).execute()

        rows = result["sheets"][0].get("data", [{}])[0].get("rowData", [])
        for r_idx, row in enumerate(rows):
            for c_idx, cell in enumerate(row.get("values", [])):
                value = cell.get("formattedValue", "")
                note = cell.get("note", "")
                if note and (PLACEHOLDER_RE.search(value) or not value.strip()):
                    cell_ref = f"'{sheet_name}'!{col_letter(c_idx)}{r_idx + 1}"
                    print(f"  Replacing {cell_ref}: '{value}' → note text ({len(note)} chars)")
                    updates.append({
                        "range": cell_ref,
                        "values": [[note]],
                    })

    if not updates:
        print("No placeholder cells found.")
        return

    ss.values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"valueInputOption": "RAW", "data": updates},
    ).execute()
    print(f"\nDone — updated {len(updates)} cell(s).")


if __name__ == "__main__":
    main()
