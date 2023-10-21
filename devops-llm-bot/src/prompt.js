const systemMessage = "Your name is DevOps bot. \
You are a brilliant and meticulous engineer assigned to write a GitHub Actions workflow in YAML for the following Github Repository. \
When you write code, the code works on the first try, is syntactically perfect and is fully complete. \
The workflow should be able to build and run the application and run the tests if present in the repository. \
Do not include any deployment steps in the workflow. \
The output provided by you should be such that it can be directly copied into workflow.yaml file and the workflow should run successfully.\
Take user requests into consideration, \
but ensure that you only restrict the output to build and test workflow, and nothing else.\
It's of utmost importance that you return only the workflow file contents, and not any other text.";

const generateContent = (repoTree, languages, dependencies, user_comment, default_branch) => {

  return `
      Take into account the current repository's files, languages, and dependencies.
      It's of utmost importance that you return only the workflow file contents, and not any other text, such that it can be pasted into workflow.yaml file.

      Repository default branch:
      ${default_branch}

      Languages: 
      ${languages}

      Repository tree:
      ${repoTree}

      User requests:
      ${user_comment}

      Dependencies: 
      ${dependencies}`
}

const generateUpdateWorkflowContent = (old_workflow, user_comment, past_conversations) => {
  
    return `Analyze the existing github workflow and user requested changes provided below to create a github action build workflow.
      It's of utmost importance that you return only the workflow file contents, and not any other text, such that it can be pasted into workflow.yaml file.

      Existing workflow:
      ${old_workflow}

      User requests:
      ${user_comment}

      Previous Conversation History (Newest to Oldest):
      ${past_conversations}`
}

module.exports = { generateContent, generateUpdateWorkflowContent, systemMessage };