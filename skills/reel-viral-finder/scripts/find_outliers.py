#!/usr/bin/env python3
"""Find short-form videos that beat their own creator's usual numbers.

TikTok and YouTube Shorts: views from each creator's latest videos (yt-dlp, no login).
Instagram: likes + comments from the reel links you pass (views aren't public).

Usage:
  python find_outliers.py --tiktok @a @b --youtube @c --limit 30 --min-ratio 2 --json out.json
  python find_outliers.py --instagram https://www.instagram.com/reel/XXXX/ ...
"""
import argparse
import json
import re
import shutil
import statistics
import subprocess
import sys


HANDLE_RE = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
IG_RE = re.compile(r"^https://(www\.)?instagram\.com/(reel|reels|p)/[A-Za-z0-9_-]+/?(\?.*)?$")


def ytdlp_cmd():
    exe = shutil.which("yt-dlp")
    if exe:
        return [exe]
    # pip installs yt-dlp as a module even when its launcher isn't on PATH.
    return [sys.executable, "-m", "yt_dlp"]


def run_json(args, url, timeout=180):
    # No shell; options first, then "--" so the URL can never be read as a yt-dlp option.
    cmd = ytdlp_cmd() + ["--no-exec"] + args + ["--", url]
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=timeout, shell=False)
    except FileNotFoundError:
        sys.exit("yt-dlp not found. Install it with: pip install yt-dlp")
    except subprocess.TimeoutExpired:
        return None, "timed out"
    if out.returncode != 0:
        err = out.stderr.decode("utf-8", "replace").strip().splitlines()
        return None, (err[-1] if err else "yt-dlp failed")[:300]
    try:
        return json.loads(out.stdout.decode("utf-8", "replace")), None
    except json.JSONDecodeError:
        return None, "could not read yt-dlp output"


def handle(h):
    h = h.strip().rstrip("/")
    if "/" in h:
        h = h.split("/@")[-1].split("/")[0]
    h = h.lstrip("@")
    return h if HANDLE_RE.match(h) else None


def scan_feed(platform, h, limit):
    name = handle(h)
    if not name:
        return [], f"{platform}: skipped {h[:40]!r} (not a valid handle)"
    url = (f"https://www.tiktok.com/@{name}" if platform == "tiktok"
           else f"https://www.youtube.com/@{name}/shorts")
    data, err = run_json(["--flat-playlist", "-J", "--playlist-end", str(limit)], url)
    if err:
        return [], f"{platform} @{name}: {err}"
    rows = []
    for e in data.get("entries") or []:
        v = e.get("view_count")
        if isinstance(v, int):
            rows.append({
                "platform": platform,
                "creator": "@" + name,
                "title": (e.get("title") or e.get("description") or "").replace("\n", " ")[:90],
                "url": e.get("url") or e.get("webpage_url") or "",
                "metric": v,
            })
    if not rows:
        return [], f"{platform} @{name}: no view counts returned"
    return rows, None


def scan_instagram(urls):
    rows, errors = [], []
    for u in urls:
        if not IG_RE.match(u):
            errors.append(f"instagram: skipped {u[:60]!r} (not an instagram.com reel or post link)")
            continue
        data, err = run_json(["--skip-download", "-J"], u, timeout=90)
        if err:
            errors.append(f"instagram {u}: {err}")
            continue
        likes = data.get("like_count") or 0
        comments = data.get("comment_count") or 0
        creator = data.get("channel") or data.get("uploader_id") or data.get("uploader") or "?"
        rows.append({
            "platform": "instagram",
            "creator": "@" + str(creator),
            "title": (data.get("description") or "").replace("\n", " ")[:90],
            "url": u,
            "metric": likes + comments,
            "likes": likes,
            "comments": comments,
        })
    return rows, errors


def score(rows, min_ratio):
    groups = {}
    for r in rows:
        groups.setdefault((r["platform"], r["creator"]), []).append(r)
    hits = []
    for items in groups.values():
        usual = statistics.median(i["metric"] for i in items)
        for i in items:
            i["usual"] = usual
            i["ratio"] = round(i["metric"] / usual, 2) if usual else 0.0
            i["sample"] = len(items)
            if i["ratio"] >= min_ratio and len(items) >= 3:
                hits.append(i)
    return sorted(hits, key=lambda r: r["ratio"], reverse=True)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--tiktok", nargs="*", default=[], help="TikTok handles")
    p.add_argument("--youtube", nargs="*", default=[], help="YouTube handles (their Shorts)")
    p.add_argument("--instagram", nargs="*", default=[], help="Instagram reel URLs")
    p.add_argument("--limit", type=int, default=30, help="latest videos per creator")
    p.add_argument("--min-ratio", type=float, default=2.0, help="times the creator's median")
    p.add_argument("--json", help="also write all results to this file")
    a = p.parse_args()
    if not (a.tiktok or a.youtube or a.instagram):
        p.error("give at least one of --tiktok, --youtube, --instagram")

    rows, errors = [], []
    for plat, handles in (("tiktok", a.tiktok), ("youtube", a.youtube)):
        for h in handles:
            r, e = scan_feed(plat, h, a.limit)
            rows += r
            if e:
                errors.append(e)
    if a.instagram:
        r, e = scan_instagram(a.instagram)
        rows += r
        errors += e

    hits = score(rows, a.min_ratio)
    print(f"Scanned {len(rows)} videos. Outliers at {a.min_ratio}x or more: {len(hits)}")
    print("(Each video is compared with the median of its own creator's videos in this scan.)\n")
    print("| ratio | platform | creator | metric | usual | title | link |")
    print("|---|---|---|---|---|---|---|")
    for h in hits:
        unit = "likes+comments" if h["platform"] == "instagram" else "views"
        title = h["title"].replace("|", "/")
        print(f"| {h['ratio']}x | {h['platform']} | {h['creator']} | {h['metric']:,} {unit} | "
              f"{h['usual']:,.0f} | {title} | {h['url']} |")
    if errors:
        print("\nCouldn't read:")
        for e in errors:
            print(" -", e)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"outliers": hits, "all": rows, "errors": errors}, f,
                      ensure_ascii=False, indent=2)
        print(f"\nSaved {a.json}")


if __name__ == "__main__":
    main()
