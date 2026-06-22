"""
rebuild.py — regenerate index.html from index_src.html + data.json

Run this any time after:
  - editing index_src.html (template), or
  - regenerating data.json (via build_seed.py or build_dataset.py)

Usage:
  python3 rebuild.py
  python3 rebuild.py --src index_src.html --data data.json --out index.html
"""

import argparse
import json
import pathlib
import sys


def main():
    ap = argparse.ArgumentParser(
        description="Embed data.json into index_src.html to produce index.html."
    )
    ap.add_argument("--src",  default="index_src.html", help="HTML template file (contains __DATA__)")
    ap.add_argument("--data", default="data.json",      help="JSON dataset file")
    ap.add_argument("--out",  default="index.html",     help="Output HTML file")
    args = ap.parse_args()

    src_path  = pathlib.Path(args.src)
    data_path = pathlib.Path(args.data)
    out_path  = pathlib.Path(args.out)

    if not src_path.exists():
        sys.exit(f"Error: template '{src_path}' not found. Run from the project directory.")
    if not data_path.exists():
        sys.exit(f"Error: dataset '{data_path}' not found. Run build_seed.py or build_dataset.py first.")

    template = src_path.read_text(encoding="utf-8")
    if "__DATA__" not in template:
        sys.exit(f"Error: '{src_path}' has no __DATA__ placeholder. Is this the right source file?")

    data   = json.loads(data_path.read_text(encoding="utf-8"))
    compact = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    output = template.replace("__DATA__", compact)
    out_path.write_text(output, encoding="utf-8")

    songs   = len(data.get("songs", []))
    artists = len({a for s in data.get("songs", []) for a in s.get("artists", [])})
    print(f"Wrote {out_path}  —  {songs} songs, {artists} artists embedded.")


if __name__ == "__main__":
    main()
