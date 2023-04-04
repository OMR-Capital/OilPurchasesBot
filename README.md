# Oil Purchases Bot

## Description

That Telegram bot helps manage purchases, dispatches, and sailing of waste oil for retail companies. It is designed to automate the process of purchasing waste oil, dispatching it to the company's warehouse, and sailing it to the customer. The bot is designed to be used by employees of the company, who can create purchase applications and dispatches, and by the company's management, who can approve purchases and set up the sailing of oil dispatches.

The bot supports three different roles with unique functions and permissions:
1. The Superuser creates and deletes accounts and has access to administrative functionalities. 
2. The Admin views purchase statistics and approves purchases made by employees and sets up the sailing of oil dispatches. 
3. The Employee creates new purchase applications and dispatches, ensuring the process is executed seamlessly.

To access the bot's functionalities, users need to call the login form using the /start command and then login with a specific access key, ensuring authorized access.

This Telegram bot is an effective solution for managing the purchases, dispatching, and sailing of waste oil for retail companies. Its streamlined functionalities and user-friendly interface can improve the efficiency and productivity of businesses, leading to better profits and growth.

The bot is an example of how Telegram bots can solve complex business tasks, highlighting the benefits of using such solutions. It can serve as a starting point for building customized solutions, saving time and effort in development.

The bot is hosted on the [Deta Space](https://deta.space/) cloud platform, designed for building, deploying, and scaling web applications and APIs. Deta Space provides developers with powerful tools and services, such as automated deployment, version control, and performance monitoring, making it easier to build and manage complex applications.


## Deployment

### Prerequisites
Before deploying the Telegram bot, ensure the following prerequisites are met:

1. Create a Telegram bot via [@BotFather](https://t.me/BotFather) and obtain a token.
2. Create a new or use an existing Google Sheet for purchases statistics.
3. Create a service account for Google Sheet and obtain the credentials file ([see](https://console.cloud.google.com)).

### Deploy
To deploy the Telegram bot, follow these steps:

1. Create a developer account on [Deta Space](https://deta.space/).
2. Install the [Space CLI](https://deta.space/docs/en/basics/cli).
3. Clone the project using the command `git clone https://github.com/OMR-Capital/OilPurchasesBot.git`.
4. Add the credentials file to the project directory.
5. In the project directory, run `space new` and follow the instructions.
6. Open the project in the [Builder](https://deta.space/builder).
7. In the `Configuration` tab, specify the settings with your Telegram bot token and Google Sheet data.
8. Set up the Telegram webhook (refer to the [Telegram docs](https://core.telegram.org/bots/api#setwebhook)) with the URL from `Builder` and token from `BotFather`. Note: You must specify `TELEGRAM_SECRET` in the `Configuration` tab of `Builder` before setting up the webhook and use it in the webhook.
9. Type `/start` in the Telegram chat with your bot and enjoy!

> To get access to the first superuser, use the `/create_root` command from the account specified in `ROOT_USERNAME`.

## Thanks

This project was created with [Deta Space](https://deta.space/), [ODetaM](https://github.com/rickh94/ODetaM) and [aiogram](https://github.com/aiogram/aiogram) 

