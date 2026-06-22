# The Feature Line

A "six degrees of separation" game for music. You're given two artists — a **start
station** and a **target station** — and you connect them by chaining songs they
appear on together. Tap the **+** between two stations to add an artist who shares
a track with the artist before them. Reach the target and the line lights up.

It's built around a transit-map metaphor: artists are stations, and each song is a
glowing rail segment linking the people on it. "On it" is the operative word: an artist
counts if they're actually on the track, even if a streaming service leaves them out of
the printed credits — they all go in the same list.

---

## What's included

| File | What it is |
|------|------------|
| `index.html` | The complete game. Self-contained — open it and play. This is the thing you publish. |
| `data.json` | The song/artist dataset the game reads. Edit or regenerate this to change the game. |
| `build_dataset.py` | Generator that builds a **large, sourced** dataset from the MusicBrainz API. |
| `build_seed.py` | The script that produced the hand-curated starter `data.json` (157 songs, 100 artists). |
| `overrides.json` | *(optional, you create it)* Extra on-track artists to merge into specific songs (for people the API misses). |

`index.html` already has the seed dataset baked into it, so it runs even with no web
server and no `data.json` next to it. When `data.json` *is* present alongside it, the
game loads that instead — so growing the dataset is just "drop in a new `data.json`."

---

## Run it locally

Simplest: double-click `index.html`. It opens in your browser with the embedded seed
data and is fully playable.

To test it the way it'll behave online (loading `data.json` over HTTP), serve the
folder:

```bash
cd feature-line
python3 -m http.server 8000
# then open http://localhost:8000
```

---

## Publish it online

It's a static site — one HTML file — so hosting is free and takes a couple of minutes.
Pick any one:

**Netlify drop (no account math, fastest):** go to https://app.netlify.com/drop and
drag the `feature-line` folder onto the page. You get a live URL immediately.

**GitHub Pages:** create a repo, push these files, then in the repo go to
*Settings → Pages → Build and deployment → Source: Deploy from a branch*, pick `main`
and `/ (root)`, save. Your game lives at `https://<you>.github.io/<repo>/`.

**Any static host** (Cloudflare Pages, Vercel, S3, your own server): upload `index.html`
and `data.json` to the same directory. That's the whole deploy.

---

## About the "fastest path using neural networks"

You asked for an option that gives the fastest connection using neural networks. I built
that feature — it's the **Shortest path** button — but I used a different method on
purpose, and I want to be straight with you about why.

Finding the shortest chain through a collaboration graph is a classic *shortest-path*
problem. The right tool for it is **breadth-first search (BFS)**, and it has a property
a neural network can't match here: it's **provably optimal**. BFS doesn't estimate or
approximate — it returns the genuinely shortest possible chain, every time, instantly,
with no training data and nothing to get wrong. A neural network would be slower to run,
need a training pipeline, and still only *approximate* what BFS gives you exactly.

