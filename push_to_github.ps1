param(
    [string]$RemoteUrl = "https://github.com/omanox-dev/StreamPick.git",
    [string]$Branch = "main"
)

Write-Host "Preparing repository for push to $RemoteUrl on branch $Branch"

if (-not (git rev-parse --is-inside-work-tree 2>$null)) {
    git init
    Write-Host "Initialized git repository."
}

git add -A

$status = git status --porcelain
if ($status) {
    git commit -m "Prepare repo for GitHub push: add push script and instructions"
    Write-Host "Committed changes."
} else {
    Write-Host "No changes to commit."
}

try {
    $cur = git remote get-url origin 2>$null
    if ($cur -ne $RemoteUrl) {
        git remote remove origin 2>$null
        git remote add origin $RemoteUrl
        Write-Host "Set origin to $RemoteUrl"
    } else {
        Write-Host "Remote origin already set to $RemoteUrl"
    }
} catch {
    git remote add origin $RemoteUrl
    Write-Host "Added origin $RemoteUrl"
}

git branch -M $Branch
Write-Host "Pushing to origin/$Branch ... (may prompt for credentials)"
git push -u origin $Branch

Write-Host "Done. If the push failed due to credentials, run this script again after configuring your credentials or use SSH.
"
