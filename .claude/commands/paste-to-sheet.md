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

---

## Rules (apply to ALL platforms)

### 1. Post vs Comment column
- If the entry is a **post**, write the content in the `post` field — never in `comment`
- If the entry is a **comment**, write the content in the `comment` field — never in `post`
- Never mix them up regardless of platform

### 2. Title
- If a title is provided, use it
- If no title is provided and the entry is a **post**, generate a short descriptive title (5–10 words) based on the content and write it in the `title` field
- Comments do not need a generated title unless one is clearly implied

### 3. Post Link logic
- **For posts:** put the subreddit, channel, group, or community name/URL where the post will be made in `post_link` (e.g. `r/Annapolis`, `https://www.facebook.com/groups/...`, YouTube channel URL, etc.)
- **For comments:** search for the actual URL of the thread/post/video being commented on and put that in `post_link`. Use WebSearch to find it if not provided. If no confident match is found, leave it empty and tell the user.

---

## Steps

1. Parse the user's input and extract all entries. Each entry has:
   - `platform` (required): reddit / quora / youtube / facebook / x
   - `post` OR `comment` (required, never both): the content
   - `title`: provided or auto-generated for posts
   - `post_link`: subreddit/community for posts, thread URL for comments

2. For comment entries without a `post_link`, use WebSearch to find the thread URL before writing.

3. Convert to JSON and run the script:

**Single entry:**
```powershell
python "$env:USERPROFILE\.claude\write_sheet.py" '{"platform": "reddit", "post": "...", "title": "...", "post_link": "r/example"}'
```

**Multiple entries (batch):**
```powershell
python "$env:USERPROFILE\.claude\write_sheet.py" '[{"platform": "reddit", "post": "...", "title": "...", "post_link": "r/example"}, {"platform": "quora", "comment": "...", "post_link": "https://quora.com/..."}]'
```

4. The script will:
   - Find the first empty row in the correct tab
   - Write today's date, title, post or comment content, and link
   - Print confirmation for each row written

5. Report back: platform, row number, what was written, and what link was used or found.

---

## Notes
- `credentials.json` lives at `~/.claude/credentials.json` (never committed to git)
- If dependencies are missing: `pip install google-auth google-auth-httplib2 google-api-python-client`
- Always use batch mode for multiple entries — one script call with a JSON array
- For WebSearch on comments: prefer direct links to the specific thread/video/post, not homepage or profile pages
