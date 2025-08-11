import os
import shutil
from github import Github
from git import Repo
from time import sleep

# === Configuration ===
GITHUB_USERNAME = "REPO_USER"
GITHUB_TOKEN = "REPO_TOKEN"
REPO_NAME = "kpmg-nexus-aks-sapi"
FEATURE_BRANCH = "feature/cicdautomation"
LOCAL_DIR = "./temp_repo"

# === Authenticate with GitHub ===
g = Github(REPO_TOKEN)
user = g.get_user()

# Create the Repository
try:
    repo = user.create_repo(REPO_NAME, private=True, auto_init=False)
    print(f"✅ Repository '{REPO_NAME}' created successfully.")
except Exception as e:
    print(f"⚠️ Failed to create repo or repo already exists: {e}")
    repo = g.get_repo(f"{GITHUB_USERNAME}/{REPO_NAME}")

# Clone Repo and Add Files ===
if os.path.exists(LOCAL_DIR):
    shutil.rmtree(LOCAL_DIR)

clone_url = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
repo_local = Repo.clone_from(clone_url, LOCAL_DIR)

# Create a sample file
readme_path = os.path.join(LOCAL_DIR, "README.md")
with open(readme_path, "w") as f:
    f.write("# KPMG Nexus FOT\n\nThis is a CI/CD automation repository.\n")

# Git operations
repo_local.git.add(A=True)
repo_local.index.commit("Initial commit with README.md")
origin = repo_local.remote(name="origin")
origin.push(refspec="main")

print("📁 Initial commit pushed to main branch.")

# === Step 3: Create Feature Branch from Main ===
repo_git = repo_local.git
repo_git.checkout("HEAD", b=FEATURE_BRANCH)
repo_local.index.commit("Initial commit on feature branch")
origin.push(refspec=f"{FEATURE_BRANCH}:{FEATURE_BRANCH}")

print(f"🌿 Feature branch '{FEATURE_BRANCH}' created and pushed.")

# === Step 4: Enable Branch Protection on Main ===
try:
    branch = repo.get_branch("main")
    branch.edit_protection(
        required_approving_review_count=1,
        enforce_admins=True,
        require_code_owner_reviews=False,
        dismiss_stale_reviews=True
    )
    print("🔒 Branch protection rules applied on 'main'.")
except Exception as e:
    print(f"❌ Failed to set branch protection: {e}")

# Cleanup local directory
shutil.rmtree(LOCAL_DIR)
print("✅ Automation complete. Local directory cleaned up.")
