#!/bin/bash
set -e

REPO_NAME="kpmg_nuxus-aks-sapi"
DESCRIPTION="Automated repo creation"
VISIBILITY="private"

echo "Creating repository: $REPO_NAME"
gh repo create "$REPO_NAME" --description "$DESCRIPTION" --$VISIBILITY --confirm

