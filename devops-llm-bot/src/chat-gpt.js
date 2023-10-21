const { OpenAIApi, Configuration } = require("openai");
const { generateContent, generateUpdateWorkflowContent, systemMessage } = require("./prompt");

var configuration, openai;

function setup() {
    configuration = new Configuration({
      apiKey: process.env.OPENAI_API_KEY,
    });
    openai = new OpenAIApi(configuration);
}

async function invoke_openai(user_message) {
    const completion = await openai.createChatCompletion({
      model: "gpt-3.5-turbo-16k",
      temperature: 0.2,
      max_tokens: 1000,
      messages: [
        {
          "role": "system",
          "content": systemMessage,
        },
        {
          "role": "user",
          "content": user_message,
        },
      ]
    });
    return completion.data.choices[0].message['content'];
}

const generate_pipeline = async (repoTree, languages, dependencies, user_comment, default_branch) => {
    setup();
    let user_message = generateContent(repoTree, languages, dependencies, user_comment, default_branch);
    // Restrict user_message to 8000 characters
    user_message = user_message;
    if (user_message.length > 8000) {
      user_message = user_message.substring(0, 8000);
      user_message = user_message + " ... Output truncated to 8000 characters.";
    }

    return await invoke_openai(user_message);
}

const update_pipeline = async (old_workflow, user_comment, past_conversations) => {
    setup();
    let user_message = generateUpdateWorkflowContent(old_workflow, user_comment, past_conversations);
    // Restrict user_message to 8000 characters
    if (user_message.length > 8000) {
      user_message = user_message.substring(0, 8000);
      user_message = user_message + " ... Output truncated to 8000 characters.";
    }

    return await invoke_openai(user_message);
}

module.exports = { generate_pipeline, update_pipeline };