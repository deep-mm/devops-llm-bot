import openai

# Function to load the API key from a file
def load_api_key(api_key_file_path):
    with open(api_key_file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

# Load your API key from a file
api_key = load_api_key('api-key-1.txt')

# Set up the OpenAI API client
openai.api_key = api_key

def get_chat_response(user_prompt, system_message, model="gpt-3.5-turbo", max_tokens=1000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": user_prompt}],
        max_tokens=max_tokens,
        temperature = 0.2
    )
    return response.choices[0].message['content'].strip()

system_message = "Your name is Dev bot. You are a brilliant and meticulous engineer assigned to write a GitHub Actions workflow in YAML for the following Github Repository. When you write code, the code works on the first try, is syntactically perfect and is fully complete. The workflow should be able to build and run the application and run the tests if present in the repository. Take into account the current repository's language, frameworks, and dependencies. "

user_prompt = """
Analyze the github repository structure, language, framework and dependencies provide below to create a github action workflow.
repository
Repository structure:
{repo_structure}

Language: 
{language}

dependencies: 
{dependencies}

You will provide the github action workflow as the answer. Only include the yaml file in the output. Do not add any other text before or after the code.
"""

request_input = {
    'repo_structure': '''.github/workflows
                            bin
                            public/stylesheets
                            routes
                            views
                            .gitattributes
                            .gitignore
                            app.js
                            package-lock.json
                            package.json
                            web.config''',
    'language': 'Javascript',
    'dependencies': '''
                {
                "name": "myexpressapp",
                "version": "0.0.0",
                "private": true,
                "scripts": {
                    "start": "node ./bin/www"
                },
                "dependencies": {
                    "cookie-parser": "~1.4.4",
                    "debug": "~2.6.9",
                    "express": "~4.16.1",
                    "http-errors": "~1.6.3",
                    "morgan": "~1.9.1",
                    "pug": "2.0.0-beta11"
                }
                }'''
}

user_prompt = user_prompt.format(**request_input)

response = get_chat_response(user_prompt=user_prompt, system_message=system_message)
print(response)

final_response = response.strip("```")
file_name = "outputs/workflow.txt"
with open(file_name, "w") as file:
    # Write the string to the file
    file.write(response)