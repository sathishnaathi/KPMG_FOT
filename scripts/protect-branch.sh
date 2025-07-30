#!/bin/bash
set -e

REPO_NAME="kpmg_nuxus-aks-sapi"
BRANCH_NAME="feature/cicd_automation"

echo "Enabling branch protection on $BRANCH_NAME"
gh api -X PUT "repos/${GITHUB_ACTOR}/${REPO_NAME}/branches/${BRANCH_NAME}/protection" \
  -H "Accept: application/vnd.github+json" \
  -F required_status_checks='null' \
  -F enforce_admins=true \
  -F required_pull_request_reviews.dismiss_stale_reviews=true \
  -F restrictions='null'
