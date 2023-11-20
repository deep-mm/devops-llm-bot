import Helper
import requests
import json
import time
import yaml
import subprocess

def get_repository_tree(repository_identifier, branch='main'):
    repository_tree = []
    response = requests.get(f'https://api.github.com/repos/{repository_identifier}/git/trees/{branch}', headers=Helper.get_github_headers())
    data = response.json()

    if response.status_code == 200:
        for item in data['tree']:
            if item['type'] == 'tree':
                repository_tree.append(f"Directory: {item['path']}")
            else:
                repository_tree.append(f"File: {item['path']}")
    else:
        print(f"Failed to fetch tree: {data['message']}")

    return repository_tree


def get_recursive_repository_tree(repository_identifier, branch='main'):
    repository_tree = []
    response = requests.get(f'https://api.github.com/repos/{repository_identifier}/git/trees/{branch}?recursive=1', headers=Helper.get_github_headers())
    data = response.json()

    if response.status_code == 200:
        for item in data['tree']:
            if item['type'] == 'tree':
                repository_tree.append(f"Directory: {item['path']}")
            else:
                repository_tree.append(f"File: {item['path']}")
    else:
        print(f"Failed to fetch tree: {data['message']}")

    return repository_tree

def get_list_of_languages(repository_identifier):
    url = 'https://api.github.com/repos/' + repository_identifier + '/languages'

    response = requests.get(url, headers=Helper.get_github_headers())
    
    return response.json().keys()

def get_list_of_dependencies(repository_identifier):
    url = 'https://api.github.com/repos/' + repository_identifier + '/dependency-graph/sbom'

    response = requests.get(url, headers=Helper.get_github_headers())
    try:
        response.json()['sbom']['packages']
        dependency_names = [package['name'] + ', version = ' + package['versionInfo'] for package in response.json()['sbom']['packages']]
    except:
        dependency_names = []
    
    return dependency_names

def get_default_branch(repository_identifier):
    url = 'https://api.github.com/repos/' + repository_identifier

    response = requests.get(url, headers=Helper.get_github_headers())

    responseJson = response.json()
    
    return responseJson['default_branch']

def get_all_workflow_files(repository_identifier):
    url = 'https://api.github.com/repos/' + repository_identifier + '/actions/workflows'

    response = requests.get(url, headers=Helper.get_github_headers())
    workflow_files = [workflow_file['path'] for workflow_file in response.json()['workflows']]

    # Filter only those files with path starting with .github/workflows
    workflow_files = [workflow_file for workflow_file in workflow_files if workflow_file.startswith('.github/workflows')]
    
    return workflow_files

def get_workflow_file_content(repository_identifier, workflow_file_path, default_branch='main'):
    url = 'https://raw.githubusercontent.com/' + repository_identifier + f'/{default_branch}/' + workflow_file_path

    response = requests.get(url, headers=Helper.get_github_headers())
    if response.status_code != 200:
        return ''
    
    workflow_file_content = response.text
    return workflow_file_content

def check_yaml_syntax(yaml_file_content):
    try:
        yaml.safe_load(yaml_file_content)
    except yaml.YAMLError as exc:
        return False

    return True

def run_action_lint(workflow_file_content):
    # Write workflow file content to a file
    with open('workflow.yml', 'w', newline='\n') as f:
        f.write(workflow_file_content)
    try :
        subprocess.run(['actionlint', 'workflow.yml'], check = True)
        return True
    except subprocess.CalledProcessError as e:
        print(e)
        return False
    
def is_workflow_syntax_valid (workflow_file_content):
    url = 'https://api.github.com/repos/devops-llm-bot/github-action-lint/actions'
    data = {
        "ref": "main", 
        "inputs": { "workflow_content": f"{workflow_file_content}" }
    }

    # Convert data to JSON string
    data = json.dumps(data)

    response = requests.post(url + '/workflows/75703243/dispatches', headers=Helper.get_github_headers(), data=data)
    if response.status_code == 204:
        response = requests.get(url + f'/workflows/75703243/runs', headers=Helper.get_github_headers())
        data = response.json()
        run_id = data['workflow_runs'][0]['id']
        # Delay 10s to wait for the workflow to finish
        time.sleep(10)

        response = requests.get(url + f'/runs/{run_id}', headers=Helper.get_github_headers())
        data = response.json()
        conclusion = data['conclusion']
        if conclusion == 'success':
            return True
        else:
            return False

    return False