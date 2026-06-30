# paste-to-sheet

Log social media posts or comments to the correct sheet tab in the tracking spreadsheet.

## Sheet structure

| Sheet tab       | Platforms accepted |
|-----------------|--------------------|
| Reddit          | reddit             |
| Quora           | quora              |
| YouTube         | youtube            |
| Facebook Groups | facebook           |
| X Communities   | x, twitter         |

Each tab has columns: Date · Title · Post · Comment · Post Link · Comment Link · Notes
(Quora adds a Platform column between Date and Title.)

## How to use this skill

The user will give you one of:
- A direct message describing one or more posts/comments with their platforms
- A text file path containing multiple entries

### Steps

1. Parse the user's input and extract entries. Each entry has:
   - `platform` (required): reddit / quora / youtube / facebook / x
   - `post` or `comment` (at least one): the actual text content
   - `title` (optional): post title or group/community name
   - `post_link` (optional): URL of the post

2. Convert to JSON and run `write_sheet.py` from the repo root:

**Single entry:**
```bash
python write_sheet.py '{"platform": "reddit", "post": "...", "title": "...", "post_link": "..."}'
```

**Multiple entries (batch):**
```bash
python write_sheet.py '[{"platform": "reddit", "post": "..."}, {"platform": "quora", "comment": "..."}]'
```

3. The script will:
   - Find the first empty row in the correct tab
   - Write today's date, the content, and the link
   - Print confirmation for each row written

4. Report back to the user: which platform, which row, and what was written.

## Notes
- `credentials.json` must exist in the repo root (gitignored)
- If dependencies are missing: `pip install google-auth google-auth-httplib2 google-api-python-client`
- Always use batch mode when handling multiple entries — one `write_sheet.py` call with a JSON array
