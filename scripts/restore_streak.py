#!/usr/bin/env python3
"""
author: Michael Perry Tettey
repo: dsa-grind

purpose:
- restore streaks within 48 hours of last activity
- check if streak can be restored based on config settings
- provide manual streak restoration capability
- smart restoration: updates file metadata and git commit history
"""

from __future__ import annotations

import json
import sys
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# --------------------------------------------------
# Paths
# --------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_FILE = REPO_ROOT / "config" / "grind.json"

# --------------------------------------------------
# Config Management
# --------------------------------------------------

def load_config() -> dict:
    """Load configuration from grind.json"""
    if not CONFIG_FILE.exists():
        print("❌ Config file not found. Run update_stats.py first.")
        sys.exit(1)
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config: dict) -> None:
    """Save configuration to grind.json"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# --------------------------------------------------
# Streak Restoration Logic
# --------------------------------------------------

def can_restore_streak(last_activity_date_str: str) -> tuple[bool, int]:
    """
    Check if streak can be restored (within 48 hours).
    Returns (can_restore, days_since_activity)
    """
    if not last_activity_date_str:
        return False, -1
    
    try:
        last_activity = datetime.strptime(last_activity_date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        days_since = (today - last_activity).days
        
        # Within 48 hours means 1 or 2 days
        can_restore = 1 <= days_since <= 2
        return can_restore, days_since
    except Exception as e:
        print(f"❌ Error parsing date: {e}")
        return False, -1

def get_problem_files() -> list[tuple[Path, datetime]]:
    """Get all problem files with their created dates."""
    problem_files = []
    
    for path in REPO_ROOT.glob("*"):
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        if path.name in ["TEMPLATE.py", "README.md", "README.MD"]:
            continue
        
        # Check if it matches problem pattern (Platform_Name.ext)
        if "_" in path.name and path.suffix in [".py", ".js", ".ts", ".cpp", ".java", ".go", ".rs"]:
            # Extract created date from file
            try:
                content = path.read_text(encoding="utf-8")
                match = re.search(r'created:\s*(\d{4}-\d{2}-\d{2})', content)
                if match:
                    created = datetime.strptime(match.group(1), "%Y-%m-%d")
                    problem_files.append((path, created))
            except Exception:
                continue
    
    # Sort by created date (most recent first)
    problem_files.sort(key=lambda x: x[1], reverse=True)
    return problem_files

def update_file_created_date(file_path: Path, new_date: str) -> bool:
    """Update the 'created' field in a problem file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # Replace the created date
        updated_content = re.sub(
            r'created:\s*\d{4}-\d{2}-\d{2}',
            f'created: {new_date}',
            content
        )
        
        if updated_content != content:
            file_path.write_text(updated_content, encoding="utf-8")
            return True
        return False
    except Exception as e:
        print(f"❌ Error updating {file_path.name}: {e}")
        return False

