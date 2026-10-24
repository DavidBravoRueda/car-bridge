import json, subprocess, sys

URL = "https://www.youtube.com/playlist?list=PLPBl-I93G56Y"

r = subprocess.run(["yt-dlp", "--flat-playlist", "-J", URL], capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr)
    sys.exit(1)

d = json.loads(r.stdout)
items = [
    {
        "id": e["id"],
        "title": e.get("title"),
        "by": e.get("channel") or e.get("uploader") or "",
        "dur": int(e.get("duration") or 0),
        "views": e.get("view_count"),
    }
    for e in d.get("entries", [])
    if e and e.get("id")
]
if not items:
    print("La lista salió vacía, no se guarda nada.")
    sys.exit(1)

with open("lista.json", "w", encoding="utf-8") as f:
    json.dump(
        {"title": d.get("title"), "uploader": d.get("channel") or d.get("uploader"), "items": items},
        f, ensure_ascii=False,
    )
print(len(items), "vídeos guardados")
