import os
import requests
import base64

# Environment variables
token = os.getenv("REPO_TOKEN")
username = os.getenv("REPO_USER")
repo_name = "kpmg_nuxus-kpmg-sapi"
branch_name = "feature/CICDAutomation"
default_branch = "main"  # Change to 'master' if needed

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# Create repository
print(f"Creating repository: {repo_name}")
repo_url = "https://api.github.com/user/repos"
repo_data = {
    "name": repo_name,
    "private": True,
    "auto_init": True
}
response = requests.post(repo_url, headers=headers, json=repo_data)

if response.status_code == 201:
    print(f"Repository '{repo_name}' created successfully.")
else:
    print(f"Failed to create repository: {response.status_code}")
    print(response.json())
    exit(1)
repo_api_url = f"https://api.github.com/repos/{username}/{repo_name}"  


# Step 2: Get actual default branch
repo_info = requests.get(repo_api_url, headers=headers)
actual_default_branch = repo_info.json().get("default_branch", default_branch)
print(f"Detected default branch: {actual_default_branch}")

# Create feature branch from default branch
print(f"Creating feature branch: {branch_name}")
main_ref_url = f"{repo_api_url}/git/ref/heads/{default_branch}"
main_ref_response = requests.get(main_ref_url, headers=headers)

if main_ref_response.status_code != 200:
    print(f"Failed to get default branch reference: {main_ref_response.status_code}")
    print(main_ref_response.json())
    exit(1)

main_sha = main_ref_response.json()["object"]["sha"]
branch_data = {
    "ref": f"refs/heads/{branch_name}",
    "sha": main_sha
}
branch_response = requests.post(f"{repo_api_url}/git/refs", headers=headers, json=branch_data)

if branch_response.status_code == 201:
    print(f"Branch '{branch_name}' created successfully.")
else:
    print(f"Failed to create branch: {branch_response.status_code}")
    print(branch_response.json())
    exit(1)

# Enable branch protection on feature branch
print(f"Enabling branch protection for: {branch_name}")
protection_url = f"{repo_api_url}/branches/{branch_name}/protection"
protection_headers = headers.copy()
protection_headers["Accept"] = "application/vnd.github+json"

protection_rules = {
    "required_status_checks": {
        "strict": True,
        "contexts": []
    },
    "enforce_admins": True,
    "required_pull_request_reviews": {
        "required_approving_review_count": 1
    },
    "restrictions": None
}
protection_response = requests.put(protection_url, headers=protection_headers, json=protection_rules)

if protection_response.status_code == 200:
    print(f"Branch protection enabled for '{branch_name}'.")
else:
    print(f"Failed to enable branch protection: {protection_response.status_code}")
    print(protection_response.json())
