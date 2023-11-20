import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import base64
import sys
import os
import json

# df = pd.read_csv(
#     '/home/sgujar/results.csv', usecols=['name', 'mainLanguage', 'defaultBranch'], encoding='ISO-8859-1')
# # print(df.head(10))
# github_link = "https://github.com/"
# GITHUB_PAT = str(sys.argv[1])
# # rows = None
# # try:
# #     if len(sys.argv) > 1:
# #         if sys.argv[1].isdigit():
# #             rows = int(sys.argv[1])
# #             print(f"Scanning {rows} rows.")
# # except:
# #     print("All rows will be scanned.")
    
    
def has_build_command(language, content):
    if content is None or language is None:
        return False
    lower_content = content.lower()
    language_commands = {
        'javascript': ['npm run build', 'npm test', 'yarn build', 'yarn test', 'gulp build', 'jest', 'webpack'],
        'python': ['pip install', 'pytest', 'python setup.py install', 'tox', 'pipenv install', 'django-admin test'],
        'java': ['./gradlew build', 'gradle test', 'mvn clean install', 'ant build', 'javac', 'jar cf'],
        'c': ['make', 'gcc', 'cmake', 'ctest', 'autoreconf', 'autoconf', 'automake'],
        'ruby': ['bundle install', 'rake', 'ruby setup.rb', 'rspec', 'gem build', 'gem install'],
        'kotlin': ['./gradlew build', 'gradle test', 'kotlinc', 'kotlin test', 'kotlin compile'],
        'c#': ['dotnet build', 'dotnet test', 'msbuild', 'nunit', 'csc', 'nuget restore'],
        'c++': ['make', 'g++', 'cmake', 'ctest', 'autoreconf', 'autoconf', 'automake'],
        'typescript': ['npm run build', 'npm test', 'yarn build', 'yarn test', 'tsc', 'tslint'],
        'shell': ['make', 'gcc', 'bash', 'sh', 'shellcheck', 'shfmt'],
        'php': ['composer install', 'phpunit', 'php artisan serve', 'php -S localhost:8000', 'phpcs', 'phpcbf'],
        'objective-c': ['xcodebuild', 'xctest', 'xcode-select', 'xcrun', 'osacompile', 'agvtool'],
        'go': ['go build', 'go test', 'go run', 'gofmt', 'golangci-lint', 'godoc'],
        'dart': ['dart build', 'dart test', 'dart pub get', 'dart analyze', 'dartfmt', 'pub'],
        'elixir': ['mix deps.get', 'mix test', 'mix compile', 'iex', 'elixirc', 'mix format'],
        'swift': ['swift build', 'swift test', 'swift package', 'swift run', 'swiftformat', 'swiftlint'],
        'rust': ['cargo build', 'cargo test', 'cargo run', 'rustc', 'rustfmt', 'cargo clippy'],
        'groovy': ['gradle build', 'gradle test', 'grails run-app', 'grails test-app', 'groovy', 'groovyc'],
        'nix': ['nix-build', 'nix-shell', 'nix-collect-garbage', 'nix-env', 'nix-instantiate', 'nix-store'],
        'smalltalk': ['Metacello new', 'Smalltalk testAll.', 'Smalltalk saveImage', 'Smalltalk addToStartUpList', 'gst', 'Smalltalk image save']
    }
    return language.lower() in language_commands and any(command in lower_content for command in language_commands[language.lower()])


# def get_workflow_file_contents(repo_name, workflow_path):
#     github_api_url = f"https://api.github.com/repos/{repo_name}/contents/{workflow_path}"
#     headers = {'Authorization': f'token {GITHUB_PAT}'}
#     response = requests.get(github_api_url, headers=headers)

#     if response.status_code == 200:
#         try:
#             data = response.json()
#             if isinstance(data, dict) and 'content' in data:
#                 content = base64.b64decode(data['content']).decode('utf-8')
#                 return content
#             else:
#                 print(f"Invalid JSON format in response. Repo: {repo_name}")
#         except json.decoder.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#             print(f"Repo: {repo_name}")

#     return None


# def has_workflow_with_build_yaml_files(repo_name, branch, language):
#     url = f"{github_link}{repo_name}/tree/{branch}/.github/workflows"
#     headers = {'Authorization': f'token {GITHUB_PAT}'}
#     response = requests.get(url, headers=headers)
#     build_files = []
    
#     if response.status_code == 200:
#         try:
#             data = response.json()
#             if 'payload' not in data or 'tree' not in data['payload'] or 'items' not in data['payload']['tree']:
#                 return 0, []  
            
