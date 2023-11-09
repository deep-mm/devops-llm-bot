import Helper
import requests

def get_repository_tree(repository_identifier, branch='main'):
    repository_tree = []
    response = requests.get(f'https://api.github.com/repos/{repository_identifier}/git/trees/{branch}', headers=Helper.get_github_headers)
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

    response = requests.get(url, headers=Helper.get_github_headers)
    
    return response.json().keys()

def get_list_of_dependencies(repository_identifier):
    url = 'https://api.github.com/repos/' + repository_identifier + '/dependency-graph/sbom'

    response = requests.get(url, headers=Helper.get_github_headers)
    response.json()['sbom']['packages']
    dependency_names = [package['name'] + ', version = ' + package['versionInfo'] for package in response.json()['sbom']['packages']]
    
    return dependency_names

def get_default_branch(repository_identifier):
    url = 'https://api.github.com/repos/' + repository_identifier

    response = requests.get(url, headers=Helper.get_github_headers)
    
    return response.json()['default_branch']