import openai
import Helper
import Prompt
import json
from Config import Options

def get_chat_response(user_prompt, system_message, output_schema, model, max_tokens, temperature, seed):
    openai.api_key = Helper.get_gpt_api_key()
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": user_prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
        seed=seed,
        functions=[{ "name": "generate_workflow", "parameters": output_schema, "description": "Generates workflow file and it's description in JSON format. Used by code assistants" }],
        function_call={"name": "generate_workflow"}
    )
    return response.choices[0].message['function_call'].arguments

def get_chat_response_gpt4(user_prompt, system_message, output_schema, model, max_tokens, temperature, seed, organization):
    openai.api_key = Helper.get_gpt_api_key()
    openai.organization = organization
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": user_prompt}],
        max_tokens=max_tokens,
        temperature=temperature,
        seed=seed,
        functions=[{ "name": "generate_workflow", "parameters": output_schema, "description": "Generates workflow file and it's description in JSON format. Used by code assistants" }],
        function_call={"name": "generate_workflow"}
    )
    return response.choices[0].message['function_call'].arguments

def generate_build_pipeline(repo_structure, dependencies, default_branch, recursive_repo_structure):
    opts = Options()

    # response = get_chat_response(user_prompt=Prompt.get_user_prompt(repo_structure, dependencies, default_branch, recursive_repo_structure), system_message=Prompt.get_system_message(), 
    #                              output_schema=Prompt.get_output_schema(), model=opts.model, max_tokens=opts.max_tokens, temperature=opts.temperature, seed=opts.seed)

    response = get_chat_response_gpt4(user_prompt=Prompt.get_user_prompt(repo_structure, dependencies, default_branch, recursive_repo_structure), system_message=Prompt.get_system_message(), 
                                 output_schema=Prompt.get_output_schema(), model=opts.model, max_tokens=opts.max_tokens, temperature=opts.temperature, seed=opts.seed, organization=opts.organization)

    # Parse response as JSON
    response = json.loads(response)
    workflow_file_content = response['workflow_file_content']

    return workflow_file_content