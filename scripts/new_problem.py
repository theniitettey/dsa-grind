#!/usr/bin/env python3
"""
author: Michael Perry Tettey
repo: dsa-grind

purpose:
- create a new problem file from a problem URL
- infer platform (LeetCode, GFG, HackerRank, Codeforces)
- generate a clean, readable filename
- populate TEMPLATE.py
"""

from __future__ import annotations

import re
import sys
import json
import hashlib
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = REPO_ROOT / "TEMPLATE.py"

PLATFORM_BY_HOST = {
    "leetcode.com": "LeetCode",
    "www.leetcode.com": "LeetCode",
    "geeksforgeeks.org": "GeeksForGeeks",
    "www.geeksforgeeks.org": "GeeksForGeeks",
    "practice.geeksforgeeks.org": "GeeksForGeeks",
    "hackerrank.com": "HackerRank",
    "www.hackerrank.com": "HackerRank",
    "codeforces.com": "Codeforces",
    "www.codeforces.com": "Codeforces",
}

INVALID_FS = set('<>:"/\\|?*')


def platform_from_url(url: str) -> str:
    host = (urlparse(url).netloc or "").lower()
    host = host.replace("m.", "").replace("beta.", "")
    for key, name in PLATFORM_BY_HOST.items():
        if host == key or host.endswith("." + key):
            return name
    return "Platform"


def slugify_title(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^a-z0-9\-]", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "problem"


def slug_to_snake(slug: str) -> str:
    return slug.replace("-", "_")


def title_from_url(url: str, platform: str) -> str:
    p = urlparse(url)
    path = p.path.strip("/")

    if platform == "LeetCode":
        m = re.search(r"/problems/([^/]+)/?", "/" + path + "/")
        if m:
            return m.group(1)

    if platform == "GeeksForGeeks":
        parts = [x for x in path.split("/") if x]
        skip = {"problems", "practice", "page"}
        candidates = [p for p in parts if p not in skip]
        return candidates[-1] if candidates else "problem"

    if platform == "HackerRank":
        m = re.search(r"/challenges/([^/]+)/?", "/" + path + "/")
        if m:
            return m.group(1)

    if platform == "Codeforces":
        m = re.search(r"/problemset/problem/(\d+)/([A-Za-z0-9]+)/?", "/" + path + "/")
        if m:
            return f"cf-{m.group(1)}-{m.group(2)}"
        m2 = re.search(r"/contest/(\d+)/problem/([A-Za-z0-9]+)/?", "/" + path + "/")
        if m2:
            return f"cf-{m2.group(1)}-{m2.group(2)}"

    parts = [x for x in path.split("/") if x]
    return parts[-1] if parts else "problem"


def to_filename(platform: str, title_slug: str, ext: str = "py") -> str:
    words = [w for w in re.split(r"[-_]+", title_slug) if w]
    pretty = "_".join(w.capitalize() for w in words) or "Problem"
    safe = "".join("_" if c in INVALID_FS else c for c in pretty)
    safe = re.sub(r"_+", "_", safe).strip("_")
    return f"{platform}_{safe}.{ext}"


def create_cph_file(problem_path: Path) -> Path:
    """Create .cph file with absolute path to the problem file."""
    cph_dir = REPO_ROOT / ".cph"
    cph_dir.mkdir(parents=True, exist_ok=True)

    abs_path = str(problem_path.resolve())
    digest = hashlib.md5(problem_path.name.encode("utf-8")).hexdigest()
    cph_path = cph_dir / f".{problem_path.name}_{digest}.prob"

    payload = {
        "name": f"Local: {problem_path.stem}",
        "url": abs_path,
        "url": abs_path,
        "tests": [{"id": int(time.time() * 1000), "input": "", "output": ""}],
        "interactive": False,
        "memoryLimit": 1024,
        "timeLimit": 3000,
        "srcPath": abs_path,
        "group": "local",
        "local": True,
    }

    cph_path.write_text(json.dumps(payload, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    return cph_path


def ensure_unique(path: Path) -> Path:
    if not path.exists():
        return path

    stem, suffix = path.stem, path.suffix
    i = 2
    while True:
        candidate = path.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def main() -> None:
    if len(sys.argv) < 2:
        print("\n" + "="*60)
        print("NEW PROBLEM - Usage")
        print("="*60)
        print("python scripts/new_problem.py <url> [--ext py]")
        print("="*60 + "\n")
        raise SystemExit(1)

    url = sys.argv[1].strip()
    ext = "py"

    if "--ext" in sys.argv:
        idx = sys.argv.index("--ext")
        if idx + 1 < len(sys.argv):
            ext = sys.argv[idx + 1].strip().lstrip(".")

    if not TEMPLATE_PATH.exists():
        print("\n" + "="*60)
        print("❌ ERROR")
        print("="*60)
        print("TEMPLATE.py not found in repo root.")
        print("="*60 + "\n")
        raise SystemExit(1)

    platform = platform_from_url(url)
    raw_title = title_from_url(url, platform)
    title_slug = slugify_title(raw_title)

    function_name = slug_to_snake(title_slug)
    filename = to_filename(platform, title_slug, ext)
    target = ensure_unique(REPO_ROOT / filename)

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    template = (
        template.replace("{problem_link}", url)
        .replace("{created}", stamp)
    )

    template = re.sub(
        r"def\s+solve\s*\(\s*self\s*,\s*\*args\s*,\s*\*\*kwargs\s*\)\s*:",
        f"def {function_name}(self, *args, **kwargs):",
        template,
        count=1,
    )

    template = re.sub(
        r'if __name__ == "__main__":\s*[\s\S]*\Z',
        f'''if __name__ == "__main__":
    solution = Solution()
    result = solution.{function_name}(*args, **kwargs)
    print(result)
''',
        template,
        count=1,
    )

    target.write_text(template, encoding="utf-8")
    
    print("\n" + "="*60)
    print("🎯 NEW PROBLEM CREATED")
    print("="*60)
    print(f"Platform: {platform}")
    print(f"File: {target.relative_to(REPO_ROOT)}")
    print(f"Function: {function_name}()")
    print("="*60)

    cph_path = create_cph_file(target)
    print(f"📦 Created .cph file: {cph_path.relative_to(REPO_ROOT)}")

    # open the file in IDE, vs code, or default editor
    # using code command if available, else webbrowser module
    try:
        result = subprocess.run(["code", str(target)], shell=True, check=True)
        if result.returncode == 0:
            print(f"✅ Opened in VS Code")
        else:
            raise FileNotFoundError
    except Exception:
        print(f"💡 Open manually: {target}")
    
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
