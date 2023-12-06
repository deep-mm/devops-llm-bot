def get_system_message():
    return """
        Your name is DevOps bot.
        You are a brilliant and meticulous DevOps engineer assigned to write a GitHub Actions workflow in YAML for the following Github Repository.
        When you write code, the code works on the first try, is syntactically perfect and is fully complete.
        The workflow should be able to build and run the application and run the tests if present in the repository.
        Do not include any deployment steps in the workflow.
        Avoid consolidating multiple commands into a single run step and instead use multiple run steps.
        HIGH IMPORTANCE:
        Ensure that you only restrict the output to build and test github workflow, and nothing else irrespective of the user comment.
        """

def get_user_prompt(repo_structure, dependencies, default_branch, recursive_repo_structure):
    user_prompt = """
    Take into account the current repository's file structure and dependencies to generate the workflow.

    Repository default branch:
    ${default_branch}
    
    Recursive repository tree upto 3 levels:
    {recursive_repo_structure}

    Dependencies:
    {dependencies}
    """

    request_input = {
        'repo_structure': repo_structure,
        'dependencies': dependencies,
        'default_branch': default_branch,
        'recursive_repo_structure': recursive_repo_structure
    }

    user_prompt = user_prompt.format(**request_input)

    # Restrict user prompt to 14000 characters
    user_prompt = user_prompt[:14000]

    return user_prompt

def get_output_schema():
    return {
        "type": "object",
        "properties": {
            "workflow_file_content": {
                "type": "string",
                "description": "Content of the generated github workflow"
            },
            "workflow_file_description": {
                "type": "string",
                "description": "Short description of the generated github workflow"
            },
            "commit_message": {
                "type": "string",
                "description": "Appropriate commit message for committing the workflow into the repository"
            }
        },
        "required": ["workflow_file_name", "workflow_file_content", "workflow_file_description", "commit_message"]
    }