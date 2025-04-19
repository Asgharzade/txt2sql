#!/usr/bin/env pwsh
# Script to remove sensitive information from Git history

Write-Host "Creating a backup branch of your current state..."
git branch -m backup-before-cleaning

Write-Host "Creating a new clean-history branch..."
git checkout --orphan clean-history

Write-Host "Getting all files from the last commit but excluding .env..."
git reset
Remove-Item -Path ".env" -Force -ErrorAction SilentlyContinue
git add .
git commit -m "Initial commit with clean history (secrets removed)"

Write-Host "Replacing .env with a template .env.example..."
Copy-Item -Path ".env.example" -Destination ".env.example" -Force

Write-Host "Adding .env to .gitignore if not already present..."
if (-not (Select-String -Path ".gitignore" -Pattern "^\.env$" -Quiet)) {
    Add-Content -Path ".gitignore" -Value "`n# Exclude environment files with secrets`n.env"
}

git add .gitignore .env.example
git commit -m "Add .env.example template and ensure .env is gitignored"

Write-Host "`nProcess complete!"
Write-Host "Your history is now clean in the 'clean-history' branch."
Write-Host "The original history is preserved in the 'backup-before-cleaning' branch."
Write-Host "`nTo continue working with the clean history:"
Write-Host "1. Delete the old .env file and create a new one with your secrets"
Write-Host "2. Force push this branch to origin if needed with: git push -f origin clean-history:main" 