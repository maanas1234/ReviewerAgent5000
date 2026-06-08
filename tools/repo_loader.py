import os
from github import Github

# Automatically looks for an environment variable named 'GITHUB_TOKEN'
token = os.getenv("GITHUB_TOKEN")

# Initialize PyGithub with your token
g = Github(token) if token else Github()

repo = g.get_repo("anvijain1/India-Air-Quality-Analysis")

contents = repo.get_contents("", ref="main")

for content_file in contents:
    # Filter for files ending in .py
    if content_file.type == "file" and content_file.name.endswith(".py"):
        print(f"--- File Name: {content_file.name} ---")
        
        # Download and print file content without cloning
        print(content_file.decoded_content.decode("utf-8"))
        print("\n" + "="*40 + "\n")
