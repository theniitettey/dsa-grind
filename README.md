<!-- GRIND_BADGES -->

![Solved](https://img.shields.io/badge/Solved-30-blue?style=for-the-badge) ![Streak](https://img.shields.io/badge/Streak-1%20Days-orange?style=for-the-badge) ![Longest Streak](https://img.shields.io/badge/Longest%20Streak-16%20Days-red?style=for-the-badge) ![Time Spent](https://img.shields.io/badge/Time%20Spent-1h%200m-success?style=for-the-badge)

<!-- GRIND_BADGES_END -->

## current stats

<!-- GRIND_STATS_TABLE -->

| Platform          | Solved | Easy | Medium | Hard | Avg Time | Avg Tries | Vibe       |
| :---------------- | :----: | :--: | :----: | :--: | :------: | :-------: | :--------- |
| **GeeksForGeeks** |   3    |  3   |   0    |  0   |    2m    |    1.0    | warming up |
| **LeetCode**      |   19   |  13  |   6    |  0   |    2m    |    1.0    | cooking    |
| **HackerRank**    |   2    |  2   |   0    |  0   |    2m    |    1.0    | warming up |
| **Codeforces**    |   6    |  6   |   0    |  0   |    1m    |    1.0    | warming up |

<!-- GRIND_STATS_TABLE_END -->

### topics covered

<!-- GRIND_TOPICS -->

- **arrays** (24)
- **hash tables** (11)
- **implementation** (10)
- **math** (9)
- **strings** (9)
- **hash sets** (4)
- **greedy** (2)
- **counting** (1)
- **geometry** (1)
- **hashing** (1)
- **matrix** (1)
- **prefix sums** (1)
- **sorting** (1)
- **two pointers** (1)
- **voting algorithm** (1)

<!-- GRIND_TOPICS_END -->

## _last updated: <!-- GRIND_TIMESTAMP -->now<!-- GRIND_TIMESTAMP_END -->_

---

documenting my journey from  
**“what’s a linked list?”**  
to **“okay… i won’t embarrass myself in interviews today.”**

this repo exists because:

- vibes don’t pass interviews
- “i’ll figure it out on the job” apparently isn’t a strategy
- muscle memory doesn’t build itself

so yeah. we grind.

---

<details>
<summary><strong>the mission</strong></summary>

solve problems.  
understand _why_ they work.  
get better over time.  
land a job.  
stop being terrible at this.

**preferably in that order.**

</details>

---

<details><summary><strong>streak system (48hr restoration)</strong></summary>

### how it works

the repo tracks streaks with a **48-hour restoration window** to keep you motivated without being punishing.

**streak logic:**

1. **Active** — solved a problem today? streak continues 🔥
2. **Restorable** — haven't solved anything today BUT last activity was 1-2 days ago? solve today to restore your streak ⚠️
3. **Broken** — 3+ days since last activity? streak resets to 0, but your longest streak is preserved 🏆

### two types of streaks

- **Current Streak** — your active consecutive day count
- **Longest Streak** — your personal best ever (never resets)

both show up in the badges at the top.

### restore_streak.py

use this script to check and restore your streak:

```bash
# check if streak can be restored
python scripts/restore_streak.py

# view current streak status
python scripts/restore_streak.py status

# smart restore: backdate files & git commits (within 48hr window)
python scripts/restore_streak.py --smart

# preview what smart restore would do
python scripts/restore_streak.py --smart --dry-run

# show help
python scripts/restore_streak.py help
```

### smart restoration

**what it does:**

when you run `python scripts/restore_streak.py --smart`, the script:

1. **finds recent problem files** that can be backdated
2. **updates file metadata** — changes the `created:` date in problem files
3. **modifies git history** — creates/amends commits with backdated timestamps
4. **fills the gap** — makes it look like you solved problems on missing days

**when to use:**

- you forgot to commit on time
- you solved problems but didn't push
- your streak broke but you're within the 48hr window
- you want your github commit history to reflect consistent activity

**example:**

```bash
$ python scripts/restore_streak.py --smart

============================================================
🔧 SMART STREAK RESTORATION PLAN (interesting)
============================================================
Mode: LIVE (will modify files and git)
Missing Days: 2
============================================================

📝 LeetCode_Contains_Duplicate.py
  Current date: 2026-01-30
  New date:     2026-02-01

============================================================

⚠️  This will modify files and git history. Continue? (yes/no):
```

**⚠️ warning:**

- modifies file content and git commit history
- requires force push if commits already pushed: `git push --force`
- use dry-run mode first to preview changes
- in CI/workflows, set `restore_streak_auto_apply` to `true` in grind.json
- can't undo easily — backup before running

**example output:**

```
============================================================
🔥 STREAK RESTORATION CHECK
============================================================
Last Activity: 2026-01-31
Days Since Activity: 2
Current Streak: 5 days
Restoration Enabled: ✅ Yes
============================================================
✅ Streak can be restored! You have 0 day(s) remaining.
   Solve a problem today to maintain your 5-day streak!

💡 Tip: Run 'python scripts/new_problem.py' to start a new problem.
============================================================
```

### example scenarios

**scenario 1: active streak**

- last activity: today
- current streak: 5 days
- status: ✅ active — keep going!

**scenario 2: restorable streak**

- last activity: yesterday or 2 days ago
- current streak: 5 days
- status: ⚠️ restorable — solve today to keep your streak!

**scenario 3: broken streak**

- last activity: 3+ days ago
- current streak: 0 days
- longest streak: 5 days (preserved)
- status: ❌ broken — start fresh, but you've done 5 days before!

### configuration

in `config/grind.json`:

```json
{
  "readme": {
    "restore_streak_when_possible": true
  }
}
```

- **`true`** (default) — 48hr restoration window enabled
- **`false`** — traditional streak (must solve today or yesterday)

### automatic tracking

when you run `python scripts/update_stats.py`, the system:

1. calculates current streak (with 48hr window if enabled)
2. updates longest streak if you beat your record
3. tracks last activity date
4. updates both streak badges in README

### benefits

- **forgiveness** — life happens, 48hrs prevents harsh resets
- **motivation** — longest streak shows you what you're capable of
- **transparency** — clear status feedback keeps you accountable
- **flexibility** — can disable restoration if you want traditional tracking

</details>

---

<details>
<summary><strong>where the pain happens</strong></summary>

**current platforms:**

- **[geeksforgeeks](https://www.geeksforgeeks.org/)** — my current home base (warming up here)
- **[leetcode](https://leetcode.com/)** — the final boss (loading…)
- **[hackerrank](https://www.hackerrank.com/)** — when i need variety
- **[codeforces](https://codeforces.com/)** — when i’m feeling brave (or reckless)

no platform loyalty. only progress.

</details>

---

<details>
<summary><strong>how i organize the chaos</strong></summary>

### file naming

```
PlatformName_Question_Title.py
```

examples:

- `GeeksForGeeks_Union_Of_Array_With_Duplicates.py`
- `LeetCode_Two_Sum.py` (soon™)

no setup tax. just think.

### `TEMPLATE.py`

the blueprint every problem file starts from.

**why it exists:**

- keeps documentation consistent
- forces me to think about complexity, edge cases, and takeaways
- removes decision fatigue

the generator:

- fills metadata like `problem_link` and `created`
- renames the `solve` function to match the problem title

no imports.  
no assumptions.  
just structure.

### `scripts/update_stats.py`

keeps the README honest.

**what it does:**

- scans the repo for solved problems using filename prefixes
- counts solutions per platform
- updates the **current stats** table
- refreshes the “last updated” date
- normalizes `.cph` file paths to relative format (`.\\filename.py`)

**manual run:**

```bash
python scripts/update_stats.py
```

### `scripts/fix_cph_paths.py`

fixes `.cph` metadata paths after cloning/forking so Competitive Companion can run testcases correctly.

**what it does:**

- scans `.cph/*.prob`
- converts `srcPath` and `url` to absolute paths in your local repo

**usage:**

```bash
python scripts/fix_cph_paths.py
```

### `scripts/new_problem.py`

scaffolds new problem files with one command.

**what it does:**

- extracts problem title and platform from URL
- generates filename following naming convention
- fills in metadata (link, created date, function name)
- creates `.cph` file for CP Helper integration
- opens the file in VS Code automatically

**usage:**

```bash
python scripts/new_problem.py <url> [--ext py]
```

**example:**

```bash
python scripts/new_problem.py https://leetcode.com/problems/two-sum/
```

outputs:

- `LeetCode_Two_Sum.py` (templated solution file)
- `.cph/.LeetCode_Two_Sum.py_<hash>.prob` (CP Helper metadata)

### `scripts/init_grind.py`

initializes `config/grind.json` with your settings.

**what it does:**

- auto-detects your name from git config
- prompts you to choose: use defaults or enter details manually
- saves user config for README customization

**usage:**

```bash
python scripts/init_grind.py
```

**options:**

- **[1] Use defaults** — auto-detected from git config (fastest)
- **[2] Enter details** — prompt for name and GitHub username

you can always edit `config/grind.json` later to update settings.

### GitHub Actions (automatic stats updates)

there’s a GitHub Actions workflow that runs on every push.

**what it does:**

- detects new commits
- runs `scripts/update_stats.py`
- updates the README automatically if stats changed

so stats stay accurate **without me thinking about it**.

system > motivation.

</details>

---

<details>
<summary><strong>helpers</strong></summary>

small utilities to keep the grind smooth.

### `helpers/leet_2_cph.py`

converts leetcode-style list inputs into CPH test format.

**examples:**

```bash
python helpers/leet_2_cph.py [1,2,3]
echo [[1,2],[3,4]] | python helpers/leet_2_cph.py
```

**output format:**

```
3
1
2
3
```

```
2
1 2
3 4
```

</details>

---

<details>
<summary><strong>configuration (grind.json)</strong></summary>

the `grind.json` file lets you customize how your README looks and stores optimization data.

### quick settings

**customize your name:**

```json
{
  "user": {
    "name": "Your Name",
    "github_username": "yourusername"
  }
}
```

**toggle what shows up:**

```json
{
  "readme": {
    "show_badges": true, // badges at the top
    "show_stats_table": true, // platform stats table
    "show_topics": true, // topics breakdown
    "show_streak": true // streak badge
  }
}
```

**change badge style:**

```json
{
  "readme": {
    "badge_style": "for-the-badge" // or "flat", "flat-square", etc.
  }
}
```

**filter topics:**

```json
{
  "readme": {
    "topic_filters": {
      "exclude": ["?", "misc"], // skip these topics
      "min_count": 1 // only show topics with X+ problems
    }
  }
}
```

**reorder platforms:**

```json
{
  "readme": {
    "platforms": ["LeetCode", "GeeksForGeeks", "HackerRank", "Codeforces"]
  }
}
```

### what gets stored

the script saves optimization data so it doesn't have to rescan everything:

- `optimization.cache` — cached stats (solved count, time, streak, topics)
- `stats.platforms` — breakdown by platform (count, easy/medium/hard)
- `optimization.last_update` — when stats were last updated

### placeholders in README

these get replaced when you run `python scripts/update_stats.py`:

- `![Solved](https://img.shields.io/badge/Solved-8-blue?style=for-the-badge) ![Streak](https://img.shields.io/badge/Streak-2%20Days-orange?style=for-the-badge) ![Time Spent](https://img.shields.io/badge/Time%20Spent-17m-success?style=for-the-badge)` → badges
- | `                 | Platform | Solved | Easy | Medium | Hard | Avg Time | Avg Tries  | Vibe                     |
  | :---------------- | :------: | :----: | :--: | :----: | :--: | :------: | :--------- | ------------------------ |
  | **GeeksForGeeks** |    3     |   3    |  0   |   0    |  2m  |   1.0    | warming up |
  | **LeetCode**      |    5     |   4    |  1   |   0    |  1m  |   1.0    | warming up |
  | **HackerRank**    |    0     |   0    |  0   |   0    |  -   |    -     | ghost town |
  | **Codeforces**    |    0     |   0    |  0   |   0    |  -   |    -     | ghost town | ` → platform stats table |
- `- **arrays** (5)
- **dictionaries** (4)
- **array** (3)
- **hashing** (3)
- **sets** (2)
- **hash map** (1)
- **math** (1)
- **voting algorithm** (1)` → topics list
- `2026-01-30` → last update date

so you can write whatever you want in the README, and only the stats get auto-updated.

no more manual counting. no more stale stats.

</details>

---

_if you’re reading this, you’re probably grinding too._  
_we’ll figure it out. eventually._

_ps: that “sigh…” in my code comments? yeah. that’s real._
