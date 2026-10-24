
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
        print("ERROR: La descarga ha tardado demasiado.")
        sys.exit(1)

    if result.returncode != 0:
        print("ERROR al obtener la lista:")
        print(result.stderr)
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print("ERROR: YouTube no ha devuelto un JSON válido.")
        print(result.stderr)
        sys.exit(1)

    items = []

    for entry in data.get("entries") or []:
        if not entry or not entry.get("id"):
            continue

        video_id = entry["id"]

        # Cada canción tendrá su propio enlace de radio.
        youtube_url = (
            f"https://www.youtube.com/watch?v={video_id}"
            f"&list=RD{video_id}&start_radio=1"
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
        print("ERROR: La lista está vacía. No se ha modificado lista.json.")
        sys.exit(1)

    output = {
        "title": data.get("title") or "Mi lista",
        "uploader": (
            data.get("channel")
            or data.get("uploader")
            or ""
        ),
        "items": items,
    }

    # Guardar primero en un archivo temporal para evitar
    # dejar lista.json incompleto si ocurre un error.
    temp_file = OUTPUT_FILE.with_suffix(".json.tmp")

    try:
        temp_file.write_text(
            json.dumps(output, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_file.replace(OUTPUT_FILE)
    except OSError as error:
        print(f"ERROR al guardar lista.json: {error}")
        sys.exit(1)

    print(f"Correcto: {len(items)} vídeos guardados en {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
