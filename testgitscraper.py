
from github import Github

g=Github("acomeaux93", "Runner1900!!!!!")
repos=g.search_repositories(query="language:python")
for repo in repos:
    print(repo)
