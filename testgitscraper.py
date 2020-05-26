
from github import Github

g=Github("acomeaux93", "Runner1900!!!!!")

user=g.get_user()
#repo=user.create_repo("coviddata")
repo=g.get_repo("acomeaux93/coviddata")
cont=repo.get_contents("coviddata.csv")
repo.delete_file(cont.path, "needs update", cont.sha, branch='master')
repo.create_file("coviddata.csv","commit","This is an update to the file")
