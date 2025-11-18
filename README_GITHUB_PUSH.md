# Push instructions for GitHub

This file explains how to push this project to GitHub. The repository you requested is:

```
https://github.com/omanox-dev/StreamPick
```

How to run the provided PowerShell helper script (recommended):

1. Open PowerShell in the project root: `C:\Users\Om\Documents\GIG Workshop\Mini Project`
2. Run the script (may prompt for credentials):

```powershell
.\push_to_github.ps1
```

Notes:
- The script will `git init` if this folder is not already a git repo, stage all files, commit if there are changes, set the `origin` remote to the repository above, rename the current branch to `main` and push with `-u origin main`.
- If your Git is configured with credential manager or SSH keys, the push will succeed without additional steps. If not, Git may prompt for username/password or for a personal access token (PAT). Use a PAT in place of your password if required by GitHub.
- If the push fails due to execution policy preventing scripts, run PowerShell as Administrator and set `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` and try again.
- If you prefer SSH, add an SSH remote and run `git push -u origin main` yourself.

If you want me to also add a `.gitattributes` or use `git lfs` for large media, say so and I will add helper files.
