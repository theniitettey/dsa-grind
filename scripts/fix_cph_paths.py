#!/usr/bin/env python3
"""
Fix CPH (Competitive Programming Helper) config files.
Converts relative paths in .cph/*.prob files to absolute paths.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CPH_DIR = REPO_ROOT / ".cph"


def fix_cph_files():
    if not CPH_DIR.exists():
        print(f"Directory not found: {CPH_DIR}")
        return

    print(f"Scanning {CPH_DIR}...")
    
    count = 0
    fixed = 0
    
    for prob_file in CPH_DIR.glob("*.prob"):
        count += 1
        try:
            content = prob_file.read_text(encoding="utf-8")
            data = json.load(prob_file.open(encoding="utf-8"))
            
            changed = False
            
            # check srcPath
            src_path = data.get("srcPath")
            if src_path and (src_path.startswith(".") or not Path(src_path).is_absolute()):
                # Assuming relative to repo root if it starts with .
                # The broken files seem to be like ".\LeetCode_Missing_Number.py" which is relative to wherever CPH thinks it is
                # But actual file is in REPO_ROOT
                
                # Strip leading .\ or ./
                rel = src_path.lstrip(".\\/")
                abs_path = REPO_ROOT / rel
                
                if abs_path.exists():
                    data["srcPath"] = str(abs_path)
                    changed = True
                else:
                     print(f"⚠️  Could not resolve srcPath: {src_path} -> {abs_path}")

            # check url
            url = data.get("url")
            if url and (url.startswith(".") or not Path(url).is_absolute()):
                 # Same logic
                rel = url.lstrip(".\\/")
                abs_path = REPO_ROOT / rel
                
                if abs_path.exists():
                    data["url"] = str(abs_path)
                    changed = True

            if changed:
                print(f"Fixing {prob_file.name}")
                prob_file.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
                fixed += 1
                
        except Exception as e:
            print(f"Error processing {prob_file.name}: {e}")

    print(f"\nScanned {count} files.")
    print(f"Fixed {fixed} files.")


if __name__ == "__main__":
    fix_cph_files()
