#!/usr/bin/env python3
"""
Initialize grind.json with user settings.

Auto-detects from git config or allows manual input:
- User name (from git config user.name)
- GitHub username (optional)
"""

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = REPO_ROOT / "config" / "grind.json"


def get_git_user() -> tuple[str, str]:
    """Try to get user name and github username from git config."""
    name = ""
    github_username = ""
    
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
    except Exception:
        pass
    
    # Try to get github username from git config
    try:
        github_username = subprocess.check_output(
            ["git", "config", "github.user"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
    except Exception:
        pass
    
    return name or "", github_username or ""


def init_grind() -> None:
    """Initialize grind.json with auto-detected or manual settings."""
    
    print("\n" + "="*60)
    print("🔧 GRIND.JSON INITIALIZATION")
    print("="*60)
    
    # Load existing config if it exists
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("Status: Found existing config")
    else:
        print("Status: Creating new config")
        config = {
            "user": {},
            "readme": {
                "title": "dsa grind 💪",
                "show_badges": True,
                "show_stats_table": True,
                "show_topics": True,
                "show_streak": True,
                "restore_streak_when_possible": True,
                "restore_streak_auto_apply": False,
                "platforms": ["GeeksForGeeks", "LeetCode", "HackerRank", "Codeforces"],
                "badge_style": "for-the-badge",
                "topic_filters": {
                    "exclude": ["?", "misc"],
                    "min_count": 1
                }
            },
            "optimization": {
                "last_update": None,
                "total_files_scanned": 0,
                "cache": {
                    "total_solved": 0,
                    "total_time_mins": 0,
                    "current_streak": 0,
                    "topics": {}
                }
            },
            "stats": {
                "total_solved": 0,
                "platforms": {},
                "last_scan_timestamp": None
            }
        }
    
    # Auto-detect user info from git config
    git_name, git_username = get_git_user()
    
    print("="*60)
    print("📋 Configuration Options")
    print("="*60)
    print("  [1] Use defaults from git config (fastest)")
    print("  [2] Enter details manually")
    print("\n💡 Tip: You can edit config/grind.json anytime")
    print("="*60)
    
    choice = input("\nChoose option (1 or 2) [1]: ").strip() or "1"
    print()
    
    if "user" not in config:
        config["user"] = {}
    
    if choice == "2":
        # Manual input
        current_name = config.get("user", {}).get("name", git_name)
        name = input(f"Your name [{current_name}]: ").strip()
        config["user"]["name"] = name or current_name
        
        current_gh = config.get("user", {}).get("github_username", git_username)
        gh_user = input(f"GitHub username [{current_gh}]: ").strip()
        config["user"]["github_username"] = gh_user or current_gh
        
        print()
    else:
        # Use auto-detected values
        config["user"]["name"] = git_name
        config["user"]["github_username"] = git_username
    
    # Save config
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # Display what we saved
    print("="*60)
    print("✅ CONFIGURATION SAVED")
    print("="*60)
    if config["user"]["name"]:
        print(f"User: {config['user']['name']}")
    if config["user"]["github_username"]:
        print(f"GitHub: {config['user']['github_username']}")
    print(f"Location: {CONFIG_FILE.relative_to(REPO_ROOT)}")
    print("="*60)
    print("\n💡 Next steps:")
    print("   • python scripts/new_problem.py <url>")
    print("   • python scripts/update_stats.py")
    print("="*60 + "\n")



if __name__ == "__main__":
    init_grind()
