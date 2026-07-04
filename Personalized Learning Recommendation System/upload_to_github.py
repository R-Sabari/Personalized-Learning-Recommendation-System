"""
Upload project files to GitHub repository via GitHub REST API.
No Git installation required.

Usage:
    python upload_to_github.py --token YOUR_GITHUB_TOKEN

How to get a token:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name, select "repo" scope, and generate
4. Copy the token and paste it below or pass via --token argument
"""

import os
import sys
import base64
import json
import urllib.request
import urllib.error
import argparse
import time

# ─── CONFIG ────────────────────────────────────────────────────────────────────
GITHUB_OWNER = "R-Sabari"
GITHUB_REPO  = "Personalized-Learning-Recommendation-System"
BRANCH       = "main"
PROJECT_DIR  = os.path.dirname(os.path.abspath(__file__))

# Files/folders to EXCLUDE from upload
EXCLUDE = {
    "__pycache__", ".git", "learning_system.db",
    "upload_to_github.py", ".env", "*.pyc"
}
# ───────────────────────────────────────────────────────────────────────────────


def should_exclude(path: str) -> bool:
    parts = path.replace("\\", "/").split("/")
    for part in parts:
        if part in EXCLUDE or part.endswith(".pyc"):
            return True
    return False


def collect_files(base_dir: str):
    """Walk directory and return list of (relative_path, abs_path) tuples."""
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        # Filter excluded dirs in-place so os.walk skips them
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for filename in filenames:
            abs_path = os.path.join(root, filename)
            rel_path = os.path.relpath(abs_path, base_dir).replace("\\", "/")
            if not should_exclude(rel_path):
                files.append((rel_path, abs_path))
    return files


def github_api(token: str, method: str, endpoint: str, data: dict = None):
    """Make a GitHub API request."""
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "User-Agent": "Python-GitHub-Uploader/1.0"
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode()), resp.status
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return json.loads(body) if body else {}, e.code


def get_existing_sha(token: str, path: str):
    """Get the SHA of an existing file in the repo (needed for updates)."""
    resp, status = github_api(token, "GET",
        f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}?ref={BRANCH}")
    if status == 200 and "sha" in resp:
        return resp["sha"]
    return None


def upload_file(token: str, rel_path: str, abs_path: str):
    """Upload a single file to GitHub."""
    with open(abs_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()

    sha = get_existing_sha(token, rel_path)

    payload = {
        "message": f"Add {rel_path}",
        "content": content,
        "branch": BRANCH,
    }
    if sha:
        payload["message"] = f"Update {rel_path}"
        payload["sha"] = sha

    resp, status = github_api(token, "PUT",
        f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{rel_path}", payload)

    return status in (200, 201), status, resp.get("message", "")


def ensure_repo_and_branch(token: str):
    """Check repo exists and create README + branch if needed."""
    # Check if repo exists
    resp, status = github_api(token, "GET",
        f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}")
    if status != 200:
        print(f"  ✗ Repository not found: {GITHUB_OWNER}/{GITHUB_REPO}")
        print("    Please create the repository on GitHub first.")
        sys.exit(1)
    print(f"  ✓ Repository found: {resp['full_name']}")

    # Check if branch exists
    resp, status = github_api(token, "GET",
        f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/branches/{BRANCH}")
    if status == 200:
        print(f"  ✓ Branch '{BRANCH}' exists")
        return

    # Branch doesn't exist — create it from default branch or init with README
    default_branch = resp.get("default_branch", "main") if status != 200 else BRANCH

    # Try to get HEAD SHA
    resp2, status2 = github_api(token, "GET",
        f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/git/ref/heads/{default_branch}")

    if status2 == 200:
        sha = resp2["object"]["sha"]
        # Create branch
        github_api(token, "POST",
            f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/git/refs",
            {"ref": f"refs/heads/{BRANCH}", "sha": sha})
        print(f"  ✓ Created branch '{BRANCH}' from '{default_branch}'")
    else:
        # Repo might be empty — create initial README commit
        readme_content = base64.b64encode(
            f"# {GITHUB_REPO}\n\nPersonalized Learning Recommendation System\n".encode()
        ).decode()
        github_api(token, "PUT",
            f"/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/README.md",
            {"message": "Initial commit", "content": readme_content, "branch": BRANCH})
        print(f"  ✓ Initialized repo with README on '{BRANCH}'")


def main():
    parser = argparse.ArgumentParser(description="Upload project to GitHub via API")
    parser.add_argument("--token", required=True,
        help="GitHub Personal Access Token (needs 'repo' scope)")
    args = parser.parse_args()

    token = args.token.strip()

    print("\n╔══════════════════════════════════════════════════╗")
    print("║   GitHub Repository Uploader (No Git Required)  ║")
    print("╚══════════════════════════════════════════════════╝\n")

    # Validate token
    resp, status = github_api(token, "GET", "/user")
    if status != 200:
        print("✗ Invalid or expired GitHub token. Please check your token.")
        sys.exit(1)
    print(f"✓ Authenticated as: {resp['login']}\n")

    # Ensure repo and branch exist
    print("Checking repository...")
    ensure_repo_and_branch(token)

    # Collect files
    files = collect_files(PROJECT_DIR)
    print(f"\nFound {len(files)} files to upload:\n")
    for rel, _ in files:
        print(f"  • {rel}")

    print(f"\nUploading to https://github.com/{GITHUB_OWNER}/{GITHUB_REPO} ...\n")

    success_count = 0
    fail_count = 0

    for i, (rel_path, abs_path) in enumerate(files, 1):
        try:
            ok, status, msg = upload_file(token, rel_path, abs_path)
            if ok:
                print(f"  [{i}/{len(files)}] ✓ {rel_path}")
                success_count += 1
            else:
                print(f"  [{i}/{len(files)}] ✗ {rel_path} (HTTP {status}: {msg})")
                fail_count += 1
        except Exception as e:
            print(f"  [{i}/{len(files)}] ✗ {rel_path} ({e})")
            fail_count += 1

        # Small delay to avoid rate limiting
        time.sleep(0.3)

    print(f"\n{'═'*52}")
    print(f"  Done! ✓ {success_count} uploaded   ✗ {fail_count} failed")
    print(f"  🔗 View at: https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}")
    print(f"{'═'*52}\n")


if __name__ == "__main__":
    main()
