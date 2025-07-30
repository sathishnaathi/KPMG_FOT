#!/bin/bash
set -e

REPO_NAME="kpmg_nuxus-aks-sapi"

echo "Cloning $REPO_NAME"
git clone "https://github.com/${GITHUB_ACTOR}/${REPO_NAME}.git"
cd "$REPO_NAME"

echo "# $REPO_NAME" > README.md

git config user.name "$GITHUB_ACTOR"
git config user.email "${GITHUB_ACTOR}@users.noreply.github.com"

git add README.md
git commit -m "Initial commit"
git push origin main