So the button does exactly what you wanted (reveal the fastest connection) — it's just
honest about being mathematically optimal rather than a guess. The length is shown the
way you'd describe the chain out loud: the number of **artists** between the two
endpoints (a two-song hop through one person reads as "one artist"). If you specifically
want an ML angle later (say, ranking *interesting* paths rather than shortest ones, or
predicting likely collaborations that don't exist yet), that's a real and fun use of a
model, and we can add it on top.

---

## The dataset

### Schema

`data.json` looks like this:

```json
{
  "version": 1,
  "songs": [
    {
      "title": "Ultralight Beam",
      "artists": ["Kanye West", "Chance the Rapper", "Kelly Price", "The-Dream", "Kirk Franklin"]
    }
  ]
}
```

- **`title`** — the song name.
- **`artists`** — everyone on the track. List them all here, including anyone who's on
  the song but missing from the official streaming credits. Order doesn't matter; the
  game treats every pair on a song as connected. (That's why, for example, Chance the
  Rapper connects through *Ultralight Beam* — he's just one of the artists on it.)

There's no separate "hidden features" field. If someone is on the track, they belong in
`artists`; if they're not, they don't. One list, no special cases.

The game builds a graph from this: every artist who shares a song with another artist
gets an edge between them. That's all it needs.

### Honest caveat about the seed data

The starter `data.json` is **hand-curated from memory** — 157 real, well-known
collaborations. It's enough to be fun out of the box and it forms one fully-connected
web (every artist can reach every other). But hand-built credits can have mistakes, and
157 songs is small. For a "really big" and *accurate* dataset, regenerate it from a real
source with the script below.

### Grow it with `build_dataset.py`

This pulls real credits from **MusicBrainz** (open music database, no API key needed).

```bash
# Start from the artists already in your data.json, crawl their collaborators,
# and write a much larger data.json:
python3 build_dataset.py --expand --max-artists 200 \
  --user-agent "FeatureLine/1.0 ( you@example.com )"

# Or seed from your own list of artists:
python3 build_dataset.py --seed "Drake,Kendrick Lamar,J. Cole,Future,21 Savage" --expand \
  --user-agent "FeatureLine/1.0 ( you@example.com )"

# Seed from a file (one artist per line):
python3 build_dataset.py --seed @artists.txt --expand \
  --user-agent "FeatureLine/1.0 ( you@example.com )"
```

Then rebuild `index.html` so the embedded fallback matches your new data (optional but
tidy):

```bash
python3 -c "import json,pathlib; data=pathlib.Path('data.json').read_text(); src=pathlib.Path('index.src.html').read_text(); compact=json.dumps(json.loads(data),ensure_ascii=False,separators=(',',':')); pathlib.Path('index.html').write_text(src.replace('__DATA__',compact))"
```

(If you don't rebuild, that's fine too — the live site reads `data.json` directly. The
embedded copy is only the offline fallback.)

**Important:** MusicBrainz asks for a real **User-Agent with contact info** and limits
you to ~1 request/second. The script already throttles itself to stay polite; just pass
a real contact string in `--user-agent` or you may get blocked. A big crawl
(`--expand --max-artists 200`) takes a while because of that 1/sec limit — let it run.

Useful flags:

| Flag | Effect |
|------|--------|
| `--expand` | Crawl outward from your seed artists to their collaborators (this is what makes it big). |
| `--max-artists N` | Cap on how many artists to crawl (default 200). |
| `--max-recordings-per-artist N` | Cap per artist (default 400). |
| `--rels` | Also pull performer relationships from MusicBrainz and fold on-track performers (people on the song but missing from the main credit) into the `artists` list. *Approximate* and slower. |
| `--overrides overrides.json` | Merge in your hand-maintained extra on-track artists (below). |
| `--genius TOKEN` | Use a Genius API token to improve *credited* feature completeness. |
| `--out FILE` | Output path (default `data.json`). |

---

## Adding people the credits leave off

You wanted artists who are *on* a track to connect even when a streaming service didn't
print them in the credits (the ghost verses and uncredited hooks). The game handles that
with no special machinery: those people just go in the song's `artists` list alongside
everyone else, and they connect like any other collaboration. There's no toggle and no
second list to keep in sync.

Two ways to capture the ones an automatic pull would miss:

**1. A hand-maintained overrides file (most accurate).** Create `overrides.json`:

```json
{
  "Some Song": ["Artist The Credits Missed", "Another One"],
  "Another Song": ["Someone Else"]
}
```

Then pass `--overrides overrides.json` when running `build_dataset.py`, and those names
get merged into the matching songs' `artists` lists. It's manual, but it's the only way
to get *correct* data for people no database lists.

**2. Relationship crawl (approximate).** `--rels` pulls performer relationships from
MusicBrainz that sometimes include people beyond the main credit, and folds them into
`artists` automatically. It's a rough proxy — expect some noise — but it needs no manual
work.

The seed `data.json` already lists the well-known people on each track (that's why the
example chains resolve); the two options above are for going further.

---

## Tweaking the game itself

Everything — layout, logic, styling — lives in `index.src.html` (the template) and gets
baked into `index.html`. If you edit the look or behavior, edit `index.src.html` and
re-run the rebuild command above. Colors and fonts are defined as CSS variables near the
top of the `<style>` block, so the transit-map palette is easy to retheme.
