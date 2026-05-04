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

new_stats = f"""
## 📊 GitHub Stats

- Current Streak: {current_streak}
- Longest Streak: {longest_streak}
- Total Contributions: {calendar["totalContributions"]}
"""

import re
updated = re.sub(
    r"## 📊 GitHub Stats[\s\S]*",
    new_stats,
    content
)

with open("README.md", "w") as f:
    f.write(updated)
