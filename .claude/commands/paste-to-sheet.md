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

2. **Reddit-specific — auto-search for thread link:**
   If the platform is Reddit and the user has NOT provided a `post_link`, check if the post or comment text references a specific Reddit thread, topic, or subreddit. If it does:
   - Use WebSearch to find the real Reddit thread URL (search for the topic + "reddit" or the subreddit name)
   - Use the most relevant result as `post_link`
   - If no confident match is found, leave `post_link` empty and mention it to the user

3. Convert to JSON and run the script:

**Single entry:**
```powershell
python "$env:USERPROFILE\.claude\write_sheet.py" '{"platform": "reddit", "post": "...", "title": "...", "post_link": "..."}'
```

**Multiple entries (batch):**
```powershell
python "$env:USERPROFILE\.claude\write_sheet.py" '[{"platform": "reddit", "post": "..."}, {"platform": "quora", "comment": "..."}]'
```

4. The script will:
   - Find the first empty row in the correct tab
   - Write today's date, the content, and the link
   - Print confirmation for each row written

5. Report back to the user: which platform, which row, what was written, and what link was found (if auto-searched).

## Notes
- `credentials.json` lives at `~/.claude/credentials.json` (never committed to git)
- If dependencies are missing: `pip install google-auth google-auth-httplib2 google-api-python-client`
- Always use batch mode when handling multiple entries — one script call with a JSON array
- For Reddit auto-search: prefer direct reddit.com thread links over subreddit homepages
