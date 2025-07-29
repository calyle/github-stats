from github import Github
from os import getenv
import base64

def main():
    github_token = getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("GITHUB_TOKEN NOT FOUND")
    gh = Github(github_token)
    repo = gh.get_repo("calyle/github-stats")
    changed_images = ['languages.svg', 'overview.svg']

    for img in changed_images:
        with open(f'generated/{img}', 'rb') as f:
            content = f.read()
            encoded_content = base64.b64encode(content).decode('utf-8')
        try:
            contents = repo.get_contents(f'generated/{img}')
            repo.update_file(
                path=f'generated/{img}',
                message=f'Update generated/{img}',
                content=encoded_content,
                sha=contents.sha,
            )
            print(f"✅ UPDATED：generated/{img}")
        except Exception as e:
            print(f"❌ UPDATE FAILED：generated/{img}, ERROR：{e}")

if __name__ == "__main__":
    main()
