import git


#g=git.Git(r"C:\WORK\VM_SHARE\python\testGit").

GIT_REPO="https://github.com/ganeshkp/apex-read.git"
GIT_FILDER="C:/WORK/VM_SHARE/apex-read"

repo=git.Repo(GIT_FILDER)
o=repo.remotes.origin
o.pull()

print("GIT Cloned")
