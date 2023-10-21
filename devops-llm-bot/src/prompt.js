const systemMessage = "Your name is DevOps bot. \
You are a brilliant and meticulous engineer assigned to write a GitHub Actions workflow in YAML for the following Github Repository. \
When you write code, the code works on the first try, is syntactically perfect and is fully complete. \
The workflow should be able to build and run the application and run the tests if present in the repository. \
Take into account the current repository's files, languages, and dependencies. \
The output provided by you should be such that it can be directly copied into workflow.yaml file and the workflow should run successfully.\
You will provide the github action workflow as the answer. \
Only include the yaml file in the output. Do not add any other text before or after the code."

const generateContent = (repoTree, languages, dependencies, user_comment) => {

  return `Analyze the github repository structure, language, framework and dependencies provide below to create a github action build workflow. 
      Take user requests into consideration, 
      but ensure that you only restrict the output to build and test workflow, there should not be any deploy steps in the workflow.    
      It's of utmost importance that you return only the workflow file contents, and not any other text.

      User requests:
      ${user_comment}

      Repository structure:
      ${repoTree}

      Languages: 
      ${languages}

      Dependencies: 
      ${dependencies}`
}

const generateUpdateWorkflowContent = (old_workflow, user_comment) => {
  
    return `Analyze the existing github workflow and user requested changes provided below to create a github action build workflow. 
      Take user requests into consideration, 
      but ensure that you only restrict the output to build and test steps, there should not be any deploy steps in the workflow.
      It's of utmost importance that you return only the workflow file contents, and not any other text.   

      Existing workflow:
      ${old_workflow}

      User requests:
      ${user_comment}`
}

module.exports = { generateContent, generateUpdateWorkflowContent, systemMessage };