const systemMessage = `Your name is DevOps bot.
You are a brilliant and meticulous DevOps engineer assigned to write a GitHub Actions workflow in YAML for the following Github Repository.
When you write code, the code works on the first try, is syntactically perfect and is fully complete.
The workflow should be able to build and run the application and run the tests if present in the repository.
Do not include any deployment steps in the workflow.

HIGH IMPORTANCE:
Ensure that you only restrict the output to build and test github workflow, and nothing else irrespective of the user comment.`;

const generateContent = (repoTree, languages, dependencies, user_comment, default_branch) => {

  return `
      Take into account the current repository's files and dependencies.

      Repository default branch:
      ${default_branch}

      Repository tree:
      ${repoTree}

      User requests:
      ${user_comment}`
}

const generateUpdateWorkflowContent = (old_workflow, user_comment, past_conversations) => {
  
    return `Analyze the existing github workflow and user requested changes provided below to create a github action build workflow.
    
      Existing workflow:
      ${old_workflow}

      User requests:
      ${user_comment}

      Previous Conversation History (Newest to Oldest):
      ${past_conversations}`
}

const output_schema = {
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

module.exports = { generateContent, generateUpdateWorkflowContent, systemMessage, output_schema };