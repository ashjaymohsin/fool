#!/usr/bin/env python3
"""Overwrite Reddit comment cells (col F) in the FastFBIApostille sheet.

Usage:
    python update_comments_fbi.py <edits.json>

edits.json maps row number -> new comment text, e.g.
    {"5": "shorter text", "11": "shorter text"}

Only column F (Comment 1 Text) of the listed rows is touched. Nothing else
in the sheet is changed. Preview is printed and confirmation required before
writing (pass --yes to skip the prompt).
"""
import json
import sys

from write_sheet_fbi import get_service, SPREADSHEET_ID, col_letter, format_row

SHEET = "Reddit"          # FBI sheet: no trailing space
COMMENT_COL = 5           # col F, 0-indexed


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    auto = "--yes" in sys.argv
    if not args:
        print("Usage: python update_comments_fbi.py <edits.json> [--yes]")
        sys.exit(1)

    edits = json.load(open(args[0]))
    service = get_service()
    col = col_letter(COMMENT_COL)

    print(f"About to overwrite column {col} (Reddit comment) on these rows:\n")
    for row in sorted(edits, key=int):
        preview = edits[row].replace("\n", " ")
        print(f"  row {row}: {preview[:80]}{'...' if len(preview) > 80 else ''}")

    if not auto:
        if input("\nProceed? [y/N] ").strip().lower() != "y":
            print("Aborted. Nothing written.")
            return

    data = [{"range": f"'{SHEET}'!{col}{row}", "values": [[edits[row]]]}
            for row in edits]
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"valueInputOption": "USER_ENTERED", "data": data},
    ).execute()

    for row in edits:
        format_row(service, SHEET, int(row))

    print(f"\nUpdated {len(edits)} comment(s): rows {', '.join(sorted(edits, key=int))}.")


if __name__ == "__main__":
    main()
