# Function to load the API key from a file
def load_api_key(api_key_file_path):
    with open(api_key_file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

def get_gpt_api_key():
    return load_api_key('secrets/api-key.txt')

def get_github_pat():
    return load_api_key('secrets/github-pat.txt')

def get_github_headers():
    headers = {'Authorization': 'token ' + get_github_pat(), 'Accept': 'application/vnd.github.v3+json'}
    return headers