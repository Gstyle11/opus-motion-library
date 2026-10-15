# Adding to the Opus 5.5 Motion Library

The library is `library.json` (videos) and `externals.json` (external libraries) in this repo.
The site at https://gstyle11.github.io/opus-motion-library/ reads them on every visit.
Writing needs the owner's fine-grained GitHub token (this repo only, Contents: read and write).

## Option A — one call (simplest)

```bash
curl -X POST https://api.github.com/repos/Gstyle11/opus-motion-library/dispatches \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"event_type":"add-video","client_payload":{"urls":"https://x.com/user/status/123 https://x.com/user/status/456"}}'
```

GitHub answers `204` and a workflow appends the links within about a minute. Duplicates are skipped.

## Option B — write the file directly

`GET /repos/Gstyle11/opus-motion-library/contents/library.json` → decode `content` (base64, UTF-8),
prepend `{"id": "<post id>", "post": "https://x.com/<user>/status/<post id>"}`, then
`PUT` the same path with `message`, `content` (base64 of the UTF-8 JSON) and the `sha` you read.
On `409`/`422` read again and retry.

A lean entry `{id, post}` (or even a bare URL string) is enough: the page fetches video, poster,
duration, text and prompt from X and writes the full entry back on its next connected visit.

External libraries: same pattern on `externals.json` with `{"id", "name", "url", "image", "note"}`.
