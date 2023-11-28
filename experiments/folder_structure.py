import requests


def get_latest_commit_sha(owner, repo, branch='main', token=None):
    api_url = f'https://api.github.com/repos/{owner}/{repo}/branches/{branch}'
    headers = {'Accept': 'application/vnd.github.v3+json'}

    if token:
        headers['Authorization'] = f'Token {token}'

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return response.json().get('commit', {}).get('sha')
    else:
        print(
            f"Failed to fetch latest commit SHA. Status code: {response.status_code}")
        return None


def get_github_folder_structure(owner, repo, tree_sha, max_depth=3, token=None):
    api_url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1'
    headers = {'Accept': 'application/vnd.github.v3+json'}

    if token:
        headers['Authorization'] = f'Token {token}'

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        tree_data = response.json().get('tree', [])

        folder_structure = [
            entry['path'] for entry in tree_data
            if len(entry['path'].split('/')) <= max_depth
        ]

        return folder_structure

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


def print_folder_structure(folder_structure):
    for path in folder_structure:
        segments = path.split('/')
        indent = '    ' * (len(segments) - 1)
        print(f"{indent}| - {segments[-1]}")


github_url = 'https://github.com/DapperLib/Dapper'
owner, repo = github_url.split('/')[-2:]
token = 'PAT'

latest_commit_sha = get_latest_commit_sha(owner, repo, token=token)
if latest_commit_sha:
    folder_structure = get_github_folder_structure(
        owner, repo, latest_commit_sha, token=token)

    if folder_structure:
        print(folder_structure)
        print("Folder Structure:")
        print_folder_structure(folder_structure)
