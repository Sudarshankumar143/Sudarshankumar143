import json
import os
import re
import urllib.request

USER = os.environ.get("GH_USER", "Sudarshankumar143")
TOKEN = os.environ.get("GITHUB_TOKEN")
LIMIT = 6  # kitne repos dikhane hain
THEME = "tokyonight"

url = f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=pushed"
req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
if TOKEN:
    req.add_header("Authorization", f"Bearer {TOKEN}")

with urllib.request.urlopen(req) as r:
    repos = json.load(r)

# Sirf apne repos: fork, archived aur profile repo hide
repos = [
    x for x in repos
    if not x["fork"] and not x["archived"] and x["name"].lower() != USER.lower()
]
repos.sort(key=lambda x: x["pushed_at"], reverse=True)
repos = repos[:LIMIT]

cards = [
    f'<a href="{x["html_url"]}"><img src="https://github-readme-stats.vercel.app/api/pin/'
    f'?username={USER}&repo={x["name"]}&theme={THEME}" width="48%" alt="{x["name"]}" /></a>'
    for x in repos
]

rows = []
for i in range(0, len(cards), 2):
    rows.append('<p align="center">\n  ' + "\n  ".join(cards[i:i + 2]) + "\n</p>")

block = "\n".join(rows) if rows else "_Abhi koi public repo nahi hai._"

with open("README.md", encoding="utf-8") as f:
    content = f.read()

new = re.sub(
    r"<!--REPOS:START-->.*?<!--REPOS:END-->",
    f"<!--REPOS:START-->\n{block}\n<!--REPOS:END-->",
    content,
    flags=re.DOTALL,
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new)
￼Enter
