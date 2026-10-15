"""Append X post links to library.json as lean entries; the page fills in video, poster and prompt on its next load."""
import json, re, sys

PATH = "library.json"
STATUS = re.compile(r"(?:x|twitter|fxtwitter|vxtwitter|fixupx)\.com/([^/?#\s]+)/status(?:es)?/(\d+)", re.I)

links = [m for m in STATUS.finditer(" ".join(sys.argv[1:]))]
with open(PATH, encoding="utf-8") as f:
    library = json.load(f)

def post_id(entry):
    if isinstance(entry, str):
        m = STATUS.search(entry)
        return m and m.group(2)
    m = STATUS.search(entry.get("post", "") or "")
    return entry.get("id") if not m else m.group(2)

known = {post_id(e) for e in library}
fresh = []
for m in links:
    pid = m.group(2)
    if pid in known:
        continue
    known.add(pid)
    fresh.append({"id": pid, "post": f"https://x.com/{m.group(1)}/status/{pid}"})

if fresh:
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(fresh + library, f, ensure_ascii=False, indent=2)
        f.write("\n")
print(f"added {len(fresh)} of {len(links)} link(s)")
