import os

import requests
from datetime import datetime

USERNAME = "SushantBaniya"
TOKEN = os.getenv("HELLO")  # Set GitHub token as an environment variable for security
print("token exists", TOKEN is not None)


url = "https://api.github.com/graphql"
headers = {"Authorization": f"bearer {TOKEN}"}

query = """
{
  user(login: "%s") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
""" % USERNAME

response = requests.post(url, json={'query': query}, headers=headers)
data = response.json()

calendar = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
print("Total contributions (last year):", calendar["totalContributions"])

# Calculate streaks
days = []
for week in calendar["weeks"]:
    for day in week["contributionDays"]:
        if day["contributionCount"] > 0:
            days.append(datetime.strptime(day["date"], "%Y-%m-%d").date())

days.sort()
longest_streak = current_streak = 0
streak = 1

for i in range(1, len(days)):
    if (days[i] - days[i-1]).days == 1:
        streak += 1
        longest_streak = max(longest_streak, streak)
    else:
        streak = 1
current_streak = streak

print("Current streak:", current_streak)
print("Longest streak:", longest_streak)

with open("README.md", "r") as f:
    content = f.read()


import re

pct = min(100, round((current_streak / longest_streak) * 100)) if longest_streak else 0
bar_filled = round(pct / 5)   # 20-char bar
bar_empty  = 20 - bar_filled

streak_bar = "█" * bar_filled + "░" * bar_empty

new_stats = f"""
## 📊 GitHub Stats

<!-- STATS_START -->
| | |
|---|---|
| 🔥 Current streak | **{current_streak} days** |
| 🏆 Longest streak | **{longest_streak} days** |
| 📈 Total contributions | **{calendar["totalContributions"]}** |

`{streak_bar}` {pct}% of best streak
<!-- STATS_END -->
"""

updated = re.sub(
    r"<!-- STATS_START -->[\s\S]*<!-- STATS_END -->",
    f"""<!-- STATS_START -->
- Current Streak: {current_streak}
- Longest Streak: {longest_streak}
- Total Contributions: {calendar["totalContributions"]}
<!-- STATS_END -->""",
    content
)

if content == updated:
    print("No changes detected in README")
else:
    print("README updated")

with open("README.md", "w") as f:
    f.write(updated)