#             items = data['payload']['tree']['items']
#             for item in items:
#                 if item.get('contentType') == 'file' and (item['name'].endswith('.yml') or item['name'].endswith('.yaml')):
#                     contents = get_workflow_file_contents(repo_name, item['path'])
#                     if has_build_command(language, contents):
#                         build_files.append(contents)
                    
#             return len(build_files), build_files
#         except json.decoder.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#             print(f"Repo : {repo_name}")

#     return 0, []



# def get_csv_dict(Index, GitHub_repo_link, GitHub_Build_Pipeline_File_Content, Language):
#     return pd.DataFrame({
#         'Index': [Index],
#         'GitHub_Repo_Link': [GitHub_repo_link],
#         'GitHub_Build_Pipeline_File_Content': [GitHub_Build_Pipeline_File_Content],
#         'Generated_Build_Pipeline_File_Content': [''],
#         'Exact_Match_Score': [''],
#         'BLEU_Score': [''],
#         'Syntax_Check': [''],
#         'DevOps_Aware_Score': [''],
#         'Language': [Language]
#     })


# def get_extra_csv_dict(Index, GitHub_repo_link, GitHub_Build_Pipeline_File_Content, Language):
#     df = {
#         'Index': [Index],
#         'GitHub_Repo_Link': [GitHub_repo_link],
#         'Build_Pipeline_Count': [len(GitHub_Build_Pipeline_File_Content)],
#         'Generated_Build_Pipeline_File_Content': [''],
#         'Exact_Match_Score': [''],
#         'BLEU_Score': [''],
#         'Syntax_Check': [''],
#         'DevOps_Aware_Score': [''],
#         'Language': [Language]
#     }
#     for i, file in enumerate(GitHub_Build_Pipeline_File_Content):
#         df[f'GitHub_Build_Pipeline_File_Content_{i+1}'] = [file]
#     for i in range(len(GitHub_Build_Pipeline_File_Content)+1, 51):
#         df[f'GitHub_Build_Pipeline_File_Content_{i+1}'] = ['']

#     return pd.DataFrame(df)

# def create_empty_csv_files():
#     filtered_repo_path = 'filtered_repo.csv'
#     extra_repo_path = 'extra_repo.csv'
#     filtered_repo_columns = [
#         'Index', 'GitHub_Repo_Link', 'GitHub_Build_Pipeline_File_Content',
#         'Generated_Build_Pipeline_File_Content', 'Exact_Match_Score',
#         'BLEU_Score', 'Syntax_Check', 'DevOps_Aware_Score', 'Language'
#     ]
#     extra_repo_columns = [
#         'Index', 'GitHub_Repo_Link', 'Build_Pipeline_Count',
#         'Generated_Build_Pipeline_File_Content', 'Exact_Match_Score',
#         'BLEU_Score', 'Syntax_Check', 'DevOps_Aware_Score', 'Language'
#     ]
#     for i in range(1, 51):
#         extra_repo_columns.append(f'GitHub_Build_Pipeline_File_Content_{i}')
#     create_empty_csv(filtered_repo_path, filtered_repo_columns)
#     create_empty_csv(extra_repo_path, extra_repo_columns)
    
    
# def create_empty_csv(file_path, column_names):
#     if os.path.exists(file_path):
#         os.remove(file_path)
#     df = pd.DataFrame(columns=column_names)
#     df.to_csv(file_path, index=False)
    
# def main():
#     create_empty_csv_files()
#     filtered_repos = 0
#     extra_repos = 0
#     start_index = 0 
#     end_index = float("inf")   

#     for i in range(start_index, min(end_index, len(df))):
#         row = df.iloc[i]
#         repo_name = row['name']
#         default_branch = row['defaultBranch']
#         primaryLanguage = row['mainLanguage']
#         count, files = has_workflow_with_build_yaml_files(
#             repo_name, default_branch, primaryLanguage)
#         if count > 0:
#             link = github_link + repo_name
#             if count == 1:
#                 filtered_repos += 1
#                 row_df = get_csv_dict(
#                     filtered_repos, link, files[0], primaryLanguage)
#                 row_df.to_csv('filtered_repos.csv', mode='a',
#                               header=False, index=False)
#             else:
#                 extra_repos += 1
#                 row_df = get_extra_csv_dict(
#                     extra_repos, link, files, primaryLanguage)
#                 row_df.to_csv('extra_repos.csv', mode='a',
#                               header=False, index=False)
#         if (i+1) % 1000 == 0:
#             print(f"{i+1} repositories scanned")
#             print(f"{filtered_repos} repositories found with workflows")
#             print(f"{extra_repos} repositories found with multiple workflows")
        
# if __name__ == "__main__":
#     main()
