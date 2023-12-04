const { OpenAIApi, Configuration } = require("openai");
const { generateContent, generateUpdateWorkflowContent, systemMessage, output_schema } = require("./prompt");

var configuration, openai;

function setup() {
    configuration = new Configuration({
      apiKey: process.env.OPENAI_API_KEY,
      organization: "org-vIJLObb0BM3QCjwZzWKNknn8"
    });
    openai = new OpenAIApi(configuration);
}

async function invoke_openai(user_message) {
    try {
      const completion = await openai.createChatCompletion({
        model: "gpt-3.5-turbo-1106",
        temperature: 0.2,
        max_tokens: 4000,
        messages: [
          {
            "role": "system",
            "content": systemMessage,
          },
          {
            "role": "user",
            "content": user_message,
          },
        ],
        functions: [{ name: "generate_workflow", parameters: output_schema, "description": "Generates workflow file and it's description in JSON format. Used by code assistants" }],
        function_call: {name: "generate_workflow"}
      });
      return JSON.parse(completion.data.choices[0].message['function_call'].arguments);
    } catch (error) {
      console.log(error);
      return null;
    }
}

const generate_pipeline = async (repoTree, languages, dependencies, user_comment, default_branch) => {
    setup();
    let user_message = generateContent(repoTree, languages, dependencies, user_comment, default_branch);
    // Restrict user_message to 14000 characters
    user_message = user_message;
    if (user_message.length > 14000) {
      user_message = user_message.substring(0, 14000);
      user_message = user_message + " ... Output truncated to 14000 characters.";
    }

    return await invoke_openai(user_message);
}

const update_pipeline = async (old_workflow, user_comment, past_conversations) => {
    setup();
    let user_message = generateUpdateWorkflowContent(old_workflow, user_comment, past_conversations);
    // Restrict user_message to 14000 characters
    if (user_message.length > 14000) {
      user_message = user_message.substring(0, 14000);
      user_message = user_message + " ... Output truncated to 14000 characters.";
    }

    return await invoke_openai(user_message);
}

module.exports = { generate_pipeline, update_pipeline };