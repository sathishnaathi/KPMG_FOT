#!/bin/bash
set -e

REPO_NAME="kpmg_nuxus-aks-sapi"
BRANCH_NAME="feature/cicd_automation"

cd "$REPO_NAME"
git checkout -b "$BRANCH_NAME"
git push origin "$BRANCH_NAME"
