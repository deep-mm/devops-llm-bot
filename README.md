# DevOps LLM Bot 🤖

[![GitHub Release](https://img.shields.io/github/v/release/deep-mm/devops-llm-bot?style=plastic)](https://github.com/deep-mm/devops-llm-bot/releases)
[![GitHub Tag](https://img.shields.io/github/v/tag/deep-mm/devops-llm-bot?style=plastic)](https://github.com/deep-mm/devops-llm-bot/releases)
[![GitHub contributors](https://img.shields.io/github/contributors/deep-mm/devops-llm-bot)](https://github.com/deep-mm/devops-llm-bot/graphs/contributors)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/deep-mm/devops-llm-bot)](https://github.com/deep-mm/devops-llm-bot/graphs/commit-activity)
[![GitHub license](https://img.shields.io/github/license/deep-mm/devops-llm-bot)](https://github.com/deep-mm/devops-llm-bot/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/deep-mm/devops-llm-bot)](https://github.com/deep-mm/devops-llm-bot/issues)
[![Build and deploy Node.js project to Azure Function App - github-app](https://github.com/deep-mm/devops-llm-bot/actions/workflows/build-deploy-app.yml/badge.svg)](https://github.com/deep-mm/devops-llm-bot/actions/workflows/build-deploy-app.yml)

## DevOps-LLM-Bot: Generate GitHub workflows utlizing the power of LLMs

Use this bot as a Junior DevOps Engineer at your company that can work under the guidance of your Senior engineers. Leave the grunt work to this engineer while your senior engineers focus on the architecture and design of your system.

Ask it to generate build & test workflows, it will utilize the following context from your repository including:

1. Repository file structure (Just the file names and path)
2. Repository dependencies
3. Repository languages

Additionally, you can make custom requests for the bot to consider.

## How to use?

1. Create a new issue with title beginning with @devops, which would trigger the bot to help you generate your workflow. The issue description will be used by the bot to consider any custom requests while generating the workflow.

    ![Create new issue](docs/create_new_issue.png)

2. Next, you should see a comment on your issue provided by the bot mentioning that your request is in process.

    ![Bot Issue Reply](docs/bot_issue_reply.png)

3. After about a minute, you will see the issue transforms into a pull request and your workflow file is generated.

    ![Pull request created](docs/pr_created.png)

4. If you are happy with the workflow, you can go ahead and merge your pull request.

5. If you want any modifications, just add a comment in the pull request mentioning the changes required. Just ensure the comment begins with '@devops-llm-bot', this will trigger the bot to consider your changes and re-generate the workflow.

    ![PR-comment](docs/pr_comment.png)

6. Once generated, the bot will reply on the PR and add a new commit.

    ![PR new updates](docs/pr_new_changes.png)


7. Feel free to explore the bot with this example PR: https://github.com/deep-mm/myExpressApp/pull/40

----

## DISCLAIMER

1. This bot is currently only capable of generating build and test steps in workflow, and will not entertain any requests to add deploy steps.

2. Please use this bot responsibly and under the guidance of experiences developers.

3. Please don't exploit the free app currently by making unnecessary calls.

## We love our contributors ❤️❤️

Make a [pull request](https://github.com/deep-mm/devops-llm-bot/compare) to help contribute.

<a href="https://github.com/deep-mm/devops-llm-bot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=deep-mm/devops-llm-bot&columns=24&max=480" />
</a>