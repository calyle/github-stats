from github import Github
from os import getenv
import hashlib

def blob_sha1(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode('utf-8')
    blob_content = header + content
    return hashlib.sha1(blob_content).hexdigest()

def main():
    github_token = getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN NOT FOUND")
    gh = Github(github_token)
    repo = gh.get_repo("calyle/github-stats")
    changed_images = ['languages.svg', 'overview.svg']

    for img in changed_images:
        with open(f'generated/{img}', 'rb') as f:
            new_content = f.read()
        try:
            old_content = repo.get_contents(f'generated/{img}')
            new_sha = blob_sha1(new_content)
            if new_sha == old_content.sha:
                continue
            repo.update_file(
                path=f'generated/{img}',
                message=f'Update generated/{img}',
                content=new_content,
                sha=old_content.sha,
            )
            print(f"✅ UPDATED：generated/{img}")
        except Exception as e:
            print(f"❌ UPDATE FAILED：generated/{img}, ERROR：{e}")

if __name__ == "__main__":
    main()