def get_git_commits_for_file(file_path: Path, days_back: int = 7) -> list[dict]:
    """Get recent git commits for a specific file."""
    try:
        # Get commits for this file from the last N days
        result = subprocess.run(
            ["git", "log", "--format=%H|%ai|%s", f"--since={days_back} days ago", "--", str(file_path.name)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue
            parts = line.split('|', 2)
            if len(parts) == 3:
                commits.append({
                    'hash': parts[0],
                    'date': parts[1],
                    'message': parts[2]
                })
        return commits
    except Exception:
        return []

def update_git_commit_date(commit_hash: str, new_date: str) -> bool:
    """Update the date of a git commit using filter-branch or rebase."""
    try:
        # Format: YYYY-MM-DD to full ISO datetime (use noon for consistency)
        dt = datetime.strptime(new_date, "%Y-%m-%d")
        # Set to noon local time
        iso_date = dt.strftime("%Y-%m-%d 12:00:00")
        
        # Use git filter-branch to change the commit date
        # This is simpler than interactive rebase for automation
        env = {
            'GIT_COMMITTER_DATE': iso_date,
            'GIT_AUTHOR_DATE': iso_date
        }
        
        result = subprocess.run(
            ["git", "commit", "--amend", "--no-edit", "--date", iso_date],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            env={**subprocess.os.environ, **env}
        )
        
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️  Could not update git commit: {e}")
        return False

def smart_restore_streak(days_to_fill: int, dry_run: bool = False, auto_confirm: bool = False) -> bool:
    """
    Smart streak restoration: updates file metadata and git history.
    
    Args:
        days_to_fill: Number of missing days to fill (1-2)
        dry_run: If True, show what would be done without doing it
    
    Returns:
        True if successful, False otherwise
    """
    problem_files = get_problem_files()
    
    if not problem_files:
        print("❌ No problem files found to restore streak with.")
        return False
    
    print("\n⚠️  IMPORTANT: If commits already pushed to remote:")
    print("   git push --force-with-lease")
    print("   This rewrites history - use with caution!")
    
    # We need files to fill the gap
    # If we're 2 days behind, we need to backdate the most recent file(s)
    today = datetime.now().date()
    files_to_update = []
    
    # Get the most recent files that we can backdate
    for i in range(min(days_to_fill, len(problem_files))):
        file_path, created = problem_files[i]
        # Calculate what date this should be to fill the gap
        target_date = today - timedelta(days=days_to_fill - i)
        target_date_str = target_date.strftime("%Y-%m-%d")
        
        files_to_update.append({
            'path': file_path,
            'current_date': created.strftime("%Y-%m-%d"),
            'target_date': target_date_str,
            'file_name': file_path.name
        })
    
    if not files_to_update:
        print("❌ No suitable files found for streak restoration.")
        return False
    
    # Show what will be done
    print("\n" + "="*60)
    print("🔧 SMART STREAK RESTORATION PLAN")
    print("="*60)
    print(f"Mode: {'DRY RUN (preview only)' if dry_run else 'LIVE (will modify files and git)'}")
    print(f"Missing Days: {days_to_fill}")
    print("="*60)
    
    for item in files_to_update:
        print(f"\n📝 {item['file_name']}")
        print(f"   Current date: {item['current_date']}")
        print(f"   New date:     {item['target_date']}")
    
    print("="*60)
    
    if dry_run:
        print("\n💡 Run without --dry-run to apply these changes")
        return True
    
    # Ask for confirmation (or auto-confirm in non-interactive environments)
    if auto_confirm:
        print("\n✅ Auto-confirm enabled (workflow mode). Proceeding...")
    else:
        response = input("\n⚠️  This will modify files and git history. Continue? (yes/no): ").strip().lower()
        if response != 'yes':
            print("❌ Restoration cancelled.")
            return False
    
    # Apply changes
    print("\n" + "="*60)
    print("🚀 APPLYING CHANGES")
    print("="*60)
    
    success_count = 0
    for item in files_to_update:
        print(f"\n📝 Updating {item['file_name']}...")
        
        # Update file metadata
        if update_file_created_date(item['path'], item['target_date']):
            print(f"   ✅ File metadata updated")
            success_count += 1
            
            # Stage the file for git
            try:
                subprocess.run(
                    ["git", "add", str(item['path'].name)],
                    cwd=REPO_ROOT,
                    check=True,
                    capture_output=True
                )
                print(f"   ✅ Staged for git commit")
            except Exception as e:
                print(f"   ⚠️  Could not stage file: {e}")
        else:
            print(f"   ❌ Failed to update file metadata")
    
    # Create backdated commits (including empty commits for missing days)
    if success_count > 0:
        print("\n🔄 Updating git history...")
        try:
            # Check if there are staged changes
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True
            )

            # Build unique target dates (sorted)
            target_dates = sorted({item['target_date'] for item in files_to_update})

            # If we have staged changes, commit them on the most recent target date
            committed_date = None
            if status.stdout.strip():
                committed_date = target_dates[-1]
                dt = datetime.strptime(committed_date, "%Y-%m-%d")
                iso_date = dt.strftime("%Y-%m-%d 12:00:00")

                env = dict(subprocess.os.environ)
                env['GIT_AUTHOR_DATE'] = iso_date
                env['GIT_COMMITTER_DATE'] = iso_date

                result = subprocess.run(
                    ["git", "commit", "-m", f"Restore streak: backdate to {committed_date}"],
                    cwd=REPO_ROOT,
                    env=env,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"   ✅ Created git commit with date: {committed_date}")
                else:
                    print(f"   ⚠️  Git commit failed: {result.stderr}")
            else:
                print("   ℹ️  No staged changes. Will create backdated empty commits.")

            # Create empty commits for any remaining missing dates
            for date_str in target_dates:
                if date_str == committed_date:
                    continue
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                iso_date = dt.strftime("%Y-%m-%d 12:00:00")

                env = dict(subprocess.os.environ)
                env['GIT_AUTHOR_DATE'] = iso_date
                env['GIT_COMMITTER_DATE'] = iso_date

                result = subprocess.run(
                    ["git", "commit", "--allow-empty", "-m", f"Restore streak: backdate to {date_str}"],
                    cwd=REPO_ROOT,
                    env=env,
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"   ✅ Created empty commit for: {date_str}")
                else:
                    print(f"   ⚠️  Empty commit failed for {date_str}: {result.stderr}")

            print("\n💡 If these commits were already pushed, you may need:")
            print("   git push --force")
        except Exception as e:
            print(f"   ⚠️  Could not update git history: {e}")
    
    print("="*60)
    print(f"\n✅ Restoration complete! Updated {success_count} file(s)")
    print("🔥 Run 'python scripts/update_stats.py' to refresh your streak!")
    print("="*60 + "\n")
    
    return success_count > 0

def restore_streak() -> None:
    """Attempt to restore streak if within 48-hour window."""
    config = load_config()
    
    # Check if restore is enabled
    restore_enabled = config.get("readme", {}).get("restore_streak_when_possible", False)
    
    if not restore_enabled:
        print("⚠️  Streak restoration is disabled in config.")
        print("   Set 'restore_streak_when_possible': true in config/grind.json to enable.")
        return
    
    # Get cached data
    cache = config.get("optimization", {}).get("cache", {})
    last_activity_date = cache.get("last_activity_date")
    current_streak = cache.get("current_streak", 0)
    
    if not last_activity_date:
        print("ℹ️  No previous activity found. Start solving problems to begin your streak!")
        return
    
    # Check if restoration is possible
    can_restore, days_since = can_restore_streak(last_activity_date)
    
    today = datetime.now().date()
    last_date = datetime.strptime(last_activity_date, "%Y-%m-%d").date()
    
    print("\n" + "="*60)
    print("🔥 STREAK RESTORATION CHECK")
    print("="*60)
    print(f"Last Activity: {last_activity_date}")
    print(f"Days Since Activity: {days_since}")
    print(f"Current Streak: {current_streak} days")
    print(f"Restoration Enabled: {'✅ Yes' if restore_enabled else '❌ No'}")
    print("="*60)
    
    if days_since == 0:
        print("✅ You've already solved problems today! Streak is active.")
        print(f"   Current streak: {current_streak} days")
    elif can_restore:
        print(f"✅ Streak can be restored! You have {2 - days_since} day(s) remaining.")
        print(f"   Your {current_streak}-day streak can be saved!")
        print("\n" + "="*60)
        print("💡 RESTORATION OPTIONS")
        print("="*60)
        print("Option 1: Solve a new problem today (recommended)")
        print("   → python scripts/new_problem.py <url>")
        print("\nOption 2: Smart restore (backdate recent files)")
        print("   → python scripts/restore_streak.py --smart")
        print("   → Modifies file metadata and git history")
        print("="*60)
    else:
        if days_since > 2:
            print(f"❌ Streak cannot be restored. It's been {days_since} days since your last activity.")
            print(f"   The 48-hour window has passed.")
            print(f"\n   Your previous streak was: {current_streak} days")
            print("   Start a new streak by solving a problem today! 💪")
        else:
            print("ℹ️  No streak to restore yet. Keep grinding!")
    
    print("="*60 + "\n")

def check_streak_status() -> None:
    """Display current streak status information."""
    config = load_config()
    cache = config.get("optimization", {}).get("cache", {})
    
    current_streak = cache.get("current_streak", 0)
    longest_streak = cache.get("longest_streak", 0)
    last_activity = cache.get("last_activity_date", "Never")
    total_solved = cache.get("total_solved", 0)
    
    print("\n" + "="*60)
    print("📊 STREAK STATUS")
    print("="*60)
    print(f"Total Problems Solved: {total_solved}")
    print(f"Current Streak: {current_streak} days 🔥")
    print(f"Longest Streak: {longest_streak} days 🏆")
    print(f"Last Activity: {last_activity}")
    print("="*60 + "\n")

# --------------------------------------------------
# CLI
# --------------------------------------------------

def main():
    """Main entry point for streak restoration script."""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command in ["status", "check", "info"]:
            check_streak_status()
        elif command in ["--smart", "smart", "-s"]:
            # Smart restoration mode
            config = load_config()
            cache = config.get("optimization", {}).get("cache", {})
            last_activity_date = cache.get("last_activity_date")
            readme_cfg = config.get("readme", {})
            auto_confirm_cfg = readme_cfg.get("restore_streak_auto_apply", False)
            
            if not last_activity_date:
                print("❌ No previous activity found. Nothing to restore.")
                return
            
            can_restore, days_since = can_restore_streak(last_activity_date)
            
            if not can_restore:
                print(f"❌ Cannot restore streak. Days since last activity: {days_since}")
                if days_since > 2:
                    print("   The 48-hour window has passed.")
                return
            
            # Check for flags
            dry_run = "--dry-run" in sys.argv or "--preview" in sys.argv
            auto_confirm_flag = "--yes" in sys.argv or "-y" in sys.argv
            
            # Perform smart restoration
            smart_restore_streak(days_since, dry_run=dry_run, auto_confirm=auto_confirm_flag or auto_confirm_cfg)
            
        elif command in ["help", "-h", "--help"]:
            print("\n" + "="*60)
            print("RESTORE STREAK - Usage")
            print("="*60)
            print("python scripts/restore_streak.py")
            print("   Check if streak can be restored")
            print()
            print("python scripts/restore_streak.py status")
            print("   Show current streak status")
            print()
            print("python scripts/restore_streak.py --smart")
            print("   Smart restore: backdate recent files & git commits")
            print("   (modifies file metadata and git history)")
            print()
            print("python scripts/restore_streak.py --smart --dry-run")
            print("   Preview what smart restore would do")
            print()
            print("python scripts/restore_streak.py help")
            print("   Show this help message")
            print("="*60 + "\n")
        else:
            print(f"❌ Unknown command: {command}")
            print("   Use 'help' for available commands.")
    else:
        restore_streak()

if __name__ == "__main__":
    main()
