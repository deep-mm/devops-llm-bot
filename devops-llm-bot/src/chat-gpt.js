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
          "content": systemMessage
        },
        {
          "role": "user",
          "content": user_message,
        },
      ]
    });
    return completion.data.choices[0].message['content'];
}

const generate_pipeline = async (repoTree, languages, dependencies, user_comment) => {
    setup();
    return await invoke_openai(generateContent(repoTree, languages, dependencies, user_comment));    
}

const update_pipeline = async (old_workflow, user_comment) => {
    setup();
    return await invoke_openai(generateUpdateWorkflowContent(old_workflow, user_comment));
}

module.exports = { generate_pipeline, update_pipeline };