import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import deque

MB_ROOT = "https://musicbrainz.org/ws/2"
GENIUS_ROOT = "https://api.genius.com"

DEFAULT_SEED = [
    "Drake", "Kendrick Lamar", "J. Cole", "Kanye West", "Jay-Z", "Lil Wayne",
    "Nicki Minaj", "Future", "Travis Scott", "21 Savage", "Lil Baby", "Gunna",
    "Young Thug", "Migos", "DJ Khaled", "Rick Ross", "2 Chainz", "Big Sean",
    "Eminem", "Dr. Dre", "Snoop Dogg", "50 Cent", "Kid Cudi", "The Weeknd",
    "Chance the Rapper", "Saba", "Post Malone", "Cardi B", "Megan Thee Stallion",
]


class Limiter:
    def __init__(self, min_interval=1.1):
        self.min_interval = min_interval
        self.last = 0.0

    def wait(self):
        dt = time.time() - self.last
        if dt < self.min_interval:
            time.sleep(self.min_interval - dt)
        self.last = time.time()


def http_get(url, headers, limiter, tries=5):
    for attempt in range(tries):
        limiter.wait()
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 503:
                back = 2 ** attempt
                print(f"  503 rate-limited; backing off {back}s", file=sys.stderr)
                time.sleep(back)
                continue
            if e.code == 404:
                return None
            print(f"  HTTP {e.code} for {url}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"  error: {e}", file=sys.stderr)
            time.sleep(1.5)
    return None


def mb_headers(ua):
    return {"User-Agent": ua, "Accept": "application/json"}


def resolve_artist(name, ua, limiter):
    q = urllib.parse.quote(name)
    url = f"{MB_ROOT}/artist?query={q}&fmt=json&limit=5"
    data = http_get(url, mb_headers(ua), limiter)
    if not data or not data.get("artists"):
        return None
    best = None
    for a in data["artists"]:
        if a.get("name", "").lower() == name.lower():
            best = a
            break
    best = best or data["artists"][0]
    return best["id"], best["name"]


def fetch_recordings(mbid, ua, limiter, max_recordings, with_rels):
    inc = "artist-credits"
    offset, fetched = 0, 0
    while fetched < max_recordings:
        limit = min(100, max_recordings - fetched)
        url = (f"{MB_ROOT}/recording?artist={mbid}&inc={inc}"
               f"&fmt=json&limit={limit}&offset={offset}")
        data = http_get(url, mb_headers(ua), limiter)
        if not data:
            break
        recs = data.get("recordings", [])
        if not recs:
            break
        for rec in recs:
            credit = rec.get("artist-credit", []) or []
            names, ids = [], []
            for c in credit:
                art = c.get("artist") or {}
                nm = art.get("name")
                if nm and nm not in names:
                    names.append(nm)
                    ids.append(art.get("id"))
            if with_rels:
                for extra in fetch_track_performers(rec.get("id"), names, ua, limiter):
                    names.append(extra)
            if len(names) < 2:
                continue
            yield rec.get("title", "").strip(), names, ids


def fetch_track_performers(rec_id, credited, ua, limiter):
    if not rec_id:
        return []
    url = f"{MB_ROOT}/recording/{rec_id}?inc=artist-rels&fmt=json"
    data = http_get(url, mb_headers(ua), limiter)
    if not data:
        return []
    out = []
    credited_lower = {c.lower() for c in credited}
    for rel in data.get("relations", []):
        rtype = rel.get("type", "")
        if rtype in ("vocal", "performer", "performing orchestra", "instrument"):
            nm = (rel.get("artist") or {}).get("name")
            if nm and nm.lower() not in credited_lower and nm not in out:
                out.append(nm)
    return out


def genius_features(title, primary, token, limiter):
    h = {"Authorization": f"Bearer {token}"}
    q = urllib.parse.quote(f"{title} {primary}")
    s = http_get(f"{GENIUS_ROOT}/search?q={q}", h, limiter)
    try:
        hits = s["response"]["hits"]
    except (TypeError, KeyError):
        return []
    if not hits:
        return []
    song_id = hits[0]["result"]["id"]
    d = http_get(f"{GENIUS_ROOT}/songs/{song_id}", h, limiter)
    try:
        song = d["response"]["song"]
    except (TypeError, KeyError):
        return []
    return [a.get("name") for a in song.get("featured_artists", []) if a.get("name")]


def load_existing_seed(path="data.json"):
    try:
        d = json.load(open(path, encoding="utf-8"))
        names = set()
        for s in d.get("songs", []):
            names.update(s.get("artists", []))
        return sorted(names)
    except Exception:
        return []


def parse_seed(arg):
    if not arg:
        return None
    if arg.startswith("@"):
        return [l.strip() for l in open(arg[1:], encoding="utf-8") if l.strip()]
    return [s.strip() for s in arg.split(",") if s.strip()]


def main():
    ap = argparse.ArgumentParser(description="Build a feature dataset from MusicBrainz.")
    ap.add_argument("--seed", help="Comma list, or @file with one artist per line. "
                                   "Defaults to artists in existing data.json, else a rap seed.")
    ap.add_argument("--out", default="data.json")
    ap.add_argument("--max-artists", type=int, default=200,
                    help="Stop after resolving/processing this many artists.")
    ap.add_argument("--max-recordings-per-artist", type=int, default=400)
    ap.add_argument("--expand", action="store_true",
                    help="Crawl collaborators discovered on recordings (grows the graph).")
    ap.add_argument("--rels", action="store_true",
                    help="Also fetch recording relationships and fold on-track performers "
                         "(people on the track but missing from streaming credits) into the "
                         "artist list. Slower.")
    ap.add_argument("--overrides", help="JSON file mapping song title to a list of extra "
                                        "on-track artists to merge into that song's credits.")
    ap.add_argument("--genius", help="Genius API token to enrich credited features (optional).")
    ap.add_argument("--user-agent",
                    default="TheFeatureLine/1.0 ( your-email@example.com )",
                    help="MusicBrainz requires a real contact here.")
    args = ap.parse_args()

    if "example.com" in args.user_agent:
        print("WARNING: set --user-agent with your real contact; MusicBrainz "
              "may block the default.\n", file=sys.stderr)

    seed = parse_seed(args.seed) or load_existing_seed(args.out) or DEFAULT_SEED
    print(f"Seed: {len(seed)} artists. Expand={args.expand} Rels={args.rels}")

    lim = Limiter()
    ua = args.user_agent

    queue = deque()
    seen_mbid, seen_name = set(), set()
    for nm in seed:
        if nm.lower() in seen_name:
            continue
        res = resolve_artist(nm, ua, lim)
        if not res:
            print(f"  ? could not resolve: {nm}", file=sys.stderr)
            continue
        mbid, canon = res
        if mbid in seen_mbid:
            continue
        seen_mbid.add(mbid); seen_name.add(nm.lower())
        queue.append((canon, mbid))
        print(f"  + {canon}")

    songs = {}
    processed = 0
    while queue and processed < args.max_artists:
        name, mbid = queue.popleft()
        processed += 1
        print(f"[{processed}/{args.max_artists}] {name}")
        for title, names, ids in fetch_recordings(
                mbid, ua, lim, args.max_recordings_per_artist, args.rels):
            if not title:
                continue
            key = title.lower() + "|" + "||".join(sorted(n.lower() for n in names))
            if key not in songs:
                songs[key] = {"title": title, "artists": names}
            if args.expand and len(seen_mbid) < args.max_artists * 3:
                for nm2, id2 in zip(names, ids):
                    if id2 and id2 not in seen_mbid:
                        seen_mbid.add(id2)
                        queue.append((nm2, id2))

    songs_list = list(songs.values())

    if args.genius:
        print("Enriching credited features via Genius…")
        for s in songs_list:
            try:
                for f in genius_features(s["title"], s["artists"][0], args.genius, lim):
                    if f not in s["artists"]:
                        s["artists"].append(f)
            except Exception as e:
                print(f"  genius skip {s['title']}: {e}", file=sys.stderr)

    if args.overrides:
        ov = json.load(open(args.overrides, encoding="utf-8"))
        ov_lower = {k.lower(): v for k, v in ov.items()}
        for s in songs_list:
            extra = ov_lower.get(s["title"].lower())
            if extra:
                for h in extra:
                    if h not in s["artists"]:
                        s["artists"].append(h)

    out = {"version": 1, "songs": songs_list}
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    artists = {a for s in songs_list for a in s["artists"]}
    print(f"\nWrote {args.out}: {len(songs_list)} collab songs, {len(artists)} artists.")
    print("Reload the game (or re-run the embed step) to use it.")


if __name__ == "__main__":
    main()
