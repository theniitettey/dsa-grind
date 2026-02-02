#!/usr/bin/env python3
"""
author: Michael Perry Tettey
repo: dsa-grind

purpose:
- automatically update the stats table in README.md
- parse metadata from solution files (time_spent, difficulty, etc.)
- calculate streaks and total time spent
- generate a cool dashboard-like README
- use grind.json for configuration and optimization
"""

from __future__ import annotations

import re
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import NamedTuple, Optional, List, Dict
from urllib.parse import urlparse

# --------------------------------------------------
# Paths
# --------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
CONFIG_FILE = REPO_ROOT / "config" / "grind.json"

# --------------------------------------------------
# Config Management
# --------------------------------------------------

def load_config() -> dict:
    """Load configuration from grind.json"""
    if not CONFIG_FILE.exists():
        # Create default config
        default_config = {
            "user": {
                "name": "",
                "github_username": ""
            },
            "readme": {
                "title": "dsa grind 💪",
                "show_badges": True,
                "show_stats_table": True,
                "show_streak": True,
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
        save_config(default_config)
        return default_config
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config: dict) -> None:
    """Save configuration to grind.json"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# --------------------------------------------------
# Constants & Config
# --------------------------------------------------

PLATFORM_MAP = {
    "GeeksForGeeks": "geeksforgeeks",
    "LeetCode": "leetcode",
    "HackerRank": "hackerrank",
    "Codeforces": "codeforces",
}

PLATFORM_MAP_LOWER = {k.lower(): v for k, v in PLATFORM_MAP.items()}

ALLOWED_EXTS = ("py", "js", "ts", "cpp", "java", "go", "rs")

# File pattern: PlatformName_Anything.ext
FILE_RE = re.compile(
    rf"^(?P<platform>{'|'.join(map(re.escape, PLATFORM_MAP.keys()))})_.+\.({'|'.join(ALLOWED_EXTS)})$",
    re.IGNORECASE,
)

# --------------------------------------------------
# Data Structures
# --------------------------------------------------

class Problem(NamedTuple):
    filename: str
    platform: str
    difficulty: str
    time_spent_str: str
    time_spent_mins: int
    created: Optional[date]
    tries: int
    topic: str
    url: str

# --------------------------------------------------
# Parsing Logic
# --------------------------------------------------

def parse_time(time_str: str) -> int:
    """
    Parses time strings like "10 mins", "1h 30m", "2 hours" into minutes.
    Returns 0 if parsing fails or input is ?
    """
    if not time_str or "?" in time_str:
        return 0
    
    time_str = time_str.lower().strip()
    total_mins = 0
    
    # Simple regex for finding parts like "1h" or "30m"
    hours = re.search(r'(\d+)\s*h', time_str)
    mins = re.search(r'(\d+)\s*m', time_str)
    
    if hours:
        total_mins += int(hours.group(1)) * 60
    if mins:
        total_mins += int(mins.group(1))
        
    # Fallback: if just a number is given, assume minutes? 
    # Or if string contains "min", grab the number.
    if total_mins == 0 and "min" in time_str:
        nums = re.findall(r'\d+', time_str)
        if nums:
            total_mins += int(nums[0])
            
    return total_mins

def parse_file(path: Path) -> Optional[Problem]:
    m = FILE_RE.match(path.name)
    if not m:
        return None
    
    platform_key = m.group("platform")
    platform = PLATFORM_MAP_LOWER.get(platform_key.lower(), "unknown")
    
    content = path.read_text(encoding="utf-8")
    
    # Extract docstring content (naive approach)
    # usually between triple quotes at the top
    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    metadata_text = docstring_match.group(1) if docstring_match else ""
    
    # Extract fields
    def get_val(key: str, default="?") -> str:
        # distinct keys followed by colon
        m = re.search(rf"^\s*{key}:\s*(.+)$", metadata_text, re.MULTILINE | re.IGNORECASE)
        return m.group(1).strip() if m else default

    difficulty = get_val("difficulty", "Unknown")
    time_str = get_val("time_spent", "?")
    time_mins = parse_time(time_str)
    tries_str = get_val("tries", "1")
    tries = int(re.search(r'\d+', tries_str).group()) if re.search(r'\d+', tries_str) else 1
    topic = get_val("topic", "misc")
    url = get_val("problem_link", "#")
    created_str = get_val("created", "?")
    
    created_date = None
    if created_str and "?" not in created_str:
        try:
            created_date = datetime.strptime(created_str, "%Y-%m-%d").date()
        except ValueError:
            pass # ignore bad dates

    return Problem(
        filename=path.name,
        platform=platform,
        difficulty=difficulty,
        time_spent_str=time_str,
        time_spent_mins=time_mins,
        created=created_date,
        tries=tries,
        topic=topic,
        url=url
    )

def scan_problems() -> List[Problem]:
    problems = []
    for p in REPO_ROOT.glob("*"):
        if not p.is_file(): continue
        if p.name.startswith("."): continue
        if p.name == "TEMPLATE.py": continue
        if p.name in ("README.md", "README.MD"): continue
        
        prob = parse_file(p)
        if prob:
            problems.append(prob)
    return problems

def normalize_cph_paths(problems: List[Problem]) -> int:
    """Normalize .cph .prob url/srcPath to relative paths (.\\filename format)."""
    cph_dir = REPO_ROOT / ".cph"
    if not cph_dir.exists():
        return 0

    filename_to_rel = {}
    for p in problems:
        rel_path = f".\\{p.filename}"
        filename_to_rel[p.filename] = rel_path
        filename_to_rel[p.filename.lower()] = rel_path

    updated = 0
    for prob_file in cph_dir.glob("*.prob"):
        try:
            data = json.loads(prob_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        def normalize_path(value: str) -> Optional[str]:
            if not value:
                return None
            name = None
            if value.startswith("file:"):
                try:
                    parsed = urlparse(value)
                    name = Path(parsed.path).name
                except Exception:
                    name = None
            if not name:
                name = Path(value).name
            if name in filename_to_rel:
                return filename_to_rel[name]
            if name.lower() in filename_to_rel:
                return filename_to_rel[name.lower()]
            return None

        changed = False
        if isinstance(data, dict):
            for key in ("url", "srcPath"):
                if key in data and isinstance(data[key], str):
                    new_val = normalize_path(data[key])
                    if new_val and data[key] != new_val:
                        data[key] = new_val
                        changed = True

        if changed:
            prob_file.write_text(json.dumps(data, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
            updated += 1

    return updated

# --------------------------------------------------
# Stats Calculation
# --------------------------------------------------

def can_restore_streak(last_activity_date: date, today: date) -> bool:
    """Check if streak can be restored (within 48 hours)."""
    delta = (today - last_activity_date).days
    return 1 <= delta <= 2  # 1 or 2 days = within 48 hours

def calc_streak(problems: List[Problem], config: dict) -> tuple[int, int]:
    """
    Calculate current streak and longest streak.
    Returns (current_streak, longest_streak).
    
    With restore_streak_when_possible enabled:
    - If no activity today but last activity was within 48hrs (1-2 days ago), streak continues
    - Otherwise, streak breaks and resets to 0
    """
    dates = sorted({p.created for p in problems if p.created})
    if not dates:
        return 0, 0
    
    today = datetime.now().date()
    restore_enabled = config.get("readme", {}).get("restore_streak_when_possible", False)
    
    # Get cached data
    cache = config.get("optimization", {}).get("cache", {})
    cached_longest = cache.get("longest_streak", 0)
    last_activity_str = cache.get("last_activity_date")
    last_activity = datetime.strptime(last_activity_str, "%Y-%m-%d").date() if last_activity_str else None
    
    # Calculate current streak working backwards from today
    current_streak = 0
    check_date = today
    
    # If no activity today, check if we can restore the streak
    if check_date not in dates:
        if restore_enabled and last_activity and can_restore_streak(last_activity, today):
            # Streak can be restored - continue from yesterday or 2 days ago
            check_date = last_activity
        else:
            # Check yesterday only
            check_date = today - timedelta(days=1)
    
    # Count consecutive days
    while check_date in dates:
        current_streak += 1
        check_date -= timedelta(days=1)
    
    # If streak broke beyond restore window, reset to 0
    if current_streak == 0 and restore_enabled:
        if last_activity and (today - last_activity).days > 2:
            current_streak = 0
    
    # Calculate longest streak ever (scan all dates)
    longest_streak = 0
    temp_streak = 0
    prev_date = None
    
    for date in dates:
        if prev_date is None:
            temp_streak = 1
        elif (date - prev_date).days == 1:
            temp_streak += 1
        else:
            temp_streak = 1
        
        longest_streak = max(longest_streak, temp_streak)
        prev_date = date
    
    # Compare with cached longest streak
    longest_streak = max(longest_streak, cached_longest, current_streak)
    
    return current_streak, longest_streak

def format_duration(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes}m"
    h, m = divmod(minutes, 60)
    return f"{h}h {m}m"

def generate_topics_breakdown(problems: List[Problem], config: dict) -> str:
    """Generate a markdown list of topics covered with counts."""
    topic_counter = Counter()
    topic_filters = config.get("readme", {}).get("topic_filters", {})
    exclude = topic_filters.get("exclude", ["?", "misc"])
    min_count = topic_filters.get("min_count", 1)
    
    for p in problems:
        # Split topics by comma and clean them up
        topics = [t.strip().lower() for t in p.topic.split(',')]
        for topic in topics:
            if topic and topic not in exclude:
                topic_counter[topic] += 1
    
    if not topic_counter:
        return "_No topics tracked yet._"
    
    # Filter by min_count
    topic_counter = {k: v for k, v in topic_counter.items() if v >= min_count}
    
    # Sort by count (descending), then alphabetically
    sorted_topics = sorted(topic_counter.items(), key=lambda x: (-x[1], x[0]))
    
    lines = []
    for topic, count in sorted_topics:
        # Format: "arrays (12)", "hashing (8)", etc.
        lines.append(f"- **{topic}** ({count})")
    
    return "\n".join(lines)

# --------------------------------------------------
# Markdown Generation
# --------------------------------------------------

def generate_badges(total_solved: int, current_streak: int, longest_streak: int, total_time_mins: int, config: dict) -> str:
    """Generate badges based on config settings."""
    readme_config = config.get("readme", {})
    badge_style = readme_config.get("badge_style", "for-the-badge")
    show_streak = readme_config.get("show_streak", True)
    
    badges = []
    badges.append(f"![Solved](https://img.shields.io/badge/Solved-{total_solved}-blue?style={badge_style})")
    
    if show_streak:
        badges.append(f"![Streak](https://img.shields.io/badge/Streak-{current_streak}%20Days-orange?style={badge_style})")
        badges.append(f"![Longest Streak](https://img.shields.io/badge/Longest%20Streak-{longest_streak}%20Days-red?style={badge_style})")
    
    time_str = format_duration(total_time_mins).replace(" ", "%20")
    badges.append(f"![Time Spent](https://img.shields.io/badge/Time%20Spent-{time_str}-success?style={badge_style})")
    
    return " ".join(badges)

def generate_progress_table(problems: List[Problem], config: dict) -> str:
    """Generate stats table based on config platform order."""
    readme_config = config.get("readme", {})
    platform_order = readme_config.get("platforms", ["GeeksForGeeks", "LeetCode", "HackerRank", "Codeforces"])
    
    # Reverse map for display: slug -> Proper Name
    slug_to_name = {v: k for k, v in PLATFORM_MAP.items()}
    
    # Group by Proper Name
    grouped = defaultdict(list)
    for p in problems:
        display_name = slug_to_name.get(p.platform, p.platform.title())
        grouped[display_name].append(p)
    
    # Add any others found
    remaining_keys = sorted([k for k in grouped.keys() if k not in platform_order])
    final_order = platform_order + remaining_keys
    
    lines = []
    # Columns: Platform | Solved | Easy | Medium | Hard | Avg Time | Avg Tries | Vibe
    lines.append("| Platform | Solved | Easy | Medium | Hard | Avg Time | Avg Tries | Vibe |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    for plat in final_order:
        probs = grouped.get(plat, [])
        # Only skip if empty AND not in our main list (we want to show 0s for main platforms)
        if not probs and plat not in platform_order:
            continue
            
        count = len(probs)
        
        # Difficulty breakdown
        easy = sum(1 for p in probs if "easy" in p.difficulty.lower())
        medium = sum(1 for p in probs if "medium" in p.difficulty.lower())
        hard = sum(1 for p in probs if "hard" in p.difficulty.lower())
        
        # Avg Stats
        valid_times = [p.time_spent_mins for p in probs if p.time_spent_mins > 0]
        avg_time = int(sum(valid_times) / len(valid_times)) if valid_times else 0
        
        valid_tries = [p.tries for p in probs]
        avg_tries = sum(valid_tries) / len(valid_tries) if valid_tries else 0.0
        
        # Vibe Check
        vibe = "ghost town"
        if count > 0:
            vibe = "warming up"
            if count > 10: vibe = "cooking"
            if count > 50: vibe = "on fire"
            if "LeetCode" in plat and hard > 5: vibe = "god mode"
        
        # Row
        avg_tries_str = f"{avg_tries:.1f}" if count > 0 else "-"
        avg_time_str = format_duration(avg_time) if count > 0 else "-"
        
        lines.append(f"| **{plat}** | {count} | {easy} | {medium} | {hard} | {avg_time_str} | {avg_tries_str} | {vibe} |")
        
    return "\n".join(lines)

def update_readme(problems: List[Problem], config: dict):
    """Update README using placeholders and save optimization data to config."""
    if not README.exists():
        return

    old_text = README.read_text(encoding="utf-8")
    text = old_text
    
    # Calculate stats
    current_streak, longest_streak = calc_streak(problems, config)
    total_time = sum(p.time_spent_mins for p in problems)
    total_solved = len(problems)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Get latest activity date
    dates = sorted({p.created for p in problems if p.created})
    last_activity_date = dates[-1].strftime("%Y-%m-%d") if dates else timestamp
    
    # Generate content based on config
    readme_config = config.get("readme", {})
    
    badges_md = ""
    if readme_config.get("show_badges", True):
        badges_md = generate_badges(total_solved, current_streak, longest_streak, total_time, config)
    
    stats_table = ""
    if readme_config.get("show_stats_table", True):
        stats_table = generate_progress_table(problems, config)
    
    topics_md = ""
    if readme_config.get("show_topics", True):
        topics_md = generate_topics_breakdown(problems, config)
    
    # Replace placeholders with preservation
    def replace_chunk(content: str, marker: str, new_content: str, inline: bool = False) -> str:
        # Pattern for existing block: <!-- MARKER --> ... <!-- MARKER_END -->
        # Using non-greedy match
        pattern = re.compile(rf"<!-- {marker} -->(.*?)<!-- {marker}_END -->", re.DOTALL)
        
        if inline:
            formatted = f"<!-- {marker} -->{new_content}<!-- {marker}_END -->"
        else:
            # Match Prettier's behavior: blank line before and after content
            formatted = f"<!-- {marker} -->\n\n{new_content}\n\n<!-- {marker}_END -->"
        
        if pattern.search(content):
            return pattern.sub(formatted, content)
        
        # Fallback: first time replacement
        start_marker = f"<!-- {marker} -->"
        if start_marker in content:
            return content.replace(start_marker, formatted)
        
        return content

    text = replace_chunk(text, "GRIND_BADGES", badges_md)
    text = replace_chunk(text, "GRIND_STATS_TABLE", stats_table)
    text = replace_chunk(text, "GRIND_TOPICS", topics_md)
    text = replace_chunk(text, "GRIND_TIMESTAMP", timestamp, inline=True)
    
    # Only write README if content changed
    if text != old_text:
        README.write_text(text, encoding="utf-8")
    
    # Update optimization cache in config
    topic_counter = Counter()
    for p in problems:
        topics = [t.strip().lower() for t in p.topic.split(',')]
        for topic in topics:
            if topic and topic not in ["?", "misc"]:
                topic_counter[topic] += 1
    
    config["optimization"]["last_update"] = timestamp
    config["optimization"]["total_files_scanned"] = total_solved
    config["optimization"]["cache"]["total_solved"] = total_solved
    config["optimization"]["cache"]["total_time_mins"] = total_time
    config["optimization"]["cache"]["current_streak"] = current_streak
    config["optimization"]["cache"]["longest_streak"] = longest_streak
    config["optimization"]["cache"]["last_activity_date"] = last_activity_date
    config["optimization"]["cache"]["topics"] = dict(topic_counter)
    
    # Update stats section
    platform_stats = {}
    slug_to_name = {v: k for k, v in PLATFORM_MAP.items()}
    grouped = defaultdict(list)
    for p in problems:
        display_name = slug_to_name.get(p.platform, p.platform.title())
        grouped[display_name].append(p)
    
    for platform, probs in grouped.items():
        platform_stats[platform] = {
            "count": len(probs),
            "easy": sum(1 for p in probs if "easy" in p.difficulty.lower()),
            "medium": sum(1 for p in probs if "medium" in p.difficulty.lower()),
            "hard": sum(1 for p in probs if "hard" in p.difficulty.lower())
        }
    
    config["stats"]["total_solved"] = total_solved
    config["stats"]["platforms"] = platform_stats
    config["stats"]["last_scan_timestamp"] = timestamp
    
    # Save updated config
    save_config(config)
    
    # Display results
    user_info = config.get("user", {})
    user_name = user_info.get("name", "")
    
    print("\n" + "="*60)
    print("📊 STATS UPDATE COMPLETE")
    print("="*60)
    if user_name:
        print(f"User: {user_name}")
    print(f"Problems Solved: {total_solved}")
    print(f"🔥 Current Streak: {current_streak} days")
    print(f"🏆 Longest Streak: {longest_streak} days")
    print(f"⏱️  Total Time: {format_duration(total_time)}")
    print("="*60)
    print("✅ README.md updated")
    print("💾 grind.json updated")

if __name__ == "__main__":
    config = load_config()
    probs = scan_problems()
    cph_updated = normalize_cph_paths(probs)
    update_readme(probs, config)
    if cph_updated:
        print(f"🔧 Updated {cph_updated} .cph file(s)")
    print("="*60 + "\n")
