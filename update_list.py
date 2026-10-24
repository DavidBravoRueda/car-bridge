```python
import json
import subprocess
import sys
from pathlib import Path

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLPBl-I93G56Y"
OUTPUT_FILE = Path(__file__).with_name("lista.json")


def main():
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--flat-playlist",
                "--ignore-errors",
                "-J",
                PLAYLIST_URL,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=180,
        )
    except FileNotFoundError:
        print("ERROR: No se encuentra yt-dlp.")
        print("Instálalo con: python3 -m pip install -U yt-dlp")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("ERROR: Se ha agotado el tiempo de espera.")
        sys.exit(1)

    if result.returncode != 0:
        print("ERROR al obtener la lista:")
        print(result.stderr)
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("ERROR: La respuesta de yt-dlp no es un JSON válido.")
        sys.exit(1)

    items = []
    seen_ids = set()

    for entry in data.get("entries") or []:
        if not entry or not entry.get("id"):
            continue

        video_id = str(entry["id"])

        # Evitar canciones duplicadas en la biblioteca.
        if video_id in seen_ids:
            continue

        seen_ids.add(video_id)

        # Vídeo individual, sin radio ni cola automática.
        youtube_url = (
            "https://www.youtube.com/watch?v=" + video_id
        )

        items.append({
            "id": video_id,
            "url": youtube_url,
            "title": entry.get("title") or "Vídeo sin título",
            "by": (
                entry.get("channel")
                or entry.get("uploader")
                or ""
            ),
            "dur": int(entry.get("duration") or 0),
            "views": entry.get("view_count"),
            "thumb": (
                f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
            ),
        })

    if not items:
        print("ERROR: No se han encontrado vídeos.")
        print("No se ha modificado lista.json.")
        sys.exit(1)

    output = {
        "title": data.get("title") or "MiTube",
        "uploader": (
            data.get("channel")
            or data.get("uploader")
            or ""
        ),
        "items": items,
    }

    temp_file = OUTPUT_FILE.with_suffix(".json.tmp")

    try:
        temp_file.write_text(
            json.dumps(output, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_file.replace(OUTPUT_FILE)
    except OSError as error:
        print(f"ERROR al guardar la lista: {error}")
        sys.exit(1)

    print(
        f"Correcto: {len(items)} canciones guardadas en lista.json"
    )


if __name__ == "__main__":
    main()
```
