#!/usr/bin/env python3
"""Set uniform font size (10pt) across all data cells in every sheet tab."""

from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = Path(__file__).parent / "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1XVkN3dyk1Xj-UNFj2kVRMe8APBDNTlCj2oY9car8Xzk"


def get_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def main():
    service = get_service()
    ss = service.spreadsheets()

    meta = ss.get(spreadsheetId=SPREADSHEET_ID).execute()
    requests = []

    for sheet in meta["sheets"]:
        sid = sheet["properties"]["sheetId"]
        requests.append({
            "repeatCell": {
                "range": {"sheetId": sid},
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"fontSize": 10}
                    }
                },
                "fields": "userEnteredFormat.textFormat.fontSize",
            }
        })

    ss.batchUpdate(
        spreadsheetId=SPREADSHEET_ID,
        body={"requests": requests},
    ).execute()
    print(f"Font size set to 10pt across {len(requests)} sheet(s).")


if __name__ == "__main__":
    main()
