# paste-to-sheet

Log social media posts or comments to the correct sheet tab in the tracking spreadsheet.

## Sheet column layouts (0-indexed)

**Reddit** (`Reddit ` tab — note trailing space in tab name):
`#(A) · Date(B) · Title(C) · Posts(D) · Subreddit(E) · Comment 1 Text(F) · Comment 2 Text(G) · Post Link(H) · Comment Link 1(I)`

**Quora**: `Date(A) · Platform(B) · Title(C) · Post(D) · Comment(E) · Post Link(F) · Comment Link(G) · Notes(H)`

**YouTube / Facebook Groups / X Communities**: `Date(A) · Title(B) · Post(C) · Comment(D) · Post Link(E) · Comment Link(F) · Notes(G)`

## Rules for each field

| Field | Reddit | Other platforms |
|-------|--------|-----------------|
| Date | Col B (auto today) | Col A (auto today) |
| Title | Col C | Col B |
| Post text | Col D — only for posts | Col C — only for posts |
| Comment text | Col F — only for comments | Col D — only for comments |
| Subreddit | Col E — the subreddit URL (e.g. reddit.com/r/dogs/) | n/a |
| Post link | Col H — thread URL (comments only) | Col E — thread URL (comments only) |
| Comment link | Col I — direct comment permalink | Col F — direct comment permalink |

**NEVER mix post and comment fields.** If it's a post → use `post` field only. If it's a comment → use `comment` field only.

**NEVER overwrite existing data.** Always append after the last used row.

For Reddit posts: put the subreddit URL in `subreddit` field.  
For Reddit comments: put the thread URL in `post_link` and the comment permalink in `comment_link` if available.  
For posts without a title: generate a short descriptive title.  
For comments on other platforms: auto-search for the thread URL using WebSearch.

## Steps

1. Parse the user's input. Each entry needs:
   - `platform` (required): reddit / quora / youtube / facebook / x
   - `post` OR `comment` (not both — never mix)
   - `title` (required for posts; generate one if missing)
   - `subreddit` (Reddit posts/comments: the subreddit URL)
   - `post_link` (comments: thread URL)
   - `comment_link` (optional: direct permalink to the comment)

2. For comments where no link is provided, use WebSearch to find the thread URL.

3. Run `write_sheet.py` from `/home/user/fool/`:

**Single entry:**
```bash
python /home/user/fool/write_sheet.py '{"platform": "reddit", "post": "...", "title": "...", "subreddit": "https://reddit.com/r/dogs/"}'
```

**Multiple entries (batch):**
```bash
python /home/user/fool/write_sheet.py '[{"platform": "reddit", "comment": "...", "post_link": "https://..."}, {"platform": "quora", "post": "..."}]'
```

4. Report back: platform, row number, and what was written.

## Notes
- `credentials.json` must exist in the repo root (gitignored)
- If dependencies missing: `pip install google-auth google-auth-httplib2 google-api-python-client`
- Always use batch mode for multiple entries — one JSON array call
- The Reddit tab name has a trailing space: `"Reddit "` — the script handles this automatically
