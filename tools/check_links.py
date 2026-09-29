"""Check links in every Markdown file.

Default (offline, used in CI): every relative link points to an existing file,
and every `#anchor` into a Markdown file matches a heading.

    python tools/check_links.py
    python tools/check_links.py --external   # also: GitHub repos (git ls-remote) and arXiv ids (arXiv API)

The external mode needs network access. It prints the arXiv title for each id so
a human can spot a wrong id that happens to exist.
"""

import argparse
import glob
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r"\]\(([^)\s]+)\)")
SKIP_DIRS = ("node_modules", ".git")


def slugify(heading: str) -> str:
    """GitHub-style anchor: lowercase, drop punctuation except hyphens/spaces, spaces -> hyphens."""
    h = re.sub(r"[`*_\[\]()]", "", heading.strip().lower())
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def anchors(path: str):
    out = set()
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^#{1,6}\s+(.*)", line)
        if m:
            out.add(slugify(m.group(1)))
    return out


def md_files():
    for f in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if not any(s in f for s in SKIP_DIRS):
            yield f


def check_internal():
    errors = []
    for f in md_files():
        for m in LINK.finditer(open(f, encoding="utf-8").read()):
            url = m.group(1)
            if url.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, frag = url.partition("#")
            target = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
            rel = os.path.relpath(f, ROOT)
            if not os.path.exists(target):
                errors.append(f"{rel}: broken link {url}")
            elif frag and target.endswith(".md") and frag not in anchors(target):
                errors.append(f"{rel}: missing anchor #{frag} in {os.path.relpath(target, ROOT)}")
    return errors


def check_external():
    text = "\n".join(open(f, encoding="utf-8").read() for f in md_files())
    text += "\n".join(open(f).read() for f in glob.glob(os.path.join(ROOT, "code", "**", "*.py"), recursive=True))
    repos = sorted({r.rstrip(".") for r in re.findall(r"github\.com/([\w.-]+/[\w.-]+)", text)})
    errors = []
    for r in repos:
        ok = subprocess.run(["git", "ls-remote", f"https://github.com/{r}", "HEAD"],
                            capture_output=True, timeout=30).returncode == 0
        if not ok:
            errors.append(f"GitHub repo not reachable: {r}")
    ids = sorted(set(re.findall(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})", text)))
    for i in range(0, len(ids), 100):
        batch = ids[i:i + 100]
        url = "https://export.arxiv.org/api/query?max_results=200&id_list=" + ",".join(batch)
        xml = urllib.request.urlopen(url, timeout=60).read().decode()
        found = {}
        for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
            aid = re.search(r"<id>http://arxiv.org/abs/(\d{4}\.\d{4,5})", entry)
            title = re.search(r"<title>(.*?)</title>", entry, re.S)
            if aid:
                found[aid.group(1)] = " ".join(title.group(1).split()) if title else "?"
        for a in batch:
            if a in found:
                print(f"arXiv {a}: {found[a][:90]}")
            else:
                errors.append(f"arXiv id not found: {a}")
    print(f"{len(repos)} repos, {len(ids)} arXiv ids checked")
    return errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--external", action="store_true")
    a = ap.parse_args(argv)
    errors = check_internal()
    if a.external:
        errors += check_external()
    for e in errors:
        print("ERROR", e)
    print(f"{len(errors)} link errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
