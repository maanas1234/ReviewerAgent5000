import os
import json
from datetime import datetime
from github import Github
from github.Auth import Token

# ---------------------------------
# CONFIG
# ---------------------------------
REPO_NAME = "anvijain1/India-Air-Quality-Analysis"

# ---------------------------------
# GITHUB AUTH
# ---------------------------------
token = os.getenv("GITHUB_TOKEN")

if token:
    g = Github(auth=Token(token))
else:
    g = Github()

# ---------------------------------
# LOAD REPO
# ---------------------------------
repo = g.get_repo(REPO_NAME)

contents = repo.get_contents("", ref="main")

repo_files = {}

# ---------------------------------
# RECURSIVELY COLLECT PY FILES
# ---------------------------------
while contents:
    file_content = contents.pop(0)

    if file_content.type == "dir":
        contents.extend(
            repo.get_contents(
                file_content.path,
                ref="main"
            )
        )

    elif file_content.type == "file" and file_content.name.endswith(".py"):
        try:
            code = file_content.decoded_content.decode("utf-8")
        except UnicodeDecodeError:
            print(f"Skipping: {file_content.path}")
            continue

        repo_files[file_content.path] = code
        print(f"Loaded: {file_content.path}")

# ---------------------------------
# CREATE UNIQUE OUTPUT FILE
# ---------------------------------
repo_slug = REPO_NAME.split("/")[-1]

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

output_filename = f"repodumps/{repo_slug}_{timestamp}.json"

# ---------------------------------
# SAVE
# ---------------------------------
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(
        repo_files,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"\nTotal Python files loaded: {len(repo_files)}")
print(f"Saved to: {output_filename}")